import dataclasses
import json
import typing as tp


@dataclasses.dataclass
class Response:
    content_type: tp.ClassVar[str] = ""
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: tp.Optional[tp.Any] = None

    def get_headers(self) -> tp.Dict[str, str]:
        self.headers.update({"Content-Type": self.content_type})
        return self.headers


@dataclasses.dataclass
class JsonResponse(Response):
    content_type: tp.ClassVar[str] = "application/json"
    data: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    status: int = 200
    serializer: tp.Optional[tp.Callable] = None

    def __post_init__(self):
        self.body = json.dumps(self.data, default=self.serializer).encode("utf-8")
