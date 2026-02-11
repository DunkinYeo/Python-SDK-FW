# 🚀 SDK 검증 자동화 - CI/CD 설정 가이드

## 📋 목차
1. [로컬 실행](#로컬-실행)
2. [Slack 연동 설정](#slack-연동-설정)
3. [GitHub Actions 설정](#github-actions-설정)
4. [Self-hosted Runner 설정](#self-hosted-runner-설정)
5. [사용 방법](#사용-방법)

---

## 🖥️ 로컬 실행

### 전제 조건
- Python 3.11+
- Android 디바이스 (USB 연결 또는 에뮬레이터)
- Appium Server 실행 중 (http://localhost:4723)
- BLE 패치 디바이스 (Serial: 610031)

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

**처음 설정하는 경우:**
```bash
# 템플릿 파일을 복사하여 .env 파일 생성
cp .env.template .env

# .env 파일 편집
nano .env  # 또는 pico .env, open -e .env
```

`.env` 파일에서 다음 항목 **필수 설정**:
```bash
# Appium
APPIUM_SERVER_URL=http://localhost:4723/wd/hub
APPIUM_DEVICE_NAME=55ETQWBXYE1RA1  # adb devices로 확인한 디바이스 ID

# App
APPIUM_APP_PATH=/path/to/automation-sdk2.1.5.apk

# BLE Device (필수!)
BLE_DEVICE_SERIAL=610031  # 본인의 패치 Serial Number로 변경!
```

**⚠️ 중요**: `BLE_DEVICE_SERIAL`은 반드시 설정해야 합니다. 각자 테스트할 패치의 Serial Number를 입력하세요.

### 3. 테스트 실행
```bash
# 간단한 실행
python -m pytest tests/regression/test_regression.py -v -s

# HTML 리포트와 함께 실행
./scripts/run_tests_and_notify.sh
```

---

## 💬 Slack 연동 설정

### Step 1: Slack Webhook URL 생성

1. Slack 워크스페이스의 [Incoming Webhooks](https://api.slack.com/messaging/webhooks) 페이지로 이동
2. "Create your Slack app" 클릭
3. "From scratch" 선택
4. App 이름 입력 (예: "SDK Validation Bot")
5. 워크스페이스 선택
6. "Incoming Webhooks" 활성화
7. "Add New Webhook to Workspace" 클릭
8. 알림을 받을 채널 선택
9. Webhook URL 복사 (예: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`)

### Step 2: 로컬 환경 변수 설정

`.env` 파일에 Webhook URL 추가:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Step 3: 테스트

```bash
# Slack 알림과 함께 테스트 실행
./scripts/run_tests_and_notify.sh
```

성공하면 Slack 채널에 다음 정보가 포함된 메시지가 전송됩니다:
- ✅ 테스트 결과 (성공/실패)
- 📱 디바이스 정보 (Model, Serial, FW/HW/SW Version, Battery, RSSI)
- 📊 테스트 통계 (전체, 성공, 실패, 성공률)
- ⏱️ 실행 시간

---

## 🤖 GitHub Actions 설정

### Step 1: GitHub Secrets 설정

Repository Settings > Secrets and variables > Actions에서 추가:

```
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
DEVICE_ID = 55ETQWBXYE1RA1  (선택사항, 기본값 사용 가능)
```

### Step 2: Workflow 파일 확인

`.github/workflows/sdk-validation.yml` 파일이 생성되어 있는지 확인

### Step 3: Self-hosted Runner 필요

**중요**: 실제 BLE 디바이스(패치)가 필요하므로 **self-hosted runner**를 사용해야 합니다.

GitHub-hosted runner는 다음 제약사항으로 사용 불가:
- ❌ 물리적 Android 디바이스 연결 불가
- ❌ BLE 디바이스 연결 불가
- ❌ Appium Server 설정 복잡

---

## 🏠 Self-hosted Runner 설정

### Step 1: Runner 등록

1. Repository Settings > Actions > Runners > New self-hosted runner
2. OS 선택 (macOS/Linux/Windows)
3. 제공된 명령어 실행하여 runner 등록

```bash
# 예시 (macOS)
mkdir actions-runner && cd actions-runner
curl -o actions-runner-osx-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-x64-2.311.0.tar.gz
tar xzf ./actions-runner-osx-x64-2.311.0.tar.gz
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN
./run.sh
```

### Step 2: Runner 환경 설정

Runner가 실행되는 머신에 다음을 설치:

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Android SDK & adb**
   ```bash
   adb version
   adb devices  # 디바이스 확인
   ```

3. **Appium Server**
   ```bash
   npm install -g appium@next
   appium driver install uiautomator2
   appium &  # 백그라운드 실행
   ```

4. **프로젝트 의존성**
   ```bash
   cd /path/to/actions-runner/_work/YOUR_REPO/YOUR_REPO
   pip install -r requirements.txt
   ```

5. **BLE 패치 디바이스**
   - Serial: 610031인 패치를 켜두기
   - Bluetooth 연결 가능한 상태 유지

### Step 3: Runner를 서비스로 실행 (선택사항)

```bash
# macOS/Linux
cd actions-runner
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```

---

## 🎯 사용 방법

### 1. 로컬에서 실행

```bash
# 전체 테스트 + Slack 알림
./scripts/run_tests_and_notify.sh

# pytest만 실행 (Slack 없이)
python -m pytest tests/regression/test_regression.py -v -s --html=test-report.html
```

### 2. GitHub Actions에서 수동 실행

1. Repository > Actions 탭
2. "SDK 검증 자동화 테스트" workflow 선택
3. "Run workflow" 버튼 클릭
4. Test Suite 선택:
   - `all`: 전체 테스트 (기본값)
   - `read_only`: Read 화면만
   - `writeget_only`: WriteGet 화면만
   - `notify_only`: Notify 화면만
5. "Run workflow" 다시 클릭

### 3. 자동 실행

다음 경우에 자동으로 실행됩니다:
- ✅ **Push to main**: `tests/`, `scripts/`, workflow 파일 변경 시
- ✅ **매일 오전 9시 (KST)**: 스케줄된 테스트

### 4. 결과 확인

**Slack 알림**:
- 테스트 완료 후 자동으로 Slack 채널에 결과 전송
- 성공/실패 여부, 디바이스 정보, 테스트 통계 포함

**GitHub Actions**:
- Actions 탭에서 실행 로그 확인
- Artifacts에서 HTML 리포트 다운로드
- Summary에서 간단한 통계 확인

**HTML 리포트**:
- 로컬: `test-report.html` 자동 열림
- GitHub: Artifacts에서 다운로드

---

## 📊 테스트 결과 예시

### Slack 메시지
```
✅ SDK 검증 테스트 결과

상태: SUCCESS
성공률: 90% (9/10)
실행 시간: 117.4초
실행 시각: 2026-02-10 16:30:45

📱 디바이스 정보
Model: S-Patch EX
Serial: 610031
FW Version: 2.04.006
HW Version: A2
SW Version: 2.0.2
Battery: 100%
RSSI: -38 dBm
App Version: 2.1.5

✅ 성공: 9개
❌ 실패: 1개
📊 전체: 10개
⏱️ 소요 시간: 117초

[📄 상세 리포트 보기] 버튼
```

---

## 🔧 문제 해결

### Appium 연결 실패
```bash
# Appium 서버 상태 확인
curl http://localhost:4723/status

# Appium 재시작
pkill -f appium
appium &
```

### 디바이스 연결 실패
```bash
# 디바이스 확인
adb devices

# 디바이스 재연결
adb kill-server
adb start-server
adb devices
```

### Slack 알림 실패
```bash
# Webhook URL 확인
echo $SLACK_WEBHOOK_URL

# 수동 테스트
python scripts/send_slack_notification.py
```

### Self-hosted Runner 문제
```bash
# Runner 상태 확인
cd actions-runner
./run.sh

# 로그 확인
tail -f _diag/Runner_*.log
```

---

## 📝 다음 단계

1. ✅ **로컬 테스트**: `./scripts/run_tests_and_notify.sh` 실행
2. ✅ **Slack 연동**: Webhook URL 설정 및 알림 테스트
3. ✅ **Self-hosted Runner**: Runner 설정 및 등록
4. ✅ **GitHub Actions**: 수동 실행 테스트
5. ✅ **자동화 확인**: Push 또는 스케줄 트리거 테스트

---

## 🎉 완료!

이제 "버튼 한두 번만 누르면" 자동으로:
- ✅ 패치에 연결
- ✅ 모든 기능 테스트
- ✅ FW/SDK 버전 정보 추출
- ✅ Slack으로 결과 알림
- ✅ HTML 리포트 생성

**한 줄 명령어**: `./scripts/run_tests_and_notify.sh`
**GitHub Actions**: "Run workflow" 버튼 클릭
