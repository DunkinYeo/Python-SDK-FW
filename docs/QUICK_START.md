# Quick Start Guide (5-minute setup)

Run SDK validation tests with just one or two button clicks!

## Prerequisites

1. **Android device** (USB connected or emulator)
2. **BLE patch device** (Serial Number of the patch to test)
3. **Appium Server** (running locally)

---

## 3-Step Setup

### Step 1: Create environment config

```bash
# Copy template
cp .env.template .env

# Edit the .env file
nano .env   # or: pico .env, open -e .env
```

### Step 2: Edit required fields in .env

```bash
# 1. Find your Android device ID (run in terminal)
adb devices
# Output example: 55ETQWBXYE1RA1    device

# 2. Update only these fields in .env:
APPIUM_DEVICE_NAME=55ETQWBXYE1RA1         # <- device ID from above
APPIUM_APP_PATH=/path/to/your-app.apk     # <- path to APK file
BLE_DEVICE_SERIAL=610031                  # <- patch Serial Number (required!)

# 3. For Slack notifications (optional):
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**Important:** You must set `BLE_DEVICE_SERIAL` to your own patch serial number!

### Step 3: Run tests

```bash
# Run all tests + Slack notification in one command
./scripts/run_tests_and_notify.sh
```

**Done!** Tests run automatically and results are sent to Slack.

---

## Finding Your Device ID and Serial Number

### Android device ID
```bash
adb devices
```
Example output:
```
List of devices attached
55ETQWBXYE1RA1    device  <- this is APPIUM_DEVICE_NAME
```

### Patch Serial Number
- 6-digit number printed on the patch case or label (e.g. 610031)
- Or check via the app's "Read > Serial Number" feature

---

## Viewing Results

1. **Terminal output**: Real-time test progress
2. **Slack notification**: Sent automatically after tests complete (if configured)
3. **HTML report**: `test-report.html` (opens automatically in browser)

---

## Troubleshooting

### "BLE_DEVICE_SERIAL not found in environment variables!"
→ Add `BLE_DEVICE_SERIAL=YOUR_SERIAL_NUMBER` to `.env`

### "Device not found" or Appium connection failure
```bash
# 1. Check device
adb devices

# 2. Check Appium server status
curl http://localhost:4723/status

# 3. Restart Appium
pkill -f appium
appium &
```

### Slack notifications not arriving
- Check that `SLACK_WEBHOOK_URL` is set in `.env`
- Verify the webhook URL is correct
- See "Slack Integration" section in [CI_CD_SETUP.md](CI_CD_SETUP.md)

---

## Next Steps

1. **Local testing**: `./scripts/run_tests_and_notify.sh`
2. **GitHub Actions setup**: See [CI_CD_SETUP.md](CI_CD_SETUP.md)
3. **Self-hosted Runner**: See [RUNNER_SETUP.md](RUNNER_SETUP.md) for full automation

---

## Tips

- **First run**: Make sure Appium server is running (`appium &`)
- **Quick restart**: App restarts automatically if already running
- **Run specific tests**: Use pytest options to select individual tests
  ```bash
  pytest tests/regression/test_regression.py::TestReadScreen -v
  ```

**Questions or issues? See [CI_CD_SETUP.md](CI_CD_SETUP.md)!**
