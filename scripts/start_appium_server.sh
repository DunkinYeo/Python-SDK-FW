#!/bin/bash
# Appium 서버 자동 시작 스크립트

echo "🚀 Appium 서버 시작 중..."

# Appium이 설치되어 있는지 확인
if ! command -v appium &> /dev/null; then
    echo "❌ Appium이 설치되어 있지 않습니다"
    echo "설치 방법: npm install -g appium@next"
    echo "           appium driver install uiautomator2"
    exit 1
fi

# 이미 실행 중인 Appium 프로세스 확인
if pgrep -x "appium" > /dev/null; then
    echo "⚠️  Appium이 이미 실행 중입니다"
    echo "PID: $(pgrep -x appium)"
    exit 0
fi

# Appium 서버 시작 (백그라운드)
echo "📱 Appium 서버를 백그라운드에서 시작합니다..."
nohup appium --address 127.0.0.1 --port 4723 > /tmp/appium.log 2>&1 &

APPIUM_PID=$!
echo "✅ Appium 서버 시작 완료 (PID: $APPIUM_PID)"
echo "📝 로그 위치: /tmp/appium.log"

# 서버 시작 대기
echo "⏳ 서버 준비 대기 중..."
sleep 5

# 서버 상태 확인
if curl -s http://127.0.0.1:4723/status > /dev/null 2>&1; then
    echo "✅ Appium 서버 정상 작동 중"
    echo "🌐 URL: http://127.0.0.1:4723"
else
    echo "❌ Appium 서버 시작 실패"
    echo "로그를 확인하세요: tail -f /tmp/appium.log"
    exit 1
fi
