import logging
import multiprocessing.queues
import numpy as np
from _typeshed import Incomplete
from edgeiq._environment import EDGEIQ_LOGS as EDGEIQ_LOGS
from typing import Optional, Tuple

console_handler: Incomplete
log_format: str
formatter: Incomplete

def gen_logger(name: Optional[str] = ..., add_console_handler: bool = ...) -> logging.Logger: ...

LOGGER: Incomplete

class JsonFile:
    def __init__(self, path: str) -> None: ...
    @property
    def contents(self) -> Optional[dict]: ...
    def exists(self) -> bool: ...
    def load(self) -> bool: ...

class MultiprocessingCircularQueue(multiprocessing.queues.Queue):
    def __init__(self, *args, **kwargs) -> None: ...
    def put(self, obj) -> None: ...

def empty_queue(q) -> None: ...
def draw_text_with_background(image: np.ndarray, text: str, start_x: int, start_y: int, font_size: float, font_thickness: int, color: Tuple[int, int, int], background_padding: int = ...) -> Tuple[np.ndarray, int, int]: ...

random_number_generator: Incomplete
