import numpy as np
from .object_detection import ObjectDetectionResults as ObjectDetectionResults
from edgeiq import bounding_box as bounding_box
from edgeiq._constants import SupportedPurposes as SupportedPurposes
from edgeiq._production_client.production_client import PRODUCTION_CLIENT as PRODUCTION_CLIENT
from edgeiq.base_service import BaseService as BaseService
from edgeiq.exceptions import NoMoreResults as NoMoreResults
from edgeiq.model_config.model_config import ModelConfig as ModelConfig
from edgeiq.processing.object_detection.object_detection import ObjectDetectionProcessor as ObjectDetectionProcessor
from typing import Any

class ObjectDetectionAnalytics(BaseService[ObjectDetectionProcessor]):
    def __init__(self, annotations: list[list[ObjectDetectionResults]], model_id: str, model_config: ModelConfig | None = None) -> None: ...
    def detect_objects_for_stream(self, stream_idx: int, confidence_level: float = 0.3, overlap_threshold: float = 0.3) -> ObjectDetectionResults: ...
    def detect_objects(self, image: np.ndarray | None, confidence_level: float = 0.3, overlap_threshold: float = 0.3) -> ObjectDetectionResults: ...
    def detect_objects_batch(self, images: list[np.ndarray] | None, confidence_level: float = 0.3, overlap_threshold: float = 0.3) -> list[ObjectDetectionResults]: ...
    def publish_analytics(self, results: ObjectDetectionResults, tag: Any = None, **kwargs): ...
