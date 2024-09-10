from _typeshed import Incomplete
from edgeiq._globals import DEVICE_UUID as DEVICE_UUID, SYSTEM_ID as SYSTEM_ID
from edgeiq._system_cfg import get_device_config_dir_path as get_device_config_dir_path

CREDENTIAL_ENDPOINT: Incomplete
ENDPOINT: Incomplete
CLIENT_ID: Incomplete
CLIENT_ID = DEVICE_UUID

class Certificates:
    exist: bool
    cert_path: Incomplete
    key_path: Incomplete
    root_ca_path: Incomplete
    def __init__(self) -> None: ...
