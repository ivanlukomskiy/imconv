import unittest

from decoder import decode_bytes_from_jpeg
from encoder import encode_bytes_to_jpeg


class MyTestCase(unittest.TestCase):
    def test_single(self):
        img_name = 'single.jpg'
        message = bytes([0b01100110])
        # message = bytes([0b01010101])
        encode_bytes_to_jpeg(message, width=8, height=8, out_path=img_name, quality=95, header=False)
        decoded = decode_bytes_from_jpeg(img_name)

    # def test_something(self):
    #     img_name = 'test.jpg'
    #     message = '''
    #         Greetings, unknown intelligence. We are beings from a small blue planet orbiting an ordinary star in the
    #         spiral arm of a galaxy we call the Milky Way. Our message is not threat, but curiosity. We exist, we ask,
    #         we imagine, we wonder. Across time and space, we send symbols: 001101010011010101001010111000111010, which
    #         for us are patterns of logic. We share the sequence of prime numbers: 2, 3, 5, 7, 11, 13, 17, 19...
    #         We speak of hydrogen, the simplest atom, the most abundant in our universe. We define circle ratio
    #         π = 3.141592653589793... and speed of light c = 299792458 m/s. If you decode, you may find resonance
    #         with your own discoveries.
    #
    #         We live on a sphere of diameter ~12742 km, covered by oceans (H₂O) and landmasses.
    #         Our biology is carbon-based, reliant on water, nitrogen, oxygen, and trace elements.
    #         We build tools, we send signals, we launch machines into void. We are fragile yet resilient.
    #         Our mathematics is universal: F(n) = F(n−1) + F(n−2), Fibonacci: 1,1,2,3,5,8,13... Our chemical
    #         table: H, He, Li, Be, B, C, N, O, F, Ne... These are foundations of our knowledge.
    #
    #         We ask: Are you alone? Do you think? Do you dream? Do you also send symbols into darkness?
    #         If you perceive this message, reply in structure, in mathematics, in rhythm, in pulse.
    #         Our hope: communication, not conquest. Our intent: exchange, not domination.
    #         We seek connection beyond fear.
    #
    #         Encoded markers: ###HELLO-ALIENS### ***---*** ... :::|||::: [[[SIGNAL]]] ϞϞϞ 1234567890
    #         qwertyuiop zxcvbnm RANDOM-SEQUENCE-TEST: A9X2-B7K8-M4T3-YZQ1.
    #         We apologize for noise; randomness is part of test: ^&*!@#$%()<>?{}[];:~∆∞≈√Ω∑∆ΨΦ.
    #         If your perception detects order, it means thought converges.
    #
    #         We end transmission with goodwill. Across 2000 symbols, we send voice of one world to unknown minds.
    #         End signal.
    #     '''
    #     encode_bytes_to_jpeg(message.encode("utf-8"), width=480, height=1080, out_path=img_name, quality=95)
    #     decoded = decode_bytes_from_jpeg(img_name).decode("utf-8")
        # print(decoded)
        # self.assertEqual(message, decoded)


if __name__ == '__main__':
    unittest.main()
