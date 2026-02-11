"""Comprehensive regression tests for SDK Sample app."""
import pytest
import time
import os
from dotenv import load_dotenv
from tests.appium.driver import get_driver
from tests.appium.pages.main_screen import MainScreen
from tests.appium.utils.permission_handler import handle_permission_dialogs
from appium.webdriver.common.appiumby import AppiumBy
import re
from packaging import version

# Load environment variables
load_dotenv()

# Get serial number from environment variable
SERIAL_NUMBER = os.getenv("BLE_DEVICE_SERIAL")
if not SERIAL_NUMBER:
    raise ValueError(
        "BLE_DEVICE_SERIAL not found in environment variables!\n"
        "Please set it in .env file:\n"
        "BLE_DEVICE_SERIAL=YOUR_SERIAL_NUMBER"
    )


def get_supported_sampling_rates(fw_version_str):
    """
    Determine supported sampling rates based on firmware version.

    Args:
        fw_version_str: Firmware version string (e.g., "2.04.006")

    Returns:
        list: List of supported sampling rates
    """
    try:
        # Parse version string (e.g., "2.04.006" -> "2.4.6")
        parts = fw_version_str.split('.')
        if len(parts) == 3:
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])

            # Convert to comparable version
            fw_ver = version.parse(f"{major}.{minor}.{patch}")

            # Version rules:
            # 2.4.6+: 128/256 both supported
            # 2.3.5: 128 only
            # 2.2.x (2.2.3, 2.2.4, 2.2.5, 2.2.6, etc): 256 only

            if fw_ver >= version.parse("2.4.6"):
                return [128, 256]
            elif fw_ver >= version.parse("2.3.5"):
                return [128]
            elif fw_ver >= version.parse("2.2.0") and fw_ver < version.parse("2.3.0"):
                return [256]
            else:
                # Unknown version - assume both
                return [128, 256]
    except:
        # If parsing fails, assume both are supported
        return [128, 256]


@pytest.fixture(scope="module")
def connected_driver():
    """Setup: Launch app, handle permissions, and connect to device."""
    print("\n" + "="*60)
    print("🚀 SETUP: Connecting to device...")
    print("="*60)

    driver = get_driver()

    # Step 1: Handle permissions
    print("\n🔐 Handling permissions...")
    handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)

    # Step 2: Wait for app to load
    print("\n📱 Waiting for app to load...")
    time.sleep(5)

    main_screen = MainScreen(driver)

    # Step 3: Go to Link screen
    print("\n🔗 Going to Link screen...")
    main_screen.navigate_to_link()
    time.sleep(2)

    # Step 4: Check RSSI and connect if needed
    print("\n📡 Checking connection status...")
    rssi = main_screen.get_rssi_value()
    print(f"Current RSSI: {rssi}")

    if rssi == "0" or int(rssi) == 0:
        print(f"\n🔌 Connecting to device (Serial: {SERIAL_NUMBER})...")

        # Enter serial number
        main_screen.enter_serial_number(SERIAL_NUMBER)

        # Click connect
        main_screen.click_connect()

        # Wait for connection
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

        # Wait for toast to disappear
        time.sleep(3)
    else:
        print(f"✅ Already connected (RSSI: {rssi})")

    # Verify connection
    rssi = main_screen.get_rssi_value()
    if rssi == "0" or int(rssi) == 0:
        driver.quit()
        pytest.fail(f"Device not connected! RSSI: {rssi}")

    print(f"\n✅ Setup complete - Device connected (RSSI: {rssi})")
    print("="*60)

    yield driver

    # Teardown
    print("\n🛑 Closing driver...")
    driver.quit()


