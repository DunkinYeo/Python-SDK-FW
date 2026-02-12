"""Test to extract firmware version from connected device."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from appium.webdriver.common.appiumby import AppiumBy
import re


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


def test_extract_firmware_version(driver):
    """Extract firmware version from connected device."""
    print("\n" + "="*60)
    print("🔧 Firmware Version Extraction Test")
    print("="*60)

    main_screen = MainScreen(driver)

    # Step 1: Wait for app to load
    print("\n📱 Step 1: Waiting for app to load...")
    assert main_screen.wait_for_screen_ready(timeout=20)
    time.sleep(2)
    print("✅ App loaded")

    # Step 2: Verify device is connected
    print("\n🔍 Step 2: Verifying device connection...")
    is_connected = main_screen.is_device_connected()
    print(f"📡 Connection status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    if not is_connected:
        print("\n❌ Device not connected. Please connect device first.")
        pytest.fail("Device must be connected to extract firmware version")

    rssi = main_screen.get_rssi_value()
    print(f"📶 RSSI: {rssi}")

    # Step 3: Wait for toast and app to stabilize
    print("\n⏳ Step 3: Waiting for app to stabilize (5 seconds)...")
    time.sleep(5)

    # Step 4: Navigate to Read screen
    print("\n📖 Step 4: Navigating to Read screen...")
    read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
    read_button.click()
    print("✅ Clicked Read button")

    print("⏳ Waiting for Read screen to load (5 seconds)...")
    time.sleep(5)

    driver.save_screenshot('read_screen_loaded_for_fw.png')
    print("📸 Screenshot: read_screen_loaded_for_fw.png")

    # Step 5: Verify Read screen loaded
    print("\n🔍 Step 5: Verifying Read screen elements...")
    try:
        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        print("✅ Found FIRMWARE VERSION button")
    except Exception as e:
        print(f"❌ FIRMWARE VERSION button not found: {e}")
        driver.save_screenshot('fw_button_not_found.png')
        pytest.fail("FIRMWARE VERSION button not found on Read screen")

    # Step 6: Click FIRMWARE VERSION button
    print("\n🔧 Step 6: Clicking FIRMWARE VERSION button...")
    fw_button.click()
    print("✅ Button clicked")

    # Step 7: Wait for device to respond
    print("\n⏳ Step 7: Waiting for device to respond (8 seconds)...")
    time.sleep(8)  # Give device time to communicate FW version

    driver.save_screenshot('after_fw_button_click.png')
    print("📸 Screenshot: after_fw_button_click.png")

    # Step 8: Extract firmware version
    print("\n🔍 Step 8: Extracting firmware version...")
    fw_version = None

    # Method 1: Try to find value next to "Firmware Version" label
    try:
        fw_value_elem = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
        )
        fw_text = fw_value_elem.text
        if fw_text:
            print(f"   Method 1 - Found text: '{fw_text}'")
            # Extract version pattern
            version_match = re.search(r'(\d+\.\d+\.\d+)', fw_text)
            if version_match:
                fw_version = version_match.group(1)
            elif fw_text.strip():
                fw_version = fw_text.strip()
    except Exception as e:
        print(f"   Method 1 failed: {e}")

    # Method 2: Search all TextViews for version pattern
    if not fw_version:
        print("   Trying Method 2 - Searching all TextViews...")
        try:
            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for elem in all_texts:
                text = elem.text
                if text and any(char.isdigit() for char in text):
                    # Check if it matches version pattern
                    version_match = re.search(r'(\d+\.\d+\.\d+)', text)
                    if version_match:
                        potential_version = version_match.group(1)
                        # Filter out things like "2.1.5" (app version) if we know it
                        if potential_version != "2.1.5":
                            fw_version = potential_version
                            print(f"   Method 2 - Found version: '{fw_version}' in text: '{text}'")
                            break
        except Exception as e:
            print(f"   Method 2 failed: {e}")

    # Method 3: Get page source and search
    if not fw_version:
        print("   Trying Method 3 - Searching page source...")
        page_source = driver.page_source
        with open('fw_extraction_page_source.xml', 'w', encoding='utf-8') as f:
            f.write(page_source)

        # Find all text attributes in XML
        texts_in_xml = re.findall(r'text="([^"]+)"', page_source)
        for text in texts_in_xml:
            if text and any(char.isdigit() for char in text):
                version_match = re.search(r'(\d+\.\d+\.\d+)', text)
                if version_match:
                    potential_version = version_match.group(1)
                    if potential_version != "2.1.5":
                        fw_version = potential_version
                        print(f"   Method 3 - Found version: '{fw_version}' in XML")
                        break

    # Step 9: Display results
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)

    if fw_version:
        print(f"✅ SUCCESS!")
        print(f"")
        print(f"🔧 Firmware Version: {fw_version}")
        print(f"📶 RSSI: {rssi}")
        print(f"📱 App Version: 2.1.5")
        print(f"")
        print("="*60)
    else:
        print(f"❌ FAILED")
        print(f"")
        print(f"Could not extract firmware version")
        print(f"Check screenshots and fw_extraction_page_source.xml for details")
        print(f"")
        print("="*60)

    # Assert we got a version
    assert fw_version, "Firmware version extraction failed"

    print(f"\n✅ Test completed successfully!")
    print(f"   Firmware Version: {fw_version}")
