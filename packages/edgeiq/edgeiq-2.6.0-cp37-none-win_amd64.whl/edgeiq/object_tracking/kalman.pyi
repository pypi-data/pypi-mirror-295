import numpy as np
from .defaults import DEFAULT_CONFIDENCE_THRESHOLD as DEFAULT_CONFIDENCE_THRESHOLD, DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA
from .matchers import match_greedy as match_greedy
from .tracker_algorithm import TrackerAlgorithm as TrackerAlgorithm
from _typeshed import Incomplete
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from edgeiq.object_tracking.trackable_prediction import TrackablePrediction as TrackablePrediction, TrackerCbT as TrackerCbT
from typing import Optional

class TrackableKalmanPrediction(TrackablePrediction[ObjectDetectionPrediction]):
    filter: Incomplete
    dim_x: Incomplete
    dim_z: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def estimated_position(self) -> np.ndarray: ...
    @property
    def estimated_velocity(self) -> np.ndarray: ...
    def step(self, **kwargs) -> None: ...
    def handle_found(self, prediction: ObjectDetectionPrediction, **kwargs): ...

class KalmanTracker(TrackerAlgorithm[TrackableKalmanPrediction]):
    def __init__(self, deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., confidence_threshold: float = ..., history_length: int = ..., enter_cb: Optional[TrackerCbT] = ..., exit_cb: Optional[TrackerCbT] = ...) -> None: ...
