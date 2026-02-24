"""Explore WriteSet, WriteGet, and Notify screens to identify all functions."""
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.utils.permission_handler import handle_permission_dialogs
from appium.webdriver.common.appiumby import AppiumBy
import time


def explore_screen(driver, screen_name):
    """Explore a specific screen and print all elements."""
    print("\n" + "="*60)
    print(f"📱 EXPLORING: {screen_name} SCREEN")
    print("="*60)

    # Click the screen button
    try:
        screen_button = driver.find_element(AppiumBy.XPATH, f"//*[@text='{screen_name}']")
        screen_button.click()
        print(f"✅ Navigated to {screen_name} screen")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Failed to navigate to {screen_name}: {e}")
        return

    # Take screenshot
    driver.save_screenshot(f'explore_{screen_name.lower()}.png')

    # Get all text elements
    print("\n📝 Text elements on screen:")
    print("-" * 60)

    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

    # Filter out navigation buttons
    nav_buttons = ['Link', 'Read', 'WriteSet', 'WriteGet', 'Notify']

    for i, elem in enumerate(all_texts):
        text = elem.text
        if text and text not in nav_buttons:
            print(f"{i+1:3}. {text}")

    print("-" * 60)
    print(f"Total elements: {len([e for e in all_texts if e.text and e.text not in nav_buttons])}")

    # Get all buttons
    print("\n🔘 Buttons on screen:")
    print("-" * 60)

    all_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
    for i, btn in enumerate(all_buttons):
        text = btn.text
        if text and text not in nav_buttons:
            print(f"{i+1:3}. {text}")

    # Get all edit text fields
    print("\n📝 Input fields on screen:")
    print("-" * 60)

    all_inputs = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
    for i, inp in enumerate(all_inputs):
        text = inp.text
        try:
            content_desc = inp.get_attribute("content-desc") or ""
        except:
            content_desc = ""
        print(f"{i+1:3}. Text: '{text}', Content-desc: '{content_desc}'")

    if not all_inputs:
        print("   (No input fields found)")


def main():
    print("\n" + "="*60)
    print("🚀 SCREEN EXPLORATION TOOL")
    print("="*60)

    driver = get_driver()

    try:
        # Handle permissions
        print("\n🔐 Handling permissions...")
        handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)

        # Wait for app to load
        print("\n📱 Waiting for app to load...")
        time.sleep(5)

        main_screen = MainScreen(driver)

        # Connect to device first
        print("\n🔗 Going to Link screen...")
        main_screen.navigate_to_link()
        time.sleep(2)

        rssi = main_screen.get_rssi_value()
        print(f"Current RSSI: {rssi}")

        if rssi == "0" or int(rssi) == 0:
            print("\n🔌 Connecting to device...")
            main_screen.enter_serial_number("610031")
            main_screen.click_connect()

            # Wait for connection
            for i in range(30):
                time.sleep(1)
                rssi = main_screen.get_rssi_value()
                if rssi != "0" and int(rssi) != 0:
                    print(f"✅ Connected! RSSI: {rssi}")
                    break

            time.sleep(3)

        # Hide keyboard
        try:
            driver.hide_keyboard()
        except:
            pass

        # Explore each screen
        explore_screen(driver, "WriteSet")

        time.sleep(2)
        explore_screen(driver, "WriteGet")

        time.sleep(2)
        explore_screen(driver, "Notify")

        print("\n" + "="*60)
        print("✅ EXPLORATION COMPLETE")
        print("="*60)
        print("\nScreenshots saved:")
        print("  - explore_writeset.png")
        print("  - explore_writeget.png")
        print("  - explore_notify.png")

    finally:
        print("\n🛑 Closing driver...")
        driver.quit()


if __name__ == "__main__":
    main()
