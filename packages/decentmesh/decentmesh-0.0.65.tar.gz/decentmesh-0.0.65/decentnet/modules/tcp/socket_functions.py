import asyncio
import logging
import os
import threading
from typing import Optional

from decentnet.consensus.block_sizing import BLOCK_PREFIX_LENGTH_BYTES
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger
from decentnet.modules.tcp.db_functions import remove_alive_beam_from_db

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


def recv_all(socket, host: Optional[str] = None,
             port: Optional[int] = None) -> bytes:
    """Receive all bytes of a message up to total_bytes from a socket."""
    logger.debug(
        f"Thread {threading.current_thread().name} in PID {os.getpid()} is reading socket {socket}")

    try:
        length_prefix = socket.recv(BLOCK_PREFIX_LENGTH_BYTES)
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError,
            ConnectionRefusedError) as e:
        raise e
    finally:
        if host and port:
            asyncio.run(remove_alive_beam_from_db(host, port))

    total_bytes = int.from_bytes(length_prefix, ENDIAN_TYPE, signed=False)
    if total_bytes:
        logger.debug(
            f"Incoming message will have length {total_bytes} B |"
            f" prefix {length_prefix.hex()} | Thread: {threading.current_thread().name}")
    else:
        return b''

    data = b''
    while (data_len := len(data)) < total_bytes:
        # Attempt to read enough bytes to complete the message
        remaining_bytes = total_bytes - data_len
        packet = socket.recv(remaining_bytes)
        if not packet:
            # No more data is being sent; possibly the connection was closed
            logger.debug(
                f"Data is not being sent, closing connection... Remaining {remaining_bytes} Bytes Thread: {threading.current_thread().name} "
                f"| Buffer contained {data}")
            break
        data += packet
    return data
