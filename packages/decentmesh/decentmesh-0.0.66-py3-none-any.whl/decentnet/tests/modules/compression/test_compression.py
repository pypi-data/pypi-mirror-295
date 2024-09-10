import time
import unittest

from decentnet.modules.compression.wrapper import CompressionWrapper


class CompressionWrapperTests(unittest.TestCase):
    def setUp(self):
        self.data = b"Hello, worldas1d56as4v5c5a1v846fq56w4r5q45r45" \
                    b"q6w4r56qw4r56qw4r56qw4rq5w4r56q45r4q5w6r4" \
                    b"q564rq64r56qw465r456rq4rqq6w5r4rqw!"

    def test_compress_slow(self):
        start_time = time.time()
        compressed_data = CompressionWrapper.compress_brotli(self.data, quality=10)
        end_time = time.time()
        self.assertIsInstance(compressed_data, bytes)
        self.assertGreater(len(compressed_data), 0)
        print("Brotli Compression Time:", end_time - start_time)

    def test_compress_fast(self):
        start_time = time.time()
        compressed_data = CompressionWrapper.compress_zlib(self.data, level=9)
        end_time = time.time()
        self.assertIsInstance(compressed_data, bytes)
        self.assertGreater(len(compressed_data), 0)
        print("Zlib Compression Time:", end_time - start_time)

    def test_decompress_slow(self):
        compressed_data = CompressionWrapper.compress_brotli(self.data, quality=10)
        start_time = time.time()
        decompressed_data = CompressionWrapper.decompress_brotli(compressed_data)
        end_time = time.time()
        self.assertIsInstance(decompressed_data, bytes)
        self.assertEqual(decompressed_data, self.data)
        print("Brotli Decompression Time:", end_time - start_time)

    def test_decompress_fast(self):
        compressed_data = CompressionWrapper.compress_zlib(self.data, level=9)
        start_time = time.time()
        decompressed_data = CompressionWrapper.decompress_zlib(compressed_data)
        end_time = time.time()
        self.assertIsInstance(decompressed_data, bytes)
        self.assertEqual(decompressed_data, self.data)
        print("Zlib Decompression Time:", end_time - start_time)

    def test_lz4_compression(self):
        start_time = time.time()
        original_data = b"Test data for LZ4 compression"

        # Compress using LZ4
        compressed_data = CompressionWrapper.compress_lz4(original_data, 16)
        self.assertIsNotNone(compressed_data)
        self.assertGreater(len(compressed_data), 0)

        # Decompress LZ4 compressed data
        decompressed_data = CompressionWrapper.decompress_lz4(compressed_data)
        self.assertEqual(decompressed_data, original_data)

        end_time = time.time()
        print("LZ4 Compression Time:", end_time - start_time)


if __name__ == '__main__':
    unittest.main()
