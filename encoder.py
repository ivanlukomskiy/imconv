import numpy as np
import cv2

header_size = 4

def encode_bytes_to_jpeg(data: bytes, width: int, height: int, out_path: str, quality: int = 95) -> None:
    if width % 8 != 0 or height % 8 != 0:
        raise ValueError("width and height must be multiples of 8")

    blocks_x = width // 8
    blocks_y = height // 8
    capacity = blocks_x * blocks_y

    if len(data) + header_size > capacity:
        raise ValueError(f"image too small: capacity={capacity} bytes, need={len(data)}")

    img = np.zeros((height, width), dtype=np.uint8)

    header = len(data).to_bytes(4, byteorder="big")
    data = header + data

    for i, b in enumerate(data):
        by = i // blocks_x
        bx = i % blocks_x
        y0, y1 = by * 8, (by + 1) * 8
        x0, x1 = bx * 8, (bx + 1) * 8
        img[y0:y1, x0:x1] = b

    ok = cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
    if not ok:
        raise IOError(f"failed to write JPEG to {out_path}")
