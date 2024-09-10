import multiprocessing
import threading
from edgeiq._utils import empty_queue as empty_queue, gen_logger as gen_logger
from logging import LogRecord
from typing import Optional

class LoggerThread(threading.Thread):
    def __init__(self, log_queue: multiprocessing.Queue[Optional[LogRecord]]) -> None: ...
    def run(self) -> None: ...
    def close(self) -> None: ...
