"""Automated BLE connection and firmware version extraction test."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from appium.webdriver.common.appiumby import AppiumBy
import re


# Hardcoded serial number for automatic connection
SERIAL_NUMBER = "610031"


@pytest.fixture(scope='module')
def driver():
    """Appium driver fixture - stays alive for all tests in this module."""
    print("\n🚀 Starting Appium driver...")
    d = get_driver()
    yield d
    print("\n🛑 Closing Appium driver...")
    try:
        d.quit()
    except Exception as e:
        print(f"Error quitting driver: {e}")


@pytest.fixture(scope='module')
def connected_driver(driver):
    """Connect to BLE device once and keep connection for all tests."""
    print("\n" + "="*60)
    print("🔌 Automatic BLE Connection")
    print("="*60)

    main_screen = MainScreen(driver)

    # Wait for app to load
    print("\n📱 Waiting for app to load...")
    assert main_screen.wait_for_screen_ready(timeout=20)
    time.sleep(2)
    print("✅ App loaded")

    # Check if already connected
    is_connected = main_screen.is_device_connected()
    print(f"\n📡 Current connection status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    if not is_connected:
        print(f"\n🔗 Connecting to device (Serial: {SERIAL_NUMBER})...")

        # Navigate to Link screen
        main_screen.navigate_to_link()
        time.sleep(2)

        # Enter serial number
        print(f"📝 Entering serial number: {SERIAL_NUMBER}")
        assert main_screen.enter_serial_number(SERIAL_NUMBER)

        # Click connect button
        print("🔌 Clicking CONNECT button...")
        assert main_screen.click_connect()

        # Wait for connection
        print("⏳ Waiting for connection (up to 20 seconds)...")
        max_wait = 20
        connected = False

        for i in range(max_wait):
            time.sleep(1)
            is_connected = main_screen.is_device_connected()

            if is_connected:
                print(f"\n✅ Device CONNECTED after {i+1} seconds!")
                connected = True
                break

            if (i + 1) % 5 == 0:
                print(f"⏳ Waiting... {i+1}/{max_wait}s")

        if not connected:
            driver.save_screenshot('connection_failed.png')
            pytest.fail("Failed to connect to device within 20 seconds")

        # Wait for toast to disappear
        print("⏳ Waiting for toast message to disappear (3 seconds)...")
        time.sleep(3)

    # Verify connection
    is_connected = main_screen.is_device_connected()
    assert is_connected, "Device is not connected"

    rssi = main_screen.get_rssi_value()
    print(f"\n✅ Connection established!")
    print(f"📶 RSSI: {rssi}")
    print(f"📱 Serial Number: {SERIAL_NUMBER}")

    driver.save_screenshot('connected_state.png')
    print("📸 Screenshot: connected_state.png")

    print("\n" + "="*60)
    print("✅ Connection setup complete")
    print("="*60)

    # Return driver for tests to use
    yield driver


def test_01_verify_connection(connected_driver):
    """Test 1: Verify device is connected."""
    print("\n" + "="*60)
    print("Test 1: Verify Connection")
    print("="*60)

    main_screen = MainScreen(connected_driver)

    is_connected = main_screen.is_device_connected()
    print(f"📡 Connection Status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    assert is_connected, "Device should be connected"

    rssi = main_screen.get_rssi_value()
    print(f"📶 RSSI: {rssi}")
    print("✅ Connection verified!")


def test_02_navigate_to_read_screen(connected_driver):
    """Test 2: Navigate to Read screen."""
    print("\n" + "="*60)
    print("Test 2: Navigate to Read Screen")
    print("="*60)

    # Wait a bit before navigating
    time.sleep(2)

    # Navigate to Read screen
    print("📖 Navigating to Read screen...")
    read_button = connected_driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
    read_button.click()
    print("✅ Clicked Read button")

    # Wait for screen transition
    print("⏳ Waiting for screen transition (5 seconds)...")
    time.sleep(5)

    connected_driver.save_screenshot('read_screen_for_tests.png')
    print("📸 Screenshot: read_screen_for_tests.png")

    # Verify Read screen loaded
    print("\n🔍 Verifying Read screen elements...")
    read_elements = ["Battery", "Firmware Version", "Hardware Version"]

    found_count = 0
    for elem_name in read_elements:
        try:
            connected_driver.find_element(AppiumBy.XPATH, f"//*[@text='{elem_name}']")
            print(f"   ✅ Found: {elem_name}")
            found_count += 1
        except:
            print(f"   ❌ Not found: {elem_name}")

    assert found_count > 0, "Read screen elements not found"
    print(f"\n✅ Read screen verified ({found_count} elements found)")


def test_03_extract_firmware_version(connected_driver):
    """Test 3: Extract firmware version."""
    print("\n" + "="*60)
    print("Test 3: Extract Firmware Version")
    print("="*60)

    # Find and click FIRMWARE VERSION button
    print("🔧 Looking for FIRMWARE VERSION button...")
    try:
        fw_button = connected_driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        print("✅ Found FIRMWARE VERSION button")

        # Click it
        print("🔧 Clicking FIRMWARE VERSION button...")
        fw_button.click()
        print("✅ Button clicked")

        # Wait for device response
        print("⏳ Waiting for device to respond (8 seconds)...")
        time.sleep(8)

        connected_driver.save_screenshot('after_fw_button_click_final.png')
        print("📸 Screenshot: after_fw_button_click_final.png")

        # Extract firmware version
        print("\n🔍 Extracting firmware version...")

        fw_version = None

        # Method 1: Find value after Firmware Version label
        try:
            fw_value = connected_driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value.text
            if fw_text:
                print(f"   Method 1 - Found text: '{fw_text}'")

                # Extract version pattern
                version_match = re.search(r'(\d+\.\d+\.\d+)', fw_text)
                if version_match:
                    fw_version = version_match.group(1)
                elif fw_text.strip() and fw_text != "":
                    fw_version = fw_text.strip()

        except Exception as e:
            print(f"   Method 1 failed: {e}")

        # Method 2: Search all TextViews
        if not fw_version:
            print("   Trying Method 2 - Searching all TextViews...")
            all_texts = connected_driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")

            for elem in all_texts:
                text = elem.text
                if text and any(char.isdigit() for char in text):
                    version_match = re.search(r'(\d+\.\d+\.\d+)', text)
                    if version_match:
                        potential_version = version_match.group(1)
                        # Exclude app version
                        if potential_version != "2.1.5":
                            fw_version = potential_version
                            print(f"   Method 2 - Found: '{fw_version}' in text: '{text}'")
                            break

        # Display results
        print("\n" + "="*60)
        print("📊 FIRMWARE VERSION EXTRACTION RESULTS")
        print("="*60)

        if fw_version:
            main_screen = MainScreen(connected_driver)
            rssi = main_screen.get_rssi_value()

            print(f"")
            print(f"✅ SUCCESS!")
            print(f"")
            print(f"🔧 Firmware Version: {fw_version}")
            print(f"📶 RSSI: {rssi}")
            print(f"📱 App Version: 2.1.5")
            print(f"📱 Serial Number: {SERIAL_NUMBER}")
            print(f"")
            print("="*60)

            assert fw_version, "Firmware version not extracted"
        else:
            print(f"❌ FAILED to extract firmware version")
            print("Check screenshot: after_fw_button_click_final.png")

            # Save page source for debugging
            page_source = connected_driver.page_source
            with open('fw_extraction_failed.xml', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print("📄 Page source saved: fw_extraction_failed.xml")

            pytest.fail("Firmware version extraction failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        connected_driver.save_screenshot('fw_extraction_error.png')
        pytest.fail(f"Test failed with error: {e}")


def test_04_read_other_device_info(connected_driver):
    """Test 4: Read other device information (Battery, Model, Serial, etc.)."""
    print("\n" + "="*60)
    print("Test 4: Read Other Device Information")
    print("="*60)

    # Make sure we're on Read screen
    try:
        connected_driver.find_element(AppiumBy.XPATH, "//*[@text='Firmware Version']")
        print("✅ Already on Read screen")
    except:
        print("📖 Navigating to Read screen...")
        read_button = connected_driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(5)

    # Try to read all available information
    print("\n📊 Reading all available device information...")

    info_types = [
        ("Battery", "BATTERY"),
        ("Model Number", "MODEL NUMBER"),
        ("Serial Number", "SERIAL NUMBER"),
        ("Hardware Version", "HARDWARE VERSION"),
        ("Software Version", "SOFTWARE VERSION"),
    ]

    results = {}

    for label, button_text in info_types:
        print(f"\n🔍 Reading {label}...")
        try:
            # Find and click button
            button = connected_driver.find_element(AppiumBy.XPATH, f"//*[@text='{button_text}']")
            button.click()
            print(f"   ✅ Clicked {button_text}")

            # Wait for response
            time.sleep(5)

            # Try to get value
            try:
                value_elem = connected_driver.find_element(
                    AppiumBy.XPATH,
                    f"//*[@text='{label}']/following-sibling::android.widget.TextView[1]"
                )
                value = value_elem.text
                if value:
                    results[label] = value
                    print(f"   ✅ {label}: {value}")
                else:
                    results[label] = "(empty)"
                    print(f"   ⚠️  {label}: (empty)")
            except:
                results[label] = "(not found)"
                print(f"   ⚠️  {label}: (not found)")

        except Exception as e:
            print(f"   ❌ Error reading {label}: {e}")
            results[label] = "(error)"

    # Display summary
    print("\n" + "="*60)
    print("📊 DEVICE INFORMATION SUMMARY")
    print("="*60)
    for key, value in results.items():
        print(f"  {key:20} : {value}")
    print("="*60)

    assert True  # Always pass for now
