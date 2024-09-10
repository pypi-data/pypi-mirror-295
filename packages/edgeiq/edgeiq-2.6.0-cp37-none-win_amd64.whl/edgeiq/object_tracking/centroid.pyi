from .defaults import DEFAULT_CONFIDENCE_THRESHOLD as DEFAULT_CONFIDENCE_THRESHOLD, DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA
from .matchers import match_greedy as match_greedy
from .trackable_prediction import TrackablePrediction as TrackablePrediction, TrackerCbT as TrackerCbT
from .tracker_algorithm import TrackerAlgorithm as TrackerAlgorithm
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from typing import Optional

class CentroidTracker(TrackerAlgorithm[TrackablePrediction[ObjectDetectionPrediction]]):
    def __init__(self, deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., confidence_threshold: float = ..., history_length: int = ..., enter_cb: Optional[TrackerCbT] = ..., exit_cb: Optional[TrackerCbT] = ...) -> None: ...
