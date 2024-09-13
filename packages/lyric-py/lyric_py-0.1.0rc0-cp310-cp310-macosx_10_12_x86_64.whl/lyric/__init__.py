from __future__ import annotations

from ._py_lyric import *
from .task import TaskInfo

__doc__ = _py_lyric.__doc__
if hasattr(_py_lyric, "__all__"):
    __all__ = _py_lyric.__all__