#!/bin/bash
# SDK 자동화 완전 설치 스크립트 - Self-hosted Runner + Appium

set -e

echo "🚀 SDK 검증 자동화 시스템 설치"
echo "=========================================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Homebrew 확인
echo "📦 Step 1: Homebrew 확인"
if ! command -v brew &> /dev/null; then
    echo -e "${RED}❌ Homebrew가 설치되어 있지 않습니다${NC}"
    echo "설치 방법: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi
echo -e "${GREEN}✅ Homebrew 설치됨${NC}"
echo ""

# 2. Node.js 확인
echo "📦 Step 2: Node.js 확인"
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js가 설치되어 있지 않습니다. 설치 중...${NC}"
    brew install node
fi
echo -e "${GREEN}✅ Node.js 설치됨 ($(node -v))${NC}"
echo ""

# 3. Appium 설치
echo "📱 Step 3: Appium 설치"
if ! command -v appium &> /dev/null; then
    echo -e "${YELLOW}⚠️  Appium이 설치되어 있지 않습니다. 설치 중...${NC}"
    npm install -g appium@next
    appium driver install uiautomator2
fi
echo -e "${GREEN}✅ Appium 설치됨 ($(appium -v))${NC}"
echo ""

# 4. ADB 설치
echo "🔧 Step 4: ADB 설치"
if ! command -v adb &> /dev/null; then
    echo -e "${YELLOW}⚠️  ADB가 설치되어 있지 않습니다. 설치 중...${NC}"
    brew install --cask android-platform-tools
fi
echo -e "${GREEN}✅ ADB 설치됨${NC}"
echo ""

# 5. Python 패키지 설치
echo "🐍 Step 5: Python 패키지 설치"
cd "$(dirname "$0")/.."
pip3 install -r requirements.txt
echo -e "${GREEN}✅ Python 패키지 설치 완료${NC}"
echo ""

# 6. Appium LaunchAgent 설정
echo "⚙️  Step 6: Appium 자동 시작 설정"
APPIUM_PATH=$(which appium)
PLIST_FILE="$HOME/Library/LaunchAgents/com.sdk.appium.plist"

# plist 파일 생성
cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sdk.appium</string>
    <key>ProgramArguments</key>
    <array>
        <string>$APPIUM_PATH</string>
        <string>--address</string>
        <string>127.0.0.1</string>
        <string>--port</string>
        <string>4723</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/appium.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/appium.error.log</string>
</dict>
</plist>
EOF

# LaunchAgent 로드
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"
echo -e "${GREEN}✅ Appium 자동 시작 설정 완료${NC}"
echo ""

# 7. Appium 서버 시작 확인
echo "🔍 Step 7: Appium 서버 상태 확인"
sleep 3
if curl -s http://127.0.0.1:4723/status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Appium 서버 정상 작동 중${NC}"
else
    echo -e "${YELLOW}⚠️  Appium 서버를 시작하는 중입니다. 잠시 기다려주세요...${NC}"
fi
echo ""

# 8. Self-hosted Runner 설정 안내
echo "=========================================="
echo "📝 Self-hosted Runner 설정"
echo "=========================================="
echo ""
echo "다음 링크로 이동하여 Runner를 설정하세요:"
echo -e "${GREEN}https://github.com/DunkinYeo/Python-SDK-FW/settings/actions/runners/new${NC}"
echo ""
echo "또는 회사 repository:"
echo -e "${GREEN}https://github.com/Wellysis/SDKApp-Automation-report-slack/settings/actions/runners/new${NC}"
echo ""
echo "설정 방법:"
echo "1. 위 링크에서 제공하는 토큰 복사"
echo "2. 다음 명령어 실행:"
echo ""
echo "   mkdir -p ~/actions-runner && cd ~/actions-runner"
echo "   curl -o actions-runner-osx-arm64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-arm64-2.311.0.tar.gz"
echo "   tar xzf ./actions-runner-osx-arm64-2.311.0.tar.gz"
echo "   ./config.sh --url https://github.com/DunkinYeo/Python-SDK-FW --token YOUR_TOKEN"
echo "   ./svc.sh install"
echo "   ./svc.sh start"
echo ""
echo "=========================================="
echo -e "${GREEN}✅ 자동화 시스템 설치 완료!${NC}"
echo "=========================================="
echo ""
echo "다음 작업:"
echo "1. Android 디바이스를 USB로 연결"
echo "2. Self-hosted Runner 설정 완료"
echo "3. 매일 오전 9시 자동으로 테스트 실행됩니다!"
