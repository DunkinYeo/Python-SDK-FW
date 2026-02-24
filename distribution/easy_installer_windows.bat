@echo off
REM SDK Validation Test - Full Auto Installer for Windows
TITLE SDK Validation Test - Auto Install

color 0A
echo ============================================================
echo  SDK Validation Test - Auto Install
echo ============================================================
echo.
echo Setting everything up automatically...
echo.

REM 1. Check Python
echo [Step 1] Checking Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed.
    echo.
    echo Opening Python download page automatically...
    timeout /t 2 >nul
    start https://www.python.org/downloads/
    echo.
    echo Please install Python, then run this program again.
    echo.
    echo [TIP] Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python installed
echo.

REM 2. Check ADB
echo [Step 2] Checking ADB (Android Debug Bridge)...
adb version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] ADB is not installed.
    echo.
    echo Opening Platform Tools download page...
    timeout /t 2 >nul
    start https://developer.android.com/studio/releases/platform-tools
    echo.
    echo === How to install ADB ===
    echo 1. Extract the downloaded ZIP file
    echo 2. Copy the platform-tools folder to C:\
    echo 3. Add C:\platform-tools to your system PATH environment variable
    echo.
    echo If you are unsure how to do this, contact your administrator.
    echo.
    pause
    exit /b 1
)

echo [OK] ADB installed
echo.

REM 3. Install Python packages
echo [Step 3] Installing required packages...
echo    (This may take a moment...)
echo.

python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
python -m pip install uiautomator2 adbutils --quiet

echo [OK] All packages installed!
echo.

REM 4. Check Android device
echo [Step 4] Checking Android device...
adb devices

echo.
echo ============================================================
echo [OK] Installation complete!
echo ============================================================
echo.
echo Double-click 'run_tests.bat' to run the tests!
echo.
echo This window will close in 10 seconds...
timeout /t 10
