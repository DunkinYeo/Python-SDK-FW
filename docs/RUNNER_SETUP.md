# Self-hosted Runner Setup Guide

Setup guide for fully automated SDK validation tests with a self-hosted runner.

## Overview

With a self-hosted runner you get:
- Automated test execution on a schedule
- Real BLE device testing
- Automatic Slack notifications
- Unattended 24/7 operation on Mac

## Quick Install (Automated Script)

### Step 1: Run the auto-install script

```bash
cd /Users/dunkinyeo/py-automation
./scripts/install_automation.sh
```

This script automatically installs:
- Node.js (required for Appium)
- Appium + UiAutomator2 driver
- ADB (Android Debug Bridge)
- Python packages
- Appium auto-start configuration

### Step 2: Register Self-hosted Runner

#### Personal Repository (DunkinYeo/Python-SDK-FW)

1. Open the GitHub settings page:
   ```
   https://github.com/DunkinYeo/Python-SDK-FW/settings/actions/runners/new
   ```

2. Copy the token and run:
   ```bash
   mkdir -p ~/actions-runner && cd ~/actions-runner

   # Download for macOS ARM64
   curl -o actions-runner-osx-arm64-2.311.0.tar.gz -L \
     https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-arm64-2.311.0.tar.gz

   tar xzf ./actions-runner-osx-arm64-2.311.0.tar.gz

   # Configure runner (replace YOUR_TOKEN)
   ./config.sh --url https://github.com/DunkinYeo/Python-SDK-FW --token YOUR_TOKEN

   # Install as service (auto-start)
   ./svc.sh install
   ./svc.sh start
   ```

#### Company Repository (Wellysis/SDKApp-Automation-report-slack)

1. Open the GitHub settings page:
   ```
   https://github.com/Wellysis/SDKApp-Automation-report-slack/settings/actions/runners/new
   ```

2. Same procedure as above (change URL only):
   ```bash
   ./config.sh --url https://github.com/Wellysis/SDKApp-Automation-report-slack --token YOUR_TOKEN
   ```

### Step 3: Connect Android Device

1. Connect Android device to Mac via USB
2. Enable USB debugging:
   - Settings > About Phone > tap Build Number 7 times
   - Settings > Developer options > enable USB Debugging
3. Verify connection:
   ```bash
   adb devices
   ```

### Step 4: Verify Test Execution

```bash
# Check Appium server status
curl http://127.0.0.1:4723/status

# Check self-hosted runner status
cd ~/actions-runner
./svc.sh status

# Run tests manually
cd /Users/dunkinyeo/py-automation
pytest tests/regression/test_regression.py -v
```

## Environment Configuration

### .env file

```bash
cd /Users/dunkinyeo/py-automation
cp .env.template .env
nano .env
```

Required settings:
```bash
# BLE device serial number
BLE_DEVICE_SERIAL=610031

# Slack Webhook URL (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### GitHub Secrets

In Repository Settings > Secrets and variables > Actions:

- `BLE_DEVICE_SERIAL`: BLE device serial number (e.g. 610031)
- `SLACK_WEBHOOK_URL`: Slack Webhook URL
- `DEVICE_ID`: Android device ID (optional, default value can be used)

## Status Checks and Troubleshooting

### Appium server

```bash
# View logs
tail -f /tmp/appium.log

# Check process
ps aux | grep appium

# Manual restart
launchctl unload ~/Library/LaunchAgents/com.sdk.appium.plist
launchctl load ~/Library/LaunchAgents/com.sdk.appium.plist
```

### Self-hosted runner

```bash
cd ~/actions-runner

# Check status
./svc.sh status

# Restart
./svc.sh stop
./svc.sh start

# View logs
cat _diag/Runner_*.log
```

### Android device

```bash
# Check connected devices
adb devices

# Check app installation
adb shell pm list packages | grep wellysis

# Restart ADB
adb kill-server
adb start-server
```

## Automatic Schedule

With self-hosted runner configured:
- Daily code quality check at 9:00 AM KST (GitHub-hosted runner)
- Device tests: manual trigger via GitHub Actions

## Stopping / Removing Runner

### Pause
```bash
cd ~/actions-runner
./svc.sh stop
```

### Full removal
```bash
cd ~/actions-runner
./svc.sh stop
./svc.sh uninstall
./config.sh remove --token YOUR_REMOVAL_TOKEN
```

### Remove Appium auto-start
```bash
launchctl unload ~/Library/LaunchAgents/com.sdk.appium.plist
rm ~/Library/LaunchAgents/com.sdk.appium.plist
```

## Tips

1. **Keep Mac awake**
   - System Settings > Battery > disable sleep mode

2. **Keep device connected**
   - Check USB cable quality
   - Ensure adequate power supply

3. **Check logs regularly**
   ```bash
   # Appium logs
   tail -f /tmp/appium.log

   # Runner logs
   tail -f ~/actions-runner/_diag/Runner_*.log
   ```

4. **Check execution history on GitHub Actions**
   - https://github.com/DunkinYeo/Python-SDK-FW/actions

## Need Help?

- **Issues**: https://github.com/DunkinYeo/Python-SDK-FW/issues
- **Slack**: #sdk-support channel
- **GitHub Actions docs**: https://docs.github.com/en/actions/hosting-your-own-runners

---

**Made with Claude Code**
