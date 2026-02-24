@echo off
REM SDK Validation Test GUI Launcher for Windows

echo ============================================================
echo  SDK Validation Test GUI
echo ============================================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed.
    echo    Install Python 3.11+: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python version:
python --version

REM Start GUI
echo.
echo Starting GUI app...
python gui_test_runner.py

echo.
echo GUI app closed.
pause
