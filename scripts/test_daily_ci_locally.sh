#!/bin/bash
# Daily CI 워크플로우를 로컬에서 테스트하는 스크립트

set -e

echo "🧪 Daily CI 워크플로우 로컬 테스트"
echo "=========================================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo -e "${BLUE}📁 프로젝트 루트: $PROJECT_ROOT${NC}"
echo ""

# Step 1: Checkout code (이미 체크아웃됨)
echo -e "${GREEN}📥 Step 1: Checkout code${NC}"
echo "✅ 로컬 코드 사용"
echo ""

# Step 2: Setup Python
echo -e "${GREEN}🐍 Step 2: Setup Python${NC}"
PYTHON_VERSION=$(python3 --version)
echo "✅ Python 버전: $PYTHON_VERSION"
echo ""

# Step 3: Install dependencies
echo -e "${GREEN}📦 Step 3: Install dependencies${NC}"
echo "의존성 설치 중..."
python3 -m pip install --upgrade pip --quiet
pip3 install -r requirements.txt --quiet
echo "✅ 모든 의존성 설치 완료"
echo ""

# Step 4: Python 문법 체크
echo -e "${GREEN}🔍 Step 4: Python 문법 체크${NC}"
echo "Python 파일 문법 검사 중..."

# 문법 체크할 Python 파일들
SYNTAX_OK=true
for file in $(find tests scripts -name "*.py" 2>/dev/null); do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "  ✅ $file"
    else
        echo -e "  ${RED}❌ $file${NC}"
        SYNTAX_OK=false
    fi
done

if [ "$SYNTAX_OK" = true ]; then
    echo -e "${GREEN}✅ 문법 체크 완료 - 모든 파일 정상${NC}"
else
    echo -e "${RED}❌ 일부 파일에 문법 오류가 있습니다${NC}"
fi
echo ""

# Step 5: 프로젝트 통계
echo -e "${GREEN}📊 Step 5: 프로젝트 통계${NC}"
echo ""
echo "## 📊 프로젝트 통계"
echo ""
PYTHON_FILES=$(find . -name '*.py' | wc -l | tr -d ' ')
TEST_FILES=$(find tests -name 'test_*.py' 2>/dev/null | wc -l | tr -d ' ')
SCRIPT_FILES=$(find scripts -name '*.py' 2>/dev/null | wc -l | tr -d ' ')

echo "- **Python 파일 수**: $PYTHON_FILES"
echo "- **테스트 파일 수**: $TEST_FILES"
echo "- **스크립트 파일 수**: $SCRIPT_FILES"
echo ""
echo "### 📦 설치된 주요 패키지"
echo "\`\`\`"
pip3 list | grep -E "(pytest|appium|selenium|uiautomator2)" || echo "관련 패키지를 찾을 수 없습니다"
echo "\`\`\`"
echo ""

# Step 6: Slack 알림 시뮬레이션
echo -e "${GREEN}📤 Step 6: Slack 알림 시뮬레이션${NC}"

if [ -n "$SLACK_WEBHOOK_URL" ]; then
    echo "Slack webhook이 설정되어 있습니다"

    # Slack 메시지 생성
    PAYLOAD=$(cat <<EOF
{
  "attachments": [{
    "color": "good",
    "title": "Daily CI - 코드 품질 체크 (로컬 테스트)",
    "text": "✅ 성공",
    "fields": [
      {
        "title": "실행 시간",
        "value": "$(date '+%Y-%m-%d %H:%M:%S KST')",
        "short": true
      },
      {
        "title": "브랜치",
        "value": "main (로컬 테스트)",
        "short": true
      },
      {
        "title": "Python 파일",
        "value": "$PYTHON_FILES",
        "short": true
      },
      {
        "title": "테스트 파일",
        "value": "$TEST_FILES",
        "short": true
      }
    ]
  }]
}
EOF
)

    echo "Slack으로 알림 전송 중..."
    if curl -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "$PAYLOAD" \
        --silent \
        --show-error; then
        echo -e "${GREEN}✅ Slack 알림 전송 성공${NC}"
    else
        echo -e "${RED}❌ Slack 알림 전송 실패${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다${NC}"
    echo "테스트를 위해 Slack 알림을 건너뜁니다"
fi
echo ""

# 최종 결과
echo "=========================================="
if [ "$SYNTAX_OK" = true ]; then
    echo -e "${GREEN}✅ Daily CI 테스트 성공!${NC}"
    echo "=========================================="
    echo ""
    echo "📋 요약:"
    echo "  - Python 문법: ✅ 통과"
    echo "  - 의존성 설치: ✅ 성공"
    echo "  - 프로젝트 통계: ✅ 생성"
    echo "  - Slack 알림: $([ -n "$SLACK_WEBHOOK_URL" ] && echo "✅ 전송" || echo "⏭️  건너뜀")"
    echo ""
    echo "🎉 모든 단계가 성공적으로 완료되었습니다!"
    echo "GitHub Actions에서도 동일하게 실행될 것입니다."
else
    echo -e "${RED}❌ Daily CI 테스트 실패${NC}"
    echo "=========================================="
    echo ""
    echo "Python 문법 오류를 수정한 후 다시 실행하세요."
    exit 1
fi
