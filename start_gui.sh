#!/bin/bash

# SDK Validation Test GUI Launcher
# GUI 앱 실행 스크립트

echo "============================================================"
echo "🚀 SDK 검증 테스트 GUI 실행"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 가상환경 활성화 중..."
    source venv/bin/activate
fi

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python이 설치되지 않았습니다."
    echo "   Python 3.11 이상을 설치하세요: https://www.python.org/"
    exit 1
fi

echo "✅ Python 버전: $(python --version)"

# Check dependencies
echo ""
echo "📦 의존성 확인 중..."
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter가 설치되지 않았습니다."
    echo "   macOS: brew install python-tk"
    echo "   Ubuntu: sudo apt-get install python3-tk"
    exit 1
fi

# Start GUI
echo ""
echo "🎨 GUI 앱 시작..."
python gui_test_runner.py

echo ""
echo "GUI 앱이 종료되었습니다."
