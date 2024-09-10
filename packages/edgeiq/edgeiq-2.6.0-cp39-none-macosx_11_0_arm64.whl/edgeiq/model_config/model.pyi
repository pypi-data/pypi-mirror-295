from _typeshed import Incomplete
from dataclasses import dataclass

data_dir: Incomplete
catalog: Incomplete
hailoModel: Incomplete
qaicModel: Incomplete
tensorrtModel: Incomplete
onnxModel: Incomplete
modelParameters: Incomplete
modelJson: Incomplete

@dataclass
class ModelJson:
    accuracy: str | None
    dataset: str
    description: str
    id: str
    inference_time: int | None
    license: str
    mean_average_precision_top_1: int | None
    mean_average_precision_top_5: int | None
    public: bool | None
    website_url: str
    model_parameters: object
    def __init__(self, accuracy, dataset, description, id, inference_time, license, mean_average_precision_top_1, mean_average_precision_top_5, public, website_url, model_parameters) -> None: ...

def validate_model(model_config: dict): ...
