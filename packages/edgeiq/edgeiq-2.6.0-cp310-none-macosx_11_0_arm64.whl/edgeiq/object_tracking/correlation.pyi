import numpy as np
from .defaults import DEFAULT_CONFIDENCE_THRESHOLD as DEFAULT_CONFIDENCE_THRESHOLD, DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA
from .matchers import match_greedy as match_greedy
from .tracker_algorithm import TrackerAlgorithm as TrackerAlgorithm, TrackingResults as TrackingResults
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from edgeiq.object_tracking.trackable_prediction import TrackablePrediction as TrackablePrediction, TrackerCbT as TrackerCbT
from enum import Enum
from typing import Callable

class TrackingState(Enum):
    DETECT = 'DETECT'
    REDETECT = 'REDETECT'

class TrackableCorrelationPrediction(TrackablePrediction[ObjectDetectionPrediction]):
    def __init__(self, *args, **kwargs) -> None: ...
    def handle_found(self, prediction: ObjectDetectionPrediction, dereg_tracked_obj: Callable[[], None], **kwargs): ...
    def handle_disappeared(self, image: np.ndarray, reg_tracked_obj: Callable[[], None], can_track_new_obj: Callable[[], bool], **kwargs): ...

class CorrelationTracker(TrackerAlgorithm[TrackableCorrelationPrediction]):
    def __init__(self, max_objects: int | None = None, deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., confidence_threshold: float = ..., history_length: int = ..., enter_cb: TrackerCbT | None = None, exit_cb: TrackerCbT | None = None) -> None: ...
    def update(self, predictions: list[ObjectDetectionPrediction], image: np.ndarray) -> TrackingResults[TrackableCorrelationPrediction]: ...
