from _typeshed import Incomplete
from typing import NamedTuple

__all__ = ['Pose']

class Coord(NamedTuple):
    x: Incomplete
    y: Incomplete

class Pose:
    def __init__(self, key_points: list[tuple[int, int]], score: float) -> None: ...
    def __eq__(self, other): ...
    @property
    def key_points(self) -> dict: ...
    @property
    def score(self) -> float: ...
