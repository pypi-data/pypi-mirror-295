from .. import utils as utils
from ._base_dataset import _BaseDataset
from _typeshed import Incomplete

class CustomMOTDataset(_BaseDataset):
    @staticmethod
    def get_default_dataset_config(): ...
    config: Incomplete
    gt_file: Incomplete
    tracker_file: Incomplete
    tracker_name: Incomplete
    def __init__(self, config: dict = ...) -> None: ...
    def get_preprocessed_seq_data(self, raw_data: dict): ...
