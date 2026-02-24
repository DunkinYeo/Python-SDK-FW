# 🚀 빠른 시작 가이드

APK를 가장 빠르게 빌드하는 방법입니다.

## ⚡ 한 줄로 빌드하기

```bash
cd mobile_app && ./build.sh
```

끝! 😎

---

## 📱 상세 단계

### 1단계: 빌드 스크립트 실행

```bash
cd mobile_app
./build.sh
```

**선택 화면이 나타납니다:**
```
빌드 옵션:
1. Debug APK (빠름, 테스트용)
2. Release APK (느림, 배포용)

선택 (1 또는 2):
```

**추천**: 처음에는 `1` (Debug) 선택

### 2단계: 기다리기 ⏳

**처음 빌드:**
- 30분 ~ 1시간 소요
- Android SDK, NDK 자동 다운로드 (약 2GB)
- 커피 한 잔 하고 오세요 ☕

**두 번째 빌드부터:**
- 5-10분 소요
- 변경된 부분만 빌드

### 3단계: APK 설치

빌드가 완료되면:

```bash
# ADB로 설치
adb install bin/sdkautotester-*.apk

# 또는 수동으로
# bin/*.apk 파일을 기기로 전송 후 설치
```

---

## 🎨 디자인 비교

### Material Design 버전 (main_md.py) ✨

```
┌─────────────────────────┐
│ 🎨 예쁜 카드 UI         │
│ 🌈 Material Design      │
│ 💫 애니메이션           │
│ 🎯 둥근 버튼            │
└─────────────────────────┘
```

**장점:**
- ✅ 훨씬 예쁜 디자인
- ✅ Material Design 가이드라인 준수
- ✅ 전문적인 느낌

**단점:**
- ⚠️ APK 크기 약간 증가 (~5MB)

### 기본 버전 (main.py)

```
┌─────────────────────────┐
│ 심플한 UI               │
│ 기본 Kivy 위젯          │
└─────────────────────────┘
```

**장점:**
- ✅ APK 크기 작음
- ✅ 빌드 속도 빠름

**현재 설정**: `build.sh`는 **Material Design 버전**으로 빌드합니다!

---

## 🔧 문제 해결

### 빌드 실패 시

```bash
# 1. 캐시 삭제
rm -rf .buildozer

# 2. 다시 빌드
./build.sh
```

### 권한 오류

```bash
chmod +x build.sh
```

### ADB 인식 안 됨

```bash
# ADB 서버 재시작
adb kill-server
adb start-server

# 디바이스 확인
adb devices
```

---

## 💡 팁

### PC에서 먼저 테스트

APK 빌드 전에 PC에서 GUI 확인:

```bash
pip install kivymd
python main_md.py
```

**주의**: uiautomator2는 Android에서만 작동

### 기본 버전으로 빌드하려면

```bash
# main.py 사용 (Material Design 아님)
# build.sh의 cp 라인을 주석 처리하거나
buildozer android debug
```

### APK 크기 줄이기

```spec
# buildozer.spec 수정
android.archs = arm64-v8a  # armeabi-v7a 제거
```

---

## 📊 예상 결과

| 항목 | 값 |
|------|-----|
| APK 크기 | ~55MB |
| 빌드 시간 (첫 번째) | 30-60분 |
| 빌드 시간 (이후) | 5-10분 |
| 지원 Android | 5.0+ (API 21+) |

---

**Made with Claude Code** 🤖
