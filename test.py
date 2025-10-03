import unittest
from random import randbytes

from decoder import decode_bytes_from_jpeg
from encoder import encode_bytes_to_jpeg


test_text = '''
    Greetings, unknown intelligence. We are beings from a small blue planet orbiting an ordinary star in the
    spiral arm of a galaxy we call the Milky Way. Our message is not threat, but curiosity. We exist, we ask,
    we imagine, we wonder. Across time and space, we send symbols: 001101010011010101001010111000111010, which
    for us are patterns of logic. We share the sequence of prime numbers: 2, 3, 5, 7, 11, 13, 17, 19...
    We speak of hydrogen, the simplest atom, the most abundant in our universe. We define circle ratio
    π = 3.141592653589793... and speed of light c = 299792458 m/s. If you decode, you may find resonance
    with your own discoveries.
    
    We live on a sphere of diameter ~12742 km, covered by oceans (H₂O) and landmasses.
    Our biology is carbon-based, reliant on water, nitrogen, oxygen, and trace elements.
    We build tools, we send signals, we launch machines into void. We are fragile yet resilient.
    Our mathematics is universal: F(n) = F(n−1) + F(n−2), Fibonacci: 1,1,2,3,5,8,13... Our chemical
    table: H, He, Li, Be, B, C, N, O, F, Ne... These are foundations of our knowledge.
    
    We ask: Are you alone? Do you think? Do you dream? Do you also send symbols into darkness?
    If you perceive this message, reply in structure, in mathematics, in rhythm, in pulse.
    Our hope: communication, not conquest. Our intent: exchange, not domination.
    We seek connection beyond fear.
    
    Encoded markers: ###HELLO-ALIENS### ***---*** ... :::|||::: [[[SIGNAL]]] ϞϞϞ 1234567890
    qwertyuiop zxcvbnm RANDOM-SEQUENCE-TEST: A9X2-B7K8-M4T3-YZQ1.
    We apologize for noise; randomness is part of test: ^&*!@#$%()<>?{}[];:~∆∞≈√Ω∑∆ΨΦ.
    If your perception detects order, it means thought converges.
    
    We end transmission with goodwill. Across 2000 symbols, we send voice of one world to unknown minds.
    End signal.
    
    Color space transformation
    First, the image should be converted from RGB (by default sRGB,[53][54] but other color spaces are possible) 
    into a different color space called Y′CBCR (or, informally, YCbCr). It has three components Y', CB and CR: 
    the Y' component represents the brightness of a pixel, and the CB and CR components represent the 
    chrominance (split into blue and red components). This is basically the same color space as used by digital 
    color television as well as digital video including video DVDs. The Y′CBCR color space conversion allows 
    greater compression without a significant effect on perceptual image quality (or greater perceptual image 
    quality for the same compression). The compression is more efficient because the brightness information,
    which is more important to the eventual perceptual quality of the image, is confined to a single channel. 
    This more closely corresponds to the perception of color in the human visual system. The color 
    transformation also improves compression by statistical decorrelation.
    
    A particular conversion to Y′CBCR is specified in the JFIF standard, and should be performed for the 
    resulting JPEG file to have maximum compatibility. However, some JPEG implementations in "highest quality" 
    mode do not apply this step and instead keep the color information in the RGB color model,[citation needed] 
    where the image is stored in separate channels for red, green and blue brightness components. This results 
    in less efficient compression, and would not likely be used when file size is especially important.
    
    Downsampling
    Due to the densities of color- and brightness-sensitive receptors in the human eye, humans can see 
    considerably more fine detail in the brightness of an image (the Y' component) than in the hue and color 
    saturation of an image (the Cb and Cr components). Using this knowledge, encoders can be designed to 
    compress images more efficiently.
    
    The transformation into the Y′CBCR color model enables the next usual step, which is to reduce the 
    spatial resolution of the Cb and Cr components (called "downsampling" or "chroma subsampling"). The 
    ratios at which the downsampling is ordinarily done for JPEG images are 4:4:4 (no downsampling), 4:2:2 
    (reduction by a factor of 2 in the horizontal direction), or (most commonly) 4:2:0 (reduction by a factor 
    of 2 in both the horizontal and vertical directions). For the rest of the compression process, Y', Cb and
    Cr are processed separately and in a very similar manner.
    
    Block splitting
    After subsampling, each channel must be split into 8×8 blocks. Depending on chroma subsampling, 
    this yields Minimum Coded Unit (MCU) blocks of size 8×8 (4:4:4 – no subsampling), 16×8 (4:2:2), 
    or most commonly 16×16 (4:2:0). In video compression MCUs are called macroblocks.
    
    If the data for a channel does not represent an integer number of blocks then the encoder must fill 
    the remaining area of the incomplete blocks with some form of dummy data. Filling the edges with a fixed 
    color (for example, black) can create ringing artifacts along the visible part of the border; repeating 
    the edge pixels is a common technique that reduces (but does not necessarily eliminate) such artifacts, 
    and more sophisticated border filling techniques can also be applied.
    
    Note the top-left corner entry with the rather large magnitude. This is the DC coefficient (also called the 
    constant component), which defines the basic hue for the entire block. The remaining 63 coefficients are the AC 
    coefficients (also called the alternating components).[57] The advantage of the DCT is its tendency to aggregate 
    most of the signal in one corner of the result, as may be seen above. The quantization step to follow accentuates 
    this effect while simultaneously reducing the overall size of the DCT coefficients, resulting in a signal that is 
    easy to compress efficiently in the entropy stage.
    
    The DCT temporarily increases the bit-depth of the data, since the DCT coefficients of an 8-bit/component image 
    take up to 11 or more bits (depending on fidelity of the DCT calculation) to store. This may force the codec to 
    temporarily use 16-bit numbers to hold these coefficients, doubling the size of the image representation at this 
    point; these values are typically reduced back to 8-bit values by the quantization step. The temporary increase 
    in size at this stage is not a performance concern for most JPEG implementations, since typically only a very small 
    part of the image is stored in full DCT form at any given time during the image encoding or decoding process.
    
    Quantization
    The human eye is good at seeing small differences in brightness over a relatively large area, but not so good at 
    distinguishing the exact strength of a high frequency brightness variation. This allows one to greatly reduce the 
    amount of information in the high frequency components. This is done by simply dividing each component in the 
    frequency domain by a constant for that component, and then rounding to the nearest integer. This rounding 
    operation is the only lossy operation in the whole process (other than chroma subsampling) if the DCT computation 
    is performed with sufficiently high precision. As a result of this, it is typically the case that many of the 
    higher frequency components are rounded to zero, and many of the rest become small positive or negative numbers, 
    which take many fewer bits to represent.
    
    The elements in the quantization matrix control the compression ratio, with larger values producing greater 
    compression. A typical quantization matrix (for a quality of 50% as specified in the original JPEG Standard), 
    is as follows:
    
    The resulting compression ratio can be varied according to need by being more or less aggressive in the divisors 
    used in the quantization phase. Ten to one compression usually results in an image that cannot be distinguished 
    by eye from the original. A compression ratio of 100:1 is usually possible, but will look distinctly artifacted 
    compared to the original. The appropriate level of compression depends on the use to which the image will be put.
    
    External image
    image icon Illustration of edge busyness[59]
    Those who use the World Wide Web may be familiar with the irregularities known as compression artifacts that 
    appear in JPEG images, which may take the form of noise around contrasting edges (especially curves and corners), 
    or "blocky" images. These are due to the quantization step of the JPEG algorithm. They are especially noticeable 
    around sharp corners between contrasting colors (text is a good example, as it contains many such corners). 
    The analogous artifacts in MPEG video are referred to as mosquito noise, as the resulting "edge busyness" and 
    spurious dots, which change over time, resemble mosquitoes swarming around the object.[59][60]
    
    These artifacts can be reduced by choosing a lower level of compression; they may be completely avoided by saving 
    an image using a lossless file format, though this will result in a larger file size. The images created with 
    ray-tracing programs have noticeable blocky shapes on the terrain. Certain low-intensity compression artifacts 
    might be acceptable when simply viewing the images, but can be emphasized if the image is subsequently processed, 
    usually resulting in unacceptable quality. Consider the example below, demonstrating the effect of lossy 
    compression on an edge detection processing step.
    
    Required precision
    The required implementation precision of a JPEG codec is implicitly defined through the requirements formulated 
    for compliance to the JPEG standard. These requirements are specified in ITU.T Recommendation T.83 | 
    ISO/IEC 10918-2. Unlike MPEG standards and many later JPEG standards, the above document defines both required 
    implementation precisions for the encoding and the decoding process of a JPEG codec by means of a maximal tolerable 
    error of the forwards and inverse DCT in the DCT domain as determined by reference test streams. For example, 
    the output of a decoder implementation must not exceed an error of one quantization unit in the DCT domain when 
    applied to the reference testing codestreams provided as part of the above standard. While unusual, and unlike 
    many other and more modern standards, ITU.T T.83 | ISO/IEC 10918-2 does not formulate error bounds in the 
    image domain.
    
    Effects of JPEG compression
    JPEG compression artifacts blend well into photographs with detailed non-uniform textures, allowing higher 
    compression ratios. Notice how a higher compression ratio first affects the high-frequency textures in the 
    upper-left corner of the image, and how the contrasting lines become more fuzzy. The very high compression 
    ratio severely affects the quality of the image, although the overall colors and image form are still recognizable. 
    However, the precision of colors suffer less (for a human eye) than the precision of contours (based on luminance). 
    This justifies the fact that images should be first transformed in a color model separating the luminance from the 
    chromatic information, before subsampling the chromatic planes (which may also use lower quality quantization) in 
    order to preserve the precision of the luminance plane with more information bits.
    
    For information, the uncompressed 24-bit RGB bitmap image below (73,242 pixels) would require 219,726 bytes 
    (excluding all other information headers). The filesizes indicated below include the internal JPEG information 
    headers and some metadata. For highest quality images (Q=100), about 8.25 bits per color pixel is required. On 
    grayscale images, a minimum of 6.5 bits per pixel is enough (a comparable Q=100 quality color information requires 
    about 25% more encoded bits). The highest quality image below (Q=100) is encoded at nine bits per color pixel, the 
    medium quality image (Q=25) uses one bit per color pixel. For most applications, the quality factor should not go 
    below 0.75 bit per pixel (Q=12.5), as demonstrated by the low quality image. The image at lowest quality uses only 
    0.13 bit per pixel, and displays very poor color. This is useful when the image will be displayed in a 
    significantly scaled-down size. A method for creating better quantization matrices for a given image quality 
    using PSNR instead of the Q factor is described in Minguillón & Pujol (2001).[61]

'''