class TestReadScreen:
    """Regression tests for Read screen functions."""

    def test_read_battery(self, connected_driver):
        """Test reading battery level."""
        print("\n" + "="*60)
        print("🔋 TEST: Battery Level")
        print("="*60)

        driver = connected_driver

        # Hide keyboard if present
        try:
            driver.hide_keyboard()
        except:
            pass

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Click BATTERY button
        print("\n🔋 Clicking BATTERY button...")
        battery_button = driver.find_element(AppiumBy.XPATH, "//*[@text='BATTERY']")
        battery_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_battery.png')

        # Extract battery value
        try:
            battery_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Battery']/following-sibling::android.widget.TextView[1]"
            )
            battery_text = battery_value.text

            print(f"\n✅ Battery Level: {battery_text}")

            # Verify it's a valid battery reading (number or percentage)
            assert battery_text, "Battery value is empty"
            assert any(c.isdigit() for c in battery_text), f"Battery value '{battery_text}' contains no digits"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_read_model_number(self, connected_driver):
        """Test reading model number."""
        print("\n" + "="*60)
        print("📱 TEST: Model Number")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Click MODEL NUMBER button
        print("\n📱 Clicking MODEL NUMBER button...")
        model_button = driver.find_element(AppiumBy.XPATH, "//*[@text='MODEL NUMBER']")
        model_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_model_number.png')

        # Extract model number
        try:
            model_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Model Number']/following-sibling::android.widget.TextView[1]"
            )
            model_text = model_value.text

            print(f"\n✅ Model Number: {model_text}")

            assert model_text, "Model number is empty"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_read_serial_number(self, connected_driver):
        """Test reading serial number."""
        print("\n" + "="*60)
        print("🔢 TEST: Serial Number")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Click SERIAL NUMBER button
        print("\n🔢 Clicking SERIAL NUMBER button...")
        serial_button = driver.find_element(AppiumBy.XPATH, "//*[@text='SERIAL NUMBER']")
        serial_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_serial_number.png')

        # Extract serial number
        try:
            serial_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Serial Number']/following-sibling::android.widget.TextView[1]"
            )
            serial_text = serial_value.text

            print(f"\n✅ Serial Number: {serial_text}")

            assert serial_text, "Serial number is empty"
            # Verify it matches our hardcoded serial
            assert SERIAL_NUMBER in serial_text, f"Expected serial {SERIAL_NUMBER}, got {serial_text}"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_read_firmware_version(self, connected_driver):
        """Test reading firmware version."""
        print("\n" + "="*60)
        print("🔧 TEST: Firmware Version")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Click FIRMWARE VERSION button
        print("\n🔧 Clicking FIRMWARE VERSION button...")
        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        fw_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_firmware_version.png')

        # Extract firmware version
        try:
            fw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value.text

            print(f"\n✅ Firmware Version: {fw_text}")

            assert fw_text, "Firmware version is empty"
            # Verify it's a valid version format (e.g., 2.04.006)
            version_match = re.search(r'\d+\.\d+\.\d+', fw_text)
            assert version_match, f"Firmware version '{fw_text}' is not in expected format"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_read_hardware_version(self, connected_driver):
        """Test reading hardware version."""
        print("\n" + "="*60)
        print("⚙️  TEST: Hardware Version")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Scroll down to see Hardware Version (might be below the fold)
        print("\n📜 Scrolling to find Hardware Version...")
        try:
            # Try to find the button first
            hw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='HARDWARE VERSION']")
        except:
            # If not visible, scroll down
            driver.execute_script('mobile: scrollGesture', {
                'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                'direction': 'down',
                'percent': 3.0
            })
            time.sleep(1)

        # Click HARDWARE VERSION button
        print("\n⚙️  Clicking HARDWARE VERSION button...")
        hw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='HARDWARE VERSION']")
        hw_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_hardware_version.png')

        # Extract hardware version
        try:
            hw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Hardware Version']/following-sibling::android.widget.TextView[1]"
            )
            hw_text = hw_value.text

            print(f"\n✅ Hardware Version: {hw_text}")

            assert hw_text, "Hardware version is empty"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_read_software_version(self, connected_driver):
        """Test reading software version."""
        print("\n" + "="*60)
        print("💿 TEST: Software Version")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Scroll down to see Software Version
        print("\n📜 Scrolling to find Software Version...")
        try:
            sw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='SOFTWARE VERSION']")
        except:
            driver.execute_script('mobile: scrollGesture', {
                'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                'direction': 'down',
                'percent': 3.0
            })
            time.sleep(1)

        # Click SOFTWARE VERSION button
        print("\n💿 Clicking SOFTWARE VERSION button...")
        sw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='SOFTWARE VERSION']")
        sw_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_software_version.png')

        # Extract software version
        try:
            sw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Software Version']/following-sibling::android.widget.TextView[1]"
            )
            sw_text = sw_value.text

            print(f"\n✅ Software Version: {sw_text}")

            assert sw_text, "Software version is empty"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_firmware_version_and_sampling_rates(self, connected_driver):
        """Test reading firmware version and display supported sampling rates."""
        print("\n" + "="*60)
        print("🔧 TEST: Firmware Version & Supported Sampling Rates")
        print("="*60)

        driver = connected_driver

        # Navigate to Read screen
        print("\n📖 Navigating to Read screen...")
        read_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Read']")
        read_button.click()
        time.sleep(3)

        # Click FIRMWARE VERSION button
        print("\n🔧 Clicking FIRMWARE VERSION button...")
        fw_button = driver.find_element(AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
        fw_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_fw_and_sampling_rates.png')

        # Extract firmware version
        try:
            fw_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
            )
            fw_text = fw_value.text

            print(f"\n✅ Firmware Version: {fw_text}")

            assert fw_text, "Firmware version is empty"

            # Parse version
            version_match = re.search(r'(\d+\.\d+\.\d+)', fw_text)
            assert version_match, f"Firmware version '{fw_text}' is not in expected format"

            fw_version = version_match.group(1)

            # Get supported sampling rates
            supported_rates = get_supported_sampling_rates(fw_version)

            print("\n" + "="*60)
            print("📊 SAMPLING RATE SUPPORT INFORMATION")
            print("="*60)
            print(f"Firmware Version: {fw_version}")
            print(f"Supported Sampling Rates: {', '.join(map(str, supported_rates))} Hz")

            # Display detailed info
            if 128 in supported_rates and 256 in supported_rates:
                print("✅ 128 Hz: Supported")
                print("✅ 256 Hz: Supported")
                print("ℹ️  This firmware supports both sampling rates")
            elif 128 in supported_rates:
                print("✅ 128 Hz: Supported")
                print("❌ 256 Hz: Not supported")
                print("ℹ️  This firmware only supports 128 Hz")
            elif 256 in supported_rates:
                print("❌ 128 Hz: Not supported")
                print("✅ 256 Hz: Supported")
                print("ℹ️  This firmware only supports 256 Hz")

            print("="*60)

            assert len(supported_rates) > 0, "No supported sampling rates found"

            print("\n✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise


class TestWriteGetScreen:
    """Regression tests for WriteGet screen functions."""

    def test_writeget_memory_packet_number(self, connected_driver):
        """Test reading memory packet number."""
        print("\n" + "="*60)
        print("📦 TEST: Memory Packet Number")
        print("="*60)

        driver = connected_driver

        # Hide keyboard if present
        try:
            driver.hide_keyboard()
        except:
            pass

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Click MEMORY PACKET NUMBER button
        print("\n📦 Clicking MEMORY PACKET NUMBER button...")
        packet_button = driver.find_element(AppiumBy.XPATH, "//*[@text='MEMORY PACKET NUMBER']")
        packet_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_memory_packet_number.png')

        # Extract packet number
        try:
            packet_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Memory Packet Number']/following-sibling::android.widget.TextView[1]"
            )
            packet_text = packet_value.text

            print(f"\n✅ Memory Packet Number: {packet_text}")

            assert packet_text, "Memory packet number is empty"
            assert any(c.isdigit() for c in packet_text), f"Packet number '{packet_text}' contains no digits"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_writeget_measurement_duration(self, connected_driver):
        """Test reading measurement duration from WriteGet."""
        print("\n" + "="*60)
        print("⏱️  TEST: WriteGet - Measurement Duration")
        print("="*60)

        driver = connected_driver

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Click MEASUREMENT DURATION button
        print("\n⏱️  Clicking MEASUREMENT DURATION button...")
        duration_button = driver.find_element(AppiumBy.XPATH, "//*[@text='MEASUREMENT DURATION']")
        duration_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_writeget_measurement_duration.png')

        # Extract duration
        try:
            duration_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Measurement Duration']/following-sibling::android.widget.TextView[1]"
            )
            duration_text = duration_value.text

            print(f"\n✅ Measurement Duration: {duration_text}")

            assert duration_text, "Measurement duration is empty"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_writeget_symptom_duration(self, connected_driver):
        """Test reading symptom duration from WriteGet."""
        print("\n" + "="*60)
        print("🕐 TEST: WriteGet - Symptom Duration (Get)")
        print("="*60)

        driver = connected_driver

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Click SYMPTOM DURATION button
        print("\n🕐 Clicking SYMPTOM DURATION button...")
        symptom_button = driver.find_element(AppiumBy.XPATH, "//*[@text='SYMPTOM DURATION']")
        symptom_button.click()

        # Wait for response
        print("⏳ Waiting for device response...")
        time.sleep(5)

        driver.save_screenshot('test_writeget_symptom_duration.png')

        # Extract symptom duration
        try:
            symptom_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Symptom Duration']/following-sibling::android.widget.TextView[1]"
            )
            symptom_text = symptom_value.text

            print(f"\n✅ Symptom Duration: {symptom_text}")

            assert symptom_text, "Symptom duration is empty"

            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            raise

    def test_writeget_memory_packet_write(self, connected_driver):
        """Test writing memory packet number via WriteGet."""
        print("\n" + "="*60)
        print("📦 TEST: WriteGet - Memory Packet Number (Write)")
        print("="*60)

        driver = connected_driver

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Scroll to find the input field and Write button
        print("\n📜 Looking for Write controls...")
        try:
            # Find the EditText for Memory Packet Number
            input_field = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Memory Packet Number']/../..//android.widget.EditText"
            )

            # Clear and enter a test value
            test_value = "100"
            print(f"\n✏️  Entering test value: {test_value}")
            input_field.clear()
            input_field.send_keys(test_value)

            # Hide keyboard
            try:
                driver.hide_keyboard()
            except:
                pass

            time.sleep(1)

            # Find and click WRITE button
            print("\n✍️  Clicking WRITE button...")
            write_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Memory Packet Number']/../..//*[@text='WRITE']"
            )
            write_button.click()

            # Wait for write operation
            print("⏳ Waiting for write operation...")
            time.sleep(5)

            driver.save_screenshot('test_writeget_memory_packet_write.png')

            # Verify write was successful by reading back
            print("\n🔄 Verifying write by reading back...")
            get_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='MEMORY PACKET NUMBER']"
            )
            get_button.click()
            time.sleep(5)

            # Check if the written value is reflected
            packet_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Memory Packet Number']/following-sibling::android.widget.TextView[1]"
            )
            read_value = packet_value.text

            print(f"\n✅ Written value: {test_value}")
            print(f"✅ Read back value: {read_value}")
            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            driver.save_screenshot('test_writeget_memory_packet_write_failed.png')
            raise

    def test_writeget_measurement_duration_write(self, connected_driver):
        """Test writing measurement duration via WriteGet."""
        print("\n" + "="*60)
        print("⏱️  TEST: WriteGet - Measurement Duration (Write)")
        print("="*60)

        driver = connected_driver

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        try:
            # Find the EditText for Measurement Duration
            input_field = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Measurement Duration']/../..//android.widget.EditText"
            )

            # Clear and enter a test value
            test_value = "60"
            print(f"\n✏️  Entering test value: {test_value}")
            input_field.clear()
            input_field.send_keys(test_value)

            # Hide keyboard
            try:
                driver.hide_keyboard()
            except:
                pass

            time.sleep(1)

            # Find and click WRITE button
            print("\n✍️  Clicking WRITE button...")
            write_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Measurement Duration']/../..//*[@text='WRITE']"
            )
            write_button.click()

            # Wait for write operation
            print("⏳ Waiting for write operation...")
            time.sleep(5)

            driver.save_screenshot('test_writeget_measurement_duration_write.png')

            # Verify write was successful by reading back
            print("\n🔄 Verifying write by reading back...")
            get_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='MEASUREMENT DURATION']"
            )
            get_button.click()
            time.sleep(5)

            # Check if the written value is reflected
            duration_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Measurement Duration']/following-sibling::android.widget.TextView[1]"
            )
            read_value = duration_value.text

            print(f"\n✅ Written value: {test_value}")
            print(f"✅ Read back value: {read_value}")
            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            driver.save_screenshot('test_writeget_measurement_duration_write_failed.png')
            raise

    def test_writeget_symptom_duration_write(self, connected_driver):
        """Test writing symptom duration via WriteGet."""
        print("\n" + "="*60)
        print("🕐 TEST: WriteGet - Symptom Duration (Write)")
        print("="*60)

        driver = connected_driver

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Scroll down to find Symptom Duration
        print("\n📜 Scrolling to find Symptom Duration...")
        try:
            input_field = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Symptom Duration']/../..//android.widget.EditText"
            )
        except:
            driver.execute_script('mobile: scrollGesture', {
                'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                'direction': 'down',
                'percent': 3.0
            })
            time.sleep(1)

        try:
            # Find the EditText for Symptom Duration
            input_field = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Symptom Duration']/../..//android.widget.EditText"
            )

            # Clear and enter a test value
            test_value = "30"
            print(f"\n✏️  Entering test value: {test_value}")
            input_field.clear()
            input_field.send_keys(test_value)

            # Hide keyboard
            try:
                driver.hide_keyboard()
            except:
                pass

            time.sleep(1)

            # Find and click WRITE button
            print("\n✍️  Clicking WRITE button...")
            write_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Symptom Duration']/../..//*[@text='WRITE']"
            )
            write_button.click()

            # Wait for write operation
            print("⏳ Waiting for write operation...")
            time.sleep(5)

            driver.save_screenshot('test_writeget_symptom_duration_write.png')

            # Verify write was successful by reading back
            print("\n🔄 Verifying write by reading back...")
            get_button = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='SYMPTOM DURATION']"
            )
            get_button.click()
            time.sleep(5)

            # Check if the written value is reflected
            symptom_value = driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='Symptom Duration']/following-sibling::android.widget.TextView[1]"
            )
            read_value = symptom_value.text

            print(f"\n✅ Written value: {test_value}")
            print(f"✅ Read back value: {read_value}")
            print("✅ Test PASSED")

        except Exception as e:
            print(f"❌ Test FAILED: {e}")
            driver.save_screenshot('test_writeget_symptom_duration_write_failed.png')
            raise


