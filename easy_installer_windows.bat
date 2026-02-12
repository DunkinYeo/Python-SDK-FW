@echo off
REM 완전 자동 설치 프로그램 - Windows용
TITLE SDK 검증 테스트 - 자동 설치

color 0A
echo ============================================================
echo 🚀 SDK 검증 테스트 - 완전 자동 설치
echo ============================================================
echo.
echo 자동으로 모든 설정을 진행합니다...
echo.

REM 1. Python 확인
echo 1️⃣  Python 확인 중...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo.
    echo 자동으로 Python 다운로드 페이지를 엽니다...
    timeout /t 2 >nul
    start https://www.python.org/downloads/
    echo.
    echo Python 설치 후 이 프로그램을 다시 실행하세요.
    echo.
    echo 💡 설치 시 "Add Python to PATH" 옵션을 꼭 체크하세요!
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python 설치됨
echo.

REM 2. ADB 확인
echo 2️⃣  ADB (Android Debug Bridge) 확인 중...
adb version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  ADB가 설치되어 있지 않습니다.
    echo.
    echo 자동으로 Platform Tools 다운로드 페이지를 엽니다...
    timeout /t 2 >nul
    start https://developer.android.com/studio/releases/platform-tools
    echo.
    echo === ADB 설치 방법 ===
    echo 1. 다운로드한 ZIP 파일을 압축 해제
    echo 2. platform-tools 폴더를 C:\ 드라이브에 복사
    echo 3. 시스템 환경 변수 PATH에 C:\platform-tools 추가
    echo.
    echo 설치 방법을 모르시면 관리자에게 문의하세요.
    echo.
    pause
    exit /b 1
)

echo ✅ ADB 설치됨
echo.

REM 3. Python 패키지 설치
echo 3️⃣  필요한 프로그램 설치 중...
echo    (시간이 조금 걸릴 수 있습니다...)
echo.

python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
python -m pip install uiautomator2 adbutils --quiet

echo ✅ 모든 프로그램 설치 완료!
echo.

REM 4. Android 디바이스 확인
echo 4️⃣  Android 디바이스 확인...
adb devices

echo.
echo ============================================================
echo ✅ 설치 완료!
echo ============================================================
echo.
echo 이제 '테스트_시작.bat' 파일을 더블클릭하여
echo 테스트를 실행하세요!
echo.
echo 이 창은 10초 후 자동으로 닫힙니다...
timeout /t 10
