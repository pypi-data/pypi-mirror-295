"""
MIT License

Copyright (c) 2024-present Puncher1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, Dict, Any

if TYPE_CHECKING:
    from aiohttp import ClientResponse


# fmt: off
__all__ = (
    "APINinjasBaseException",
    "ClientException",
    "HTTPException",
    "NotFound",
    "MethodNotAllowed",
    "APINinjasServerError",
    "StockNotFound",
)
# fmt: on


class APINinjasBaseException(Exception):
    """Base exception class.

    Every exception in this library is derived from this class.
    """

    pass


class ClientException(APINinjasBaseException):
    """Exception that's raised when an operation in the :class:`Client` fails.

    This exception is often raised due to invalid user input.
    """

    pass


class HTTPException(APINinjasBaseException):
    """HTTP Exception that's raised when an HTTP request fails.

    Attributes
    -----------
    response: :class:`aiohttp.ClientResponse`
        The response of the HTTP request.
    status: :class:`int`
        The `HTTP status code <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_.
    reason: Optional[:class:`str`]
        The HTTP reason-phrase if any.
    message: :class:`str`
        The related message sent by the API.
    """

    def __init__(self, response: ClientResponse, data: Optional[Union[str, Dict[str, Any]]]):
        self.response: ClientResponse = response

        self.status: int = self.response.status
        self.reason: Optional[str] = self.response.reason
        self.message: str

        if isinstance(data, dict):
            self.message = data.get("message") or data.get("error") or ""
        else:
            self.message = data or ""

        reason = f" {self.reason}" if self.reason is not None else ""
        msg = f"{self.status}{reason}: {self.message}"
        super().__init__(msg)


class NotFound(HTTPException):
    """HTTP Exception with status code 404.

    Derives from :exc:`HTTPException`.
    """

    pass


class MethodNotAllowed(HTTPException):
    """HTTP Exception with status code 405.

    Derives from :exc:`HTTPException`.
    """

    pass


class APINinjasServerError(HTTPException):
    """HTTP Exception with status code above 500.

    Derives from :exc:`HTTPException`.
    """

    pass


class StockNotFound(ClientException):
    """Exception that's raised when a requested stock could not be found.

    This exception is raised when the data returned by the API
    is invalid due to invalid user input.

    Derives from :exc:`ClientException`.
    """

    pass
