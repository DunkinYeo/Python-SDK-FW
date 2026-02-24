# 📱 SDK Auto Tester - Mobile App

Android에서 직접 SDK 검증 테스트를 실행하는 모바일 앱입니다.

## ✨ 주요 기능

- ✅ **간편한 GUI**: 버튼 클릭만으로 테스트 실행
- ✅ **자동 BLE 연결**: 시리얼 넘버만 입력하면 자동 연결
- ✅ **실시간 진행 상황**: 테스트 진행률과 로그 실시간 표시
- ✅ **결과 공유**: 테스트 결과를 다른 앱으로 공유
- ✅ **PC 불필요**: Android 기기만 있으면 테스트 가능

## 🎯 사용 방법

### 1단계: APK 설치

```bash
# ADB로 설치
adb install sdkautotester-1.0.0-debug.apk

# 또는 APK 파일을 기기로 전송 후 직접 설치
```

### 2단계: 앱 실행

1. **SDK Auto Tester** 앱 실행
2. BLE 시리얼 넘버 입력 (예: 610031)
3. 테스트 항목 선택:
   - Read 테스트
   - WriteGet 테스트
   - Notify 테스트
   - 패킷 모니터링 (선택)
4. **테스트 시작** 버튼 클릭

### 3단계: 결과 확인

- 테스트가 자동으로 실행됩니다
- 진행 상황을 실시간으로 확인
- 완료 후 결과 화면에서 성공/실패 확인
- **공유** 버튼으로 결과 공유 가능

## 📸 스크린샷

```
┌─────────────────────────────┐
│  SDK 자동 검증기             │
├─────────────────────────────┤
│ BLE 시리얼: [610031]        │
│ ☑ Read 테스트               │
│ ☑ WriteGet 테스트           │
│ ☑ Notify 테스트             │
│ ☐ 패킷 모니터링             │
│   타겟: [60] 개             │
│ [테스트 시작]               │
└─────────────────────────────┘
```

## 🛠️ 개발 및 빌드

### 요구사항

- Python 3.8+
- Buildozer (APK 빌드용)
- Android SDK & NDK (Buildozer가 자동 설치)

### 개발 환경 설정

```bash
cd mobile_app

# 의존성 설치
pip install -r requirements.txt

# PC에서 테스트 (GUI만)
python main.py
```

### APK 빌드

```bash
# 디버그 APK 빌드
buildozer android debug

# Release APK 빌드
buildozer android release
```

상세한 빌드 방법은 [BUILD_GUIDE.md](BUILD_GUIDE.md)를 참조하세요.

## 📋 테스트 항목

### Read 테스트 (7개)
- Battery Level
- Model Number
- Serial Number
- Firmware Version
- Hardware Version
- Software Version
- Firmware Version & Supported Sampling Rates

### WriteGet 테스트
- Start
- Pause
- Restart

### Notify 테스트
- ECG Notify 활성화

### 패킷 모니터링
- 사용자 지정 패킷 수만큼 모니터링
- 기본값: 60개

## 🔧 기술 스택

- **Kivy**: Python GUI 프레임워크
- **Python-for-Android**: Python을 Android APK로 변환
- **uiautomator2**: Android UI 자동화
- **ADB Utils**: Android 디바이스 제어

## 📱 지원 플랫폼

- ✅ Android 5.0 (API 21) 이상
- ✅ ARM64, ARMv7 아키텍처

## 🐛 알려진 이슈

- 첫 번째 빌드는 시간이 오래 걸립니다 (30분~1시간)
- APK 크기가 큽니다 (~50MB) - Python 런타임 포함

## 🔜 향후 계획

- [ ] iOS 버전 개발
- [ ] 다국어 지원
- [ ] 테스트 히스토리 저장
- [ ] Slack 알림 통합
- [ ] 자동 스케줄링

## 🤝 기여

이슈나 개선 사항이 있으시면 알려주세요!

---

**Made with Claude Code** 🤖
