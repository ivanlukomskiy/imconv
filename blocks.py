import math
from typing import Dict, Tuple, Iterable, List
import numpy as np
import cv2
from config import NORMALIZE_MULTIPLY, NORMALIZE_ADD

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
def qim_embed_coef(symbol: int, bits_in_coef: int) -> float:
    if bits_in_coef == 0:
        return 0
    max_value = 1 << bits_in_coef
    res = 1. / max_value * symbol
    # print(f'{symbol} with max {max_value} results in {res}')
    return res

def qim_decode_coeff(c: float, bits_in_coef: int) -> int:
    """
    Recover k-bit symbol from coefficient c with step S.
    """
    if bits_in_coef == 0:
        return 0
    max_value = 1 << bits_in_coef
    step = 1 / max_value
    res = int(round(c / step))
    # print(f'c {c}, res {res}, max_value {max_value}, step {step}')
    return res

# ---------- DCT block I/O ----------
def dct2(block_spatial: np.ndarray) -> np.ndarray:
    """8x8 DCT (float32). Input can be uint8/float; returns float32."""
    B = block_spatial.astype(np.float32)
    return cv2.dct(B)

def idct2(block_dct: np.ndarray) -> np.ndarray:
    """8x8 inverse DCT (float32 → float32)."""
    return cv2.idct(block_dct.astype(np.float32))

# ---------- Public API ----------
def generate_image_block_raw(
    block_spatial: np.ndarray,
    spec: Dict[Tuple[int, int], int],
    bit_iter: Iterable[int],
):
    coefficients = np.zeros_like(block_spatial)
    for (u, v), bits_count_for_coef in spec.items():
        if bits_count_for_coef <= 0:
            continue
        symbol = take_bits(bit_iter, bits_count_for_coef)  # 0..(2^k - 1)
        coefficients[u, v] = qim_embed_coef(symbol, bits_count_for_coef)

    return idct2(coefficients)

def encode_block_qim(
    block_spatial: np.ndarray,
    spec: Dict[Tuple[int, int], int],
    bit_iter: Iterable[int],
) -> np.ndarray:
    im = generate_image_block_raw(block_spatial, spec, bit_iter)
    # print(f"min {np.min(im)}, max {np.max(im)}")
    # mul = 255. / (np.max(im) - np.min(im))
    # add = np.min(im) * mul
    # print(f"add {add}, mul {mul}")
    out = im * NORMALIZE_MULTIPLY + NORMALIZE_ADD
    return out

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
    # print("BLOCK")
    block_spatial = (block_spatial.astype(np.float32)- NORMALIZE_ADD)  / NORMALIZE_MULTIPLY
    # print(block_spatial)
    coefficients = cv2.dct(block_spatial)
    # coefficients = dct2(block_spatial) / NORMALIZE_MULTIPLY - NORMALIZE_ADD
    out_bits: List[int] = []

    for (u, v), k in spec.items():
        if k <= 0:
            continue
        symbol = qim_decode_coeff(float(coefficients[u, v]), k)
        out_bits.extend(int_to_bits(symbol, k))

    return out_bits
