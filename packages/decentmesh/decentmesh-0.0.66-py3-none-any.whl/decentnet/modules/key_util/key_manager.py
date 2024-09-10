import logging

import pyximport
from ecdsa import SigningKey, VerifyingKey
from sqlalchemy import select, delete

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.cryptography.asymetric import AsymCrypt
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.models import OwnedKeys
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

pyximport.install()
try:
    from decentnet.modules.convert.byte_to_base64_fast import bytes_to_base64  # noqa
except ImportError as ex:
    logger.debug(f"Operating in slow mode because of {ex}")
    logger.warning("Base64 convert module is operating in slow mode")
    from decentnet.modules.convert.byte_to_base64_slow import bytes_to_base64


class KeyManager:
    @classmethod
    def generate_singing_key_pair(cls):
        sign_keys = AsymCrypt.generate_key_pair_signing()
        private_key = sign_keys[0].to_string()
        public_key = sign_keys[1]
        return private_key, public_key

    @classmethod
    def generate_encryption_key_pair(cls):
        sign_keys = AsymCrypt.generate_key_pair_encryption()
        private_key = sign_keys[0]
        public_key = sign_keys[1]
        return private_key, public_key

    @classmethod
    def key_to_base64(cls, key: bytes):
        return bytes_to_base64(key)

    @classmethod
    def import_ssh_key_pair(cls, private_key_path, public_key_path):
        # TODO Implement
        raise NotImplemented()

    @classmethod
    def export_ssh_key_pair(cls, private_key_obj, public_key_obj):
        private_key_str = private_key_obj.get_base64()
        public_key_str = f"{public_key_obj.get_name()} {public_key_obj.get_base64().decode('utf-8')}"
        return private_key_str, public_key_str

    @classmethod
    async def clear_db(cls):
        async with session_scope() as session:
            # Delete all records from OwnedKeys table
            await session.execute(delete(OwnedKeys))
            await session.commit()

    @classmethod
    async def save_to_db(cls, private_key, public_key, description, can_encrypt, alias):
        async with session_scope() as session:
            ssh_key_pair = OwnedKeys(
                private_key=private_key,
                public_key=public_key,
                description=description,
                can_encrypt=can_encrypt,
                alias=alias
            )
            session.add(ssh_key_pair)
            await session.commit()
            return ssh_key_pair.id

    @classmethod
    async def retrieve_ssh_key_pair_from_db(cls, key_id: int, can_encrypt: bool = False) -> \
            tuple[
                SigningKey,
                VerifyingKey] | \
            tuple[
                bytes, bytes]:
        """Retrieve SSH key pair from the database.

        Args:
            key_id (int): The unique identifier of the SSH key pair to retrieve.

        Returns:
            Tuple[str, str] or Tuple[None, None]: A tuple containing the private key
            and public key retrieved from the database. If the specified key_id is not found,
            it returns (None, None).
            :param key_id: Key id to retrieve
            :param can_encrypt: property of a key
        """
        async with session_scope() as session:
            # Use an asynchronous query to find the key pair
            result = await session.execute(
                select(OwnedKeys).where(
                    OwnedKeys.id == key_id, OwnedKeys.can_encrypt == can_encrypt
                )
            )
            key_pair = result.scalar_one_or_none()

            if key_pair:
                return AsymCrypt.key_pair_from_private_key_base64(
                    key_pair.private_key, key_pair.can_encrypt
                )
            else:
                raise Exception(f"No Key with id {key_id} found")

    @classmethod
    async def get_private_key(cls, public_key: str):
        async with session_scope() as session:
            result = await session.execute(
                select(OwnedKeys).where(OwnedKeys.public_key == public_key)
            )
            key_pair = result.scalar_one_or_none()

            if key_pair:
                return AsymCrypt.key_pair_from_private_key_base64(
                    key_pair.private_key, key_pair.can_encrypt
                )[0]
            else:
                raise Exception(f"No Private Key found for public key {public_key}")
