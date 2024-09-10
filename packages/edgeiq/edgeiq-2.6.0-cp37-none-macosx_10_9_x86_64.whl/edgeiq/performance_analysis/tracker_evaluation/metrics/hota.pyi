from ._base_metric import _BaseMetric
from _typeshed import Incomplete

class HOTA(_BaseMetric):
    plottable: bool
    array_labels: Incomplete
    integer_array_fields: Incomplete
    float_array_fields: Incomplete
    float_fields: Incomplete
    fields: Incomplete
    summary_fields: Incomplete
    def __init__(self, config: dict = ...) -> None: ...
    def eval_sequence(self, data: dict): ...
