import numpy as np
from .processor import Processor
from dataclasses import dataclass
from edgeiq.model_config import ModelConfig
from edgeiq.pose_estimation_pose import Pose
from typing import Any, Callable

__all__ = ['PoseEstimationProcessor']

@dataclass
class PreProcessParams:
    image: np.ndarray
    size: tuple[int, int]
    scalefactor: float
    mean: tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, image, size, scalefactor, mean, swaprb, crop) -> None: ...

@dataclass
class PostProcessParams:
    results: Any
    image: np.ndarray
    def __init__(self, results, image) -> None: ...
PostProcessT = Callable[[PostProcessParams], list[Pose]]

class PoseEstimationProcessor(Processor):
    def __init__(self, model_config: ModelConfig) -> None: ...
    def load(self) -> None: ...
    def pre_process(self, image: np.ndarray) -> np.ndarray: ...
    def post_process(self, results: Any, image: np.ndarray) -> list[Pose]: ...
