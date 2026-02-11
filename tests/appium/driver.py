from appium import webdriver
from appium.options.android import UiAutomator2Options
import os


def get_driver():
    """Return an Appium webdriver.Remote instance using environment-configured capabilities.

    Environment variables:
      - APPIUM_SERVER_URL (default: http://localhost:4723/wd/hub)
      - APPIUM_PLATFORM_NAME (default: Android)
      - APPIUM_DEVICE_NAME (default: Android Emulator)
      - APPIUM_APP_PATH (path to app under test)
      - APPIUM_AUTOMATION_NAME (default: UiAutomator2)
      - APPIUM_APP_PACKAGE (optional: app package name)
      - APPIUM_APP_ACTIVITY (optional: main activity)
    """
    # Create options object (new Appium API)
    options = UiAutomator2Options()
    options.platform_name = os.getenv('APPIUM_PLATFORM_NAME', 'Android')
    options.device_name = os.getenv('APPIUM_DEVICE_NAME', 'Android Emulator')

    app_path = os.getenv('APPIUM_APP_PATH', '')
    if app_path:
        options.app = app_path

    # SDK Sample app specifics
    options.app_package = os.getenv('APPIUM_APP_PACKAGE', 'com.wellysis.spatch.sdk.sample')
    options.app_activity = os.getenv('APPIUM_APP_ACTIVITY', 'com.wellysis.spatch.sdk.sample.MainActivity')

    # Automatically grant permissions (location, bluetooth, notifications, etc.)
    options.auto_grant_permissions = True

    # Don't reset app state between sessions (keeps app running and connected)
    options.no_reset = True
    options.full_reset = False

    server_url = os.getenv('APPIUM_SERVER_URL', 'http://localhost:4723/wd/hub')
    return webdriver.Remote(server_url, options=options)
