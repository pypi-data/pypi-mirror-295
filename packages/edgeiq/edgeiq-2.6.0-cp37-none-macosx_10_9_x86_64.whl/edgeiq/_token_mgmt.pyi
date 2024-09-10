from _typeshed import Incomplete
from edgeiq._system_cfg import DevHostCredentialsFile as DevHostCredentialsFile, DeviceConfigFile as DeviceConfigFile, DeviceConfigFileLegacy as DeviceConfigFileLegacy, get_system_id as get_system_id
from typing import Dict, List, Optional

LOGGER: Incomplete
DAYS_TO_SECONDS: int

class ErrorCode:
    def __init__(self) -> None: ...
    @property
    def list(self): ...
    def log(self, code) -> None: ...

ERROR_CODE: Incomplete

def reset_errors() -> None: ...
def log_error(error_code) -> None: ...

ERROR_NO_CREDENTIALS_FILE: int
ERROR_SYSTEM_ID: int
ERROR_DEVICE_UUID: int
ERROR_NO_DEVICE_TOKENS: int
ERROR_DEVICE_TOKEN_REFRESH_FAILURE_EXCEPTION: int
ERROR_DEVICE_TOKEN_REFRESH_FAILURE_STATUS: int
ERROR_DEVICE_TOKEN_REFRESH_FAILURE_FORMAT: int
ERROR_NO_DEV_HOST_TOKENS: int
ERROR_DEV_HOST_TOKEN_REFRESH_FAILURE_EXCEPTION: int
ERROR_DEV_HOST_TOKEN_REFRESH_FAILURE_FORMAT: int
ERROR_NO_INTERNET_CONNECTION: int
ERROR_TOKEN_HEADERS_FAILURE: int
ERROR_NO_PUBLIC_KEY: int
ERROR_TOKEN_SIGNATURE_FAILED: int
ERROR_TOKEN_CLAIM_INVALID: int
ERROR_TOKEN_SIGNATURE_EXPIRED: int
ERROR_TOKEN_SIGNATURE_INVALID: int
ERROR_TOKEN_EXPIRED: int
ERROR_MALFORMED_TOKEN: int
ERROR_NO_ID_TOKEN_OR_KEYS: int
ERROR_UNHANDLED: int
ERROR_NO_USERNAME: int

class DeviceUserPool:
    user_pool_id: str
    development_client_id: str
    production_client_id: str
    keys: List[Dict[str, str]]
    def __init__(self, user_pool_id, development_client_id, production_client_id, keys) -> None: ...

class DevHostUserPool:
    user_pool_id: str
    client_id: str
    keys: List[Dict[str, str]]
    def __init__(self, user_pool_id, client_id, keys) -> None: ...

DEVICE_USER_POOL_CONFIG: Dict[str, DeviceUserPool]
DEV_HOST_USER_POOL_CONFIG: Dict[str, DevHostUserPool]
REGION: str
REFRESH_DEVICE_ENDPOINT: Incomplete

class Token:
    token: Incomplete
    def __init__(self, token: str, keys: List[Dict[str, str]], audiences: List[str]) -> None: ...
    def decode(self): ...
    def validate_expiry(self): ...
    def get_audience(self, is_id_token: bool = ...): ...
    @property
    def claims(self): ...

class TokenGroup:
    def __init__(self, refresh_token: Optional[str], undecoded_id_token: Optional[str], user_pool_id: str, keys: Optional[List[Dict[str, str]]], audiences: List[str]) -> None: ...
    def exists(self): ...
    def decode(self): ...
    def validate(self): ...
    def get_username(self) -> Optional[str]: ...

class DeviceTokens(TokenGroup):
    mode: str
    def __init__(self, refresh_token: Optional[str], id_token: Optional[str], system_id: str, device_uuid: str) -> None: ...
    def decode(self): ...
    def refresh(self): ...

class DevelopmentHostTokens(TokenGroup):
    def __init__(self, token_file: DevHostCredentialsFile, system_id: str) -> None: ...
    def refresh(self): ...

def validate_device_tokens(system_id: str) -> bool: ...
def validate_development_host_tokens(system_id: str) -> bool: ...
def validate_credentials() -> None: ...
