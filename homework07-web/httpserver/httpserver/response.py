import dataclasses
import http.client
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        return (
            f"HTTP/1.1 {self.status} {http.client.responses[self.status]}\r\n"
            + "\r\n".join(
                [
                    f"{key}: {value}"
                    for key, value in zip(self.headers.keys(), self.headers.values())
                ]
            )
            + f"\r\n\r\n{self.body.decode()}"
        ).encode()
