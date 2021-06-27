import sys
import traceback
import typing as tp
from http.client import responses as http_responses

from parse import parse
from slowapi.request import Request
from slowapi.response import Response
from slowapi.router import Route


class SlowAPI:
    def __init__(self):
        self.routes: tp.List[Route] = []
        self.middlewares = []

    def __call__(
        self,
        environ: tp.Dict[str, tp.Any],
        start_response: tp.Callable[[str, tp.List[tp.Tuple[str, str]]], None],
    ):

        environ["PATH_INFO"] = self.tailing_slash_processing(environ["PATH_INFO"])

        # ---

        request = Request(environ)
        middlewares_iterator = iter([*self.middlewares, lambda _: self.process_request])

        def next_middleware(*args, **kwargs) -> Response:
            middleware = next(middlewares_iterator)
            return middleware(next_middleware)(*args, **kwargs)

        response = next_middleware(request)
        response_status = str(response.status) + " " + http_responses[response.status]
        response_headers = [(key, value) for key, value in response.get_headers().items()]
        start_response(response_status, response_headers)

        return [response.body]

    def process_request(self, request: Request) -> Response:
        router, parsed_args = self.get_router(request)

        if router is None or parsed_args is None:
            response = Response(404, body=b"No Route detected for requested path")
        else:
            try:
                response = router.func(request, **parsed_args)
            except Exception as e:
                print("Exception:", e)
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                response = Response(
                    500, body=b"Cannot get a response object from the specified callable"
                )

        return response

    def get_router(
        self, request
    ) -> tp.Tuple[tp.Optional[Route], tp.Optional[tp.Dict[str, tp.Any]]]:
        method, path = request.method, request.path
        for rt in self.routes:
            if rt.method != method:
                continue

            parse_result = parse(rt.path, path)
            if parse_result is not None:
                return rt, parse_result.named
        return None, None

    def route(self, path=None, method=None, **options):
        def wrapper(handler):
            modified_path = self.tailing_slash_processing(path)
            self.routes.append(Route(path=modified_path, method=method, func=handler))
            return handler

        return wrapper

    @staticmethod
    def tailing_slash_processing(path: str):
        return path[:-1] if path.endswith("/") else path

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)

    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
