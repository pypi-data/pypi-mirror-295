import asyncio
import logging
import os
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.local_config import DB_FILENAME, DATABASE_URL
from decentnet.modules.db.models import Base
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


@lru_cache()
def get_root_dir() -> Path:
    return Path(os.path.abspath(__file__)).parent.parent.parent.parent


async def init_db(eng):
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


db_file = get_root_dir() / DB_FILENAME
engine = create_async_engine(DATABASE_URL, echo=False)

asyncio.run(init_db(engine))


@asynccontextmanager
async def session_scope():
    """Provide a transactional scope around a series of operations asynchronously."""
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )()
    try:
        yield async_session
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        raise e
    finally:
        await async_session.close()
