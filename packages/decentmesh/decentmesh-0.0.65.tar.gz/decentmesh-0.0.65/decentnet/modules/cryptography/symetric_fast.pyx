#cython: language_level=3
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AESCipher:
    def __init__(self, password: bytes, key_size: int = 256, salt: bytes = None):
        if key_size not in (128, 192, 256):
            raise ValueError("Key size must be 128, 192, or 256 bits.")
        self.password = password
        self.key_size = key_size
        self.salt = salt if salt is not None else os.urandom(16)
        self.backend = default_backend()

    def derive_key(self, password: bytes, salt: bytes, key_size: int):
        """Derive a cryptographic key from the given password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_size // 8,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password)

    def encrypt(self, plaintext: bytes) -> bytes:
        key = self.derive_key(self.password, self.salt, self.key_size)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), self.backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        return self.salt + iv + cipher_text  # Prepend the salt and IV to the ciphertext

    def decrypt(self, cipher_text: bytes) -> bytes:
        salt = cipher_text[:16]  # Extract the salt
        iv = cipher_text[16:32]  # Extract the IV
        key = self.derive_key(self.password, salt,
                              self.key_size)  # Re-derive the key using the extracted salt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(cipher_text[32:]) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext
