# SDK Validation Automation System

Automatically test all functions of the SDK validation app and receive results via Slack — with just two button clicks!

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Appium](https://img.shields.io/badge/Appium-2.0-green.svg)](https://appium.io/)
[![pytest](https://img.shields.io/badge/pytest-8.0-orange.svg)](https://pytest.org/)

---

## Features

- **Auto BLE connection**: Automatically connects using patch Serial Number
- **Regression tests**: Full test coverage for Read, WriteGet, and Notify screens
- **Packet monitoring**: Long-duration stability test (configurable packet count)
- **Device info extraction**: Automatically collects FW/HW/SW version, Battery, RSSI
- **Slack notifications**: Automatically sends test results and device info
- **HTML reports**: Detailed test result reports generated automatically
- **GitHub Actions**: CI/CD automation support
- **GUI app**: Graphical interface for non-developers

---

## Quick Start (Developers)

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Android device** (USB connected or emulator)
- **BLE patch device** (Serial Number of the patch to test)

### Install

```bash
# 1. Clone the repository
git clone https://github.com/DunkinYeo/Python-SDK-FW.git
cd Python-SDK-FW

# 2. Install dependencies
pip install -r requirements.txt
```

### Configure

```bash
# 1. Create environment config
cp .env.template .env

# 2. Edit .env file
nano .env  # Set your patch Serial Number
```

### Run

```bash
# GUI app (recommended)
python distribution/standalone_gui.py

# Or run via command line
pytest tests/regression/test_regression.py -v
```

---

## Test Items

### Read Screen (7 tests)
- Battery Level
- Model Number
- Serial Number
- Firmware Version
- Hardware Version
- Software Version
- Firmware Version & Supported Sampling Rates

### Data Collection Workflow (1 integration test)

Complete data collection scenario:

1. **WriteSet**: Start — begin measurement
2. **WriteSet**: Pause — pause measurement
3. **WriteSet**: Restart — resume measurement
4. **Notify**: Verify all data streams active
5. **[Optional] Long-duration stability test**: ECG packet monitoring
6. **WriteSet**: Stop — end measurement
7. **WriteSet**: Reset Device — reset device

**Total: 8 tests** (~3 minutes)

---

## Slack Notifications

Information automatically sent to Slack after tests complete:

- **Test results**: Pass/fail, pass rate
- **Device info**: Model, Serial, FW/HW/SW version, Battery, RSSI
- **Execution time**: Total elapsed time
- **Failed tests**: List of failed items

### Slack Setup

1. Create a webhook at [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
2. Add to `.env` file:
   ```bash
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

---

## CI/CD (GitHub Actions)

### Manual Trigger

1. GitHub Repository → **Actions** tab
2. Select **"SDK Validation Automation Test"**
3. Click **"Run workflow"**

### Scheduled

- Daily at 9:00 AM KST (runs code quality check)

> **Note**: Actual BLE device tests require a **self-hosted runner**. See [docs/RUNNER_SETUP.md](docs/RUNNER_SETUP.md).

---

## Project Structure

```
py-automation/
├── .github/
│   ├── scripts/                  # CI helper scripts
│   └── workflows/                # GitHub Actions workflows
├── distribution/                 # Non-developer package
│   ├── standalone_gui.py         # Standalone GUI app (no Appium)
│   ├── gui_test_runner.py        # Full GUI test runner
│   ├── build_standalone.py       # APK build script
│   ├── create_portable_package.py
│   ├── start_gui.sh / start_gui.bat
├── docs/                         # Documentation
│   ├── download.html             # APK download page (GitHub Pages)
│   ├── QUICK_START.md
│   ├── CI_CD_SETUP.md
│   ├── RUNNER_SETUP.md
│   ├── SETUP_GUIDE.md
│   └── USER_GUIDE.md
├── mobile_app/                   # Android app (Kivy/KivyMD)
│   ├── main_md.py
│   └── core/test_runner.py
├── scripts/                      # Utility scripts
├── tests/                        # Test code
│   ├── conftest.py
│   ├── appium/                   # Appium-based UI tests
│   ├── regression/               # Regression test suite
│   ├── sampling/                 # Sampling utilities
│   └── smoke/
├── .env.template                 # Environment config template
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Troubleshooting

### "ADB not found" error
```bash
# Re-run auto setup or install manually:
# https://developer.android.com/studio/releases/platform-tools
```

### Device not detected
```bash
# Check connected devices
adb devices

# Restart ADB
adb kill-server && adb start-server
```

### HTML report summary not showing
Resolved automatically — previous reports are deleted before each test run.

---

## Update History

### 2026-02-24
- Full English conversion (all Korean text removed from UI, workflows, docs)
- Project structure reorganized (docs/, distribution/ folders)
- Removed duplicate package variants (super_easy_package 2-7, etc.)
- Rebuilt APK with crash fix (sys.environ → os.environ)

### 2026-02-13
- Windows compatibility improvements (removed emoji from .bat files)
- HTML report stabilization (auto-delete previous report before run)
- pytest-html 4.2.0 upgrade

### 2026-02-12
- Full auto-install system (Python, ADB, SDK app)
- Non-developer distribution package released

### 2026-02-11
- Standalone GUI app (no Appium required, Python + ADB only)
- Real-time log display
- Auto HTML report opening

### 2026-02-10
- Removed hardcoded serial numbers, added .env.template
- Regression test suite completed (Read screen 7 tests)
- Slack notifications with device info
- GitHub Actions workflow setup

---

## Need Help?

- **Documentation**: [docs/](docs/)
- **Quick Start**: [docs/QUICK_START.md](docs/QUICK_START.md)
- **Runner Setup**: [docs/RUNNER_SETUP.md](docs/RUNNER_SETUP.md)
- **Issues**: [GitHub Issues](https://github.com/DunkinYeo/Python-SDK-FW/issues)
- **Chat**: Slack #sdk-support

---

**Made with Claude Code**
