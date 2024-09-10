from _typeshed import Incomplete
from abc import ABC
from typing import Any

__all__ = ['generate_event_timestamp', 'OccurrenceEvent', 'ValueEvent', 'StartTimedEvent', 'EndTimedEvent', 'CompleteTimedEvent']

def generate_event_timestamp(): ...

class BaseEvent(ABC):
    timestamp: Incomplete
    event_label: Incomplete
    object_label: Incomplete
    object_id: Incomplete
    event_id: Incomplete
    camera_label: Incomplete
    zone_label: Incomplete
    data: Incomplete
    def __init__(self, timestamp: str, event_label: str, event_id: str | None = None, object_label: str | None = None, object_id: str | None = None, camera_label: str | None = None, zone_label: str | None = None, data: Any | None = None) -> None: ...
    def __eq__(self, other): ...
    def publish_event(self, **kwargs) -> None: ...

class OccurrenceEvent(BaseEvent): ...

class ValueEvent(BaseEvent):
    value: Incomplete
    def __init__(self, timestamp: str, event_label: str, value: int | float, event_id: str | None = None, object_label: str | None = None, object_id: str | None = None, camera_label: str | None = None, zone_label: str | None = None, data: Any | None = None) -> None: ...
    def __eq__(self, other): ...

class StartTimedEvent(BaseEvent): ...

class EndTimedEvent(BaseEvent):
    def __init__(self, timestamp: str, event_label: str, event_id: str, object_label: str | None = None, object_id: str | None = None, camera_label: str | None = None, zone_label: str | None = None, data: Any | None = None) -> None: ...

class CompleteTimedEvent:
    start_timed_event: Incomplete
    end_timed_event: Incomplete
    def __init__(self, start_timestamp, end_timestamp, event_label, event_id: Incomplete | None = None, start_object_label: Incomplete | None = None, start_object_id: Incomplete | None = None, start_camera_label: Incomplete | None = None, start_zone_label: Incomplete | None = None, data: Incomplete | None = None, end_camera_label: Incomplete | None = None, end_zone_label: Incomplete | None = None, end_object_id: Incomplete | None = None, end_object_label: Incomplete | None = None) -> None: ...
    def publish_event(self) -> None: ...
