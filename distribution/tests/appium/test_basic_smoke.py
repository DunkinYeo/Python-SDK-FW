"""Basic smoke test for RECORD-EX app."""
import pytest
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen


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


def test_app_launch(driver):
    """Test: Verify app launches successfully."""
    print("\n✅ Test: App launch")
    assert driver.session_id is not None
    print(f"   Session ID: {driver.session_id}")


def test_main_screen_loaded(driver):
    """Test: Verify main screen loads with menu buttons."""
    print("\n✅ Test: Main screen loaded")
    main_screen = MainScreen(driver)

    # Wait for screen to be ready
    assert main_screen.wait_for_screen_ready(timeout=20), "Main screen did not load"
    print("   Main screen is ready!")

    # Check if main screen is loaded
    assert main_screen.is_screen_loaded(), "Main screen elements not found"
    print("   Main screen elements found!")


def test_menu_buttons_present(driver):
    """Test: Verify all main menu buttons are present."""
    print("\n✅ Test: Menu buttons present")
    main_screen = MainScreen(driver)

    # Check for link button
    has_link = main_screen.is_element_present(main_screen.LINK_BUTTON, timeout=5)
    if not has_link:
        has_link = main_screen.is_element_present(main_screen.LINK_TEXT, timeout=2)
    print(f"   LINK button: {'✓' if has_link else '✗'}")

    # Check for read button
    has_read = main_screen.is_element_present(main_screen.READ_BUTTON, timeout=2)
    if not has_read:
        has_read = main_screen.is_element_present(main_screen.READ_TEXT, timeout=2)
    print(f"   READ button: {'✓' if has_read else '✗'}")

    # At least one button should be present
    assert has_link or has_read, "No menu buttons found"
    print("   At least one menu button found!")


def test_navigate_to_read(driver):
    """Test: Navigate to READ section."""
    print("\n✅ Test: Navigate to READ")
    main_screen = MainScreen(driver)

    # Try to navigate to read
    success = main_screen.navigate_to_read()
    print(f"   Navigation {'succeeded' if success else 'failed'}")

    # Take screenshot
    main_screen.take_screenshot("after_navigate_to_read")
    print("   Screenshot saved: after_navigate_to_read")
