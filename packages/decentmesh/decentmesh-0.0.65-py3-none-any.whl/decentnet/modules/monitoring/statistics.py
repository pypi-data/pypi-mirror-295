import logging
import multiprocessing
from threading import Thread
from wsgiref.simple_server import make_server

import prometheus_client
from prometheus_client import Histogram

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.local_config import PROMETHEUS_PORT, PROMETHEUS_HOST
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

block_difficulty_bits = Histogram('block_difficulty_bits', 'Difficulty of blockchain bits')
block_difficulty_memory = Histogram('block_difficulty_memory',
                                    'Difficulty of blockchain memory')
block_difficulty_time = Histogram('block_difficulty_time', 'Difficulty of blockchain time')
block_difficulty_parallel = Histogram('block_difficulty_parallel',
                                      'Difficulty of blockchain parallel')
data_header_ratio = Histogram('data_header_ratio', 'Header/Data Ratio')
prom_block_process_time = Histogram('block_process_time', 'Time spent processing a block')
prom_data_received = Histogram("data_received_for_relay", "Data received for relaying")
prom_path_length = Histogram("path_length", "Path length for relaying data")
prom_data_published = Histogram("data_published_for_relay", "Data published for relaying")


class Stats:
    @staticmethod
    def start_prometheus_server(log_dict: dict):
        log_dict["block_difficulty_bits"] = multiprocessing.Pipe()
        log_dict["block_difficulty_memory"] = multiprocessing.Pipe()
        log_dict["block_difficulty_time"] = multiprocessing.Pipe()
        log_dict["block_difficulty_parallel"] = multiprocessing.Pipe()
        log_dict["data_header_ratio"] = multiprocessing.Pipe()
        log_dict["block_process_time"] = multiprocessing.Pipe()
        log_dict["data_received_for_relay"] = multiprocessing.Pipe()
        log_dict["path_length"] = multiprocessing.Pipe()
        log_dict["data_published_for_relay"] = multiprocessing.Pipe()
        log_dict["prom_path_length"] = multiprocessing.Pipe()
        log_dict["prom_data_received"] = multiprocessing.Pipe()
        log_dict["prom_data_published"] = multiprocessing.Pipe()
        log_dict["prom_block_process_time"] = multiprocessing.Pipe()

        Stats.wait_write_stats(log_dict)
        logger.debug("Starting prometheus client...")
        app = prometheus_client.make_wsgi_app()
        httpd = make_server(PROMETHEUS_HOST, PROMETHEUS_PORT, app)
        httpd.serve_forever()

        for value in log_dict.values():
            value[0].close()
            value[1].close()

    @staticmethod
    def wait_write_stats(log_dict: dict):
        for key, log_pipe in log_dict.items():
            Thread(target=Stats.wait_write, args=(key, log_pipe), name=f"Observing {key}",
                   daemon=True).start()

    @staticmethod
    def wait_write(key, log_pipe):
        while True:
            value = log_pipe[0].recv()
            globals().get(key).observe(value)
