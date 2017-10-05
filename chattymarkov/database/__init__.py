"""Chattymarkov database submodule.

This submodule gathers all the supported database formats.
"""

# flake8: noqa
from .json import JSONFileDatabase
from .memory import MemoryDatabase
from .redis import RedisDatabase
