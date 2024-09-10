from ._base_metric import _BaseMetric
from _typeshed import Incomplete

class Count(_BaseMetric):
    integer_fields: Incomplete
    fields: Incomplete
    summary_fields: Incomplete
    def __init__(self, config: dict = ...) -> None: ...
    def eval_sequence(self, data: dict): ...
