"""Test with automatic permission handling."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.utils.permission_handler import handle_permission_dialogs
from appium.webdriver.common.appiumby import AppiumBy


# Hardcoded serial number
SERIAL_NUMBER = "610031"


def test_launch_and_handle_permissions():
    """Launch app and automatically handle permission dialogs."""
    print("\n🚀 Starting driver...")
    driver = get_driver()

    try:
        print("✅ Driver started")

        # Immediately handle any permission dialogs
        print("\n🔐 Handling permission dialogs...")
        dialogs_handled = handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)
        print(f"✅ Handled {dialogs_handled} permission dialogs")

        # Now app should be ready
        print("\n📱 Waiting for app to be ready...")
        main_screen = MainScreen(driver)

        if main_screen.wait_for_screen_ready(timeout=15):
            print("✅ App is ready!")
        else:
            print("⚠️  App not ready yet, waiting 5 more seconds...")
            time.sleep(5)

        # Take screenshot
        driver.save_screenshot('after_permission_handling.png')
        print("📸 Screenshot: after_permission_handling.png")

        # Check if we can see main screen elements
        try:
            link_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Link']")
            print("✅ Found Link button - app loaded successfully!")

            # Check connection status
            is_connected = main_screen.is_device_connected()
            print(f"\n📡 Connection Status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

            if not is_connected:
                print(f"\n🔗 Connecting to device (Serial: {SERIAL_NUMBER})...")

                # Enter serial number
                print(f"📝 Entering serial number: {SERIAL_NUMBER}")
                main_screen.enter_serial_number(SERIAL_NUMBER)

                # Click connect
                print("🔌 Clicking CONNECT...")
                main_screen.click_connect()

                # Wait for connection
                print("⏳ Waiting for connection...")
                for i in range(20):
                    time.sleep(1)
                    if main_screen.is_device_connected():
                        print(f"\n✅ Connected after {i+1} seconds!")
                        break
                    if (i + 1) % 5 == 0:
                        print(f"⏳ {i+1}/20s")

                # Wait for toast to disappear
                time.sleep(3)

            # Verify connection
            is_connected = main_screen.is_device_connected()
            if is_connected:
                rssi = main_screen.get_rssi_value()
                print(f"\n✅ Device connected!")
                print(f"📶 RSSI: {rssi}")
                print(f"📱 Serial: {SERIAL_NUMBER}")

                driver.save_screenshot('connected_successfully.png')
                print("📸 Screenshot: connected_successfully.png")

                print("\n✅ All steps completed successfully!")
            else:
                print("\n⚠️  Not connected")

        except Exception as e:
            print(f"❌ Error: {e}")

            # Show what's on screen
            all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
            print(f"\n📝 Current screen has {len(all_texts)} text elements:")
            for elem in all_texts[:15]:
                if elem.text:
                    print(f"   - {elem.text}")

    finally:
        print("\n🛑 Closing driver...")
        driver.quit()


if __name__ == "__main__":
    test_launch_and_handle_permissions()
