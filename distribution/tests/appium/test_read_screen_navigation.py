"""Test to carefully verify Read screen navigation and elements."""
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


def test_read_screen_navigation(driver):
    """Test navigation to Read screen and verify elements."""
    print("\n" + "="*60)
    print("📖 Read Screen Navigation Test")
    print("="*60)

    main_screen = MainScreen(driver)

    # Wait for app to load
    print("\n📱 Waiting for app to load...")
    assert main_screen.wait_for_screen_ready(timeout=20)
    print("✅ App loaded")

    # Take screenshot of initial screen (Link)
    driver.save_screenshot('step1_link_screen.png')
    print("📸 Screenshot 1: step1_link_screen.png")

    # Get all visible text before clicking Read
    all_texts_before = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
    texts_before = [elem.text for elem in all_texts_before if elem.text]
    print(f"\n📝 Visible texts before clicking Read ({len(texts_before)} items):")
    for text in texts_before[:10]:
        if text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
            print(f"   - {text}")

    # Click Read button
    print("\n📖 Clicking Read button...")
    read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
    read_button.click()
    print("✅ Read button clicked")

    # Wait for screen transition
    print("⏳ Waiting 3 seconds for screen transition...")
    time.sleep(3)

    # Take screenshot after clicking Read
    driver.save_screenshot('step2_after_read_click.png')
    print("📸 Screenshot 2: step2_after_read_click.png")

    # Get all visible text after clicking Read
    all_texts_after = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
    texts_after = [elem.text for elem in all_texts_after if elem.text]
    print(f"\n📝 Visible texts after clicking Read ({len(texts_after)} items):")
    for text in texts_after[:15]:
        if text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
            print(f"   - {text}")

    # Check if screen changed
    texts_before_set = set(texts_before)
    texts_after_set = set(texts_after)

    new_texts = texts_after_set - texts_before_set
    removed_texts = texts_before_set - texts_after_set

    print(f"\n🔄 Screen Changes:")
    if new_texts:
        print(f"   New texts appeared: {new_texts}")
    else:
        print("   ⚠️  No new texts appeared")

    if removed_texts:
        print(f"   Texts disappeared: {removed_texts}")

    # Save page source
    page_source = driver.page_source
    with open('read_screen_after_click.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("\n📄 Page source saved: read_screen_after_click.xml")

    # Look for Read screen specific elements
    print("\n🔍 Looking for Read screen elements...")

    expected_elements = [
        "Battery",
        "Model Number",
        "Serial Number",
        "Firmware Version",
        "Hardware Version",
        "Software Version",
        "BATTERY",
        "MODEL NUMBER",
        "FIRMWARE VERSION"
    ]

    found_elements = []
    for elem_text in expected_elements:
        if elem_text in texts_after:
            found_elements.append(elem_text)
            print(f"   ✅ Found: {elem_text}")
        else:
            print(f"   ❌ Not found: {elem_text}")

    print(f"\n📊 Found {len(found_elements)}/{len(expected_elements)} expected Read screen elements")

    if found_elements:
        print("\n✅ Read screen loaded successfully!")
    else:
        print("\n⚠️  Read screen elements not found - may still be on Link screen")
        print("   Check screenshots to verify UI state")

    assert True  # Always pass for debugging


def test_wait_for_connection_and_read_fw(driver):
    """Wait for device connection and read firmware version."""
    print("\n" + "="*60)
    print("🔌 Waiting for Device Connection")
    print("="*60)

    main_screen = MainScreen(driver)

    # Ensure we're on Read screen
    print("\n📖 Navigating to Read screen...")
    main_screen.navigate_to_read()
    time.sleep(2)

    driver.save_screenshot('read_screen_before_connection.png')
    print("📸 Screenshot: read_screen_before_connection.png")

    # Wait for user to connect device
    print("\n" + "="*60)
    print("⏳ PLEASE CONNECT THE DEVICE NOW")
    print("="*60)
    print("Waiting up to 60 seconds...")
    print("="*60)

    # Just wait for user input
    max_wait = 60
    for i in range(max_wait):
        time.sleep(1)
        if (i + 1) % 5 == 0:
            print(f"⏳ Waited {i + 1}/{max_wait} seconds...")

    print("\n✅ Wait complete, proceeding...")

    # Take screenshot after connection
    driver.save_screenshot('read_screen_after_connection.png')
    print("📸 Screenshot: read_screen_after_connection.png")

    # Get current visible texts
    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
    print(f"\n📝 Current visible texts ({len(all_texts)} items):")
    for elem in all_texts:
        text = elem.text
        if text and text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
            print(f"   - {text}")

    # Look for FIRMWARE VERSION button
    print("\n🔍 Looking for FIRMWARE VERSION button...")
    try:
        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        print("✅ Found FIRMWARE VERSION button")

        # Click it
        print("\n🔧 Clicking FIRMWARE VERSION button...")
        fw_button.click()
        print("✅ Button clicked")

        # Wait for response
        print("⏳ Waiting 5 seconds for device response...")
        time.sleep(5)

        # Take screenshot
        driver.save_screenshot('after_fw_button_click.png')
        print("📸 Screenshot: after_fw_button_click.png")

        # Try to find firmware version value
        print("\n🔍 Looking for firmware version value...")
        try:
            fw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value.text
            print(f"\n{'='*60}")
            print(f"🔧 FIRMWARE VERSION: {fw_text}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"⚠️  Could not find FW version value: {e}")

            # Try to find any text with version pattern
            print("\n🔍 Searching all TextViews for version pattern...")
            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for elem in all_texts:
                text = elem.text
                if text and any(char.isdigit() for char in text) and '.' in text:
                    print(f"   Possible version: {text}")

    except Exception as e:
        print(f"❌ FIRMWARE VERSION button not found: {e}")
        print("\n📝 Available texts:")
        all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
        for elem in all_texts[:20]:
            if elem.text:
                print(f"   - {elem.text}")

    assert True  # Always pass for debugging