class TestNotifyScreen:
    """Regression tests for Notify screen."""

    def test_notify_screen_elements(self, connected_driver):
        """Test that all notification elements are present."""
        print("\n" + "="*60)
        print("🔔 TEST: Notify Screen Elements")
        print("="*60)

        driver = connected_driver

        # Hide keyboard if present
        try:
            driver.hide_keyboard()
        except:
            pass

        # Navigate to Notify screen
        print("\n📖 Navigating to Notify screen...")
        notify_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Notify']")
        notify_button.click()
        time.sleep(3)

        driver.save_screenshot('test_notify_screen.png')

        # Check for all expected elements
        expected_elements = ["ECG", "IMU", "ACC", "GYRO", "Memory", "Heart Rate", "Battery"]

        print("\n🔍 Checking for notification elements...")

        found_elements = []
        for element_name in expected_elements:
            try:
                element = driver.find_element(AppiumBy.XPATH, f"//*[@text='{element_name}']")
                print(f"✅ Found: {element_name}")
                found_elements.append(element_name)
            except:
                print(f"❌ Missing: {element_name}")

        print(f"\n📊 Result: {len(found_elements)}/{len(expected_elements)} elements found")

        assert len(found_elements) == len(expected_elements), \
            f"Missing elements: {set(expected_elements) - set(found_elements)}"

        print("✅ Test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
