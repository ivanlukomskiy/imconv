import math
from typing import Dict, Tuple, Iterable, List
import numpy as np
import cv2

# ---------- bit helpers ----------
def take_bits(bit_iter: Iterable[int], k: int) -> int:
    """Consume k bits from bit_iter (0/1 ints). If not enough bits, pad with zeros."""
    val = 0
    for _ in range(k):
        try:
            b = next(bit_iter)
        except StopIteration:
            b = 0
        val = (val << 1) | (b & 1)
    return val

def int_to_bits(x: int, k: int) -> List[int]:
    """Return k bits of x (MSB first)."""
    return [(x >> i) & 1 for i in range(k - 1, -1, -1)]

# Robust mod in [0, S)
def frac_mod(x: float, S: float) -> float:
    """Return x modulo S in [0, S). Works well for negatives."""
    return x - S * math.floor(x / S)

# ---------- core QIM mapping ----------
def qim_embed_coeff(c: float, symbol: int, k: int, S: float) -> float:
    """
    Embed a k-bit symbol in coefficient c using QIM with step S.
    We make M=2^k bins uniformly spaced within each step-width interval.
    """
    if k == 0:
        return c
    M = 1 << k
    bin_width = S / M
    # Bin centers at (m + 0.5) * bin_width inside the S-interval
    target_residue = (symbol + 0.5) * bin_width  # in [0, S)
    # Snap c to nearest lattice point having that residue
    base = math.floor((c - target_residue) / S)
    c_star = base * S + target_residue
    # Resolve tie by picking the closer of the two neighbors
    # (usually unnecessary, but good to keep)
    alt = (base + 1) * S + target_residue
    return c_star if abs(c - c_star) <= abs(c - alt) else alt

def qim_decode_coeff(c: float, k: int, S: float) -> int:
    """
    Recover k-bit symbol from coefficient c with step S.
    """
    if k == 0:
        return 0
    M = 1 << k
    bin_width = S / M
    r = frac_mod(c, S)  # residue in [0, S)
    # Map residue to nearest bin center
    symbol = int(round((r - bin_width * 0.5) / bin_width))
    # Wrap into [0, M-1]
    symbol %= M
    return symbol

# ---------- DCT block I/O ----------
def dct2(block_spatial: np.ndarray) -> np.ndarray:
    """8x8 DCT (float32). Input can be uint8/float; returns float32."""
    B = block_spatial.astype(np.float32)
    return cv2.dct(B)

def idct2(block_dct: np.ndarray) -> np.ndarray:
    """8x8 inverse DCT (float32 → float32)."""
    return cv2.idct(block_dct.astype(np.float32))

# ---------- Public API ----------
def encode_block_qim(
    block_spatial: np.ndarray,
    spec: Dict[Tuple[int, int], int],
    bits: Iterable[int],
    step: float = 16.0
) -> Tuple[np.ndarray, int]:
    """
    Encode an 8x8 spatial block using QIM in DCT domain.

    Parameters
    ----------
    block_spatial : np.ndarray
        8x8 spatial block (grayscale). dtype can be uint8 or float.
    spec : dict[(u,v)->k]
        Map of coefficient positions to number of bits (k). Include (0,0) for DC if desired.
        Example: {(0,0):8, (1,0):4, (0,1):4, (1,1):2}
    bits : iterable of ints (0/1)
        Bitstream to embed; if shorter than required, zero-padding is applied.
    step : float
        QIM step S. Must exceed expected recompression quantization to be robust.

    Returns
    -------
    new_block_spatial : np.ndarray (float32)
        8x8 block after embedding (not clipped to [0,255]).
    consumed_bits : int
        Number of bits actually consumed from 'bits' (sum of k in spec).
    """
    # DCT
    C = dct2(block_spatial).copy()

    # Make a true iterator we can consume from
    bit_iter = iter(bits)

    consumed = 0
    for (u, v), k in spec.items():
        if k <= 0:
            continue
        symbol = take_bits(bit_iter, k)  # 0..(2^k - 1)
        C[u, v] = qim_embed_coeff(float(C[u, v]), symbol, k, step)
        consumed += k

    # IDCT back to spatial domain
    out = idct2(C)  # float32
    return out, consumed

def decode_block_qim(
    block_spatial: np.ndarray,
    spec: Dict[Tuple[int, int], int],
    step: float = 16.0
) -> List[int]:
    """
    Decode bits from an 8x8 spatial block using the same QIM spec/step.

    Returns
    -------
    bits : List[int]  (MSB-first per symbol)
    """
    C = dct2(block_spatial)
    out_bits: List[int] = []

    for (u, v), k in spec.items():
        if k <= 0:
            continue
        symbol = qim_decode_coeff(float(C[u, v]), k, step)
        out_bits.extend(int_to_bits(symbol, k))

    return out_bits
