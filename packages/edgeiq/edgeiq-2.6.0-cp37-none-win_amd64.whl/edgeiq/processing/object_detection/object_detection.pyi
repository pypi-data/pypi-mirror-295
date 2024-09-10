import numpy as np
from ..processor import Processor as Processor
from .types import ObjectDetectionPostProcessBatchParams as ObjectDetectionPostProcessBatchParams, ObjectDetectionPostProcessParams as ObjectDetectionPostProcessParams, ObjectDetectionPreProcessBatchParams as ObjectDetectionPreProcessBatchParams, ObjectDetectionPreProcessParams as ObjectDetectionPreProcessParams
from _typeshed import Incomplete
from edgeiq._utils import gen_logger as gen_logger
from edgeiq.bounding_box import BoundingBox as BoundingBox
from edgeiq.model_config import ModelConfig as ModelConfig
from typing import Any, Callable, List, Optional, Tuple

PreProcessT: Incomplete
PreProcessBatchT: Incomplete
PostProcessT = Callable[[ObjectDetectionPostProcessParams], Tuple[List[BoundingBox], List[float], List[int]]]
PostProcessBatchT = Callable[[ObjectDetectionPostProcessBatchParams], Tuple[List[List[BoundingBox]], List[List[float]], List[List[int]]]]

class ObjectDetectionProcessor(Processor):
    def __init__(self, model_config: ModelConfig, pre_process: Optional[PreProcessT] = ..., pre_process_batch: Optional[PreProcessBatchT] = ..., post_process: Optional[PostProcessT] = ..., post_process_batch: Optional[PostProcessBatchT] = ...) -> None: ...
    def load(self) -> None: ...
    def pre_process(self, image: np.ndarray) -> np.ndarray: ...
    def pre_process_batch(self, images: List[np.ndarray]) -> np.ndarray: ...
    def post_process(self, results: Any, image: np.ndarray, confidence_level: float, overlap_threshold: float) -> Tuple[List[BoundingBox], List[float], List[int]]: ...
    def post_process_batch(self, results: List[Any], images: List[np.ndarray], confidence_level: float, overlap_threshold: float) -> Tuple[List[List[BoundingBox]], List[List[float]], List[List[int]]]: ...
