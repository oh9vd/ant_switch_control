from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppState:
    connected: bool = False
    last_message: str = ""
