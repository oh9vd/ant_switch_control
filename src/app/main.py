from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from PySide6.QtGui import QGuiApplication

from config.settings import load_settings
from core.logging_setup import configure_logging
from core.app_controller import AppController
from core.state import AppState
from ui.qml_app import create_qml_engine


def main() -> int:
    settings = load_settings(Path("config.json"))
    configure_logging(settings.log_level, settings.log_console, settings.log_file)
    controller = AppController(settings=settings, state=AppState())
    controller.start()

    app = QGuiApplication(sys.argv)
    engine = create_qml_engine(controller)
    if not engine.rootObjects():
        controller.stop()
        return 1

    exit_code = app.exec()
    controller.stop()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
