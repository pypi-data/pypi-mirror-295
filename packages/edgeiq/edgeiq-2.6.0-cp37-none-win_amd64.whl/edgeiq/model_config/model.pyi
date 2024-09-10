from _typeshed import Incomplete
from typing import Optional

data_dir: Incomplete
catalog: Incomplete
hailoModel: Incomplete
qaicModel: Incomplete
tensorrtModel: Incomplete
onnxModel: Incomplete
modelParameters: Incomplete
modelJson: Incomplete

class ModelJson:
    accuracy: Optional[str]
    dataset: str
    description: str
    id: str
    inference_time: Optional[int]
    license: str
    mean_average_precision_top_1: Optional[int]
    mean_average_precision_top_5: Optional[int]
    public: Optional[bool]
    website_url: str
    model_parameters: object
    def __init__(self, accuracy, dataset, description, id, inference_time, license, mean_average_precision_top_1, mean_average_precision_top_5, public, website_url, model_parameters) -> None: ...

def validate_model(model_config: dict): ...
