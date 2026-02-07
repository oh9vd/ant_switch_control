from __future__ import annotations

from dataclasses import dataclass

from config.settings import AppSettings
from core.state import AppState
from net.udp_client import UdpClient, UdpConfig
from net.websocket_client import WebSocketClient, WebSocketConfig


@dataclass
class AppController:
    settings: AppSettings
    state: AppState

    def __post_init__(self) -> None:
        self.ws_client = WebSocketClient(
            WebSocketConfig(url=self.settings.ws_url)
        )
        self.udp_client = UdpClient(
            UdpConfig(host=self.settings.udp_host, port=self.settings.udp_port)
        )

    def start(self) -> None:
        self.ws_client.connect()
        self.udp_client.open()

    def stop(self) -> None:
        self.ws_client.close()
        self.udp_client.close()

    def send_text(self, text: str) -> None:
        self.ws_client.send(text)
        self.udp_client.send(text.encode("utf-8"))
