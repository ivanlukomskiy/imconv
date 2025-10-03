import unittest

from decoder import decode_bytes_from_jpeg
from encoder import encode_bytes_to_jpeg


class MyTestCase(unittest.TestCase):
    def test_something(self):
        img_name = 'test.jpg'
        original = b"hello world!"
        encode_bytes_to_jpeg(original, width=320, height=240, out_path=img_name, quality=95)
        decoded = decode_bytes_from_jpeg(img_name, max_bytes=20)
        print(decoded)
        self.assertEqual(original, decoded)


if __name__ == '__main__':
    unittest.main()
