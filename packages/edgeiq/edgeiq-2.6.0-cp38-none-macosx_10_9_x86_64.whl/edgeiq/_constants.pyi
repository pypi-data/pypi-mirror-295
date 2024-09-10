from _typeshed import Incomplete
from enum import Enum

HAILO_VID: str
HAILO_PID: str
CUDA_SUPPORTED_BOARDS: Incomplete
TEGRA_MODEL_PATH: str
HAILO_SUPPORTED_OS: Incomplete
QAIC_SUPPORTED_OS: Incomplete

class SupportedDevices(str, Enum):
    XAVIER_NX: str
    AGX_XAVIER: str
    AGX_ORIN: str
    ORIN_NX: str

class SupportedPurposes(str, Enum):
    OBJECT_DETECTION: str
    IMAGE_CLASSIFICATION: str
    POSE_ESTIMATION: str
    REIDENTIFICATION: str
    INSTANCE_SEGMENTATION: str
    SEMANTIC_SEGMENTATION: str
    BARCODE_DETECTION: str
    QRCODE_DETECTION: str
