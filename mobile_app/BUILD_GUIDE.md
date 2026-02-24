# SDK Auto Tester - 빌드 가이드

Android APK를 빌드하는 방법입니다.

## 📋 준비사항

### macOS/Linux

```bash
# Buildozer 설치
pip3 install buildozer

# Cython 설치 (빌드 속도 향상)
pip3 install cython

# Android SDK/NDK는 Buildozer가 자동으로 설치합니다
```

### Ubuntu/Debian 추가 패키지

```bash
sudo apt update
sudo apt install -y python3-pip build-essential git python3 python3-dev \
    ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev \
    libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    openjdk-17-jdk unzip
```

## 🚀 빌드 방법

### 1단계: 프로젝트 디렉토리로 이동

```bash
cd mobile_app
```

### 2단계: 디버그 APK 빌드 (처음 빌드 시 시간이 걸림)

```bash
buildozer android debug
```

**처음 빌드 시:**
- Android SDK, NDK 자동 다운로드 (약 1-2GB)
- Python-for-Android 빌드
- 30분 ~ 1시간 소요 (인터넷 속도에 따라 다름)

**두 번째 빌드부터:**
- 변경된 부분만 빌드
- 5-10분 소요

### 3단계: APK 확인

빌드가 완료되면 APK 파일이 생성됩니다:

```
mobile_app/bin/sdkautotester-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

## 📱 APK 설치

### 방법 1: ADB로 설치

```bash
adb install bin/sdkautotester-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 방법 2: 직접 전송

APK 파일을 기기로 전송하고 직접 설치:

1. APK 파일을 기기로 복사
2. 파일 매니저에서 APK 클릭
3. "알 수 없는 출처" 허용
4. 설치

## 🔧 Release APK 빌드 (배포용)

```bash
# Release 빌드
buildozer android release

# 서명 (필요 시)
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
    -keystore my-release-key.keystore \
    bin/sdkautotester-1.0.0-arm64-v8a_armeabi-v7a-release-unsigned.apk \
    alias_name
```

## 🐛 문제 해결

### 빌드 실패 시

```bash
# 빌드 캐시 삭제
rm -rf .buildozer

# 다시 빌드
buildozer android debug
```

### 로그 확인

```bash
# 실시간 로그 확인
adb logcat | grep python
```

### 권한 오류

```bash
# buildozer.spec 파일에서 권한 추가
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE
```

## 🎨 앱 커스터마이징

### 아이콘 변경

1. 512x512 PNG 이미지 준비
2. `data/icon.png`로 저장
3. `buildozer.spec`에서 주석 해제:
   ```
   icon.filename = %(source.dir)s/data/icon.png
   ```

### 스플래시 화면

1. 1280x1920 PNG 이미지 준비
2. `data/presplash.png`로 저장
3. `buildozer.spec`에서 주석 해제:
   ```
   presplash.filename = %(source.dir)s/data/presplash.png
   ```

## 📊 빌드 최적화

### APK 크기 줄이기

```spec
# buildozer.spec 수정
android.archs = arm64-v8a  # armeabi-v7a 제거
```

### 빌드 속도 향상

```bash
# Cython 사용
pip install cython

# 병렬 빌드
buildozer android debug --jobs 4
```

## 📱 테스트 방법

### 로컬 테스트 (PC에서)

```bash
# Kivy 설치
pip install kivy

# 앱 실행 (PC에서 테스트)
python main.py
```

**주의**: uiautomator2는 Android 기기에서만 작동하므로, PC에서는 GUI만 확인 가능

### 실제 기기 테스트

1. APK 빌드 및 설치
2. Android 기기에서 앱 실행
3. 테스트 시나리오 실행
4. 로그 확인: `adb logcat | grep python`

## 🔗 유용한 링크

- [Kivy 공식 문서](https://kivy.org/doc/stable/)
- [Buildozer 공식 문서](https://buildozer.readthedocs.io/)
- [Python-for-Android](https://python-for-android.readthedocs.io/)

---

**Made with Claude Code** 🤖
