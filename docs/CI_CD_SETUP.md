# SDK Validation Automation - CI/CD Setup Guide

## Table of Contents
1. [Local Execution](#local-execution)
2. [Slack Integration](#slack-integration)
3. [GitHub Actions Setup](#github-actions-setup)
4. [Self-hosted Runner Setup](#self-hosted-runner-setup)
5. [Usage](#usage)

---

## Local Execution

### Prerequisites
- Python 3.11+
- Android device (USB connected or emulator)
- Appium Server running (http://localhost:4723)
- BLE patch device (Serial: 610031)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

**First-time setup:**
```bash
# Copy template to create .env file
cp .env.template .env

# Edit .env file
nano .env  # or: pico .env, open -e .env
```

Required fields in `.env`:
```bash
# Appium
APPIUM_SERVER_URL=http://localhost:4723/wd/hub
APPIUM_DEVICE_NAME=55ETQWBXYE1RA1  # Device ID from: adb devices

# App
APPIUM_APP_PATH=/path/to/automation-sdk2.1.5.apk

# BLE Device (required!)
BLE_DEVICE_SERIAL=610031  # Replace with your patch Serial Number!
```

**Important**: `BLE_DEVICE_SERIAL` is required. Enter the Serial Number of the patch you are testing.

### 3. Run tests
```bash
# Simple run
python -m pytest tests/regression/test_regression.py -v -s

# With HTML report and Slack notification
./scripts/run_tests_and_notify.sh
```

---

## Slack Integration

### Step 1: Create a Slack Webhook URL

1. Go to [Incoming Webhooks](https://api.slack.com/messaging/webhooks) for your Slack workspace
2. Click "Create your Slack app"
3. Select "From scratch"
4. Enter an app name (e.g. "SDK Validation Bot")
5. Select your workspace
6. Enable "Incoming Webhooks"
7. Click "Add New Webhook to Workspace"
8. Select the channel to post notifications to
9. Copy the Webhook URL (e.g. `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`)

### Step 2: Set local environment variable

Add the Webhook URL to your `.env` file:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Step 3: Test

```bash
# Run tests with Slack notification
./scripts/run_tests_and_notify.sh
```

On success, a message will be posted to Slack containing:
- Test results (pass/fail)
- Device info (Model, Serial, FW/HW/SW Version, Battery, RSSI)
- Test statistics (total, passed, failed, pass rate)
- Execution time

---

## GitHub Actions Setup

### Step 1: Add GitHub Secrets

In Repository Settings > Secrets and variables > Actions:

```
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
DEVICE_ID = 55ETQWBXYE1RA1  (optional, default value can be used)
BLE_DEVICE_SERIAL = 610031
```

### Step 2: Verify workflow file

Confirm that `.github/workflows/sdk-validation.yml` exists.

### Step 3: Self-hosted runner required

**Important**: A real BLE device (patch) is required, so you must use a **self-hosted runner**.

GitHub-hosted runners cannot be used due to:
- No physical Android device connection
- No BLE device connection
- Complex Appium server setup

---

## Self-hosted Runner Setup

### Step 1: Register runner

1. Go to Repository Settings > Actions > Runners > New self-hosted runner
2. Select your OS (macOS/Linux/Windows)
3. Run the provided commands to register the runner

```bash
# Example (macOS ARM64)
mkdir actions-runner && cd actions-runner
curl -o actions-runner-osx-arm64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-arm64-2.311.0.tar.gz
tar xzf ./actions-runner-osx-arm64-2.311.0.tar.gz
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN
./run.sh
```

### Step 2: Configure runner environment

Install the following on the machine running the runner:

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Android SDK & ADB**
   ```bash
   adb version
   adb devices  # verify device connection
   ```

3. **Appium Server**
   ```bash
   npm install -g appium@next
   appium driver install uiautomator2
   appium &  # run in background
   ```

4. **Project dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **BLE patch device**
   - Keep the patch with Serial 610031 powered on
   - Ensure Bluetooth is in a connectable state

### Step 3: Run runner as a service (optional)

```bash
# macOS/Linux
cd actions-runner
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```

For detailed instructions, see [RUNNER_SETUP.md](RUNNER_SETUP.md).

---

## Usage

### 1. Local execution

```bash
# Full test suite + Slack notification
./scripts/run_tests_and_notify.sh

# pytest only (no Slack)
python -m pytest tests/regression/test_regression.py -v -s --html=test-report.html
```

### 2. Manual trigger via GitHub Actions

1. Go to Repository > Actions tab
2. Select "SDK Validation Automation Test" workflow
3. Click "Run workflow"
4. Select test suite:
   - `all`: full test suite (default)
   - `read_only`: Read screen only
   - `writeget_only`: WriteGet screen only
   - `notify_only`: Notify screen only
5. Click "Run workflow" again

### 3. Scheduled execution

Runs automatically:
- **Daily code quality check**: every day at 9:00 AM KST (GitHub-hosted runner)
- **Device tests**: manual trigger only (requires self-hosted runner with device)

### 4. Viewing results

**Slack notification:**
- Results sent automatically to Slack after tests complete
- Includes pass/fail status, device info, and test statistics

**GitHub Actions:**
- View execution logs in the Actions tab
- Download HTML report from Artifacts
- View summary statistics in the workflow summary

**HTML report:**
- Local: `test-report.html` opens automatically
- GitHub: download from Artifacts

---

## Example Test Results

### Slack message
```
SDK Validation Test Results

Status: SUCCESS
Pass rate: 90% (9/10)
Execution time: 117.4s
Time: 2026-02-10 16:30:45

Device Info
Model: S-Patch EX
Serial: 610031
FW Version: 2.04.006
HW Version: A2
SW Version: 2.0.2
Battery: 100%
RSSI: -38 dBm
App Version: 2.1.5

Passed: 9
Failed: 1
Total: 10
Duration: 117s

[View detailed report] button
```

---

## Troubleshooting

### Appium connection failure
```bash
# Check Appium server status
curl http://localhost:4723/status

# Restart Appium
pkill -f appium
appium &
```

### Device connection failure
```bash
# Check devices
adb devices

# Reconnect device
adb kill-server
adb start-server
adb devices
```

### Slack notification failure
```bash
# Check webhook URL
echo $SLACK_WEBHOOK_URL

# Manual test
python scripts/send_slack_notification.py
```

### Self-hosted runner issues
```bash
# Check runner status
cd actions-runner
./run.sh

# View logs
tail -f _diag/Runner_*.log
```

---

## Next Steps

1. **Local testing**: Run `./scripts/run_tests_and_notify.sh`
2. **Slack integration**: Set webhook URL and test notifications
3. **Self-hosted runner**: Register and configure runner
4. **GitHub Actions**: Test manual trigger
5. **Verify automation**: Test push or schedule trigger

---

**Made with Claude Code**
