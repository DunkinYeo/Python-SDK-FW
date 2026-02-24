"""Simple test to check app state after launch."""
import pytest
import time
from tests.appium.driver import get_driver
from appium.webdriver.common.appiumby import AppiumBy


def test_check_app_state_after_launch():
    """Check what's on screen after app launches."""
    print("\n🚀 Starting driver...")
    driver = get_driver()

    try:
        print("✅ Driver started")
        print(f"📱 Session ID: {driver.session_id}")

        # Wait a bit for app to load
        print("\n⏳ Waiting 10 seconds for app to fully load...")
        time.sleep(10)

        # Take screenshot
        driver.save_screenshot('app_state_after_launch.png')
        print("📸 Screenshot: app_state_after_launch.png")

        # Get current activity
        try:
            activity = driver.current_activity
            print(f"\n📱 Current activity: {activity}")
        except:
            print("⚠️  Could not get current activity")

        # Get all visible text elements
        print("\n📝 Looking for all text elements...")
        try:
            all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
            print(f"Found {len(all_texts)} elements with text:")

            for i, elem in enumerate(all_texts[:30]):
                try:
                    text = elem.text
                    if text:
                        print(f"   {i+1:3}. {text}")
                except:
                    pass
        except Exception as e:
            print(f"Error finding text elements: {e}")

        # Save page source
        page_source = driver.page_source
        with open('app_state_page_source.xml', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("\n📄 Page source saved: app_state_page_source.xml")

        # Look for specific elements
        print("\n🔍 Looking for specific elements...")

        elements_to_find = [
            "Link", "Read", "WriteSet", "WriteGet", "Notify",
            "ALLOW", "Allow", "허용", "DENY", "Deny", "거부",
            "OK", "확인", "Cancel", "취소"
        ]

        for elem_text in elements_to_find:
            try:
                elem = driver.find_element(AppiumBy.XPATH, f"//*[@text='{elem_text}']")
                print(f"   ✅ Found: {elem_text}")
            except:
                pass

        print("\n✅ Test completed - check screenshots and page source")

    finally:
        print("\n🛑 Closing driver...")
        try:
            driver.quit()
        except:
            pass
