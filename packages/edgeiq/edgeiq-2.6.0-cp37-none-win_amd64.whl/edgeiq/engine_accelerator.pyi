from enum import Enum

class Engine(str, Enum):
    DNN: str
    DNN_CUDA: str
    TENSOR_RT: str
    HAILO_RT: str
    QAIC_RT: str
    ONNX_RT: str
    PYTORCH: str

class Accelerator(str, Enum):
    DEFAULT: str
    CPU: str
    GPU: str
    NVIDIA: str
    NVIDIA_FP16: str
    NVIDIA_DLA_0: str
    NVIDIA_DLA_1: str
    HAILO: str
    QAIC: str
