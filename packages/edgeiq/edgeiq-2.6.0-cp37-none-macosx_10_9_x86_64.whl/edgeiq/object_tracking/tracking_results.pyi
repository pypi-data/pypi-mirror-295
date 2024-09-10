from .trackable_prediction import TrackablePrediction as TrackablePrediction, TrackablePredictionT as TrackablePredictionT
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from edgeiq.tools import to_json_serializable as to_json_serializable
from typing import Dict

class TrackingResults(Dict[int, TrackablePredictionT]):
    def __init__(self, objects: Dict[int, TrackablePredictionT], tracking_algorithm: str) -> None: ...
    @property
    def tracking_algorithm(self): ...
