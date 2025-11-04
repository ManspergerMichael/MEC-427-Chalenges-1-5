from typing import Any


class TouchIn:
    raw_value: int
    def __init__(self, pin: Any) -> None: ...
    def deinit(self) -> None: ...
