#!/bin/bash
# Self-hosted GitHub Actions Runner 설정 스크립트

set -e

echo "🚀 Self-hosted GitHub Actions Runner 설정"
echo "=========================================="
echo ""

# 1. Runner 디렉토리 생성
RUNNER_DIR="$HOME/actions-runner"
echo "📁 Runner 디렉토리: $RUNNER_DIR"

if [ ! -d "$RUNNER_DIR" ]; then
    mkdir -p "$RUNNER_DIR"
    echo "✅ Runner 디렉토리 생성 완료"
else
    echo "⚠️  Runner 디렉토리가 이미 존재합니다"
fi

cd "$RUNNER_DIR"

# 2. Runner 다운로드 (macOS ARM64)
echo ""
echo "📥 GitHub Actions Runner 다운로드 중..."
RUNNER_VERSION="2.311.0"
RUNNER_FILE="actions-runner-osx-arm64-${RUNNER_VERSION}.tar.gz"

if [ ! -f "$RUNNER_FILE" ]; then
    curl -o "$RUNNER_FILE" -L "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${RUNNER_FILE}"
    echo "✅ 다운로드 완료"
else
    echo "⚠️  Runner 파일이 이미 존재합니다"
fi

# 3. 압축 해제
echo ""
echo "📦 압축 해제 중..."
if [ ! -f "config.sh" ]; then
    tar xzf "$RUNNER_FILE"
    echo "✅ 압축 해제 완료"
else
    echo "⚠️  이미 압축 해제되어 있습니다"
fi

# 4. 설정 안내
echo ""
echo "=========================================="
echo "📝 다음 단계:"
echo "=========================================="
echo ""
echo "1. GitHub Repository 페이지로 이동:"
echo "   https://github.com/DunkinYeo/Python-SDK-FW/settings/actions/runners/new"
echo ""
echo "2. 페이지에서 제공하는 토큰을 복사"
echo ""
echo "3. 다음 명령어 실행:"
echo "   cd $RUNNER_DIR"
echo "   ./config.sh --url https://github.com/DunkinYeo/Python-SDK-FW --token YOUR_TOKEN"
echo ""
echo "4. Runner 이름 입력 (예: mac-mini-sdk-test)"
echo ""
echo "5. 서비스로 설치:"
echo "   ./svc.sh install"
echo "   ./svc.sh start"
echo ""
echo "=========================================="
echo "✅ 준비 완료! 위 단계를 따라 설정하세요"
echo "=========================================="
