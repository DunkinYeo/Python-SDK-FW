#!/bin/bash

##################################################
# SDK Auto Tester - Clean Build Script
# 클린 빌드를 수행합니다
##################################################

set -e  # 에러 발생 시 즉시 중단

echo "=========================================="
echo "🧹 SDK Auto Tester - 클린 빌드"
echo "=========================================="
echo ""

# Java 17 설정 (Android 빌드 필수)
echo "☕ Java 17 설정 중..."
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export PATH="/opt/homebrew/opt/gpatch/libexec/gnubin:$JAVA_HOME/bin:$PATH"
echo "✅ JAVA_HOME: $JAVA_HOME"
java -version

# CMake 호환성 설정 (CMake < 3.5 에러 방지)
export CMAKE_ARGS="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
echo "✅ CMAKE_ARGS: $CMAKE_ARGS"
echo ""

# Material Design 버전을 main.py로 복사
echo "📋 Material Design 버전으로 설정 중..."
if [ -f "main_md.py" ]; then
    cp main_md.py main.py
    echo "✅ main_md.py -> main.py 복사 완료"
else
    echo "❌ main_md.py 파일을 찾을 수 없습니다"
    exit 1
fi
echo ""

# Buildozer 설치 확인
echo "🔍 Buildozer 확인 중..."
if ! command -v buildozer &> /dev/null; then
    echo "⚠️  Buildozer가 설치되지 않았습니다. 설치 중..."
    pip install --upgrade buildozer
else
    echo "✅ Buildozer가 이미 설치되어 있습니다"
fi
echo ""

# 클린 빌드
echo "🧹 이전 빌드 파일 삭제 중..."
rm -rf .buildozer bin
echo "✅ 클린 완료"
echo ""

# 빌드 옵션 선택
echo "빌드 옵션:"
echo "1. Debug APK (빠름, 테스트용)"
echo "2. Release APK (느림, 배포용)"
echo ""
read -p "선택 (1 또는 2): " choice

case $choice in
    1)
        echo ""
        echo "🔨 Debug APK 빌드 시작..."
        echo "⏰ 첫 빌드는 30분~1시간 소요될 수 있습니다"
        echo ""
        buildozer -v android debug
        ;;
    2)
        echo ""
        echo "🔨 Release APK 빌드 시작..."
        echo "⏰ 첫 빌드는 30분~1시간 소요될 수 있습니다"
        echo ""
        buildozer -v android release
        ;;
    *)
        echo "❌ 잘못된 선택입니다"
        exit 1
        ;;
esac

# 빌드 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ APK 빌드 성공!"
    echo "=========================================="
    echo ""
    echo "📦 APK 위치: bin/"
    ls -lh bin/*.apk 2>/dev/null || echo "⚠️  APK 파일을 찾을 수 없습니다"
    echo ""
    echo "다음 단계:"
    echo "1. ADB로 설치: adb install bin/*.apk"
    echo "2. 또는 APK 파일을 기기로 전송 후 설치"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ APK 빌드 실패"
    echo "=========================================="
    echo ""
    echo "문제 해결:"
    echo "1. 에러 로그 확인: .buildozer/android/platform/build-*/build.log"
    echo "2. Buildozer 버전: buildozer --version"
    echo "3. Python 버전: python --version"
    echo "4. Java 버전: java -version"
    echo ""
    exit 1
fi
