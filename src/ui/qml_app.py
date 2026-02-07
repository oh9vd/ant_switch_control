from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

from core.app_controller import AppController
from core.version import get_version
from ui.qml_bridge import QmlBridge


def _resource_path() -> Path:
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return base_dir / "ui" / "qml" / "Main.qml"


def create_qml_engine(controller: AppController) -> QQmlApplicationEngine:
    engine = QQmlApplicationEngine()
    bridge = QmlBridge(controller)
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty(
        "appTitle",
        "2x6 Remote Switch Controller",
    )
    engine.rootContext().setContextProperty("appVersion", get_version())

    qml_path = _resource_path()
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    return engine
