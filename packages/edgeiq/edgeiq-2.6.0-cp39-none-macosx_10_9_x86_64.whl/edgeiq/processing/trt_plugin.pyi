from edgeiq._utils import gen_logger as gen_logger
from edgeiq.tools import find_nvidia_gpu as find_nvidia_gpu, get_gpu_archs as get_gpu_archs, is_jetson as is_jetson, is_jetson_agx_orin as is_jetson_agx_orin, is_jetson_agx_xavier as is_jetson_agx_xavier, is_jetson_xavier_nx as is_jetson_xavier_nx
from edgeiq.tools.hw_discovery import is_jetson_orin_nx as is_jetson_orin_nx

compute_architecture: list[str]

def load_trt_plugin() -> None: ...
