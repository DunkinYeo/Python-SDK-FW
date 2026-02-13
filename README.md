# 🚀 SDK 검증 자동화 시스템

**버튼 두 번만 누르면** SDK 검증 앱의 모든 기능을 자동으로 테스트하고 결과를 Slack으로 받아볼 수 있습니다!

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Appium](https://img.shields.io/badge/Appium-2.0-green.svg)](https://appium.io/)
[![pytest](https://img.shields.io/badge/pytest-8.0-orange.svg)](https://pytest.org/)

> 🎨 **NEW!** 비개발자도 쉽게 사용할 수 있는 완전 자동화 패키지! Python, ADB, APK까지 자동 설치!

## 📋 목차

- [✨ 주요 기능](#-주요-기능)
- [🎨 초간단 버전 (추천!)](#-초간단-버전-추천)
- [🎯 빠른 시작 (개발자용)](#-빠른-시작-개발자용)
- [🧪 테스트 항목](#-테스트-항목)
- [💬 Slack 알림](#-slack-알림)
- [🤖 CI/CD (GitHub Actions)](#-cicd-github-actions)
- [❓ 문제 해결](#-문제-해결)
- [📝 업데이트 히스토리](#-업데이트-히스토리)

---

## ✨ 주요 기능

- ✅ **완전 자동 설치**: Python, ADB, SDK 앱까지 한 번에 자동 설치
- ✅ **자동 BLE 연결**: 패치 Serial Number로 자동 연결
- ✅ **Regression 테스트**: Read, WriteGet, Notify 화면 전체 테스트
- ✅ **패킷 모니터링**: 장시간 안정성 테스트 (사용자 정의 패킷 수)
- ✅ **디바이스 정보 추출**: FW/HW/SW 버전, Battery, RSSI 자동 수집
- ✅ **Slack 알림**: 테스트 결과 및 디바이스 정보 자동 전송
- ✅ **HTML 리포트**: 상세한 테스트 결과 리포트 자동 생성
- ✅ **GitHub Actions**: CI/CD 자동화 지원
- 🎨 **GUI 앱**: 비개발자도 쉽게 사용할 수 있는 그래픽 인터페이스

---

## 🎨 초간단 버전 (추천!)

**컴퓨터 기본 사용만 할 수 있다면 누구나 사용 가능!**

### 📦 다운로드

1. [SDK검증테스트_초간단버전.zip](https://github.com/DunkinYeo/Python-SDK-FW/releases) 다운로드
2. 압축 해제
3. 운영체제에 맞는 설치 프로그램 더블클릭:
   - **Windows**: `easy_installer_windows.bat`
   - **Mac**: `easy_installer.command`

### 🚀 실행

설치 완료 후:
- **Windows**: `테스트_시작.bat` 더블클릭
- **Mac**: `테스트_시작.command` 더블클릭

### 📸 GUI 화면

```
┌─────────────────────────────────────┐
│  ✅ SDK 검증 테스트                  │
│  단 두번의 클릭만으로 테스트 완료     │
├─────────────────────────────────────┤
│ BLE 시리얼: [610031         ]      │
│                                     │
│ ☐ 패킷 모니터링 포함                 │
│   타겟: [60] 개                     │
│                                     │
│ [    🚀 테스트 시작    ]            │
└─────────────────────────────────────┘
```

### 🎯 특징

- ⭐ **Python 자동 설치** (Windows만 해당)
- ⭐ **ADB 자동 설치**
- ⭐ **SDK 검증 앱 자동 다운로드 및 설치**
- ⭐ **Windows 완벽 호환** (이모지 없는 깔끔한 인터페이스)
- ⭐ **HTML 리포트 자동 정리** (손상 방지)

### 📚 상세 가이드

비개발자를 위한 초간단 가이드: [`super_easy_package/초간단가이드.md`](super_easy_package/초간단가이드.md)

---

## 🎯 빠른 시작 (개발자용)

### 1️⃣ 필수 준비물

- **Python 3.11+** ([다운로드](https://www.python.org/downloads/))
- **Android 디바이스** (USB 연결 또는 에뮬레이터)
- **BLE 패치 디바이스** (테스트할 패치의 Serial Number)

### 2️⃣ 설치

```bash
# 1. 저장소 클론
git clone https://github.com/DunkinYeo/Python-SDK-FW.git
cd Python-SDK-FW

# 2. 의존성 설치
pip install -r requirements.txt
```

### 3️⃣ 설정

```bash
# 1. 환경 설정 파일 생성
cp .env.template .env

# 2. .env 파일 편집
nano .env  # 패치 Serial Number 설정
```

### 4️⃣ 실행

```bash
# GUI 앱 실행 (추천)
python standalone_gui.py

# 또는 명령어로 실행
pytest tests/regression/test_regression.py -v
```

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

### 데이터 수집 워크플로우 (1개 통합 테스트)

완전한 데이터 수집 시나리오:

1. **WriteSet**: Start → 측정 시작
2. **WriteSet**: Pause → 측정 일시정지
3. **WriteSet**: Restart → 측정 재시작
4. **Notify**: 모든 데이터 스트림 활성화 확인
5. **[선택] 장시간 안정성 테스트**: ECG 패킷 모니터링
6. **WriteSet**: Stop → 측정 종료
7. **WriteSet**: Reset Device → 디바이스 초기화

**총 8개 테스트** (약 3분 소요)

---

## 💬 Slack 알림

테스트 완료 후 자동으로 Slack 채널에 전송되는 정보:

- 📊 **테스트 결과**: 성공/실패, 성공률
- 📱 **디바이스 정보**: Model, Serial, FW/HW/SW 버전, Battery, RSSI
- ⏱️ **실행 시간**: 총 소요 시간
- ❌ **실패한 테스트**: 실패 항목 목록

### Slack 설정

1. [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) 페이지에서 Webhook 생성
2. `.env` 파일에 추가:
   ```bash
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

---

## 🤖 CI/CD (GitHub Actions)

### 수동 실행

1. GitHub Repository → **Actions** 탭
2. **"SDK 검증 자동화 테스트"** 선택
3. **"Run workflow"** 클릭

### 자동 실행

- ✅ **매일 오전 9시 (KST)**
- ✅ **main 브랜치 push 시**

**⚠️ 주의**: 실제 BLE 디바이스가 필요하므로 **Self-hosted Runner** 사용 권장

---

## ❓ 문제 해결

### "Python not found" 오류
```bash
# easy_installer_windows.bat를 다시 실행 (자동 설치)
```

### "ADB not found" 오류
```bash
# easy_installer를 다시 실행 (자동 설치)
```

### 디바이스 연결 안 됨
```bash
# 디바이스 확인
adb devices

# ADB 재시작
adb kill-server && adb start-server
```

### HTML 리포트 Summary 안 보임
→ **자동 해결됨!** 테스트 실행 전 자동으로 이전 리포트 삭제

---

## 🏗️ 프로젝트 구조

```
py-automation/
├── super_easy_package/          # 🎨 초간단 패키지 (비개발자용)
│   ├── easy_installer_windows.bat  # Windows 자동 설치
│   ├── easy_installer.command      # Mac 자동 설치
│   ├── 테스트_시작.bat             # Windows 실행
│   ├── 테스트_시작.command         # Mac 실행
│   ├── standalone_gui.py           # GUI 앱
│   ├── requirements.txt            # Python 패키지 목록
│   ├── scripts/                    # 스크립트
│   ├── tests/                      # 테스트 코드
│   └── 초간단가이드.md             # 사용 가이드
├── .github/workflows/           # GitHub Actions
├── scripts/                     # 유틸리티 스크립트
├── tests/                       # 테스트 코드 (개발자용)
├── .env.template               # 환경 설정 템플릿
└── README.md                   # 이 파일
```

---

## 📝 업데이트 히스토리

### 2026-02-13
- ✅ **Windows 호환성 개선**
  - Windows .bat 파일에서 이모지 제거 (인코딩 문제 해결)
  - `[OK]`, `[ERROR]`, `[Download]` 등으로 대체
- ✅ **HTML 리포트 안정화**
  - 테스트 실행 전 이전 리포트 자동 삭제
  - "Summary 안 보임" 문제 완전 해결
- ✅ **GUI 개선**
  - 아이콘 변경: 🚀 → ✅
  - 메시지 개선: "단 두번의 클릭만으로 테스트 완료"
- ✅ **pytest-html 4.2.0 업그레이드**
  - HTML 리포트 detail 표시 개선

### 2026-02-12
- ✅ **완전 자동 설치 시스템 구축**
  - Windows: Python 자동 다운로드 및 설치
  - Windows/Mac: ADB 자동 설치
  - Windows/Mac: SDK 검증 앱 자동 다운로드 및 설치
- ✅ **초간단 패키지 출시**
  - `super_easy_package` 디렉토리 생성
  - 비개발자용 GUI 앱 및 자동 설치 스크립트
  - 초간단가이드.md 작성

### 2026-02-11
- ✅ **Standalone GUI 앱 완성**
  - Appium 불필요, Python + ADB만으로 실행
  - 실시간 로그 표시
  - 자동 HTML 리포트 열기
- ✅ **Packaging 개선**
  - ZIP 파일 생성 자동화
  - 한글 파일명 인코딩 문제 해결

### 2026-02-10
- ✅ **환경 설정 개선**
  - Serial Number 하드코딩 제거
  - .env.template 추가
  - QUICK_START.md 가이드 작성
- ✅ **Regression Test Suite 완성**
  - Read 화면 7개 테스트
  - 데이터 수집 워크플로우 통합 테스트
- ✅ **Slack 알림 기능 추가**
  - 디바이스 정보 자동 수집 및 전송
  - 테스트 결과 요약
- ✅ **GitHub Actions 워크플로우 구축**
  - 수동/자동 실행 지원
  - CI/CD 문서화 완료

### 초기 버전
- ✅ 기본 Appium 테스트 프레임워크 구축
- ✅ Page Object Model 구현
- ✅ 기본 테스트 케이스 작성

---

## 🎯 사용 시나리오

### 시나리오 1: 비개발자 - 초간단 버전
1. ZIP 파일 다운로드 및 압축 해제
2. `easy_installer` 실행 (한 번만)
3. `테스트_시작` 더블클릭
4. 결과 확인!

⏱️ **소요 시간**: 첫 설치 5분 + 테스트 3분

### 시나리오 2: 개발자 - 로컬 테스트
```bash
python standalone_gui.py
```
⏱️ **소요 시간**: 3분

### 시나리오 3: GitHub Actions - 자동화
1. Actions → Run workflow 클릭
2. Slack에서 결과 확인

⏱️ **소요 시간**: 자동

---

## 🤝 팀원에게 공유하기

### 비개발자 팀원
1. [최신 Release](https://github.com/DunkinYeo/Python-SDK-FW/releases)에서 `SDK검증테스트_초간단버전.zip` 다운로드
2. `초간단가이드.md` 참고하도록 안내

### 개발자 팀원
1. 저장소 공유
2. [QUICK_START.md](QUICK_START.md) 참고하도록 안내
3. 각자의 패치 Serial Number 준비

---

## 📞 도움이 필요하신가요?

- 📖 **비개발자**: [`super_easy_package/초간단가이드.md`](super_easy_package/초간단가이드.md)
- 📖 **개발자**: [QUICK_START.md](QUICK_START.md), [CI_CD_SETUP.md](CI_CD_SETUP.md)
- 🐛 **이슈**: [GitHub Issues](https://github.com/DunkinYeo/Python-SDK-FW/issues)
- 💬 **질문**: Slack #sdk-support 채널

---

## 🎉 시작하세요!

**버튼 두 번**만 누르면 SDK 검증이 자동으로 완료됩니다! 🚀

**Made with Claude Code** 🤖
