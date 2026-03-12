"""Regression tests for SDK Sample app Read screen."""
import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
import re
from packaging import version


def get_supported_sampling_rates(fw_version_str):
    """Determine supported sampling rates based on firmware version."""
    try:
        parts = fw_version_str.split('.')
        if len(parts) == 3:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            fw_ver = version.parse(f"{major}.{minor}.{patch}")

            if fw_ver >= version.parse("2.4.6"):
                return [128, 256]
            elif fw_ver >= version.parse("2.3.5"):
                return [128]
            elif version.parse("2.2.0") <= fw_ver < version.parse("2.3.0"):
                return [256]
    except Exception:
        pass
    return [128, 256]


class TestReadScreen:
    """Regression tests for Read screen — 7 characteristics + sampling rate info."""

    def test_read_battery(self, connected_driver):
        """Test reading battery level."""
        print("\n" + "="*60)
        print("🔋 TEST: Battery Level")
        print("="*60)

        driver = connected_driver

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        # Battery BLE service loads slower than DevInfo — poll up to 30s
        print("\n🔋 Waiting for BATTERY button (up to 30s)...")
        battery_button = None
        for _wait in range(30):
            try:
                battery_button = driver.find_element(AppiumBy.XPATH, "//*[@text='BATTERY']")
                print(f"✅ BATTERY button found after {_wait}s")
                break
            except Exception:
                time.sleep(1)
        if battery_button is None:
            raise Exception("BATTERY button not found after 30 seconds")
        battery_button.click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_battery.png')

        battery_value = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Battery']/following-sibling::android.widget.TextView[1]"
        )
        battery_text = battery_value.text
        print(f"\n✅ Battery Level: {battery_text}")
        assert battery_text, "Battery value is empty"
        assert any(c.isdigit() for c in battery_text), f"Battery value '{battery_text}' has no digits"
        print("✅ Test PASSED")

    def test_read_model_number(self, connected_driver):
        """Test reading model number."""
        print("\n" + "="*60)
        print("📱 TEST: Model Number")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        print("\n📱 Clicking MODEL NUMBER button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='MODEL NUMBER']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_model_number.png')

        model_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Model Number']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Model Number: {model_text}")
        assert model_text, "Model number is empty"
        print("✅ Test PASSED")

    def test_read_serial_number(self, connected_driver):
        """Test reading serial number."""
        print("\n" + "="*60)
        print("🔢 TEST: Serial Number")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        print("\n🔢 Clicking SERIAL NUMBER button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='SERIAL NUMBER']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_serial_number.png')

        import os
        serial_number = os.getenv("BLE_DEVICE_SERIAL", "")
        serial_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Serial Number']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Serial Number: {serial_text}")
        assert serial_text, "Serial number is empty"
        assert serial_number in serial_text, f"Expected serial {serial_number}, got {serial_text}"
        print("✅ Test PASSED")

    def test_read_firmware_version(self, connected_driver):
        """Test reading firmware version."""
        print("\n" + "="*60)
        print("🔧 TEST: Firmware Version")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        print("\n🔧 Clicking FIRMWARE VERSION button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_firmware_version.png')

        fw_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Firmware Version: {fw_text}")
        assert fw_text, "Firmware version is empty"
        assert re.search(r'\d+\.\d+\.\d+', fw_text), f"Firmware version '{fw_text}' not in expected format"
        print("✅ Test PASSED")

    def test_read_hardware_version(self, connected_driver):
        """Test reading hardware version."""
        print("\n" + "="*60)
        print("⚙️  TEST: Hardware Version")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        # Hardware Version is on first screen — no scroll needed
        print("\n⚙️  Clicking HARDWARE VERSION button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='HARDWARE VERSION']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_hardware_version.png')

        hw_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Hardware Version']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Hardware Version: {hw_text}")
        assert hw_text, "Hardware version is empty"
        print("✅ Test PASSED")

    def test_read_software_version(self, connected_driver):
        """Test reading software version."""
        print("\n" + "="*60)
        print("💿 TEST: Software Version")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        # Software Version is below the fold — scroll down
        print("\n📜 Scrolling down to find Software Version...")
        driver.execute_script('mobile: scrollGesture', {
            'left': 100, 'top': 800, 'width': 500, 'height': 1000,
            'direction': 'down', 'percent': 0.75
        })
        time.sleep(1)

        print("\n💿 Clicking SOFTWARE VERSION button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='SOFTWARE VERSION']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_software_version.png')

        sw_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Software Version']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Software Version: {sw_text}")
        assert sw_text, "Software version is empty"
        print("✅ Test PASSED")

    def test_read_manufacture_name(self, connected_driver):
        """Test reading manufacture name."""
        print("\n" + "="*60)
        print("🏭 TEST: Manufacture Name")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        # Manufacture Name is below the fold — scroll down
        print("\n📜 Scrolling down to find Manufacture Name...")
        driver.execute_script('mobile: scrollGesture', {
            'left': 100, 'top': 800, 'width': 500, 'height': 1000,
            'direction': 'down', 'percent': 0.75
        })
        time.sleep(1)

        print("\n🏭 Clicking MANUFACTURE NAME button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='MANUFACTURE NAME']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_manufacture_name.png')

        mfr_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Manufacture Name']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Manufacture Name: {mfr_text}")
        assert mfr_text, "Manufacture name is empty"
        print("✅ Test PASSED")

    def test_firmware_version_and_sampling_rates(self, connected_driver):
        """Test firmware version and display supported sampling rates."""
        print("\n" + "="*60)
        print("🔧 TEST: Firmware Version & Supported Sampling Rates")
        print("="*60)

        driver = connected_driver

        print("\n📖 Navigating to Read screen...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='Read']").click()
        time.sleep(3)

        print("\n🔧 Clicking FIRMWARE VERSION button...")
        driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']").click()

        print("⏳ Waiting for device response...")
        time.sleep(5)
        driver.save_screenshot('test_fw_and_sampling_rates.png')

        fw_text = driver.find_element(
            AppiumBy.XPATH,
            "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
        ).text
        print(f"\n✅ Firmware Version: {fw_text}")
        assert fw_text, "Firmware version is empty"

        version_match = re.search(r'(\d+\.\d+\.\d+)', fw_text)
        assert version_match, f"Firmware version '{fw_text}' is not in expected format"

        fw_version = version_match.group(1)
        supported_rates = get_supported_sampling_rates(fw_version)

        print("\n" + "="*60)
        print("📊 SAMPLING RATE SUPPORT")
        print("="*60)
        print(f"Firmware Version : {fw_version}")
        print(f"Supported Rates  : {', '.join(map(str, supported_rates))} Hz")
        for rate in [128, 256]:
            status = "✅" if rate in supported_rates else "❌"
            print(f"{status} {rate} Hz")
        print("="*60)

        assert len(supported_rates) > 0, "No supported sampling rates found"
        print("\n✅ Test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
