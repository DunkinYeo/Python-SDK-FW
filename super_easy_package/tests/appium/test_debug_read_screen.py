"""Debug test to see what's actually on the Read screen when device is connected."""
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


def test_debug_read_screen_with_connection(driver):
    """Debug what's on Read screen when device is connected."""
    print("\n🔍 Debugging Read screen with connected device...")

    main_screen = MainScreen(driver)

    # Wait for app to load
    assert main_screen.wait_for_screen_ready(timeout=20)
    print("✅ App loaded")

    # Check connection status
    is_connected = main_screen.is_device_connected()
    print(f"\n📡 Connection status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")

    if is_connected:
        rssi = main_screen.get_rssi_value()
        print(f"📶 RSSI: {rssi}")

    # Navigate to Read screen
    print("\n📖 Navigating to Read screen...")
    main_screen.navigate_to_read()
    time.sleep(3)

    # Get page source
    page_source = driver.page_source
    with open('read_screen_connected.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("📄 Page source saved to: read_screen_connected.xml")

    # Find all text elements
    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

    print(f"\n📝 Found {len(all_texts)} elements with text:")
    print("-" * 60)

    for i, elem in enumerate(all_texts):
        try:
            text = elem.text
            if text and text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
                print(f"  {i+1:3}. {text}")
        except:
            pass

    print("-" * 60)

    # Find all buttons
    all_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
    print(f"\n🔘 Found {len(all_buttons)} buttons")

    # Find all clickable views
    clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
    print(f"👆 Found {len(clickable)} clickable elements")

    # Take screenshot
    driver.save_screenshot('read_screen_debug_connected.png')
    print("\n📸 Screenshot saved: read_screen_debug_connected.png")

    assert True  # Always pass, this is just for debugging
