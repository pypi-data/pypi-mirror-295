import logging

from sqlalchemy import select

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.models import NodeInfoTable, AliveBeam
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


async def remove_alive_beam_from_db(host: str, port: int):
    async with session_scope() as session:
        node_info = await session.execute(
            select(NodeInfoTable).where(
                (
                        (NodeInfoTable.ipv4 == host) | (NodeInfoTable.ipv6 == host)
                ) & (NodeInfoTable.port == port)
            )
        )
        node_info = node_info.scalar_one_or_none()

        if node_info:
            pub_key_base64 = node_info.pub_key
            logger.debug(f"Removing dead beam {pub_key_base64}")
            ab = await session.execute(
                select(AliveBeam).where(AliveBeam.pub_key == pub_key_base64)
            )
            ab = ab.scalar_one_or_none()

            if ab:
                await session.delete(ab)
                await session.commit()


async def remove_alive_beam_from_db_w_pub_key(pub_key_base64: str):
    if not pub_key_base64:
        return
    async with session_scope() as session:
        logger.debug(f"Removing dead beam {pub_key_base64}")
        ab = await session.execute(
            select(AliveBeam).where(AliveBeam.pub_key == pub_key_base64)
        )
        ab = ab.scalar_one_or_none()

        if ab:
            await session.delete(ab)
            await session.commit()
