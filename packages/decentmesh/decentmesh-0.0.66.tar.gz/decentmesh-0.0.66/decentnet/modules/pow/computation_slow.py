import argon2

from decentnet.consensus.blockchain_params import BlockchainParams
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.modules.pow.hashing import sha256_hash_func


def int_to_bytes(num: int, buffer=None):
    if num == 0:
        return b'\x00'

        # Calculate the number of bytes needed to represent the integer
    byte_length = (num.bit_length() + 7) // 8

    # If no buffer is provided or it's too small, return the bytes directly
    if buffer is None or len(buffer) < byte_length:
        return num.to_bytes(byte_length, ENDIAN_TYPE)

    # Convert integer to bytes directly into the provided buffer
    num_bytes = num.to_bytes(byte_length, ENDIAN_TYPE)

    buffer[:byte_length] = num_bytes
    return bytes(buffer[:byte_length])


def compute_argon2_pow(n_bits, hash_t, nonce):
    _bits = hash_t.diff.hash_len_chars * 8 - n_bits
    # Clone the original hash_t to avoid modifying the original object

    while int.from_bytes(argon2.hash_password_raw(int_to_bytes(hash_t.value_as_int() + nonce),
                                                  BlockchainParams.default_salt, hash_t.diff.t_cost,
                                                  hash_t.diff.m_cost,
                                                  hash_t.diff.p_cost, hash_t.diff.hash_len_chars),
                         ENDIAN_TYPE).bit_length() > _bits:
        nonce += 1

    # Return the correct nonce but do not modify the original hash_t
    return nonce


def compute_sha256_pow(n_bits, hash_t, nonce):
    _bits = hash_t.diff.hash_len_chars * 8 - n_bits

    # Loop until the condition is satisfied
    while int.from_bytes(
            sha256_hash_func(int_to_bytes(hash_t.value_as_int() + nonce)),
            ENDIAN_TYPE).bit_length() > _bits:
        nonce += 1

    # Return the correct nonce without modifying the original hash_t
    return nonce
