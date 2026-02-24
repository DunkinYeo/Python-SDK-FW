# SDK Validation Test - User Guide

> Run SDK validation tests with just two clicks. No development experience required.

## What You Need

- Windows PC or Mac
- Android phone (connected via USB)
- BLE patch device

---

## Quick Start

### 1. Download the APK

Go to the [download page](https://dunkinyeo.github.io/Python-SDK-FW/download) and scan the QR code with your Android phone, or click the download button.

### 2. Install the APK on your Android phone

```
Settings > Install unknown apps > Allow
```

Then open the downloaded APK file to install.

### 3. Connect your Android phone to the computer

Use a USB cable. When prompted on the phone, tap **"Allow"** for USB debugging.

Check the connection:
```bash
adb devices
```

### 4. Run the test

Open the app on your phone:
1. Enter the BLE device serial number (e.g. `610031`)
2. Select which tests to run
3. Tap **Start Test**

---

## Test Items

| Test | Description | Duration |
|------|-------------|----------|
| Read Test | Read device info (FW version, battery, etc.) | ~30 sec |
| WriteGet Test | Set parameters and verify | ~60 sec |
| Notify Test | Verify data streaming | ~60 sec |
| Packet Monitoring | Long-duration stability test | Configurable |

---

## Reading Results

After tests complete, the app shows:
- **PASS / FAIL** for each test
- Overall pass rate
- Option to share results

Results are also sent to Slack automatically (if configured).

---

## Troubleshooting

### App crashes immediately after opening
- Uninstall and reinstall the APK
- Make sure your Android version is 8.0 or higher

### "No device connected" message
- Check the USB cable connection
- Enable USB debugging:
  1. Settings > About Phone > tap Build Number 7 times
  2. Settings > Developer options > enable USB Debugging
- Try a different USB cable or port

### BLE device not found
- Make sure the patch is powered on
- Check the serial number (printed on the patch label)
- Keep the patch within 1 meter of the phone

### Tests are failing
- Ensure the BLE patch is fully charged
- Restart the patch (hold power button)
- Restart the app and try again

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/DunkinYeo/Python-SDK-FW/issues)
- **Slack**: #sdk-support channel
- **Developer guide**: [QUICK_START.md](QUICK_START.md)

---

**Made with Claude Code**
