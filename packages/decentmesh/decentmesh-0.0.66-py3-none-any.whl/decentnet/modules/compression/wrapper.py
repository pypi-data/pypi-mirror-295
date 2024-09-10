import logging
import zlib
from builtins import memoryview

import brotli
import lz4.frame

from decentnet.consensus.compress_params import COMPRESSION_LEVEL_LZ4
from decentnet.consensus.dev_constants import RUN_IN_DEBUG, COMPRESSION_LOG_LEVEL
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)
logger.setLevel(COMPRESSION_LOG_LEVEL)

setup_logger(RUN_IN_DEBUG, logger)


class CompressionWrapper:
    chunk_size = 1024

    @staticmethod
    def compress_brotli(data: bytes, quality: int = 11) -> bytes:
        """
        Compresses data using Brotli compression algorithm with the specified quality.

        Args:
            data (bytes): The data to compress.
            quality (int): The compression quality. Higher values result in better compression but slower speed. Defaults to 11.

        Returns:
            bytes: The compressed data.
        """
        return brotli.compress(data, quality=quality)

    @staticmethod
    def compress_zlib(data: bytes, level: int = 6) -> bytes:
        """
        Compresses data using zlib compression algorithm with the specified compression level.

        Args:
            data (bytes): The data to compress.
            level (int): The compression level. Higher values result in better compression but slower speed. Defaults to 6.

        Returns:
            bytes: The compressed data.
        """
        return zlib.compress(data, level=level)

    @staticmethod
    def decompress_brotli(compressed_data: bytes) -> bytes:
        """
        Decompresses data using Brotli decompression algorithm.

        Args:
            compressed_data (bytes): The compressed data to decompress.

        Returns:
            bytes: The decompressed data.
        """
        return brotli.decompress(compressed_data)

    @staticmethod
    def decompress_zlib(compressed_data: bytes) -> bytes:
        """
        Decompresses data using zlib decompression algorithm.

        Args:
            compressed_data (bytes): The compressed data to decompress.

        Returns:
            bytes: The decompressed data.
        """
        return zlib.decompress(compressed_data)

    @staticmethod
    def compress_lz4(data: bytes,
                     compression_level: int = COMPRESSION_LEVEL_LZ4) -> bytes:
        """
        Compresses data using LZ4 compression algorithm with the specified compression level.

        Args:
            data (bytes): The data to compress.
            compression_level (int): The compression level (0-16), higher values result in better compression but slower speed. Defaults to 8.

        Returns:
            bytes: The compressed data.
        """
        data_size_before = len(data)
        logger.debug(f"Compressing data with LZ4 initial size {data_size_before} B")
        compressed = lz4.frame.compress(data, compression_level=compression_level)
        data_size_after = len(compressed)
        logger.debug(f"Compressed data to {data_size_after} B")
        if data_size_before < data_size_after:
            logger.debug(f"Disabled compression due to data incompatibility")
            return data
        return compressed

    @staticmethod
    def decompress_lz4(compressed_data: bytes | memoryview) -> bytes:
        """
        Decompresses data using LZ4 decompression algorithm.

        Args:
            compressed_data (bytes): The compressed data to decompress.

        Returns:
            bytes: The decompressed data.
        """
        logger.debug("Decompressing data with LZ4")
        try:
            return lz4.frame.decompress(compressed_data)
        except RuntimeError:
            return compressed_data
