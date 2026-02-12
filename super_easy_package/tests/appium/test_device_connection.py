"""Test BLE device connection and firmware version extraction."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.pages.read_screen import ReadScreen


@pytest.fixture(scope='module')
def driver():
    """Appium driver fixture."""
    print("\n🚀 Starting Appium driver...")
    d = get_driver()
    yield d
    print("\n🛑 Closing Appium driver...")
    try:
        d.quit()
    except Exception as e:
        print(f"Error quitting driver: {e}")


def test_manual_device_connection(driver):
    """
    Test that guides user through manual BLE device connection.

    Steps:
    1. Launch app
    2. Wait for user to manually connect device
    3. Verify connection
    4. Navigate to Read screen
    5. Extract firmware version
    """
    print("\n" + "="*60)
    print("🔌 BLE Device Connection Test")
    print("="*60)

    # Step 1: Initialize page objects
    main_screen = MainScreen(driver)
    read_screen = ReadScreen(driver)

    # Step 2: Wait for main screen to load
    print("\n📱 Waiting for app to load...")
    assert main_screen.wait_for_screen_ready(timeout=20), "Main screen did not load"
    print("✅ App loaded successfully")

    # Step 3: Navigate to Link screen (should be default)
    print("\n🔗 Navigating to Link screen...")
    main_screen.navigate_to_link()
    time.sleep(2)

    # Take screenshot of Link screen
    driver.save_screenshot('link_screen_before_connection.png')
    print("📸 Screenshot saved: link_screen_before_connection.png")

    # Step 4: Check current connection status
    is_connected = main_screen.is_device_connected()
    print(f"\n📡 Current connection status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    # Step 5: Wait for user to connect device
    if not is_connected:
        print("\n" + "="*60)
        print("⏳ WAITING FOR MANUAL CONNECTION")
        print("="*60)
        print("Please connect the BLE device manually using the app:")
        print("1. Enter Serial Number in the input field")
        print("2. Click the CONNECT button")
        print("3. Wait for connection to complete")
        print("\nWaiting up to 60 seconds for connection...")
        print("="*60)

        # Poll for connection status
        max_wait = 60  # seconds
        check_interval = 2  # seconds
        elapsed = 0

        while elapsed < max_wait:
            time.sleep(check_interval)
            elapsed += check_interval

            is_connected = main_screen.is_device_connected()

            if is_connected:
                print(f"\n✅ Device CONNECTED after {elapsed} seconds!")
                break
            else:
                print(f"⏳ Still waiting... ({elapsed}/{max_wait}s)")

        if not is_connected:
            print("\n❌ Connection timeout - device not connected within 60 seconds")
            driver.save_screenshot('connection_timeout.png')
            pytest.fail("BLE device was not connected within timeout period")

    # Step 6: Verify connection and get RSSI
    assert main_screen.is_device_connected(), "Device is not connected"
    print("\n✅ Device connection verified!")

    rssi = main_screen.get_rssi_value()
    print(f"📶 RSSI: {rssi}")

    # Take screenshot after connection
    driver.save_screenshot('link_screen_after_connection.png')
    print("📸 Screenshot saved: link_screen_after_connection.png")

    # Step 7: Navigate to Read screen
    print("\n📖 Navigating to Read screen...")
    assert main_screen.navigate_to_read(), "Failed to navigate to Read screen"
    time.sleep(2)

    assert read_screen.is_screen_loaded(timeout=10), "Read screen did not load"
    print("✅ Read screen loaded")

    # Take screenshot of Read screen
    driver.save_screenshot('read_screen_loaded.png')
    print("📸 Screenshot saved: read_screen_loaded.png")

    # Step 8: Read Firmware Version
    print("\n🔧 Reading Firmware Version...")
    print("Clicking FIRMWARE VERSION button...")

    assert read_screen.select_firmware_version(), "Failed to click FW VERSION button"
    print("✅ FIRMWARE VERSION button clicked")

    print("⏳ Waiting for device to respond (5 seconds)...")
    fw_version = read_screen.read_fw_version(wait_time=5)

    # Take screenshot after reading FW version
    driver.save_screenshot('read_screen_after_fw_read.png')
    print("📸 Screenshot saved: read_screen_after_fw_read.png")

    # Step 9: Display results
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    print(f"🔧 Firmware Version: {fw_version if fw_version else 'NOT FOUND'}")
    print(f"📶 RSSI: {rssi}")
    print("="*60)

    if fw_version:
        print("\n✅ SUCCESS: Firmware version extracted successfully!")
    else:
        print("\n⚠️  WARNING: Could not extract firmware version")
        print("Check the screenshot 'read_screen_after_fw_read.png' to see the UI state")

    # Assert that we got a version (can be commented out for debugging)
    assert fw_version, "Firmware version was not extracted"


def test_read_all_device_info(driver):
    """
    Test reading all available device information.

    Note: Requires device to be already connected from previous test.
    """
    print("\n" + "="*60)
    print("📋 Reading All Device Information")
    print("="*60)

    # Initialize page objects
    main_screen = MainScreen(driver)
    read_screen = ReadScreen(driver)

    # Ensure we're on Read screen
    if not read_screen.is_screen_loaded(timeout=5):
        print("📖 Navigating to Read screen...")
        main_screen.navigate_to_read()
        time.sleep(2)

    print("✅ On Read screen")

    # Read all available information
    info = {}

    # Get page source to see all available text
    page_source = driver.page_source

    # Save page source for debugging
    with open('read_screen_all_info.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)

    print("\n📄 Page source saved to: read_screen_all_info.xml")

    # Try to find all displayed values
    from appium.webdriver.common.appiumby import AppiumBy

    # Look for each information type
    info_types = [
        ("Battery", "Battery"),
        ("Model Number", "Model Number"),
        ("Serial Number", "Serial Number"),
        ("Firmware Version", "Firmware Version"),
        ("Hardware Version", "Hardware Version"),
        ("Software Version", "Software Version"),
    ]

    print("\n📊 Displayed Information:")
    print("-" * 60)

    for label, name in info_types:
        try:
            # Find the value TextView after the label
            value_elem = driver.find_element(
                AppiumBy.XPATH,
                f"//*[@text='{label}']/following-sibling::android.widget.TextView[1]"
            )
            value = value_elem.text
            info[name] = value if value else "(empty)"
            print(f"  {name:20} : {info[name]}")
        except Exception as e:
            info[name] = "(not found)"
            print(f"  {name:20} : {info[name]}")

    print("-" * 60)

    # Take final screenshot
    driver.save_screenshot('read_screen_all_info.png')
    print("\n📸 Screenshot saved: read_screen_all_info.png")

    print("\n✅ Information collection complete!")
