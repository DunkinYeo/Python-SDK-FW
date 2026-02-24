@echo off
REM SDK Validation Test Launcher for Windows

TITLE SDK Validation Test

color 0B
echo ============================================================
echo  SDK Validation Test - Starting GUI
echo ============================================================
echo.
echo Launching GUI app...
echo.

REM Set Python path
if exist "python-embed\python.exe" (
    set "PYTHON_CMD=%CD%\python-embed\python.exe"
    set "PATH=%CD%\python-embed;%CD%\python-embed\Scripts;%PATH%"
) else (
    set "PYTHON_CMD=python"
)

REM Launch GUI app (standalone version - no Appium required)
if exist "standalone_gui.py" (
    %PYTHON_CMD% standalone_gui.py
) else (
    echo [ERROR] GUI app not found.
    echo.
    pause
)
