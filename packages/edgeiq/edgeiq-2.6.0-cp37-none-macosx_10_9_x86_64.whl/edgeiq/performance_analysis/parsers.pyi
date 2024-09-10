from edgeiq import Dict as Dict, ObjectDetectionResults as ObjectDetectionResults
from edgeiq.bounding_box import BoundingBox as BoundingBox
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from typing import List, Optional, Tuple

def parse_cvat_annotations(path: str, start_frame: int = ..., end_frame: Optional[int] = ..., new_id_for_occlusion: bool = ...) -> Tuple[dict, dict]: ...
def parse_coco_annotations(path: str) -> List[ObjectDetectionResults]: ...
