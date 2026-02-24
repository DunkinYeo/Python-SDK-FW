#!/bin/bash
# APK 빠른 빌드 스크립트

echo "🚀 SDK Auto Tester APK 빌드"
echo "=========================================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# main_md.py를 main.py로 복사 (Material Design 버전 사용)
echo -e "${BLUE}📝 Material Design 버전으로 빌드합니다...${NC}"
cp main_md.py main.py
echo -e "${GREEN}✅ main_md.py -> main.py 복사 완료${NC}"
echo ""

# Buildozer 설치 확인
if ! command -v buildozer &> /dev/null; then
    echo -e "${YELLOW}⚠️  Buildozer가 설치되지 않았습니다${NC}"
    echo "설치 중..."
    pip install buildozer cython
    echo -e "${GREEN}✅ Buildozer 설치 완료${NC}"
fi

echo ""
echo -e "${BLUE}📦 APK 빌드 시작...${NC}"
echo ""
echo "빌드 옵션:"
echo "1. Debug APK (빠름, 테스트용)"
echo "2. Release APK (느림, 배포용)"
echo ""
read -p "선택 (1 또는 2): " choice

if [ "$choice" = "2" ]; then
    echo ""
    echo -e "${BLUE}🔨 Release APK 빌드 중...${NC}"
    buildozer android release
else
    echo ""
    echo -e "${BLUE}🔨 Debug APK 빌드 중...${NC}"
    buildozer android debug
fi

# 빌드 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ APK 빌드 성공!${NC}"
    echo "=========================================="
    echo ""
    echo "APK 위치:"
    ls -lh bin/*.apk 2>/dev/null || echo "bin/ 디렉토리를 확인하세요"
    echo ""
    echo "다음 단계:"
    echo "1. ADB로 설치: adb install bin/*.apk"
    echo "2. 또는 APK 파일을 기기로 전송 후 직접 설치"
else
    echo ""
    echo "=========================================="
    echo -e "${RED}❌ APK 빌드 실패${NC}"
    echo "=========================================="
    echo ""
    echo "문제 해결:"
    echo "1. .buildozer 디렉토리 삭제 후 재시도"
    echo "2. 로그 확인: .buildozer/android/platform/build-*/dists/*/build.log"
    exit 1
fi
