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

from typing import TYPE_CHECKING, Optional, Union

import apininjas.abc
from .enums import CommodityType
from . import utils

if TYPE_CHECKING:
    from .http import HTTPClient
    from .types.finance import (
        Stock as StockPayload,
        Commodity as CommodityPayload,
        Gold as GoldPayload,
        Crypto as CryptoPayload,
    )


# fmt: off
__all__ = (
    "Stock",
    "Crypto",
    "Commodity",
)
# fmt: on


class Stock(apininjas.abc.FinancialInstrument):
    """Represents a stock from the Stock Price API.

    .. container:: operations

        .. describe:: x == y

            Checks if two stocks are equal.

        .. describe:: x != y

            Checks if two stocks are not equal.

        .. describe:: x < y

            Checks if a stock's price is less than another.

        .. describe:: x > y

            Checks if a stock's price is greater than another.

        .. describe:: x <= y

            Checks if a stock's price is less or equal than another.

        .. describe:: x >= y

            Checks if a stock's price is greater or equal than another.

    Attributes
    -----------
    ticker: :class:`str`
        The stock's ticker symbol.
    name: :class:`str`
        The stock's name.
    exchange: Optional[:class:`str`]
        The stock exchange the stock is traded on. ``None`` if it's not an exchange for stocks.
    price: :class:`float`
        The current price of the stock, last updated at :attr:`.updated_at`.
    """

    __slots__ = ("_http", "ticker", "name", "price", "exchange", "_updated")

    def __init__(self, *, http: HTTPClient, data: StockPayload):
        self._http = http
        self.ticker: str = data["ticker"]
        self.name: str = data["name"]
        self.exchange: Optional[str] = None

        exchange = data["exchange"]
        if exchange not in ["COMMODITY", "CRYPTO"]:
            self.exchange = exchange

        self._update(data=data)

    def __repr__(self) -> str:
        attrs = [
            ("ticker", self.ticker),
            ("name", self.name),
            ("exchange", self.exchange),
        ]
        joined = " ".join([f"{a}={v!r}" for a, v in attrs])
        return f"<Stock {joined}>"

    def __eq__(self, other: Stock) -> bool:
        return self.ticker == other.ticker

    def __ne__(self, other: Stock) -> bool:
        return not self.__eq__(other)

    def _update(self, *, data: StockPayload) -> None:
        self.price: float = data["price"]
        self._updated = data["updated"]

    @utils.copy_doc(apininjas.abc.FinancialInstrument.update)
    async def update(self) -> float:
        data = await self._http.get_stock(ticker=self.ticker)
        self._update(data=data)

        return self.price


class Commodity(apininjas.abc.FinancialInstrument):
    """Represents a commodity future from the Commodity Price API or the Gold Price API.

    .. container:: operations

        .. describe:: x == y

            Checks if two commodity futures are equal.

        .. describe:: x != y

            Checks if two commodity futures are not equal.

        .. describe:: x < y

            Checks if the price of a commodity future is less than the one of another.

        .. describe:: x > y

            Checks if the price of a commodity future is greater than the one of another.

        .. describe:: x <= y

            Checks if the price of a commodity future is less or equal than the one of another.

        .. describe:: x >= y

            Checks if the price of a commodity future is greater or equal than the one of another.

    Attributes
    -----------
    name: :class:`str`
        The name of the commodity future.
    exchange: :class:`str`
        The exchange the commodity future is traded on.
    price: :class:`float`
        The current price of the commodity future, last updated at :attr:`.updated_at`.
    type: :class:`CommodityType`
        The type of the commodity future.
    """

    __slots__ = ("_http", "name", "price", "exchange", "type", "_updated")

    def __init__(self, *, http: HTTPClient, type: CommodityType, data: Union[GoldPayload, CommodityPayload]):
        self._http = http
        self.type: CommodityType = type

        self.name: str
        self.exchange: str
        if type == CommodityType.gold:
            self.name = "Gold Futures"
            self.exchange = "CME"
        else:
            self.name: str = data["name"]  # type: ignore # can't be gold payload here
            self.exchange: str = data["exchange"]  # type: ignore # can't be gold payload here

        self._update(data=data)

    def __repr__(self) -> str:
        attrs = [
            ("name", self.name),
            ("exchange", self.exchange),
        ]
        joined = " ".join([f"{a}={v!r}" for a, v in attrs])
        return f"<Commodity {joined}>"

    def __eq__(self, other: Commodity) -> bool:
        return self.type == other.type

    def __ne__(self, other: Commodity) -> bool:
        return not self.__eq__(other)

    def _update(self, *, data: Union[GoldPayload, CommodityPayload]) -> None:
        self.price = data["price"]
        self._updated = data["updated"]

    @utils.copy_doc(apininjas.abc.FinancialInstrument.update)
    async def update(self) -> float:
        data = await self._http.get_commodity(name=self.type.value)
        self._update(data=data)

        return self.price


class Crypto(apininjas.abc.FinancialInstrument):
    """Represents a cryptocurrency from the Crypto Price API.

    .. container:: operations

        .. describe:: x == y

            Checks if two cryptocurrencies are equal.

        .. describe:: x != y

            Checks if two cryptocurrencies are not equal.

        .. describe:: x < y

            Checks if a cryptocurrency's price is less than another.

        .. describe:: x > y

            Checks if a cryptocurrency's price is greater than another.

        .. describe:: x <= y

            Checks if a cryptocurrency's price is less or equal than another.

        .. describe:: x >= y

            Checks if a cryptocurrency's price is greater or equal than another.

    Attributes
    -----------
    symbol: :class:`str`
        The cryptocurrency's symbol.
    price: :class:`float`
        The current price of the cryptocurrency, last updated at :attr:`.updated_at`.
    """

    __slots__ = ("_http", "symbol", "price", "_updated")

    def __init__(self, *, http: HTTPClient, data: CryptoPayload):
        self._http = http
        self.symbol: str = data["symbol"]
        self._update(data=data)

    def __repr__(self) -> str:
        return f"<Crypto symbol={self.symbol}>"

    def __eq__(self, other: Crypto) -> bool:
        return self.symbol == other.symbol

    def __ne__(self, other: Crypto) -> bool:
        return not self.__eq__(other)

    def _update(self, *, data: CryptoPayload) -> None:
        self.price: float = float(data["price"])
        self._updated = data["timestamp"]

    @utils.copy_doc(apininjas.abc.FinancialInstrument.update)
    async def update(self) -> float:
        data = await self._http.get_crypto(symbol=self.symbol)
        self._update(data=data)

        return self.price
