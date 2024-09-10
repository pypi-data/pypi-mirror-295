import hashlib

import argon2

from decentnet.consensus.block_sizing import HASH_LEN
from decentnet.consensus.blockchain_params import BlockchainParams
from decentnet.modules.pow.difficulty import Difficulty


def argon_hash_func(data: bytes, diff: Difficulty):
    return argon2.hash_password_raw(data, BlockchainParams.default_salt, diff.t_cost,
                                    diff.m_cost,
                                    diff.p_cost, diff.hash_len_chars)


def sha256_hash_func(data: bytes):
    return hashlib.sha256(data).digest()[:HASH_LEN]
