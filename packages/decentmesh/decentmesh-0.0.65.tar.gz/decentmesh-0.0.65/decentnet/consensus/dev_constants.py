"""
Debug Constants
"""
import logging
import os

RUN_IN_DEBUG = bool(os.getenv("DEBUG", True))
LOG_LEVEL = os.getenv("DEBUG_LEVEL", logging.DEBUG)
ENCRYPTION_DEBUG = bool(os.getenv("ENCRYPTION_DEBUG", False))
METRICS = os.getenv("METRICS", True)

SEEDS_AGENT_LOG_LEVEL = os.getenv("SEEDS_AGENT_LOG_LEVEL", logging.INFO)
COMPRESSION_LOG_LEVEL = os.getenv("COMPRESSION_LOG_LEVEL", logging.WARNING)
R2R_LOG_LEVEL = os.getenv("R2R_LOG_LEVEL", logging.INFO)
BLOCK_ERROR_DATA_LOG_LEN = 50