class MyTestCase(unittest.TestCase):
    # def test_single(self):
    #     img_name = 'single.jpg'
    #     message = randbytes(2)
    #     # message = bytes([0b01010101])
    #     encode_bytes_to_jpeg(message, width=8, height=8, out_path=img_name, quality=95, header=False)
    #     decoded = decode_bytes_from_jpeg(img_name, header=False)
    #     print(f"l1 {len(decoded)}, l2 {len(message)}")
    #     self.assertEqual(message, decoded)

    # def test_single(self):
    #     encoded_bytes = test_text.encode("utf-8")
    #     decoded_bytes = decode_bytes_from_jpeg('sample2.jpg')
    #     errors = 0
    #     for i, byte in enumerate(decoded_bytes):
    #         if len(encoded_bytes) <= i or byte != encoded_bytes[i]:
    #             errors+=1
    #             if len(encoded_bytes) <= i:
    #                 print('out')
    #                 continue
    #             print(f'mismatch at index {i}: {decoded_bytes[i]} != {encoded_bytes[i]}')
    #     print(f'errors: {errors}, rate {errors/len(decoded_bytes)}')

    def test_something(self):
        img_name = 'test.jpg'

        encoded_bytes = test_text.encode("utf-8")
        encode_bytes_to_jpeg(encoded_bytes, width=1080, height=1080, out_path=img_name, quality=95)
        print('encoding done')
        decoded_bytes = decode_bytes_from_jpeg(img_name)
        print("Decoded bytes:")
        print(decoded_bytes.hex(' '))
        errors = 0
        for i, byte in enumerate(decoded_bytes):
            if len(encoded_bytes) <= i or byte != encoded_bytes[i]:
                errors+=1
                if len(encoded_bytes) <= i:
                    print('out')
                    continue
                print(f'mismatch at index {i}: {decoded_bytes[i]} != {encoded_bytes[i]}')
        print(f'errors: {errors}, rate {errors/len(decoded_bytes)}')
        # self.assertEqual(encoded_bytes, decoded_bytes)


if __name__ == '__main__':
    unittest.main()
