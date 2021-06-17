import dataclasses
import io
import sys
import typing as tp

from httpserver import HTTPRequest


@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}

        environ["REQUEST_METHOD"] = self.method.decode()
        environ["SCRIPT_NAME"] = ""
        environ["PATH_INFO"] = self.url.decode("utf-8")
        environ["QUERY_STRING"] = self.url.decode("utf-8").split("?")[1] if "?" in self.url.decode() else ""
        environ["CONTENT_TYPE"] = self.headers.get(b"Content-Type", b"").decode()
        environ["CONTENT_LENGTH"] = self.headers.get(b"Content-Length", b"").decode()
        environ["SERVER_NAME"], environ["SERVER_PORT"] = ("127.0.0.1", "8000")  # Потом перезапишется приложением
        environ["SERVER_PROTOCOL"] = "HTTP/1.1"
        environ["wsgi.version"] = (1, 0)
        environ["wsgi.url_scheme"] = "https" if self.url.startswith(b"https") else "http"
        environ["wsgi.input"] = io.BytesIO(self.body)
        environ["wsgi.errors"] = sys.stderr
        environ["wsgi.multithread"] = True
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = True

        for header in self.headers:
            environ[f"HTTP_{header.decode().upper()}"] = self.headers[header].decode()

        return environ