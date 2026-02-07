from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class WebSocketConfig:
    url: str
    enabled: bool = True


class WebSocketClient:
    def __init__(self, config: WebSocketConfig) -> None:
        self._config = config
        self._on_message: Optional[Callable[[str], None]] = None

    def set_message_handler(self, handler: Callable[[str], None]) -> None:
        self._on_message = handler

    def connect(self) -> None:
        if not self._config.enabled:
            return
        # TODO: implement with a websocket library compatible with Qt event loop.

    def send(self, message: str) -> None:
        if not self._config.enabled:
            return
        # TODO: implement send logic.

    def close(self) -> None:
        # TODO: implement close logic.
        return
