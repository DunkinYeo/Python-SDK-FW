#!/usr/bin/env python3
"""
Create portable package that includes everything
모든 것이 포함된 휴대용 패키지 생성
"""
import subprocess
import sys
import shutil
from pathlib import Path
import zipfile


def create_portable_package():
    """Create a portable package with embedded Python."""
    print("="*70)
    print("📦 올인원 휴대용 패키지 생성")
    print("="*70)
    print()

    package_dir = Path("portable_package")
    package_dir.mkdir(exist_ok=True)

    print("1️⃣  필수 파일 복사 중...")

    # Copy essential files
    files_to_copy = [
        "standalone_gui.py",
        "gui_test_runner.py",
        "requirements.txt",
        ".env.template",
        "SETUP_GUIDE_FOR_NON_DEVELOPERS.md"
    ]

    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy(file, package_dir / file)
            print(f"   ✅ {file}")

    # Copy directories
    dirs_to_copy = [
        "tests",
        "scripts"
    ]

    for dir_name in dirs_to_copy:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, package_dir / dir_name, dirs_exist_ok=True)
            print(f"   ✅ {dir_name}/")

    print()
    print("2️⃣  설치 스크립트 생성 중...")

    # Create Windows installer
    windows_installer = package_dir / "INSTALL_WINDOWS.bat"
    windows_installer.write_text("""@echo off
echo ========================================
echo SDK 검증 테스트 - 자동 설치 (Windows)
echo ========================================
echo.

echo 1. Python 확인 중...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo.
    echo Python 3.11 이상을 먼저 설치하세요:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
python --version

echo.
echo 2. ADB 확인 중...
adb version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ADB가 설치되지 않았습니다.
    echo.
    echo Platform Tools를 다운로드하세요:
    echo https://developer.android.com/studio/releases/platform-tools
    echo.
    pause
    exit /b 1
)

echo.
echo 3. Python 패키지 설치 중...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install uiautomator2 adbutils

echo.
echo 4. Android 디바이스 확인...
adb devices

echo.
echo ========================================
echo ✅ 설치 완료!
echo ========================================
echo.
echo 다음 단계:
echo 1. Android 디바이스를 USB로 연결하세요
echo 2. START_TEST.bat를 실행하세요
echo.
pause
""")

    print(f"   ✅ {windows_installer.name}")

    # Create Mac/Linux installer
    mac_installer = package_dir / "install_mac_linux.sh"
    mac_installer.write_text("""#!/bin/bash

echo "========================================"
echo "SDK 검증 테스트 - 자동 설치 (Mac/Linux)"
echo "========================================"
echo ""

echo "1. Python 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python이 설치되지 않았습니다."
    echo ""
    echo "Python 3.11 이상을 먼저 설치하세요:"
    echo "https://www.python.org/downloads/"
    exit 1
fi
python3 --version

echo ""
echo "2. ADB 확인 중..."
if ! command -v adb &> /dev/null; then
    echo "⚠️  ADB가 설치되지 않았습니다."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Mac에서 설치: brew install android-platform-tools"
    else
        echo "Linux에서 설치: sudo apt-get install android-tools-adb"
    fi
    echo ""
    read -p "계속하시겠습니까? (y/N): " CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    adb version
fi

echo ""
echo "3. Python 패키지 설치 중..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install uiautomator2 adbutils

echo ""
echo "4. Android 디바이스 확인..."
if command -v adb &> /dev/null; then
    adb devices
fi

echo ""
echo "========================================"
echo "✅ 설치 완료!"
echo "========================================"
echo ""
echo "다음 단계:"
echo "1. Android 디바이스를 USB로 연결하세요"
echo "2. ./start_test.sh를 실행하세요"
echo ""
""")
    mac_installer.chmod(0o755)

    print(f"   ✅ {mac_installer.name}")

    # Create launcher scripts
    windows_launcher = package_dir / "START_TEST.bat"
    windows_launcher.write_text("""@echo off
echo ========================================
echo SDK 검증 테스트 실행
echo ========================================
echo.
python standalone_gui.py
pause
""")

    print(f"   ✅ {windows_launcher.name}")

    mac_launcher = package_dir / "start_test.sh"
    mac_launcher.write_text("""#!/bin/bash
echo "========================================"
echo "SDK 검증 테스트 실행"
echo "========================================"
echo ""
python3 standalone_gui.py
""")
    mac_launcher.chmod(0o755)

    print(f"   ✅ {mac_launcher.name}")

    # Create README
    readme = package_dir / "README_PORTABLE.md"
    readme.write_text("""# 📱 SDK 검증 테스트 - 휴대용 패키지

## 🚀 빠른 시작 (3단계)

### Windows 사용자:
1. `INSTALL_WINDOWS.bat` 더블클릭 (설치)
2. Android 디바이스 USB 연결
3. `START_TEST.bat` 더블클릭 (실행)

### Mac/Linux 사용자:
1. `./install_mac_linux.sh` 실행 (설치)
2. Android 디바이스 USB 연결
3. `./start_test.sh` 실행 (실행)

## 📋 필수 준비물

1. **Python 3.11+** ([다운로드](https://www.python.org/downloads/))
   - Windows: python.org에서 설치 프로그램 다운로드
   - Mac: `brew install python3`
   - Linux: `sudo apt-get install python3`

2. **ADB (Android Debug Bridge)**
   - Windows: [Platform Tools](https://developer.android.com/studio/releases/platform-tools) 다운로드
   - Mac: `brew install android-platform-tools`
   - Linux: `sudo apt-get install android-tools-adb`

3. **Android 디바이스**
   - USB 연결
   - 개발자 옵션 활성화
   - USB 디버깅 활성화

4. **BLE 패치 디바이스**
   - 시리얼 넘버 확인

## ⚙️ 설정 (.env 파일)

Slack 알림을 받으려면 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
BLE_DEVICE_SERIAL=610031
```

## 🎯 장점

- ✅ **Appium 서버 불필요** - Python + ADB만 있으면 됨
- ✅ **Node.js 불필요** - 복잡한 설정 제거
- ✅ **간단한 설치** - 자동 설치 스크립트 제공
- ✅ **GUI 인터페이스** - 클릭만으로 테스트 실행

## ❓ 문제 해결

### "Python not found" 오류
➡️ Python 3.11 이상을 설치하세요

### "ADB not found" 오류
➡️ Android Platform Tools를 설치하고 PATH에 추가하세요

### "No devices connected" 오류
➡️ USB 케이블 확인 및 USB 디버깅 활성화

## 📞 지원

문제가 있으면 개발팀에 문의하세요.

---

**Made with Claude Code** 🤖
""")

    print(f"   ✅ {readme.name}")

    print()
    print("3️⃣  패키지 압축 중...")

    # Create zip file
    zip_path = Path("SDK검증테스트_휴대용패키지.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in package_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(package_dir.parent)
                zipf.write(file, arcname)
                print(f"   📦 {arcname}")

    print()
    print("="*70)
    print("✅ 휴대용 패키지 생성 완료!")
    print("="*70)
    print()
    print(f"📦 패키지 위치: {zip_path.absolute()}")
    print(f"📁 압축 해제된 폴더: {package_dir.absolute()}")
    print()
    print("📤 다음 단계:")
    print(f"1. '{zip_path.name}' 파일을 비개발자에게 전송")
    print("2. 압축 해제 후 INSTALL 스크립트 실행")
    print("3. START_TEST 스크립트로 테스트 실행")
    print()


if __name__ == "__main__":
    create_portable_package()
