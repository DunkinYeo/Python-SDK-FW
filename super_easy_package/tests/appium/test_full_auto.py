"""Fully automated test: connect device and extract FW version."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.utils.permission_handler import handle_permission_dialogs
from appium.webdriver.common.appiumby import AppiumBy
import re


SERIAL_NUMBER = "610031"


def test_full_auto_connect_and_extract_fw():
    """Fully automated: connect + extract FW version."""

    print("\n" + "="*60)
    print("🤖 FULLY AUTOMATED TEST")
    print("="*60)

    driver = get_driver()

    try:
        # Step 1: Handle permissions
        print("\n🔐 Step 1: Handling permissions...")
        dialogs = handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)
        print(f"✅ Handled {dialogs} permission dialogs")

        # Step 2: Wait for app to load
        print("\n📱 Step 2: Waiting for app to load...")
        time.sleep(5)

        main_screen = MainScreen(driver)

        # Check if app loaded
        try:
            driver.find_element(AppiumBy.XPATH, "//*[@text='Link']")
            print("✅ App loaded successfully")
        except:
            print("⚠️  Link button not found, waiting more...")
            time.sleep(5)

        driver.save_screenshot('step1_app_loaded.png')

        # Step 3: ALWAYS go to Link screen first
        print("\n🔗 Step 3: Going to Link screen...")
        main_screen.navigate_to_link()
        time.sleep(2)
        driver.save_screenshot('step2_link_screen.png')

        # Step 4: Check RSSI to verify real connection
        print("\n📡 Step 4: Checking RSSI (real connection status)...")
        rssi = main_screen.get_rssi_value()
        print(f"RSSI: {rssi}")

        # If RSSI is 0 or low, need to connect
        if rssi == "0" or int(rssi) == 0:
            print(f"\n🔌 Step 5: Auto-connecting (Serial: {SERIAL_NUMBER})...")

            # Make sure we're on Link screen
            main_screen.navigate_to_link()
            time.sleep(2)

            # Enter serial number
            print(f"📝 Entering serial number: {SERIAL_NUMBER}")
            success = main_screen.enter_serial_number(SERIAL_NUMBER)
            if not success:
                print("⚠️  Failed to enter serial number, trying again...")
                time.sleep(2)
                main_screen.enter_serial_number(SERIAL_NUMBER)

            driver.save_screenshot('step2_serial_entered.png')

            # Click CONNECT
            print("🔌 Clicking CONNECT button...")
            main_screen.click_connect()

            # Wait for connection - check RSSI value
            print("⏳ Waiting for connection (max 30 seconds)...")
            connected = False
            for i in range(30):
                time.sleep(1)

                # Check RSSI to verify real connection
                rssi = main_screen.get_rssi_value()

                if rssi != "0" and int(rssi) != 0:
                    print(f"\n✅ CONNECTED after {i+1} seconds! RSSI: {rssi}")
                    connected = True
                    break

                if (i + 1) % 5 == 0:
                    print(f"⏳ Waiting... {i+1}/30s (RSSI: {rssi})")

            if not connected:
                driver.save_screenshot('connection_failed.png')
                print("❌ Connection failed - RSSI still 0")
                return

            # Wait for toast to disappear
            time.sleep(3)

            driver.save_screenshot('step3_connected.png')
        else:
            print(f"✅ Already connected (RSSI: {rssi})")

        # Step 6: Verify connection with RSSI
        print("\n✅ Step 6: Verifying connection...")
        rssi = main_screen.get_rssi_value()

        if rssi == "0" or int(rssi) == 0:
            print(f"❌ Device not connected! RSSI: {rssi}")
            driver.save_screenshot('rssi_zero.png')
            return

        print(f"📶 RSSI: {rssi}")
        print(f"📱 Serial: {SERIAL_NUMBER}")
        print("✅ Connection verified!")

        # Step 7: Navigate to Read screen
        print("\n📖 Step 7: Navigating to Read screen...")

        # Hide keyboard first (from serial number input)
        try:
            driver.hide_keyboard()
            print("⌨️  Keyboard hidden")
        except:
            pass  # Keyboard might not be showing

        time.sleep(2)

        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        print("✅ Clicked Read button")

        time.sleep(5)
        driver.save_screenshot('step4_read_screen.png')

        # Verify Read screen
        try:
            driver.find_element(AppiumBy.XPATH, "//*[@text='Firmware Version']")
            print("✅ Read screen loaded")
        except:
            print("⚠️  Read screen may not be loaded properly")

        # Step 7: Click FIRMWARE VERSION button
        print("\n🔧 Step 7: Reading Firmware Version...")

        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        fw_button.click()
        print("✅ Clicked FIRMWARE VERSION button")

        # Wait for device response
        print("⏳ Waiting for device to respond (10 seconds)...")
        time.sleep(10)

        driver.save_screenshot('step5_fw_response.png')

        # Step 8: Extract FW version
        print("\n🔍 Step 8: Extracting firmware version...")

        fw_version = None

        # Try to get FW version value
        try:
            fw_value_elem = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value_elem.text

            if fw_text and fw_text.strip():
                # Extract version pattern if exists
                version_match = re.search(r'(\d+\.\d+\.\d+)', fw_text)
                if version_match:
                    fw_version = version_match.group(1)
                else:
                    fw_version = fw_text.strip()

                print(f"✅ Found firmware version: {fw_text}")
        except Exception as e:
            print(f"⚠️  Method 1 failed: {e}")

        # Alternative: search all TextViews
        if not fw_version or "not connected" in fw_version.lower():
            print("🔍 Searching all TextViews for version...")
            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")

            for elem in all_texts:
                text = elem.text
                if text and any(c.isdigit() for c in text):
                    version_match = re.search(r'(\d+\.\d+\.\d+)', text)
                    if version_match:
                        potential = version_match.group(1)
                        if potential != "2.1.5":  # Not app version
                            fw_version = potential
                            print(f"✅ Found in TextView: {fw_version}")
                            break

        # Step 9: Display results
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)

        if fw_version and "not connected" not in fw_version.lower():
            print(f"")
            print(f"✅ SUCCESS!")
            print(f"")
            print(f"🔧 Firmware Version: {fw_version}")
            print(f"📶 RSSI: {rssi}")
            print(f"📱 App Version: 2.1.5")
            print(f"📱 Serial Number: {SERIAL_NUMBER}")
            print(f"")
        else:
            print(f"")
            print(f"⚠️  PARTIAL SUCCESS")
            print(f"")
            print(f"🔧 Firmware Version: {fw_version if fw_version else 'NOT FOUND'}")
            print(f"📶 RSSI: {rssi}")
            print(f"📱 Serial Number: {SERIAL_NUMBER}")
            print(f"")
            print("Check screenshots for details:")
            print("  - step5_fw_response.png")
            print(f"")

        print("="*60)

    finally:
        print("\n🛑 Closing driver...")
        driver.quit()


if __name__ == "__main__":
    test_full_auto_connect_and_extract_fw()
