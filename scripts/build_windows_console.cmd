@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0.."
pushd "%PROJECT_ROOT%"

if not exist ".venv" (
  python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --clean --noconfirm remote_switch_console.spec

popd
endlocal
