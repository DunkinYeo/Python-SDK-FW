from appium import webdriver
import os


def get_driver():
    """Return an Appium webdriver.Remote instance using environment-configured capabilities.

    Environment variables:
      - APPIUM_SERVER_URL (default: http://localhost:4723/wd/hub)
      - APPIUM_PLATFORM_NAME (default: Android)
      - APPIUM_DEVICE_NAME (default: Android Emulator)
      - APPIUM_APP_PATH (path to app under test)
      - APPIUM_AUTOMATION_NAME (default: UiAutomator2)
    """
    desired_caps = {
        'platformName': os.getenv('APPIUM_PLATFORM_NAME', 'Android'),
        'deviceName': os.getenv('APPIUM_DEVICE_NAME', 'Android Emulator'),
        'app': os.getenv('APPIUM_APP_PATH', ''),
        'automationName': os.getenv('APPIUM_AUTOMATION_NAME', 'UiAutomator2'),
    }
    server_url = os.getenv('APPIUM_SERVER_URL', 'http://localhost:4723/wd/hub')
    return webdriver.Remote(server_url, desired_caps)
