import logging
import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse

# set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="agent.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app_type: tp.Any = None
        self.app: tp.Optional[tp.Any] = None

    def set_app(self, app: tp.Any) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[tp.Any]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest, **kwargs) -> WSGIResponse:
        environ = request.to_environ()
        environ["SERVER_NAME"], environ["SERVER_PORT"] = self.address
        response = WSGIResponse()
        data_response = self.server.app(environ, response.start_response)
        logging.info(f"resp = {data_response}")
        response.body = data_response[0]

        return response