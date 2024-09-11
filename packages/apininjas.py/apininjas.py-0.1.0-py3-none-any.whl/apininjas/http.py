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

import sys

import aiohttp
from typing import TYPE_CHECKING, TypeVar, Coroutine, Any, ClassVar, Dict, Optional

from . import __version__
from .errors import (
    HTTPException,
    NotFound,
    MethodNotAllowed,
    APINinjasServerError,
)
from .types import finance

if TYPE_CHECKING:
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]


class Route:
    API_VERSION: int = 1
    BASE: ClassVar[str] = f"https://api.api-ninjas.com/v{API_VERSION}"

    def __init__(self, method: str, path: str, **kwargs: Any) -> None:
        self.method: str = method
        self.path: str = path

        url = self.BASE + self.path
        if kwargs:
            url = url.format(**kwargs)
        self.url: str = url


class HTTPClient:
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession()

        sys_vers = f"Python/{sys.version_info[0]}.{sys.version_info[1]}"
        client_vers = f"aiohttp/{aiohttp.__version__}"
        self.user_agent: str = (
            f"apininjas.py (https://github.com/Puncher1/apininjas.py {__version__}) {sys_vers} {client_vers}"
        )

    async def request(
        self,
        route: Route,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        method: str = route.method
        url: str = route.url

        headers = {"X-Api-Key": self.api_key}

        async with self.__session.request(method=method, url=url, params=params, headers=headers) as response:
            http_status = response.status
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = await response.text()

            if 200 <= http_status < 300:
                return data
            else:
                if http_status == 404:
                    raise NotFound(response, data)
                elif http_status == 405:
                    raise MethodNotAllowed(response, data)
                elif http_status >= 500:
                    raise APINinjasServerError(response, data)
                else:
                    raise HTTPException(response, data)

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()

    # Finance

    def get_stock(self, *, ticker: str) -> Response[finance.Stock]:
        params = {"ticker": ticker}
        return self.request(Route("GET", "/stockprice"), params=params)

    def get_commodity(self, *, name: str) -> Response[finance.Commodity]:
        params = {"name": name}
        return self.request(Route("GET", "/commodityprice"), params=params)

    def get_gold(self) -> Response[finance.Gold]:
        return self.request(Route("GET", "/goldprice"))

    def get_crypto(self, *, symbol: str) -> Response[finance.Crypto]:
        params = {"symbol": symbol}
        return self.request(Route("GET", "/cryptoprice"), params=params)
