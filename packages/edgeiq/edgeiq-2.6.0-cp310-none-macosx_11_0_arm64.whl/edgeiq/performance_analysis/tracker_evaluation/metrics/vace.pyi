from ._base_metric import _BaseMetric
from _typeshed import Incomplete

class VACE(_BaseMetric):
    integer_fields: Incomplete
    float_fields: Incomplete
    fields: Incomplete
    summary_fields: Incomplete
    threshold: float
    def __init__(self, config: dict = None) -> None: ...
    def eval_sequence(self, data: dict): ...
