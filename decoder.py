import numpy as np
import cv2
from config import SPEC, NORMALIZE_MULTIPLY, NORMALIZE_ADD
from blocks import decode_block_qim


def decode_bytes_from_jpeg(path: str, header: bool = True) -> bytes:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"failed to read {path}")

    h, w = img.shape
    if w % 8 != 0 or h % 8 != 0:
        raise ValueError("image width and height must be multiples of 8")

    blocks_x = w // 8
    blocks_y = h // 8
    capacity = blocks_x * blocks_y

    out = bytearray()
    for i in range(capacity):
        by = i // blocks_x
        bx = i % blocks_x
        y0, y1 = by * 8, (by + 1) * 8
        x0, x1 = bx * 8, (bx + 1) * 8
        block = img[y0:y1, x0:x1]

        vals = decode_block_qim(block, SPEC)
        # print(f"{i}: {vals}")
        for i in range(0, len(vals), 8):
            byte = 0
            for bit in vals[i:i + 8]:
                byte = (byte << 1) | bit
            out.append(byte)
        # val = int(round(block.mean()))
        # out.append(np.clip(val, 0, 255))

    binary = bytes(out)
    print('Full decoded bytes')
    print(binary.hex(' '))

    if header:
        size = int.from_bytes(binary[0:4], byteorder="big")
        print("size from header =", size)
        res = binary[4:size + 4]
        print("result size =", len(res))
        return res

    return binary
