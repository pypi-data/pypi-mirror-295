from . import datasets as datasets, metrics as metrics, utils as utils
from .metrics import Count as Count
from _typeshed import Incomplete

class MOTPerformanceAnalyzer:
    gt_path: Incomplete
    output_pth: Incomplete
    def __init__(self, gt_pth: str, tracker_pth: str, metrics_list: list[str], output_pth: str | None = None) -> None: ...
    def evaluate(self) -> None: ...
