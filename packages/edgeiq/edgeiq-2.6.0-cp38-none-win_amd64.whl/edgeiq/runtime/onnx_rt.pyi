import numpy as np
from .runtime import Runtime
from _typeshed import Incomplete
from edgeiq.engine_accelerator import Accelerator
from edgeiq.model_config import ModelConfig

__all__ = ['OnnxRT']

class OnnxRT(Runtime):
    net: Incomplete
    input_name: Incomplete
    layer_names: Incomplete
    def __init__(self, model_config: ModelConfig, accelerator: Accelerator) -> None: ...
    def forward(self): ...
    def set_input(self, image: np.ndarray): ...
