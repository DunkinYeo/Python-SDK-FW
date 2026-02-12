#!/bin/bash
# 완전 자동 설치 프로그램 - Mac용 (더블클릭으로 실행)

# 현재 스크립트 위치로 이동
cd "$(dirname "$0")"

echo "============================================================"
echo "🚀 SDK 검증 테스트 - 완전 자동 설치"
echo "============================================================"
echo ""
echo "터미널 창이 열렸습니다. 자동으로 모든 설정을 진행합니다..."
echo ""

# 1. Python 확인 및 설치 안내
echo "1️⃣  Python 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python이 설치되어 있지 않습니다."
    echo ""
    echo "자동으로 Python 설치 페이지를 엽니다..."
    sleep 2
    open "https://www.python.org/downloads/"
    echo ""
    echo "Python 설치 후 이 프로그램을 다시 실행하세요."
    echo ""
    read -p "아무 키나 누르면 종료됩니다..."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION 설치됨"
fi

echo ""

# 2. ADB 확인 및 자동 설치
echo "2️⃣  ADB (Android Debug Bridge) 확인 중..."
if ! command -v adb &> /dev/null; then
    echo "⚠️  ADB가 설치되어 있지 않습니다."
    echo ""
    echo "Homebrew로 자동 설치를 시도합니다..."

    # Homebrew 확인
    if ! command -v brew &> /dev/null; then
        echo "Homebrew가 없습니다. Homebrew를 먼저 설치합니다..."
        echo ""
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # ADB 설치
    echo "ADB 설치 중..."
    brew install android-platform-tools

    if command -v adb &> /dev/null; then
        echo "✅ ADB 설치 완료!"
    else
        echo "❌ 자동 설치 실패. 수동 설치가 필요합니다."
        echo ""
        echo "다음 링크에서 Platform Tools를 다운로드하세요:"
        open "https://developer.android.com/studio/releases/platform-tools"
        echo ""
        read -p "설치 후 아무 키나 누르세요..."
    fi
else
    ADB_VERSION=$(adb version | head -n 1)
    echo "✅ $ADB_VERSION 설치됨"
fi

echo ""

# 3. Python 패키지 설치
echo "3️⃣  필요한 프로그램 설치 중..."
echo "   (시간이 조금 걸릴 수 있습니다...)"
echo ""

python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet
python3 -m pip install uiautomator2 adbutils --quiet

echo "✅ 모든 프로그램 설치 완료!"

echo ""

# 4. Android 디바이스 확인
echo "4️⃣  Android 디바이스 확인..."
adb devices

DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l | tr -d ' ')

if [ "$DEVICE_COUNT" -gt 0 ]; then
    echo "✅ Android 디바이스가 연결되어 있습니다!"
else
    echo "⚠️  연결된 Android 디바이스가 없습니다."
    echo ""
    echo "📱 Android 디바이스를 USB로 연결하고,"
    echo "   USB 디버깅을 활성화해주세요."
    echo ""
    echo "USB 디버깅 활성화 방법:"
    echo "1. 설정 > 휴대전화 정보 > 빌드 번호 7번 탭"
    echo "2. 설정 > 개발자 옵션 > USB 디버깅 활성화"
fi

echo ""
echo "============================================================"
echo "✅ 설치 완료!"
echo "============================================================"
echo ""
echo "이제 '테스트_시작.command' 파일을 더블클릭하여"
echo "테스트를 실행하세요!"
echo ""
echo "이 창은 10초 후 자동으로 닫힙니다..."
sleep 10
