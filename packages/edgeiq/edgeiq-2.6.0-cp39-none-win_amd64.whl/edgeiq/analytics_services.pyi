from _typeshed import Incomplete
from edgeiq._constants import SupportedPurposes as SupportedPurposes
from edgeiq._production_client import PRODUCTION_CLIENT as PRODUCTION_CLIENT
from edgeiq._production_client.util import create_analytics_message_packet as create_analytics_message_packet
from edgeiq._utils import gen_logger as gen_logger
from edgeiq.barcode_detection import BarcodeDetectionResults as BarcodeDetectionResults
from edgeiq.event_services import EndTimedEvent as EndTimedEvent, OccurrenceEvent as OccurrenceEvent, StartTimedEvent as StartTimedEvent, ValueEvent as ValueEvent
from edgeiq.image_classification import ClassificationResults as ClassificationResults
from edgeiq.instance_segmentation import InstanceSegmentationResults as InstanceSegmentationResults
from edgeiq.object_detection import ObjectDetectionResults as ObjectDetectionResults
from edgeiq.object_tracking.tracking_results import TrackingResults as TrackingResults
from edgeiq.pose_estimation import HumanPoseResult as HumanPoseResult
from edgeiq.qrcode_detection import QRCodeDetectionResults as QRCodeDetectionResults
from edgeiq.re_identification import ReIdentificationResults as ReIdentificationResults
from edgeiq.tools.results_serialization import to_json_serializable as to_json_serializable
from typing import Any

logger: Incomplete
INVALID_ANALYTICS_FORMAT_MESSAGE: str
CORRUPTED_ANALYTICS_FILE_MESSAGE: str

class CustomEvent:
    def __init__(self, results: Any) -> None: ...
    @property
    def results(self) -> Any: ...
    @property
    def tag(self) -> Any | None: ...
    @tag.setter
    def tag(self, tag: Any | None): ...

def load_analytics_results(filepath: str) -> list: ...
def parse_analytics_packet(packet_str: str): ...
def publish_analytics(results, tag: Any = None, **kwargs): ...
def write_object_detection_results_to_analytics_file(output_file_path: str, results: ObjectDetectionResults) -> None: ...
def write_tracking_results_to_analytics_file(output_file_path: str, results: TrackingResults) -> None: ...
