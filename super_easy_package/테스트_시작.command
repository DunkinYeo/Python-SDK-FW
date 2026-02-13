#!/bin/bash
# SDK 검증 테스트 실행 - Mac용 (더블클릭으로 실행)

# 현재 스크립트 위치로 이동
cd "$(dirname "$0")"

clear
echo "============================================================"
echo "🚀 SDK 검증 테스트 - GUI 앱 시작"
echo "============================================================"
echo ""
echo "GUI 앱을 실행합니다..."
echo ""

# GUI 앱 실행 (Appium 불필요한 standalone 버전)
if [ -f "standalone_gui.py" ]; then
    python3 standalone_gui.py
else
    echo "❌ GUI 앱을 찾을 수 없습니다."
    echo ""
    read -p "아무 키나 누르면 종료됩니다..."
fi
