import numpy as np
from dataclasses import dataclass
from typing import Any

@dataclass
class ObjectDetectionPreProcessParams:
    image: np.ndarray
    size: tuple[int, int]
    scalefactor: float
    mean: tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, image, size, scalefactor, mean, swaprb, crop) -> None: ...

@dataclass
class ObjectDetectionPreProcessBatchParams:
    images: list[np.ndarray]
    size: tuple[int, int]
    scalefactor: float
    mean: tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, images, size, scalefactor, mean, swaprb, crop) -> None: ...

@dataclass
class ObjectDetectionPostProcessParams:
    results: Any
    image: np.ndarray
    confidence_level: float
    overlap_threshold: float
    num_classes: int
    model_input_size: tuple[int, int]
    def __init__(self, results, image, confidence_level, overlap_threshold, num_classes, model_input_size) -> None: ...

@dataclass
class ObjectDetectionPostProcessBatchParams:
    results: list[Any]
    images: list[np.ndarray]
    confidence_level: float
    overlap_threshold: float
    num_classes: int
    model_input_size: tuple[int, int]
    def __init__(self, results, images, confidence_level, overlap_threshold, num_classes, model_input_size) -> None: ...
