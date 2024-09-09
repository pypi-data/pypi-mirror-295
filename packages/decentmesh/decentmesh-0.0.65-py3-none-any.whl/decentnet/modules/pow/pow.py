import logging

import pyximport
import rich

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

pyximport.install()
try:
    from decentnet.modules.pow.computation_fast import compute_argon2_pow, compute_sha256_pow  # noqa
except ImportError as ex:
    rich.print(f"[red]POW Operating in low hashrate mode, more instructions: {ex}[/red]")
    from decentnet.modules.pow.computation_slow import compute_argon2_pow, compute_sha256_pow


class PoW:
    @staticmethod
    def compute(input_hash, n_bits: int, start_nonce=0, express=False):
        if express:
            nonce = compute_sha256_pow(n_bits, input_hash, start_nonce)
        else:
            nonce = compute_argon2_pow(n_bits, input_hash, start_nonce)
        return input_hash, nonce
