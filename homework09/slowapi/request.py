import dataclasses
import io
import json
import typing as tp
from urllib.parse import parse_qsl


@dataclasses.dataclass
class Request:
    path: str
    method: str
    query: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    body: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)

    def __init__(self, environ: tp.Dict[str, tp.Any]):
        self.path = environ.get("PATH_INFO", "")
        self.method = environ.get("REQUEST_METHOD", "GET")
        self.query = {k: v for k, v in parse_qsl(environ.get("QUERY_STRING", ""))}
        self.body = environ.get("wsgi.input", "")
        header_keys = [k for k in environ.keys() if k.startswith("HTTP_")]
        self.headers = {key[5:]: str(environ.get(key)) for key in header_keys}

    def text(self) -> str:
        body_bytes = self.body.read()
        return body_bytes.decode("utf-8")

    def json(self) -> tp.Optional[tp.Dict[str, tp.Any]]:
        body_str = self.text()
        return json.loads(body_str)
