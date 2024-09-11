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

from typing import TYPE_CHECKING, Any, Dict

from . import utils

if TYPE_CHECKING:
    import datetime


# fmt: off
__all__ = (
    "FinancialInstrument",
)
# fmt: on


class FinancialInstrument:
    """An ABC representing the common operations of a financial instrument.

    Following classes inherit from this ABC:

    - :class:`.Stock`
    - :class:`.Commodity`

    Attributes
    -----------
    price: :class:`float`
        The current price of the instrument, last updated at :attr:`updated_at`.
    """

    price: float
    _updated: int

    def __lt__(self, other: FinancialInstrument) -> bool:
        return self.price < other.price

    def __gt__(self, other: FinancialInstrument) -> bool:
        return self.price > other.price

    def __le__(self, other: FinancialInstrument) -> bool:
        return self.price <= other.price

    def __ge__(self, other: FinancialInstrument) -> bool:
        return self.price >= other.price

    def _update(self, *, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    @property
    def updated_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Date and time the :attr:`price` was last updated."""
        return utils.from_timestamp(self._updated)

    async def update(self) -> float:
        """|coro|

        Updates :attr:`price` and :attr:`.updated_at` of the current object and
        returns the new price.

        .. note::

            This makes an API call.

        Raises
        -------
        HTTPException
            Retrieving the price failed.

        Returns
        --------
        :class:`float`
            The newly updated price.
        """
        raise NotImplementedError
