from __future__ import annotations

from typing import Callable

class Action():
    def __init__(
            self,
            title: str,
            descr: str,
            func: Callable[[], None]
            ):
        self.title = title
        self.descr = descr
        self.func = func

