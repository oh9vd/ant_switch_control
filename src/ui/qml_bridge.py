from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal, Slot

from core.app_controller import AppController


class QmlBridge(QObject):
    statusChanged = Signal()

    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self._controller = controller
        self._status = "Disconnected"

    @Slot(str)
    def sendText(self, text: str) -> None:
        message = text.strip()
        if not message:
            return
        self._controller.send_text(message)

    def _get_status(self) -> str:
        return self._status

    def _set_status(self, value: str) -> None:
        if self._status == value:
            return
        self._status = value
        self.statusChanged.emit()

    status = Property(str, _get_status, _set_status, notify=statusChanged)
