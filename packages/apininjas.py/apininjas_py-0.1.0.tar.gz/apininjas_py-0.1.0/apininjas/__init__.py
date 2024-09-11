"""
apininjas.py
===========
Python Wrapper for the API-Ninjas APIs.

Copyright (c) 2024-present Puncher1
MIT License. See LICENSE for details
"""

__version__ = "0.1.0"
__author__ = "Puncher1"
__copyright__ = "Copyright (c) 2024-present Puncher1"
__license__ = "MIT"

from typing import NamedTuple, Literal

from .client import *
from .finance import *
from .errors import *
from .enums import *
from . import (
    utils as utils,
    abc as abc,
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=0, minor=1, patch=0, releaselevel="final", serial=0)

del VersionInfo, NamedTuple, Literal
