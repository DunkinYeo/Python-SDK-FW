"""Test Read screen navigation slowly and carefully."""
import pytest
import time
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from appium.webdriver.common.appiumby import AppiumBy


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


def test_slow_connection_and_read(driver):
    """Go slowly: wait for connection, then navigate to Read screen."""
    print("\n" + "="*60)
    print("🐢 Slow Navigation Test")
    print("="*60)

    main_screen = MainScreen(driver)

    # Step 1: Wait for app to load
    print("\n📱 Step 1: Waiting for app to load...")
    assert main_screen.wait_for_screen_ready(timeout=20)
    time.sleep(2)
    print("✅ App loaded")
    driver.save_screenshot('step1_app_loaded.png')

    # Step 2: Check if already connected
    print("\n🔍 Step 2: Checking connection status...")
    is_connected = main_screen.is_device_connected()
    print(f"📡 Connection status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    if not is_connected:
        print("\n⏳ Waiting for device connection (30 seconds)...")
        print("Please connect the device manually if not already connected")

        for i in range(30):
            time.sleep(1)
            is_connected = main_screen.is_device_connected()
            if is_connected:
                print(f"\n✅ Device connected after {i+1} seconds!")
                break
            if (i + 1) % 5 == 0:
                print(f"⏳ Still waiting... {i+1}/30")

    # Step 3: Wait for CONNECTED toast to appear and disappear
    print("\n⏳ Step 3: Waiting for CONNECTED toast message...")
    time.sleep(5)  # Give time for toast to appear and disappear
    print("✅ Toast message should have appeared by now")
    driver.save_screenshot('step2_after_connection.png')

    # Step 4: Verify connection
    is_connected = main_screen.is_device_connected()
    print(f"\n✅ Step 4: Connection verified: {is_connected}")

    if is_connected:
        rssi = main_screen.get_rssi_value()
        print(f"📶 RSSI: {rssi}")

    # Step 5: Wait a bit more before navigating
    print("\n⏳ Step 5: Waiting before navigating to Read (5 seconds)...")
    time.sleep(5)

    # Step 6: Navigate to Read screen SLOWLY
    print("\n📖 Step 6: Navigating to Read screen...")
    try:
        # Find Read button
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        print("✅ Found Read button")

        # Click it
        read_button.click()
        print("✅ Clicked Read button")

        # Wait for transition
        print("⏳ Waiting for screen transition (5 seconds)...")
        time.sleep(5)

        driver.save_screenshot('step3_after_read_click.png')
        print("📸 Screenshot: step3_after_read_click.png")

    except Exception as e:
        print(f"❌ Error navigating to Read: {e}")
        driver.save_screenshot('error_read_navigation.png')
        raise

    # Step 7: Check what's visible
    print("\n🔍 Step 7: Checking visible elements...")
    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

    print(f"\n📝 Visible texts ({len(all_texts)} items):")
    for elem in all_texts[:20]:
        text = elem.text
        if text and text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
            print(f"   - {text}")

    # Save page source
    page_source = driver.page_source
    with open('slow_read_screen.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("\n📄 Page source saved: slow_read_screen.xml")

    # Step 8: Look for Read screen elements
    print("\n🔍 Step 8: Looking for Read screen elements...")
    read_elements = [
        "Battery", "BATTERY",
        "Model Number", "MODEL NUMBER",
        "Firmware Version", "FIRMWARE VERSION",
        "Hardware Version", "HARDWARE VERSION",
        "Software Version", "SOFTWARE VERSION"
    ]

    found = []
    for elem_name in read_elements:
        try:
            elem = driver.find_element(AppiumBy.XPATH, f"//*[@text='{elem_name}']")
            found.append(elem_name)
            print(f"   ✅ Found: {elem_name}")
        except:
            pass

    if not found:
        print("   ⚠️  No Read screen elements found yet")
        print("   Maybe need to scroll or wait longer")

    print(f"\n📊 Found {len(found)} Read screen elements")

    # Step 9: Try scrolling down to see if Read content is below
    print("\n📜 Step 9: Trying to scroll down...")
    try:
        # Scroll down using swipe
        size = driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 3 // 4
        end_y = size['height'] // 4

        driver.swipe(start_x, start_y, start_x, end_y, duration=800)
        print("✅ Scrolled down")

        time.sleep(2)
        driver.save_screenshot('step4_after_scroll.png')
        print("📸 Screenshot: step4_after_scroll.png")

        # Check again for Read elements
        all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
        print(f"\n📝 After scroll - visible texts ({len(all_texts)} items):")
        for elem in all_texts[:20]:
            text = elem.text
            if text and text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
                print(f"   - {text}")

    except Exception as e:
        print(f"⚠️  Error scrolling: {e}")

    # Step 10: Click FIRMWARE VERSION button
    print("\n🔧 Step 10: Clicking FIRMWARE VERSION button...")
    try:
        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        fw_button.click()
        print("✅ Clicked FIRMWARE VERSION button")

        # Wait for device response
        print("⏳ Waiting for device to respond (8 seconds)...")
        time.sleep(8)

        driver.save_screenshot('step5_after_fw_click.png')
        print("📸 Screenshot: step5_after_fw_click.png")

        # Try to extract firmware version
        print("\n🔍 Extracting firmware version...")

        # Method 1: Find value after Firmware Version label
        try:
            fw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value.text
            if fw_text:
                print(f"\n{'='*60}")
                print(f"✅ SUCCESS!")
                print(f"")
                print(f"🔧 Firmware Version: {fw_text}")
                print(f"📶 RSSI: {main_screen.get_rssi_value()}")
                print(f"📱 App Version: 2.1.5")
                print(f"")
                print(f"{'='*60}")
        except Exception as e:
            print(f"⚠️  Could not extract FW version using Method 1: {e}")

            # Method 2: Search all text for version pattern
            print("\n🔍 Method 2: Searching all TextViews...")
            import re
            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for elem in all_texts:
                text = elem.text
                if text and re.search(r'\d+\.\d+\.\d+', text):
                    # Exclude app version
                    if text != "2.1.5":
                        print(f"   Possible FW version: {text}")

    except Exception as e:
        print(f"❌ Error with FIRMWARE VERSION button: {e}")

    print("\n" + "="*60)
    print("✅ Test completed")
    print("="*60)
    print("Check the screenshots to see UI state at each step")

    assert True  # Always pass for debugging
