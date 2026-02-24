# SDK Validation Test - Setup Guide

> This guide helps anyone run SDK validation tests, even without development experience.

## What You Need

1. **Windows PC or Mac**
2. **Android device** (connected via USB)
3. **BLE patch device**

---

## Step 1: Install Required Software

### 1.1 Android Debug Bridge (ADB)

**Windows:**
1. [Download Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. Extract the archive, copy the `platform-tools` folder to `C:\`
3. Add `C:\platform-tools` to your system PATH environment variable

**Mac:**
```bash
brew install android-platform-tools
```

**Verify installation** (in terminal or command prompt):
```bash
adb version
```

### 1.2 Node.js

Download and install the LTS version from the [official Node.js site](https://nodejs.org/)

**Verify:**
```bash
node --version
npm --version
```

### 1.3 Appium Server

In terminal:
```bash
npm install -g appium
appium driver install uiautomator2
```

**Verify:**
```bash
appium --version
```

---

## Step 2: Install SDK Validation Test App

### Option A: GUI app (recommended)

1. Download `sdk-auto-tester.apk` from the [latest release](https://github.com/DunkinYeo/Python-SDK-FW/releases)
2. Install on your Android device via ADB:
   ```bash
   adb install sdk-auto-tester.apk
   ```

### Option B: Run via Python script

1. Install Python 3.11+
2. From the project folder:
```bash
pip install -r requirements.txt
python distribution/gui_test_runner.py
```

---

## Step 3: Configure

### 3.1 Slack webhook URL (optional)

1. Create a `.env` file in the project folder
2. Add the following:
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
BLE_DEVICE_SERIAL=610031
```

### 3.2 Connect Android device

1. Connect your Android device to PC via USB
2. Enable **Developer options** on the device:
   - Go to Settings > About Phone > tap Build Number 7 times
3. Enable **USB debugging** in Developer options
4. Verify in terminal:
```bash
adb devices
```

Example output:
```
List of devices attached
55ETQWBXYE1RA1    device
```

---

## Step 4: Run Tests

### 4.1 Start Appium server

**Open a new terminal window and run:**
```bash
appium
```

When the server starts you will see:
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on http://localhost:4723
```

### 4.2 Run tests

```bash
# Full test suite
pytest tests/regression/test_regression.py -v

# Or use the GUI
python distribution/standalone_gui.py
```

### 4.3 View results

After tests complete:
- HTML report opens automatically in browser
- Slack notification sent (if configured)
- Logs viewable in GUI

---

## Troubleshooting

### "ADB not found" error
→ ADB not installed or not in PATH
- Check ADB installation: `adb version`
- Check PATH configuration

### "Appium server not running" error
→ Appium server is not running
- Run `appium` in terminal
- Check if port 4723 is in use

### "No devices connected" error
→ Android device not connected
- Check USB cable
- Verify USB debugging is enabled
- Run `adb devices` to check device

### "Permission denied" error
→ USB debugging authorization rejected on the device
- When the "Allow USB debugging?" popup appears on device, tap "Allow"
- Run `adb kill-server && adb start-server` and retry

---

## Additional Info

### Test types

1. **Basic tests** (~3 minutes)
   - Read screen function tests (7 items)
   - Data collection workflow test

2. **Packet monitoring test** (configurable duration)
   - 60 packets = ~1 minute
   - 600 packets = ~10 minutes
   - 3600 packets = ~1 hour
   - 86400 packets = ~1 day

### Report locations

- HTML report: `test-report.html`
- JSON report: `.report.json`

---

## Tips

1. **Before running tests**
   - Confirm the app is running on the Android device
   - Confirm the BLE patch is nearby

2. **For packet monitoring tests**
   - Manually reset the device before starting: WriteSet → STOP → RESET DEVICE

3. **Slack notifications**
   - Set `SLACK_WEBHOOK_URL` in `.env` to receive results automatically

---

## Need Help?

If problems persist:
1. Capture the log messages
2. Contact the development team
3. Report the issue on GitHub Issues

---

**Made with Claude Code**
