from .app_process import AppProcess as AppProcess
from .logger import LoggerThread as LoggerThread
from .multi_stream_app_interface import MultiStreamAppInterface as MultiStreamAppInterface
from .shared import Shared as Shared
from edgeiq._utils import gen_logger as gen_logger
from typing import List, Type

class MultiStreamFramework:
    def __init__(self, apps: List[Type[MultiStreamAppInterface]], args: List[tuple]) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
