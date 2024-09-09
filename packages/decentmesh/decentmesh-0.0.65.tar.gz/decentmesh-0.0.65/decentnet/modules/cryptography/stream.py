import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


def derive_key(salt: bytes, password: bytes, iterations: int, key_length: int) -> bytes:
    """
    Derives a key from the provided salt and password using PBKDF2.

    Args:
        salt: The salt value used in key derivation.
        password: The password to derive the key from.
        iterations: The number of iterations for the key derivation algorithm.
        key_length: The desired length of the derived key in bytes.

    Returns:
        The derived key.

    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key


def encrypt_data(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes) -> bytes:
    """
    Encrypts the provided plaintext using ChaCha20-Poly1305.

    Args:
        key: The encryption key.
        nonce: The nonce value for the encryption.
        plaintext: The data to be encrypted.
        aad: Additional authenticated data.

    Returns:
        The ciphertext.

    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(aad)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext


def decrypt_data(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> bytes:
    """
    Decrypts the provided ciphertext using ChaCha20-Poly1305.

    Args:
        key: The decryption key.
        nonce: The nonce value for the decryption.
        ciphertext: The data to be decrypted.
        aad: Additional authenticated data.

    Returns:
        The decrypted plaintext.

    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(aad)
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
