"""Shared pytest fixtures for all test modules."""
import pytest
import time
import os
from dotenv import load_dotenv
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.utils.permission_handler import handle_permission_dialogs

load_dotenv()

SERIAL_NUMBER = os.getenv("BLE_DEVICE_SERIAL")
if not SERIAL_NUMBER:
    raise ValueError(
        "BLE_DEVICE_SERIAL not found in environment variables!\n"
        "Please set it in .env file:\n"
        "BLE_DEVICE_SERIAL=YOUR_SERIAL_NUMBER"
    )


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--target-packets",
        action="store",
        default=None,
        type=int,
        help="Target packet count for packet monitoring test (e.g., 3600)"
    )


@pytest.fixture
def target_packets(request):
    """Get target packet count from command line option."""
    return request.config.getoption("--target-packets")


@pytest.fixture(scope="module")
def connected_driver():
    """Setup: Launch app, handle permissions, and connect to BLE device."""
    print("\n" + "="*60)
    print("🚀 SETUP: Connecting to device...")
    print("="*60)

    driver = get_driver()

    print("\n🔐 Handling permissions...")
    handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)

    print("\n📱 Waiting for app to load...")
    time.sleep(5)

    main_screen = MainScreen(driver)

    print("\n🔗 Going to Link screen...")
    main_screen.navigate_to_link()
    time.sleep(2)

    print("\n📡 Checking connection status...")
    rssi = main_screen.get_rssi_value()
    print(f"Current RSSI: {rssi}")

    if rssi == "0" or int(rssi) == 0:
        print(f"\n🔌 Connecting to device (Serial: {SERIAL_NUMBER})...")
        main_screen.enter_serial_number(SERIAL_NUMBER)
        main_screen.click_connect()

        print("⏳ Waiting for connection...")
        connected = False
        for i in range(30):
            time.sleep(1)
            rssi = main_screen.get_rssi_value()
            if rssi != "0" and int(rssi) != 0:
                print(f"\n✅ CONNECTED! RSSI: {rssi}")
                connected = True
                break
            if (i + 1) % 5 == 0:
                print(f"⏳ Waiting... {i+1}/30s")

        if not connected:
            driver.quit()
            pytest.fail("Failed to connect to device")

        time.sleep(3)
    else:
        print(f"✅ Already connected (RSSI: {rssi})")

    rssi = main_screen.get_rssi_value()
    if rssi == "0" or int(rssi) == 0:
        driver.quit()
        pytest.fail(f"Device not connected! RSSI: {rssi}")

    print(f"\n✅ Setup complete - Device connected (RSSI: {rssi})")
    print("="*60)

    yield driver

    print("\n🛑 Closing driver...")
    driver.quit()
