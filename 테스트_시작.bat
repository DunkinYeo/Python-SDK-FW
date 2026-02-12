@echo off
REM SDK 검증 테스트 실행 - Windows용

TITLE SDK 검증 테스트

color 0B
echo ============================================================
echo 🚀 SDK 검증 테스트
echo ============================================================
echo.
echo GUI 앱을 시작합니다...
echo.

if exist "standalone_gui.py" (
    python standalone_gui.py
) else if exist "gui_test_runner.py" (
    python gui_test_runner.py
) else (
    echo ❌ GUI 앱을 찾을 수 없습니다.
    echo.
    pause
)
