# 🚀 SDK 검증 자동화 시스템

**버튼 한두 번만 누르면** SDK 검증 앱의 모든 기능을 자동으로 테스트하고 결과를 Slack으로 받아볼 수 있습니다!

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Appium](https://img.shields.io/badge/Appium-2.0-green.svg)](https://appium.io/)
[![pytest](https://img.shields.io/badge/pytest-8.0-orange.svg)](https://pytest.org/)

> 🎨 **NEW!** 비개발자도 쉽게 사용할 수 있는 [GUI 앱](#-gui-앱-비개발자용) 추가!

## 📋 목차

- [✨ 주요 기능](#-주요-기능)
- [🎨 GUI 앱 (비개발자용)](#-gui-앱-비개발자용)
- [🎯 빠른 시작 (5분)](#-빠른-시작-5분)
- [📚 상세 문서](#-상세-문서)
- [🧪 테스트 항목](#-테스트-항목)
- [💬 Slack 알림](#-slack-알림)
- [🤖 CI/CD (GitHub Actions)](#-cicd-github-actions)
- [❓ 문제 해결](#-문제-해결)

---

## ✨ 주요 기능

- ✅ **자동 BLE 연결**: 패치 Serial Number로 자동 연결
- ✅ **Regression 테스트**: Read, WriteGet, Notify 화면 전체 테스트
- ✅ **패킷 모니터링**: 장시간 안정성 테스트 (사용자 정의 패킷 수)
- ✅ **디바이스 정보 추출**: FW/HW/SW 버전, Battery, RSSI 자동 수집
- ✅ **Slack 알림**: 테스트 결과 및 디바이스 정보 자동 전송
- ✅ **HTML 리포트**: 상세한 테스트 결과 리포트 자동 생성
- ✅ **GitHub Actions**: CI/CD 자동화 지원
- 🎨 **GUI 앱**: 비개발자도 쉽게 사용할 수 있는 그래픽 인터페이스

---

## 🎨 GUI 앱 (비개발자용)

개발 지식이 없어도 간단하게 테스트를 실행할 수 있는 GUI 애플리케이션을 제공합니다!

### 🚀 실행 방법

**macOS / Linux:**
```bash
./start_gui.sh
```

**Windows:**
```cmd
start_gui.bat
```

### 📸 주요 기능

- 🖱️ **간단한 클릭 인터페이스**: 복잡한 명령어 불필요
- 📊 **실시간 진행 상황**: 테스트 진행 상황을 실시간으로 확인
- 📝 **로그 표시**: 모든 테스트 과정을 GUI에서 확인
- ✅ **자동 리포트**: 테스트 완료 시 자동으로 HTML 리포트 열기
- 📱 **Slack 알림**: 자동 알림 전송

### 📋 사용 방법

1. GUI 앱 실행
2. 디바이스 시리얼 넘버 입력 (예: 610031)
3. 패킷 모니터링이 필요하면 체크박스 선택
4. "🚀 테스트 시작" 버튼 클릭
5. 결과 확인!

### 📚 상세 가이드

비개발자를 위한 상세 설치 및 사용 가이드: [SETUP_GUIDE_FOR_NON_DEVELOPERS.md](SETUP_GUIDE_FOR_NON_DEVELOPERS.md)

---

## 🎯 빠른 시작 (5분)

### 1️⃣ 필수 준비물

- **Python 3.11+** ([다운로드](https://www.python.org/downloads/))
- **Android 디바이스** (USB 연결 또는 에뮬레이터)
- **Appium Server** (로컬 실행 필요)
- **BLE 패치 디바이스** (테스트할 패치의 Serial Number)

### 2️⃣ 설치

```bash
# 1. 저장소 클론
git clone https://github.com/DunkinYeo/py-automation.git
cd py-automation

# 2. 의존성 설치
pip install -r requirements.txt

# 3. Appium 설치 (없는 경우)
npm install -g appium@next
appium driver install uiautomator2
```

### 3️⃣ 설정

```bash
# 1. 환경 설정 파일 생성
cp .env.template .env

# 2. .env 파일 편집
nano .env  # 또는 pico .env, open -e .env
```

**필수 설정 항목:**

```bash
# Android 디바이스 ID (adb devices 명령어로 확인)
APPIUM_DEVICE_NAME=YOUR_DEVICE_ID

# APK 파일 경로
APPIUM_APP_PATH=/path/to/automation-sdk.apk

# 패치 Serial Number (필수!)
BLE_DEVICE_SERIAL=610031  # 본인의 패치 번호로 변경
```

**디바이스 ID 확인 방법:**
```bash
adb devices
# 출력 예: 55ETQWBXYE1RA1    device
```

### 4️⃣ 실행

```bash
# Appium 서버 시작 (다른 터미널에서)
appium &

# 테스트 실행 (한 줄 명령어!)
./scripts/run_tests_and_notify.sh
```

**완료!** 🎉 테스트가 자동으로 실행되고 결과가 표시됩니다.

---

## 📚 상세 문서

- **[QUICK_START.md](QUICK_START.md)** - 5분 설정 가이드 (처음 사용자 추천)
- **[CI_CD_SETUP.md](CI_CD_SETUP.md)** - GitHub Actions 및 Self-hosted Runner 설정
- **.env.template** - 환경 설정 템플릿 (복사해서 사용)

---

## 🧪 테스트 항목

### Read 화면 (7개 테스트)
- ✅ Battery Level
- ✅ Model Number
- ✅ Serial Number
- ✅ Firmware Version
- ✅ Hardware Version
- ✅ Software Version
- ✅ **Firmware Version & Supported Sampling Rates**
  - 펌웨어 버전에 따른 지원 샘플링 레이트 자동 표시
  - 2.4.6+: 128/256 Hz 모두 지원
  - 2.3.5: 128 Hz만 지원
  - 2.2.x: 256 Hz만 지원

### 데이터 수집 워크플로우 (1개 통합 테스트)
완전한 데이터 수집 시나리오를 하나의 통합 테스트로 검증:

1. **WriteSet**: Start → 측정 시작
2. **WriteSet**: Pause → 측정 일시정지
3. **WriteSet**: Restart → 측정 재시작
4. **Notify**: 모든 데이터 스트림 활성화 확인
   - ECG, IMU, ACC, Memory, Heart Rate, Battery
5. **[선택] 장시간 안정성 테스트**: ECG 패킷 카운트 모니터링
   - `--target-packets` 옵션으로 목표 패킷 수 설정
   - 예: 1시간 = 3600 패킷, 1일 = 86400 패킷
   - 목표 도달까지 자동 대기 및 진행률 표시
6. **WriteSet**: Stop → 측정 종료
7. **WriteSet**: Reset Device → 디바이스 초기화

**총 8개 테스트** (Read 7개 + 워크플로우 1개)

#### 장시간 안정성 테스트 예시

**⚠️ 중요: 테스트 시작 전 준비사항**
1. 앱에서 **WriteSet** → **STOP** 실행
2. **WriteSet** → **RESET DEVICE** 실행
3. Packet Number가 0으로 초기화되었는지 확인
4. 테스트 시작

```bash
# 1시간 테스트 (3600 패킷)
pytest tests/regression/test_regression.py::TestDataCollectionWorkflow \
  --target-packets=3600 -v

# 12시간 테스트 (43200 패킷)
pytest tests/regression/test_regression.py::TestDataCollectionWorkflow \
  --target-packets=43200 -v

# 24시간 테스트 (86400 패킷)
pytest tests/regression/test_regression.py::TestDataCollectionWorkflow \
  --target-packets=86400 -v
```

**💡 팁:**
- 테스트 시작 시 자동으로 앱을 force-stop하지만, 디바이스 상태는 초기화되지 않습니다
- 이전 측정이 남아있으면 패킷 카운트가 계속 증가하여 테스트가 즉시 완료될 수 있습니다

---

## 💬 Slack 알림

테스트 완료 후 자동으로 Slack 채널에 다음 정보가 전송됩니다:

### 알림 내용
- 📊 **테스트 결과**: 성공/실패 상태, 성공률
- 📱 **디바이스 정보**:
  - Model: S-Patch EX
  - Serial: 610031
  - FW Version: 2.04.006
  - HW Version: A2
  - SW Version: 2.0.2
  - Battery: 100%
  - RSSI: -38 dBm
- ⏱️ **실행 시간**: 총 소요 시간
- ❌ **실패한 테스트**: 실패한 항목 목록 (있을 경우)

### Slack 설정 방법

1. [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) 페이지에서 Webhook 생성
2. `.env` 파일에 Webhook URL 추가:
   ```bash
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

상세한 설정 방법은 [CI_CD_SETUP.md](CI_CD_SETUP.md)를 참고하세요.

---

## 🤖 CI/CD (GitHub Actions)

### 수동 실행 (권장)

1. GitHub Repository → **Actions** 탭
2. **"SDK 검증 자동화 테스트"** 선택
3. **"Run workflow"** 버튼 클릭
4. Test Suite 선택 (all/read_only/writeget_only/notify_only)
5. 실행!

### 자동 실행

다음 경우에 자동으로 테스트가 실행됩니다:
- ✅ **매일 오전 9시 (KST)** - 스케줄된 테스트
- ✅ **main 브랜치 push 시** - `tests/`, `scripts/` 폴더 변경 시

### GitHub Secrets 설정

Repository Settings → Secrets and variables → Actions에서 추가:

```
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
BLE_DEVICE_SERIAL = YOUR_SERIAL_NUMBER
DEVICE_ID = YOUR_DEVICE_ID (선택사항)
```

**⚠️ 중요**: 실제 BLE 디바이스가 필요하므로 **Self-hosted Runner**를 사용해야 합니다.
설정 방법은 [CI_CD_SETUP.md](CI_CD_SETUP.md)를 참고하세요.

---

## 📊 실행 결과 예시

### 터미널 출력
```bash
============================================================
🧪 SDK 검증 자동화 테스트
============================================================

🛑 Stopping app...
🧪 Running regression tests...

tests/regression/test_regression.py::TestReadScreen::test_read_battery PASSED
tests/regression/test_regression.py::TestReadScreen::test_read_model_number PASSED
tests/regression/test_regression.py::TestReadScreen::test_read_serial_number PASSED
...

============================================================
📊 Test Results: 10 passed in 125.63s
✅ All tests passed
============================================================
```

### Slack 알림
```
✅ SDK 검증 테스트 결과

상태: SUCCESS
성공률: 100% (10/10)
실행 시간: 125.6초

📱 디바이스 정보
Model: S-Patch EX
Serial: 610031
FW Version: 2.04.006
...

[📄 상세 리포트 보기] 버튼
```

### HTML 리포트
`test-report.html` 파일이 자동으로 생성되고 브라우저에서 열립니다.

---

## ❓ 문제 해결

### "BLE_DEVICE_SERIAL not found" 에러
```bash
# .env 파일에 Serial Number 추가
echo "BLE_DEVICE_SERIAL=610031" >> .env
```

### Appium 연결 실패
```bash
# Appium 서버 상태 확인
curl http://localhost:4723/status

# Appium 재시작
pkill -f appium
appium &
```

### 디바이스 연결 안 됨
```bash
# 디바이스 확인
adb devices

# ADB 재시작
adb kill-server
adb start-server
```

### 특정 테스트만 실행하고 싶을 때
```bash
# Read 화면만 테스트
pytest tests/regression/test_regression.py::TestReadScreen -v

# WriteGet 화면만 테스트
pytest tests/regression/test_regression.py::TestWriteGetScreen -v

# Notify 화면만 테스트
pytest tests/regression/test_regression.py::TestNotifyScreen -v
```

---

## 🏗️ 프로젝트 구조

```
py-automation/
├── .env.template              # 환경 설정 템플릿
├── .github/
│   └── workflows/
│       └── sdk-validation.yml # GitHub Actions 워크플로우
├── scripts/
│   ├── run_tests_and_notify.sh      # 테스트 실행 + Slack 알림
│   └── send_slack_notification.py   # Slack 알림 스크립트
├── tests/
│   ├── appium/
│   │   ├── driver.py          # Appium 드라이버 설정
│   │   ├── pages/             # Page Object Model
│   │   └── utils/             # 유틸리티 함수
│   └── regression/
│       └── test_regression.py # Regression Test Suite
├── CI_CD_SETUP.md             # CI/CD 설정 가이드
├── QUICK_START.md             # 빠른 시작 가이드
└── README.md                  # 이 파일
```

---

## 🎯 사용 시나리오

### 시나리오 1: 로컬에서 빠른 테스트
```bash
./scripts/run_tests_and_notify.sh
```
→ 2분 안에 전체 테스트 완료 + Slack 알림

### 시나리오 2: GitHub Actions에서 자동 테스트
1. GitHub → Actions → Run workflow 클릭
2. 커피 한잔 ☕
3. Slack에서 결과 확인

### 시나리오 3: 새 FW 버전 테스트
1. 패치 업데이트
2. `./scripts/run_tests_and_notify.sh` 실행
3. Slack에서 새 FW 버전 정보 확인

---

## 🤝 팀원에게 공유하기

1. **저장소 공유**: 이 GitHub 저장소 링크 전달
2. **설정 가이드**: [QUICK_START.md](QUICK_START.md) 참고하도록 안내
3. **필수 정보**: 각자의 패치 Serial Number 준비
4. **3단계만 실행**:
   ```bash
   cp .env.template .env
   nano .env  # Serial Number 입력
   ./scripts/run_tests_and_notify.sh
   ```

---

## 📝 업데이트 히스토리

- **2026-02-10**:
  - ✅ Serial Number 하드코딩 제거, 환경 변수로 변경
  - ✅ .env.template 추가
  - ✅ QUICK_START.md 가이드 추가
  - ✅ 새 사용자 경험 개선
- **2026-02-10**:
  - ✅ Regression Test Suite 완성 (10개 테스트)
  - ✅ Slack 알림 기능 추가
  - ✅ GitHub Actions 워크플로우 구축
  - ✅ CI/CD 문서화 완료

---

## 📞 도움이 필요하신가요?

- 📖 **문서**: [QUICK_START.md](QUICK_START.md), [CI_CD_SETUP.md](CI_CD_SETUP.md)
- 🐛 **이슈**: [GitHub Issues](https://github.com/DunkinYeo/py-automation/issues)
- 💬 **질문**: Slack 채널에서 문의

---

## 🎉 축하합니다!

이제 **버튼 한두 번**만 누르면 SDK 검증이 자동으로 완료됩니다! 🚀
