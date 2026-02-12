"""Test to inspect UI structure of SDK Sample app."""
import pytest
from tests.appium.driver import get_driver
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


def test_inspect_main_screen(driver):
    """Inspect and print main screen UI elements."""
    print("\n🔍 Inspecting main screen...")

    # Wait for app to load
    time.sleep(5)

    # Get page source
    page_source = driver.page_source

    # Save to file for analysis
    with open('page_source.xml', 'w', encoding='utf-8') as f:
        f.write(page_source)

    print("\n📄 Page source saved to page_source.xml")

    # Try to find any text elements
    try:
        from appium.webdriver.common.appiumby import AppiumBy
        all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

        print(f"\n📝 Found {len(all_texts)} elements with text:")
        for i, elem in enumerate(all_texts[:20]):  # Print first 20
            try:
                text = elem.text
                if text:
                    print(f"   {i+1}. {text}")
            except:
                pass

    except Exception as e:
        print(f"Error finding text elements: {e}")

    # Try to get current activity
    try:
        activity = driver.current_activity
        print(f"\n📱 Current activity: {activity}")
    except Exception as e:
        print(f"Error getting activity: {e}")

    # Take screenshot
    driver.save_screenshot('main_screen.png')
    print("\n📸 Screenshot saved to main_screen.png")

    assert True  # Always pass, this is just for inspection
