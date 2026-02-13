@echo off
REM SDK 검증 테스트 실행 - Windows용

TITLE SDK 검증 테스트

color 0B
echo ============================================================
echo SDK 검증 테스트 - GUI 앱 시작
echo ============================================================
echo.
echo GUI 앱을 실행합니다...
echo.

REM Python 경로 설정
if exist "python-embed\python.exe" (
    set "PYTHON_CMD=%CD%\python-embed\python.exe"
    set "PATH=%CD%\python-embed;%CD%\python-embed\Scripts;%PATH%"
) else (
    set "PYTHON_CMD=python"
)

REM GUI 앱 실행 (Appium 불필요한 standalone 버전)
if exist "standalone_gui.py" (
    %PYTHON_CMD% standalone_gui.py
) else (
    echo [ERROR] GUI 앱을 찾을 수 없습니다.
    echo.
    pause
)
