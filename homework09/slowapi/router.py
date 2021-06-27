import dataclasses
import re
import typing as tp

from slowapi.response import Response


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable[..., Response]
