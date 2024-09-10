import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod

class _BaseMetric(ABC, metaclass=abc.ABCMeta):
    plottable: bool
    integer_fields: Incomplete
    float_fields: Incomplete
    array_labels: Incomplete
    integer_array_fields: Incomplete
    float_array_fields: Incomplete
    fields: Incomplete
    summary_fields: Incomplete
    registered: bool
    @abstractmethod
    def __init__(self): ...
    @abstractmethod
    def eval_sequence(self, data: dict): ...
    @classmethod
    def get_name(cls): ...
    def print_table(self, table_res: dict, tracker: str): ...
