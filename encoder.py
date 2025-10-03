import numpy as np
import cv2
from typing import Iterator
from config import SPEC
from blocks import encode_block_qim

header_size = 4

def bytes_to_bits(data: bytes) -> Iterator[int]:
    """
    Convert bytes into an iterator of bits (0/1), MSB first.
    Example: b'\xA3' (0b10100011) -> 1,0,1,0,0,0,1,1
    """
    for byte in data:
        for i in range(7, -1, -1):  # from bit 7 (MSB) down to 0 (LSB)
            yield (byte >> i) & 1

def encode_bytes_to_jpeg(data: bytes, width: int, height: int, out_path: str, quality: int = 95, header: bool = True) -> None:
    if width % 8 != 0 or height % 8 != 0:
        raise ValueError("width and height must be multiples of 8")

    blocks_x = width // 8
    blocks_y = height // 8

    block_capacity_bits = sum(SPEC.values())
    blocks_count = blocks_x * blocks_y
    capacity_bits = blocks_count * block_capacity_bits

    print(f"max image capacity (bits): {capacity_bits} ({block_capacity_bits} per block)")

    size_bytes = len(data)
    if header:
        size_bytes += 4

    size_bits = size_bytes * 8
    # if size_bits > capacity_bits:
    #     raise ValueError(f"image too small: capacity={capacity_bits} bytes, need={size_bits}")

    img = np.zeros((height, width), dtype=np.uint8)

    if header:
        print(f"EXP SIZE: {len(data)}")
        header = len(data).to_bytes(4, byteorder="big")
        data = header + data

    print("Before encoding")
    print(data.hex(' '))
    bit_iter = bytes_to_bits(data)

    for i in range(blocks_count):
        by = i // blocks_x
        bx = i % blocks_x
        y0, y1 = by * 8, (by + 1) * 8
        x0, x1 = bx * 8, (bx + 1) * 8

        blk = np.full((8, 8), 0, dtype=np.float32)
        new_block = encode_block_qim(blk, SPEC, bit_iter)
        # print(new_block.copy())
        img[y0:y1, x0:x1] = np.clip(new_block, 0, 255).astype(np.uint8)

        # if i == 0:
        #     print(new_block)

    # print(img[0:8, 0:8])
    ok = cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
    if not ok:
        raise IOError(f"failed to write JPEG to {out_path}")
