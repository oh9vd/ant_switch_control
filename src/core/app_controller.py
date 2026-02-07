from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional
from urllib.parse import urlparse, urlunparse

from config.settings import AppSettings
from core.logging_setup import get_logger
from core.state import AppState
from net.udp_client import UdpClient, UdpConfig
from net.websocket_client import WebSocketClient, WebSocketConfig


@dataclass
class AppController:
    settings: AppSettings
    state: AppState

    def __post_init__(self) -> None:
        self._logger = get_logger(self.__class__.__name__)
        self._ws_message_listener: Optional[Callable[[str], None]] = None
        ws_url = _build_ws_url(self.settings.ws_url, self.settings.ws_port)
        self.ws_client = WebSocketClient(
            WebSocketConfig(url=ws_url)
        )
        self.ws_client.set_message_handler(self._handle_ws_message)
        self.udp_client = UdpClient(
            UdpConfig(host=self.settings.udp_host, port=self.settings.udp_port)
        )

    def start(self) -> None:
        try:
            self.ws_client.connect()
        except Exception as exc:
            self._logger.exception("WebSocket connection failed: %s", exc)

        try:
            self.udp_client.open()
        except Exception as exc:
            self._logger.exception("UDP connection failed: %s", exc)

    def stop(self) -> None:
        self.ws_client.close()
        self.udp_client.close()

    def send_text(self, text: str) -> None:
        try:
            self.ws_client.send(text)
        except Exception as exc:
            self._logger.exception("WebSocket send failed: %s", exc)

        try:
            self.udp_client.send(text.encode("utf-8"))
        except Exception as exc:
            self._logger.exception("UDP send failed: %s", exc)

    def set_ws_message_listener(self, listener: Callable[[str], None]) -> None:
        self._ws_message_listener = listener

    def _handle_ws_message(self, message: str) -> None:
        self.state.last_message = message
        self._logger.info("WebSocket message received: %s", message)
        if self._ws_message_listener:
            self._ws_message_listener(message)


def _build_ws_url(raw_url: str, port: int) -> str:
    parsed = urlparse(raw_url)
    scheme = parsed.scheme or "ws"
    if scheme == "http":
        scheme = "ws"
    elif scheme == "https":
        scheme = "wss"

    hostname = parsed.hostname or raw_url
    if hostname and ":" in hostname and hostname.startswith("["):
        hostname = hostname.strip("[]")

    netloc = hostname or "127.0.0.1"
    if parsed.port is not None:
        netloc = f"{netloc}:{parsed.port}"
    else:
        netloc = f"{netloc}:{port}"

    path = parsed.path or "/"
    return urlunparse((scheme, netloc, path, "", "", ""))
