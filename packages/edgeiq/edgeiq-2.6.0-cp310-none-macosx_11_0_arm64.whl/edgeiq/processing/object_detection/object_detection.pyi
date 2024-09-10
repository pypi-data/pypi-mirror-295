import numpy as np
from ..processor import Processor as Processor
from .types import ObjectDetectionPostProcessBatchParams as ObjectDetectionPostProcessBatchParams, ObjectDetectionPostProcessParams as ObjectDetectionPostProcessParams, ObjectDetectionPreProcessBatchParams as ObjectDetectionPreProcessBatchParams, ObjectDetectionPreProcessParams as ObjectDetectionPreProcessParams
from _typeshed import Incomplete
from edgeiq._utils import gen_logger as gen_logger
from edgeiq.bounding_box import BoundingBox as BoundingBox
from edgeiq.model_config import ModelConfig as ModelConfig
from typing import Any, Callable

PreProcessT: Incomplete
PreProcessBatchT: Incomplete
PostProcessT = Callable[[ObjectDetectionPostProcessParams], tuple[list[BoundingBox], list[float], list[int]]]
PostProcessBatchT = Callable[[ObjectDetectionPostProcessBatchParams], tuple[list[list[BoundingBox]], list[list[float]], list[list[int]]]]

class ObjectDetectionProcessor(Processor):
    def __init__(self, model_config: ModelConfig, pre_process: PreProcessT | None = None, pre_process_batch: PreProcessBatchT | None = None, post_process: PostProcessT | None = None, post_process_batch: PostProcessBatchT | None = None) -> None: ...
    def load(self) -> None: ...
    def pre_process(self, image: np.ndarray) -> np.ndarray: ...
    def pre_process_batch(self, images: list[np.ndarray]) -> np.ndarray: ...
    def post_process(self, results: Any, image: np.ndarray, confidence_level: float, overlap_threshold: float) -> tuple[list[BoundingBox], list[float], list[int]]: ...
    def post_process_batch(self, results: list[Any], images: list[np.ndarray], confidence_level: float, overlap_threshold: float) -> tuple[list[list[BoundingBox]], list[list[float]], list[list[int]]]: ...
