#!/bin/bash
# SDK 검증 테스트 실행 - Mac용 (더블클릭으로 실행)

# 현재 스크립트 위치로 이동
cd "$(dirname "$0")"

clear
echo "============================================================"
echo "🚀 SDK 검증 테스트"
echo "============================================================"
echo ""
echo "GUI 앱을 시작합니다..."
echo ""

# GUI 앱 실행
if [ -f "standalone_gui.py" ]; then
    python3 standalone_gui.py
elif [ -f "gui_test_runner.py" ]; then
    python3 gui_test_runner.py
else
    echo "❌ GUI 앱을 찾을 수 없습니다."
    echo ""
    read -p "아무 키나 누르면 종료됩니다..."
fi
