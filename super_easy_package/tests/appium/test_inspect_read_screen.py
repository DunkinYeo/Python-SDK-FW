"""Test to inspect Read screen UI structure."""
import pytest
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
import time


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


def test_inspect_read_screen(driver):
    """Inspect Read screen UI elements."""
    print("\n🔍 Inspecting Read screen...")

    # Create main screen page object
    main_screen = MainScreen(driver)

    # Wait for app to load
    assert main_screen.wait_for_screen_ready(timeout=20)
    print("✅ Main screen loaded")

    # Navigate to Read section
    assert main_screen.navigate_to_read()
    print("✅ Navigated to Read section")

    # Wait a bit for screen to load
    time.sleep(3)

    # Get page source
    page_source = driver.page_source

    # Save to file
    with open('read_screen_source.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)

    print("\n📄 Page source saved to read_screen_source.xml")

    # Try to find any text elements
    try:
        from appium.webdriver.common.appiumby import AppiumBy
        all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

        print(f"\n📝 Found {len(all_texts)} elements with text:")
        for i, elem in enumerate(all_texts):
            try:
                text = elem.text
                if text and text not in ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']:
                    print(f"   {i+1}. {text}")
            except:
                pass

    except Exception as e:
        print(f"Error finding text elements: {e}")

    # Take screenshot
    driver.save_screenshot('read_screen.png')
    print("\n📸 Screenshot saved to read_screen.png")

    assert True  # Always pass, this is just for inspection
