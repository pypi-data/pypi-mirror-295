import numpy as np
from ..connection.iot_core_connection import IoTCoreConnection as IoTCoreConnection
from ..constants import IMAGE_TYPE as IMAGE_TYPE, TO_CLOUD_TOPIC_PREFIX as TO_CLOUD_TOPIC_PREFIX
from ..credentials import CLIENT_ID as CLIENT_ID
from ..util import ProdClientError as ProdClientError
from .base_client import BaseClient as BaseClient
from _typeshed import Incomplete
from edgeiq.app_config import AppConfig as AppConfig
from typing import Any

class ImageCloudWriter(BaseClient):
    cloud_connection: Incomplete
    publish_topic: Incomplete
    subscribe_url_response_topic: Incomplete
    exit_event: Incomplete
    images: Incomplete
    def __init__(self) -> None: ...
    def publish_image(self, image: np.ndarray, tag: Any = None): ...
    def publish(self, message: str): ...
    def stop(self) -> None: ...
