from __future__ import annotations
from dataclasses import dataclass
from json import dumps as json_dumps
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Final, Mapping

from httpx import URL, Request, Response

from kookit.utils import UUIDEncoder
from .utils import none_if_ellipsis


if TYPE_CHECKING:
    from types import EllipsisType

    from httpx._types import (
        HeaderTypes,
        QueryParamTypes,
        RequestContent,
        RequestData,
        RequestFiles,
    )


@dataclass
class KookitResponseRequest:
    content: bytes
    headers: Mapping[str, str] | None
    url: URL
    method: str


class KookitHTTPResponse:
    def __init__(
        self,
        url: URL | str,
        method: str | bytes,
        *,
        status_code: int = 200,
        http_version: str = "HTTP/1.1",
        headers: Mapping | None = None,
        content: bytes | None = None,
        text: str | None = None,
        html: str | None = None,
        json: Any = None,
        stream: Any = None,
        # Request matchers here
        request_params: QueryParamTypes | None = None,
        request_headers: HeaderTypes | None = None,
        request_content: RequestContent | None | EllipsisType = ...,
        request_data: RequestData | None | EllipsisType = ...,
        request_files: RequestFiles | None | EllipsisType = ...,
        request_json: Any | None | EllipsisType = ...,
    ) -> None:
        self.content_specified: Final = any(
            item is not Ellipsis
            for item in (request_content, request_data, request_files, request_json)
        )
        request = Request(
            url=url,
            method=method,
            params=request_params,
            headers=request_headers,
            content=none_if_ellipsis(request_content),  # type: ignore[arg-type]
            data=none_if_ellipsis(request_data),
            files=none_if_ellipsis(request_files),  # type: ignore[arg-type]
            json=json_loads(json_dumps(none_if_ellipsis(request_json), cls=UUIDEncoder)),
        )

        if request_headers:
            request_headers = request.headers  # lowercase headers' keys

        response: Response = Response(
            status_code=status_code,
            extensions={"http_version": http_version.encode("ascii")},
            headers=headers,
            json=json_loads(json_dumps(json, cls=UUIDEncoder)),
            content=content,
            text=text,
            html=html,
            stream=stream,
            request=request,
        )

        self.request: Final[KookitResponseRequest] = KookitResponseRequest(
            content=request.content,
            headers=request_headers,  # type: ignore[arg-type]
            url=request.url,
            method=request.method,
        )

        self.content: Final[bytes] = response.content
        self.headers: Final[Mapping[str, str]] = response.headers
        self.status_code: Final[int] = response.status_code

    def __str__(self) -> str:
        return f"<Response({self.status_code}, '{self.request.method}', '{self.request.url}')>"

    def __repr__(self) -> str:
        return str(self)
