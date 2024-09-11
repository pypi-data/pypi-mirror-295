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

from enum import Enum


# fmt: off
__all__ = (
    "CommodityType",
)
# fmt: on


class CommodityType(Enum):
    gold = "gold"
    soybean_oil = "soybean_oil"
    wheat = "wheat"
    platinum = "platinum"
    micro_silver = "micro_silver"
    lean_hogs = "lean_hogs"
    corn = "corn"
    oat = "oat"
    aluminum = "aluminum"
    soybean_meal = "soybean_meal"
    silver = "silver"
    soybean = "soybean"
    lumber = "lumber"
    live_cattle = "live_cattle"
    sugar = "sugar"
    natural_gas = "natural_gas"
    crude_oil = "crude_oil"
    orange_juice = "orange_juice"
    coffee = "coffee"
    cotton = "cotton"
    copper = "copper"
    micro_gold = "micro_gold"
    feeder_cattle = "feeder_cattle"
    rough_rice = "rough_rice"
    palladium = "palladium"
    cocoa = "cocoa"
    brent_crude_oil = "brent_crude_oil"
    gasoline_rbob = "gasoline_rbob"
    heating_oil = "heating_oil"
    class_3_milk = "class_3_milk"
