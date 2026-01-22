Appium automation setup

Overview
- Minimal Appium test helper and sample test using pytest.

Setup
1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Provide Appium environment variables (examples):

```bash
export APPIUM_SERVER_URL="http://localhost:4723/wd/hub"
export APPIUM_PLATFORM_NAME="Android"
export APPIUM_DEVICE_NAME="emulator-5554"
export APPIUM_APP_PATH="/absolute/path/to/your.apk"
export APPIUM_AUTOMATION_NAME="UiAutomator2"
```

Running tests

```bash
pytest tests/appium -q
```

Notes
- The sample test only asserts a session was created; expand tests to interact with your app's UI elements.
