# 📱 SDK 검증 테스트 - 비개발자용 설치 가이드

> 이 가이드는 개발 지식이 없어도 SDK 검증 테스트를 실행할 수 있도록 도와드립니다.

## 🎯 필요한 것

1. **Windows PC 또는 Mac**
2. **Android 디바이스** (USB로 연결)
3. **BLE 패치 디바이스**

---

## 📥 1단계: 필수 프로그램 설치

### 1.1 Android Debug Bridge (ADB) 설치

**Windows:**
1. [Platform Tools 다운로드](https://developer.android.com/studio/releases/platform-tools)
2. 압축 해제 후 `platform-tools` 폴더를 `C:\` 드라이브에 복사
3. 시스템 환경 변수 PATH에 `C:\platform-tools` 추가

**Mac:**
```bash
brew install android-platform-tools
```

**설치 확인:**
터미널(또는 명령 프롬프트)에서:
```bash
adb version
```

### 1.2 Node.js 설치

[Node.js 공식 사이트](https://nodejs.org/)에서 LTS 버전 다운로드 및 설치

**설치 확인:**
```bash
node --version
npm --version
```

### 1.3 Appium 서버 설치

터미널에서:
```bash
npm install -g appium
appium driver install uiautomator2
```

**설치 확인:**
```bash
appium --version
```

---

## 🚀 2단계: SDK 검증 테스트 앱 설치

### 옵션 A: GUI 앱 사용 (권장)

1. `SDK검증테스트.exe` (Windows) 또는 `SDK검증테스트.app` (Mac) 다운로드
2. 더블클릭하여 실행

### 옵션 B: Python 스크립트로 실행

1. Python 3.11+ 설치
2. 프로젝트 폴더에서:
```bash
pip install -r requirements.txt
python gui_test_runner.py
```

---

## ⚙️ 3단계: 설정

### 3.1 Slack 웹훅 URL 설정 (선택사항)

1. 프로젝트 폴더에 `.env` 파일 생성
2. 다음 내용 추가:
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
BLE_DEVICE_SERIAL=610031
```

### 3.2 Android 디바이스 연결

1. Android 디바이스를 USB로 PC에 연결
2. 디바이스에서 **개발자 옵션** 활성화
3. **USB 디버깅** 활성화
4. 터미널에서 확인:
```bash
adb devices
```

출력 예시:
```
List of devices attached
55ETQWBXYE1RA1    device
```

---

## 🎮 4단계: 테스트 실행

### 4.1 Appium 서버 시작

**새 터미널 창을 열고:**
```bash
appium
```

서버가 시작되면 다음과 같은 메시지가 표시됩니다:
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on http://localhost:4723
```

### 4.2 GUI 앱 실행

1. `SDK검증테스트` 앱 실행
2. 디바이스 시리얼 넘버 입력 (예: 610031)
3. 패킷 모니터링이 필요하면 체크박스 선택 및 타겟 패킷 수 입력
4. **"🚀 테스트 시작"** 버튼 클릭

### 4.3 결과 확인

테스트가 완료되면:
- ✅ 자동으로 HTML 리포트가 브라우저에서 열림
- 📱 Slack으로 알림 전송 (설정한 경우)
- 📊 GUI에서 로그 확인 가능

---

## 🔧 문제 해결

### "ADB not found" 오류
➡️ ADB가 설치되지 않았거나 PATH에 추가되지 않음
- ADB 설치 확인: `adb version`
- PATH 설정 확인

### "Appium server not running" 오류
➡️ Appium 서버가 실행되지 않음
- 터미널에서 `appium` 명령 실행
- 포트 4723이 사용 중인지 확인

### "No devices connected" 오류
➡️ Android 디바이스가 연결되지 않음
- USB 케이블 확인
- USB 디버깅 활성화 확인
- `adb devices` 명령으로 디바이스 확인

### "Permission denied" 오류
➡️ Android 디바이스에서 USB 디버깅 권한 거부
- 디바이스에서 "USB 디버깅 허용" 팝업이 나타나면 "허용" 클릭
- `adb kill-server && adb start-server` 실행 후 재시도

---

## 📚 추가 정보

### 테스트 종류

1. **기본 테스트** (약 3분)
   - Read 화면 기능 테스트 (7개)
   - 데이터 수집 워크플로우 테스트

2. **패킷 모니터링 테스트** (사용자 정의 시간)
   - 60 패킷 = 약 1분
   - 600 패킷 = 약 10분
   - 3600 패킷 = 약 1시간
   - 86400 패킷 = 약 1일

### 리포트 위치

- HTML 리포트: `test-report.html`
- JSON 리포트: `.report.json`

---

## 💡 팁

1. **테스트 전 앱 상태 확인**
   - 앱이 실행되고 있는지 확인
   - BLE 패치가 연결되어 있는지 확인

2. **패킷 모니터링 테스트 시**
   - 테스트 시작 전 디바이스를 수동으로 리셋해야 합니다
   - WriteSet → STOP → RESET DEVICE

3. **Slack 알림**
   - 테스트 결과를 자동으로 Slack으로 받고 싶다면 `.env` 파일에 웹훅 URL 설정

---

## 🆘 도움이 필요하신가요?

문제가 해결되지 않으면:
1. 로그 메시지 캡처
2. 개발팀에 문의
3. GitHub Issues에 문제 보고

---

**Made with Claude Code** 🤖
