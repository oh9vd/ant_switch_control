from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class UdpConfig:
    host: str
    port: int
    enabled: bool = True


class UdpClient:
    def __init__(self, config: UdpConfig) -> None:
        self._config = config
        self._socket: Optional[object] = None

    def open(self) -> None:
        if not self._config.enabled:
            return
        # TODO: implement socket open and bind/send as needed.

    def send(self, payload: bytes) -> None:
        if not self._config.enabled:
            return
        # TODO: implement UDP send logic.

    def close(self) -> None:
        # TODO: implement socket close.
        return
