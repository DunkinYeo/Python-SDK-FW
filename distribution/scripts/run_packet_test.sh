#!/bin/bash

# 🚀 SDK 검증 - 패킷 모니터링 테스트 실행 스크립트
# 사용자 입력을 받아서 테스트를 실행합니다

set -e

echo "============================================================"
echo "🚀 SDK 검증 - 패킷 모니터링 테스트"
echo "============================================================"
echo ""

# 현재 .env 파일에서 기본값 읽기
if [ -f .env ]; then
    source .env
    DEFAULT_SERIAL=$BLE_DEVICE_SERIAL
else
    DEFAULT_SERIAL=""
fi

# 1. 디바이스 시리얼 넘버 입력
echo "📱 디바이스 시리얼 넘버를 입력하세요"
if [ -n "$DEFAULT_SERIAL" ]; then
    echo "   (현재 .env 파일의 값: $DEFAULT_SERIAL)"
    read -p "   시리얼 넘버 [Enter=기본값 사용]: " SERIAL_INPUT
    DEVICE_SERIAL=${SERIAL_INPUT:-$DEFAULT_SERIAL}
else
    read -p "   시리얼 넘버 (예: 610031): " DEVICE_SERIAL
fi

# 2. 타겟 패킷 수 입력
echo ""
echo "🎯 타겟 패킷 수를 입력하세요"
echo "   예시:"
echo "   - 60 = 약 1분 테스트"
echo "   - 600 = 약 10분 테스트"
echo "   - 3600 = 약 1시간 테스트"
echo "   - 86400 = 약 1일 테스트"
read -p "   타겟 패킷 수 (예: 60): " TARGET_PACKETS

# 입력값 확인
echo ""
echo "============================================================"
echo "📋 테스트 설정 확인"
echo "============================================================"
echo "디바이스 시리얼: $DEVICE_SERIAL"
echo "타겟 패킷 수: $TARGET_PACKETS"
echo ""

# 예상 시간 계산
ESTIMATED_MINUTES=$((TARGET_PACKETS / 60))
if [ $ESTIMATED_MINUTES -ge 60 ]; then
    ESTIMATED_HOURS=$((ESTIMATED_MINUTES / 60))
    echo "⏱️  예상 소요 시간: 약 ${ESTIMATED_HOURS}시간"
else
    echo "⏱️  예상 소요 시간: 약 ${ESTIMATED_MINUTES}분"
fi

echo ""
read -p "계속 진행하시겠습니까? (y/N): " CONFIRM

if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "❌ 테스트가 취소되었습니다."
    exit 0
fi

# .env 파일 업데이트
echo ""
echo "📝 .env 파일 업데이트 중..."
if grep -q "^BLE_DEVICE_SERIAL=" .env 2>/dev/null; then
    # 기존 값 업데이트 (macOS 호환)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^BLE_DEVICE_SERIAL=.*/BLE_DEVICE_SERIAL=$DEVICE_SERIAL/" .env
    else
        sed -i "s/^BLE_DEVICE_SERIAL=.*/BLE_DEVICE_SERIAL=$DEVICE_SERIAL/" .env
    fi
else
    # 새로운 값 추가
    echo "BLE_DEVICE_SERIAL=$DEVICE_SERIAL" >> .env
fi

# 앱 강제 종료
echo ""
echo "🛑 앱 강제 종료 중..."
adb shell am force-stop com.wellysis.spatch.sdk.sample || true
sleep 2

# 사용자에게 디바이스 초기화 안내
echo ""
echo "============================================================"
echo "⚠️  중요: 디바이스 초기화 필요"
echo "============================================================"
echo "테스트 시작 전에 다음 단계를 수동으로 진행해주세요:"
echo ""
echo "1. 앱에서 WriteSet → STOP 클릭"
echo "2. WriteSet → RESET DEVICE 클릭"
echo "3. Packet Number가 0으로 초기화되었는지 확인"
echo ""
read -p "초기화를 완료하셨습니까? (y/N): " READY

if [[ ! $READY =~ ^[Yy]$ ]]; then
    echo "❌ 테스트가 취소되었습니다. 디바이스를 초기화한 후 다시 실행해주세요."
    exit 0
fi

# 테스트 실행
echo ""
echo "============================================================"
echo "🧪 테스트 시작"
echo "============================================================"
echo ""

# venv 활성화 및 테스트 실행
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python -m pytest tests/regression/test_regression.py::TestDataCollectionWorkflow::test_data_collection_workflow \
    --target-packets=$TARGET_PACKETS \
    -v \
    -s \
    --tb=short \
    --html=test-report.html \
    --self-contained-html

# 결과 표시
echo ""
echo "============================================================"
echo "✅ 테스트 완료!"
echo "============================================================"
echo ""
echo "📄 상세 리포트: test-report.html"
echo ""

# HTML 리포트 자동 열기 (선택사항)
read -p "HTML 리포트를 열겠습니까? (y/N): " OPEN_REPORT
if [[ $OPEN_REPORT =~ ^[Yy]$ ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open test-report.html
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open test-report.html 2>/dev/null || echo "브라우저에서 test-report.html을 직접 열어주세요."
    fi
fi
