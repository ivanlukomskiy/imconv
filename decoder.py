import numpy as np
import cv2


def decode_bytes_from_jpeg(path: str, max_bytes: int = None) -> bytes:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"failed to read {path}")

    h, w = img.shape
    if w % 8 != 0 or h % 8 != 0:
        raise ValueError("image width and height must be multiples of 8")

    blocks_x = w // 8
    blocks_y = h // 8
    capacity = blocks_x * blocks_y

    if max_bytes is None:
        max_bytes = capacity
    else:
        max_bytes = min(max_bytes, capacity)

    out = bytearray()
    for i in range(max_bytes):
        by = i // blocks_x
        bx = i % blocks_x
        y0, y1 = by * 8, (by + 1) * 8
        x0, x1 = bx * 8, (bx + 1) * 8
        block = img[y0:y1, x0:x1]
        val = int(round(block.mean()))
        out.append(np.clip(val, 0, 255))

    binary = bytes(out)
    size = int.from_bytes(binary[0:4], byteorder="big")

    return binary[4:size+4]
