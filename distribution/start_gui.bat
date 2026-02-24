@echo off
REM SDK Validation Test GUI Launcher for Windows
REM Windows용 GUI 앱 실행 스크립트

echo ============================================================
echo 🚀 SDK 검증 테스트 GUI 실행
echo ============================================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo    Python 3.11 이상을 설치하세요: https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python 버전:
python --version

REM Start GUI
echo.
echo 🎨 GUI 앱 시작...
python gui_test_runner.py

echo.
echo GUI 앱이 종료되었습니다.
pause
