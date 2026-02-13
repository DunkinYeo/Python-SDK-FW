#!/bin/bash
# SDK 검증 테스트 실행 - Mac용 (더블클릭으로 실행)

# 현재 스크립트 위치로 이동
cd "$(dirname "$0")"

clear
echo "============================================================"
echo "🚀 SDK 검증 테스트"
echo "============================================================"
echo ""

# 전체 테스트 스위트 실행
if [ -f "scripts/run_full_test_suite.sh" ]; then
    echo "전체 테스트 스위트를 실행합니다..."
    echo ""
    bash scripts/run_full_test_suite.sh
else
    echo "❌ 테스트 스크립트를 찾을 수 없습니다."
    echo ""
    read -p "아무 키나 누르면 종료됩니다..."
fi
