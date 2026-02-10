# 🚀 빠른 시작 가이드 (5분 설정)

다른 사람들도 **버튼 한두 번**만 누르면 SDK 검증 테스트를 실행할 수 있습니다!

## 📋 준비물

1. **Android 디바이스** (USB 연결 또는 에뮬레이터)
2. **BLE 패치 디바이스** (연결할 패치의 Serial Number)
3. **Appium Server** (로컬에서 실행)

---

## ⚡ 3단계로 시작하기

### 1️⃣ 환경 설정 파일 만들기

```bash
# 템플릿 복사
cp .env.template .env

# .env 파일 편집
nano .env   # 또는 pico .env, open -e .env
```

### 2️⃣ .env 파일에서 수정해야 할 항목

```bash
# 1. Android 디바이스 ID 확인 (터미널에서 실행)
adb devices
# 출력 예: 55ETQWBXYE1RA1    device

# 2. .env 파일에서 다음 항목만 수정:
APPIUM_DEVICE_NAME=55ETQWBXYE1RA1         # ← 위에서 확인한 디바이스 ID
APPIUM_APP_PATH=/path/to/your-app.apk     # ← APK 파일 경로
BLE_DEVICE_SERIAL=610031                  # ← 패치 Serial Number (필수!)

# 3. Slack 알림을 원하면 (선택사항):
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**중요:** `BLE_DEVICE_SERIAL`은 반드시 본인의 패치 시리얼 번호로 변경하세요!

### 3️⃣ 테스트 실행

```bash
# 한 줄 명령어로 모든 테스트 실행 + Slack 알림
./scripts/run_tests_and_notify.sh
```

**끝!** 테스트가 자동으로 실행되고 결과가 Slack으로 전송됩니다.

---

## 🔍 디바이스 ID와 Serial Number 찾는 법

### Android 디바이스 ID
```bash
adb devices
```
출력 예시:
```
List of devices attached
55ETQWBXYE1RA1    device  ← 이것이 APPIUM_DEVICE_NAME
```

### 패치 Serial Number
- 패치 케이스나 라벨에 적혀 있는 6자리 숫자 (예: 610031)
- 또는 앱의 "Read > Serial Number" 기능으로 확인 가능

---

## 📊 실행 결과 확인

1. **터미널 출력**: 실시간 테스트 진행 상황
2. **Slack 알림**: 테스트 완료 후 자동 전송 (설정한 경우)
3. **HTML 리포트**: `test-report.html` 파일 (자동으로 브라우저에서 열림)

---

## ❓ 문제 해결

### "BLE_DEVICE_SERIAL not found in environment variables!"
→ `.env` 파일에 `BLE_DEVICE_SERIAL=YOUR_SERIAL_NUMBER` 추가

### "Device not found" 또는 Appium 연결 실패
```bash
# 1. 디바이스 확인
adb devices

# 2. Appium 서버 상태 확인
curl http://localhost:4723/status

# 3. Appium 재시작
pkill -f appium
appium &
```

### Slack 알림이 안 옴
- `.env` 파일에 `SLACK_WEBHOOK_URL` 설정 확인
- Webhook URL이 올바른지 확인
- [CI_CD_SETUP.md](CI_CD_SETUP.md)의 "Slack 연동 설정" 참고

---

## 🎯 다음 단계

설정을 완료했다면:

1. ✅ **로컬 테스트**: `./scripts/run_tests_and_notify.sh`
2. ✅ **GitHub Actions 설정**: [CI_CD_SETUP.md](CI_CD_SETUP.md) 참고
3. ✅ **Self-hosted Runner**: 자동화를 더 강화하려면 CI/CD 문서 참고

---

## 💡 팁

- **첫 실행**: Appium 서버가 실행 중인지 확인 (`appium &`)
- **빠른 재시작**: 앱이 이미 실행 중이면 자동으로 재시작됩니다
- **테스트 선택**: pytest 옵션으로 특정 테스트만 실행 가능
  ```bash
  pytest tests/regression/test_regression.py::TestReadScreen -v
  ```

**질문이나 문제가 있으면 [CI_CD_SETUP.md](CI_CD_SETUP.md)를 참고하세요!**
