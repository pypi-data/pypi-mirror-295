from .. import utils as utils
from ._base_metric import _BaseMetric
from _typeshed import Incomplete

class Identity(_BaseMetric):
    @staticmethod
    def get_default_config(): ...
    integer_fields: Incomplete
    float_fields: Incomplete
    fields: Incomplete
    summary_fields: Incomplete
    config: Incomplete
    threshold: Incomplete
    def __init__(self, config: dict = ...) -> None: ...
    def eval_sequence(self, data: dict): ...
