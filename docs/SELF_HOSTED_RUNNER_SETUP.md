# 🤖 Self-hosted Runner 설정 가이드

완전 자동화된 SDK 검증 테스트를 위한 Self-hosted Runner 설정 방법입니다.

## 📋 개요

Self-hosted runner를 설정하면:
- ✅ **매일 오전 9시 자동 테스트 실행**
- ✅ **실제 BLE 디바이스 테스트 자동화**
- ✅ **Slack 자동 알림**
- ✅ **Mac에서 24시간 자동 실행**

## 🚀 빠른 설치 (자동 스크립트)

### 1단계: 자동 설치 스크립트 실행

```bash
cd /Users/dunkinyeo/py-automation
./scripts/install_automation.sh
```

이 스크립트는 다음을 자동으로 설치합니다:
- ✅ Node.js (Appium 실행에 필요)
- ✅ Appium + UiAutomator2 드라이버
- ✅ ADB (Android Debug Bridge)
- ✅ Python 패키지들
- ✅ Appium 자동 시작 설정

### 2단계: Self-hosted Runner 등록

#### 개인 Repository (DunkinYeo/Python-SDK-FW)

1. GitHub 페이지 열기:
   ```
   https://github.com/DunkinYeo/Python-SDK-FW/settings/actions/runners/new
   ```

2. 토큰 복사 후 다음 명령어 실행:
   ```bash
   mkdir -p ~/actions-runner && cd ~/actions-runner

   # macOS ARM64용 다운로드
   curl -o actions-runner-osx-arm64-2.311.0.tar.gz -L \
     https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-arm64-2.311.0.tar.gz

   tar xzf ./actions-runner-osx-arm64-2.311.0.tar.gz

   # Runner 설정 (토큰을 YOUR_TOKEN에 입력)
   ./config.sh --url https://github.com/DunkinYeo/Python-SDK-FW --token YOUR_TOKEN

   # 서비스로 설치 (자동 시작 설정)
   ./svc.sh install
   ./svc.sh start
   ```

#### 회사 Repository (Wellysis/SDKApp-Automation-report-slack)

1. GitHub 페이지 열기:
   ```
   https://github.com/Wellysis/SDKApp-Automation-report-slack/settings/actions/runners/new
   ```

2. 위와 동일한 방식으로 설정 (URL만 변경):
   ```bash
   ./config.sh --url https://github.com/Wellysis/SDKApp-Automation-report-slack --token YOUR_TOKEN
   ```

### 3단계: Android 디바이스 연결

1. Android 디바이스를 Mac에 USB로 연결
2. USB 디버깅 활성화:
   - 설정 > 휴대전화 정보 > 빌드 번호 7번 탭
   - 설정 > 개발자 옵션 > USB 디버깅 활성화
3. 연결 확인:
   ```bash
   adb devices
   ```

### 4단계: 테스트 실행 확인

```bash
# Appium 서버 상태 확인
curl http://127.0.0.1:4723/status

# Self-hosted runner 상태 확인
cd ~/actions-runner
./svc.sh status

# 수동으로 테스트 실행해보기
cd /Users/dunkinyeo/py-automation
pytest tests/regression/test_regression.py -v
```

## ⚙️  환경 설정

### .env 파일 설정

```bash
cd /Users/dunkinyeo/py-automation
cp .env.template .env
nano .env
```

필수 설정:
```bash
# BLE 디바이스 시리얼 넘버
BLE_DEVICE_SERIAL=610031

# Slack Webhook URL (선택)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### GitHub Secrets 설정

Repository Settings > Secrets and variables > Actions에서 추가:

- `BLE_DEVICE_SERIAL`: BLE 디바이스 시리얼 넘버 (예: 610031)
- `SLACK_WEBHOOK_URL`: Slack Webhook URL
- `DEVICE_ID`: Android 디바이스 ID (선택, 기본값 사용 가능)

## 🔍 상태 확인 및 문제 해결

### Appium 서버 확인

```bash
# 로그 확인
tail -f /tmp/appium.log

# 프로세스 확인
ps aux | grep appium

# 수동 재시작
launchctl unload ~/Library/LaunchAgents/com.sdk.appium.plist
launchctl load ~/Library/LaunchAgents/com.sdk.appium.plist
```

### Self-hosted Runner 확인

```bash
cd ~/actions-runner

# 상태 확인
./svc.sh status

# 재시작
./svc.sh stop
./svc.sh start

# 로그 확인
cat _diag/Runner_*.log
```

### Android 디바이스 확인

```bash
# 연결된 디바이스 확인
adb devices

# 앱 설치 확인
adb shell pm list packages | grep wellysis

# ADB 재시작
adb kill-server
adb start-server
```

## 📅 자동 실행 스케줄

Self-hosted runner가 설정되면:
- ✅ **매일 오전 9시 (KST)** 자동으로 테스트 실행
- ✅ 테스트 완료 후 **Slack 알림 자동 전송**
- ✅ GitHub Actions에서 결과 확인 가능

## 🛑 Runner 중지/제거

### 일시 중지
```bash
cd ~/actions-runner
./svc.sh stop
```

### 완전 제거
```bash
cd ~/actions-runner
./svc.sh stop
./svc.sh uninstall
./config.sh remove --token YOUR_REMOVAL_TOKEN
```

### Appium 자동 시작 제거
```bash
launchctl unload ~/Library/LaunchAgents/com.sdk.appium.plist
rm ~/Library/LaunchAgents/com.sdk.appium.plist
```

## 💡 팁

1. **Mac을 절전 모드로 두지 마세요**
   - 시스템 설정 > 배터리 > 절전 모드 해제

2. **디바이스를 항상 연결해두세요**
   - USB 케이블 품질 확인
   - 충분한 전원 공급 확인

3. **정기적으로 로그 확인**
   ```bash
   # Appium 로그
   tail -f /tmp/appium.log

   # Runner 로그
   tail -f ~/actions-runner/_diag/Runner_*.log
   ```

4. **GitHub Actions 페이지에서 실행 기록 확인**
   - https://github.com/DunkinYeo/Python-SDK-FW/actions

## 🆘 도움이 필요하신가요?

- 📧 Issue 등록: https://github.com/DunkinYeo/Python-SDK-FW/issues
- 💬 Slack: #sdk-support 채널
- 📖 GitHub Actions 공식 문서: https://docs.github.com/en/actions/hosting-your-own-runners

---

**Made with Claude Code** 🤖
