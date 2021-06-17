import datetime
import mimetypes
import os
import pathlib
import typing as tp
from urllib.parse import urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def url_normalize(path: str) -> str:
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3 :]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):  # type: ignore
    @tp.no_type_check
    def handle_request(self, request: HTTPRequest, **kwargs: tp.Dict[str, str]) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        content: bytes = b"No methods available"
        status: int = 405
        default_headers = {
            "Date": str(datetime.datetime.now()),
            "Server": "Static Server",
            "Content-Length": str(len(content)),
            "Content-Type": str,
            "Allow": "GET, HEAD",
        }
        content_type: tp.Optional[str] = None
        content = b""

        if request.method == b"GET" or request.method == b"HEAD":
            status = 200

            url = urlparse(url_normalize(request.url.decode()))
            default_url_path = url.path
            if url.path.endswith("/"):
                default_url_path += "index.html"
            path = pathlib.Path(str(server.document_root.absolute()) + default_url_path)

            if request.method != b"HEAD":
                if os.path.exists(path) and os.path.isfile(path):
                    try:
                        with open(path, "rb") as f:
                            content = f.read()
                        content_type, _other = mimetypes.guess_type(path)
                    except OSError as os_exc:
                        print(f"error 404.")
                        status = 404
                    except Exception as exc:
                        print(f"error 500.")
                        status = 500
                else:
                    status = 404
                    print("File not found or is not a file. 404")

            default_headers["Content-Length"] = str(len(content))
            default_headers["Content-Type"] = "text/html" if not content_type else content_type

            return self.response_klass(status=status, headers=default_headers, body=content)
        return self.response_klass(status=status, headers=default_headers, body=b"")


class StaticServer(HTTPServer):  # type: ignore
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = 5,
        request_handler_cls: tp.Type[StaticHTTPRequestHandler] = StaticHTTPRequestHandler,
        document_root: pathlib.Path = pathlib.Path("."),
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            backlog_size=backlog_size,
            max_workers=max_workers,
            timeout=timeout,
            request_handler_cls=request_handler_cls,
        )
        self.document_root = document_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=60,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
