from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from core.logging_setup import get_logger

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebSockets import QWebSocket


@dataclass
class WebSocketConfig:
    url: str
    enabled: bool = True
    auto_reconnect: bool = True
    reconnect_interval_ms: int = 3000
    max_reconnect_attempts: int = 0  # 0 = unlimited
    heartbeat_timeout_ms: int = 7000  # 0 = disabled, expect messages every ~5s


class WebSocketClient:
    def __init__(self, config: WebSocketConfig) -> None:
        self._config = config
        self._on_message: Optional[Callable[[str], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None
        self._on_disconnect: Optional[Callable[[], None]] = None
        self._on_send_failed: Optional[Callable[[str], None]] = None
        self._logger = get_logger(self.__class__.__name__)
        self._socket: QWebSocket | None = None
        self._reconnect_timer: QTimer | None = None
        self._heartbeat_timer: QTimer | None = None
        self._reconnect_attempts: int = 0
        self._intentional_close: bool = False

    def set_message_handler(self, handler: Callable[[str], None]) -> None:
        self._on_message = handler

    def set_error_handler(self, handler: Callable[[str], None]) -> None:
        self._on_error = handler

    def set_disconnect_handler(self, handler: Callable[[], None]) -> None:
        self._on_disconnect = handler

    def set_send_failed_handler(self, handler: Callable[[str], None]) -> None:
        self._on_send_failed = handler

    def connect(self) -> None:
        if not self._config.enabled:
            return
        self._intentional_close = False
        self._reconnect_attempts = 0
        if self._socket is None:
            self._socket = QWebSocket()
            self._connect_signal("textMessageReceived", self._handle_text_message)
            self._connect_signal("connected", self._handle_connected)
            self._connect_signal("disconnected", self._handle_disconnected)
            self._connect_signal("errorOccurred", self._handle_error)
        self._logger.info("Opening WebSocket: %s", self._config.url)
        self._socket.open(QUrl(self._config.url))

    def send(self, message: str) -> None:
        if not self._config.enabled:
            return
        if self._socket is not None and self._socket.isValid():
            self._logger.debug("Sending WebSocket message: %s", message)
            self._socket.sendTextMessage(message)
        else:
            self._logger.warning("WebSocket not connected; message not sent")
            if self._on_send_failed:
                self._on_send_failed("not connected")

    def close(self) -> None:
        self._intentional_close = True
        self._stop_reconnect_timer()
        self._stop_heartbeat_timer()
        if self._socket is not None:
            self._socket.close()

    def _start_reconnect_timer(self) -> None:
        if self._reconnect_timer is None:
            self._reconnect_timer = QTimer()
            self._reconnect_timer.setSingleShot(True)
            self._reconnect_timer.timeout.connect(self._attempt_reconnect)
        self._reconnect_timer.start(self._config.reconnect_interval_ms)

    def _stop_reconnect_timer(self) -> None:
        if self._reconnect_timer is not None:
            self._reconnect_timer.stop()

    def _start_heartbeat_timer(self) -> None:
        if self._config.heartbeat_timeout_ms <= 0:
            return
        if self._heartbeat_timer is None:
            self._heartbeat_timer = QTimer()
            self._heartbeat_timer.setSingleShot(True)
            self._heartbeat_timer.timeout.connect(self._handle_heartbeat_timeout)
        self._heartbeat_timer.start(self._config.heartbeat_timeout_ms)

    def _stop_heartbeat_timer(self) -> None:
        if self._heartbeat_timer is not None:
            self._heartbeat_timer.stop()

    def _reset_heartbeat_timer(self) -> None:
        if self._config.heartbeat_timeout_ms > 0 and self._heartbeat_timer is not None:
            self._heartbeat_timer.start(self._config.heartbeat_timeout_ms)

    def _handle_heartbeat_timeout(self) -> None:
        self._logger.warning("Heartbeat timeout - no message received in %d ms", self._config.heartbeat_timeout_ms)
        if self._socket is not None and self._socket.isValid():
            self._socket.close()  # This will trigger _handle_disconnected and auto-reconnect

    def _attempt_reconnect(self) -> None:
        if self._intentional_close or not self._config.enabled:
            return
        max_attempts = self._config.max_reconnect_attempts
        if max_attempts > 0 and self._reconnect_attempts >= max_attempts:
            self._logger.warning("Max reconnect attempts (%d) reached", max_attempts)
            return
        self._reconnect_attempts += 1
        self._logger.info("Reconnecting (attempt %d)...", self._reconnect_attempts)
        if self._socket is not None:
            self._socket.open(QUrl(self._config.url))

    def _handle_text_message(self, message: str) -> None:
        self._logger.debug("WebSocket text message received: %s", message)
        self._reset_heartbeat_timer()
        if self._on_message:
            self._on_message(message)

    def _handle_connected(self) -> None:
        self._logger.info("WebSocket connected")
        self._reconnect_attempts = 0
        self._start_heartbeat_timer()

    def _handle_disconnected(self) -> None:
        self._logger.info("WebSocket disconnected")
        self._stop_heartbeat_timer()
        if self._on_disconnect:
            self._on_disconnect()
        if self._config.auto_reconnect and not self._intentional_close:
            self._start_reconnect_timer()

    def _handle_error(self, error) -> None:
        message = str(error)
        self._logger.error("WebSocket error: %s", message)
        if self._on_error:
            self._on_error(message)

    def _connect_signal(self, name: str, handler) -> None:
        if self._socket is None:
            return
        signal = getattr(self._socket, name, None)
        if signal is None or not hasattr(signal, "connect"):
            self._logger.warning("WebSocket signal missing: %s", name)
            return
        try:
            signal.connect(handler)
        except Exception as exc:
            self._logger.warning("Failed to connect WebSocket signal %s: %s", name, exc)
