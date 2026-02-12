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


class TestDataCollectionWorkflow:
    """Test complete data collection workflow: WriteSet Start/Pause/Restart → Notify → WriteSet Stop/Reset"""

    def test_data_collection_workflow(self, connected_driver, target_packets):
        """
        Complete data collection workflow test.

        Steps:
        1. WriteSet: Start → Start measurement
        2. WriteSet: Pause → Pause measurement
        3. WriteSet: Restart → Resume measurement
        4. Notify: Verify all data streams are active
        5. [Optional] Monitor ECG packet count until target reached
        6. WriteSet: Stop → Stop measurement
        7. WriteSet: Reset Device → Clean up

        Args:
            target_packets: Optional target packet count for long-term test
                           (e.g., 3600 for 1 hour, 86400 for 1 day)
        """
        print("\n" + "="*80)
        print("🔬 TEST: Complete Data Collection Workflow")
        print("="*80)

        driver = connected_driver

        # Wait for UI to stabilize after connection
        print("\n⏳ Waiting for UI to stabilize...")
        time.sleep(3)

        # Hide keyboard if present
        try:
            driver.hide_keyboard()
        except:
            pass

        # =================================================================
        # STEP 1: WriteSet - Start Measurement
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 1: WriteSet - Start Measurement")
        print("="*80)

        print("\n📖 Navigating to WriteSet screen...")
        writeset_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteSet']")
        writeset_button.click()
        time.sleep(3)

        print("\n▶️  Clicking START button...")
        start_button = driver.find_element(AppiumBy.XPATH, "//*[@text='START']")
        start_button.click()

        print("⏳ Waiting for measurement to start (10 seconds)...")
        time.sleep(10)

        driver.save_screenshot('step1_writeset_start.png')
        print("✅ STEP 1 Complete - Measurement Started")

        # =================================================================
        # STEP 2: WriteSet - Pause Measurement
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 2: WriteSet - Pause Measurement")
        print("="*80)

        print("\n⏸️  Clicking PAUSE button...")
        pause_button = driver.find_element(AppiumBy.XPATH, "//*[@text='PAUSE']")
        pause_button.click()

        print("⏳ Waiting for measurement to pause (5 seconds)...")
        time.sleep(5)

        driver.save_screenshot('step2_writeset_pause.png')
        print("✅ STEP 2 Complete - Measurement Paused")

        # =================================================================
        # STEP 3: WriteSet - Restart Measurement
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 3: WriteSet - Restart Measurement")
        print("="*80)

        print("\n🔄 Clicking RESTART button...")
        restart_button = driver.find_element(AppiumBy.XPATH, "//*[@text='RESTART']")
        restart_button.click()

        print("⏳ Waiting for measurement to restart (10 seconds)...")
        time.sleep(10)

        driver.save_screenshot('step3_writeset_restart.png')
        print("✅ STEP 3 Complete - Measurement Restarted")

        # =================================================================
        # STEP 4: Notify - Verify All Data Streams
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 4: Notify - Verify All Data Streams Active")
        print("="*80)

        print("\n📖 Navigating to Notify screen...")
        notify_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Notify']")
        notify_button.click()
        time.sleep(5)  # Wait longer for data to start flowing

        driver.save_screenshot('step4_notify_before_check.png')

        # Check for all expected notification elements
        # Note: Gyro excluded as it's not present in current UI
        expected_elements = ["ECG", "IMU", "ACC", "Memory", "Heart Rate", "Battery"]

        print("\n🔍 Checking for active data streams...")

        found_elements = []
        for element_name in expected_elements:
            try:
                element = driver.find_element(AppiumBy.XPATH, f"//*[@text='{element_name}']")
                print(f"✅ Found: {element_name}")
                found_elements.append(element_name)
            except:
                # Try scrolling down multiple times to find the element
                print(f"📜 Scrolling to find: {element_name}...")
                found = False
                for scroll_attempt in range(3):  # Try up to 3 scroll attempts
                    try:
                        driver.execute_script('mobile: scrollGesture', {
                            'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                            'direction': 'down',
                            'percent': 2.0
                        })
                        time.sleep(1)
                        element = driver.find_element(AppiumBy.XPATH, f"//*[@text='{element_name}']")
                        print(f"✅ Found after scroll (attempt {scroll_attempt + 1}): {element_name}")
                        found_elements.append(element_name)
                        found = True
                        break
                    except:
                        continue

                if not found:
                    print(f"❌ Missing: {element_name}")

        print(f"\n📊 Result: {len(found_elements)}/{len(expected_elements)} elements found")

        if len(found_elements) != len(expected_elements):
            missing = set(expected_elements) - set(found_elements)
            print(f"⚠️  Missing elements: {missing}")
            # Don't fail immediately, continue to stop measurement
        else:
            print("✅ All data streams are active!")

        # =================================================================
        # Optional: Long-term Packet Monitoring
        # =================================================================
        if target_packets:
            print("\n" + "="*80)
            print(f"📊 PACKET MONITORING: Waiting for {target_packets:,} packets")
            print("="*80)

            # Calculate estimated time
            # Assuming 1 packet/second (typical ECG sampling rate)
            estimated_minutes = target_packets / 60
            estimated_hours = estimated_minutes / 60

            if estimated_hours >= 1:
                print(f"⏱️  Estimated time: {estimated_hours:.1f} hours ({estimated_minutes:.0f} minutes)")
            else:
                print(f"⏱️  Estimated time: {estimated_minutes:.0f} minutes")

            print("🔍 Monitoring ECG packet count...")

            start_time = time.time()
            last_log_time = start_time
            check_interval = 10  # Check every 10 seconds

            current_packets = 0
            consecutive_failures = 0
            max_failures = 6  # Allow 6 failures (1 minute) before giving up

            # Scroll to top of Notify screen to ensure Packet Number is visible
            print("\n📜 Scrolling to top of screen to find Packet Number...")
            try:
                for _ in range(3):
                    driver.execute_script('mobile: scrollGesture', {
                        'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                        'direction': 'up',
                        'percent': 3.0
                    })
                    time.sleep(0.5)
            except:
                pass

            while current_packets < target_packets:
                try:
                    # Find "Packet Number" element and extract count
                    packet_text = None
                    extraction_method = None

                    # Pattern 1: Find element containing "Packet Number :" (more specific)
                    try:
                        packet_element = driver.find_element(
                            AppiumBy.XPATH,
                            "//*[contains(@text, 'Packet Number :')]"
                        )
                        packet_text = packet_element.text
                        extraction_method = "contains-colon"
                        print(f"🔍 [DEBUG] Found via 'Packet Number :': '{packet_text}'")
                    except Exception as e1:
                        # Pattern 2: Find element with manual search through all TextViews
                        try:
                            # Get all TextViews and search manually
                            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                            for elem in all_texts:
                                try:
                                    text = elem.text
                                    if text and ('Packet Number' in text or 'packet number' in text.lower()):
                                        packet_text = text
                                        extraction_method = "manual-search"
                                        print(f"🔍 [DEBUG] Found via manual search: '{packet_text}'")
                                        break
                                except:
                                    continue

                            if not packet_text:
                                raise Exception("Packet Number not found in any TextView")
                        except Exception as e2:
                            print(f"❌ [DEBUG] Both XPath methods failed")
                            print(f"   Method 1: {str(e1)[:80]}")
                            print(f"   Method 2: {str(e2)[:80]}")
                            consecutive_failures += 1
                            if consecutive_failures >= max_failures:
                                print(f"\n⚠️  Too many failures ({consecutive_failures}), stopping packet monitoring")
                                break

                    # Extract packet count from text
                    if packet_text:
                        consecutive_failures = 0  # Reset failure counter

                        # Use regex to extract ONLY the packet number from "Packet Number: XXX"
                        # This avoids getting confused by sample data that follows
                        match = re.search(r'Packet Number:\s*(\d+)', packet_text, re.IGNORECASE)

                        if match:
                            prev_packets = current_packets
                            current_packets = int(match.group(1))
                            print(f"📦 [DEBUG] Packet count: {prev_packets} → {current_packets} (target: {target_packets})")

                            # Log progress every minute
                            current_time = time.time()
                            if current_time - last_log_time >= 60:
                                elapsed = (current_time - start_time) / 60
                                progress = (current_packets / target_packets) * 100
                                remaining = target_packets - current_packets
                                eta_minutes = (remaining / (current_packets / (elapsed + 0.001)))

                                print(f"\n📊 Progress: {current_packets:,}/{target_packets:,} packets ({progress:.1f}%)")
                                print(f"   Elapsed: {elapsed:.1f} min | ETA: {eta_minutes:.1f} min\n")
                                last_log_time = current_time
                        else:
                            print(f"⚠️  [DEBUG] Could not parse packet number from text (first 100 chars): '{packet_text[:100]}...'")

                    # Check if target reached
                    print(f"🎯 [DEBUG] Checking: {current_packets} >= {target_packets}? {current_packets >= target_packets}")
                    if current_packets >= target_packets:
                        total_time = (time.time() - start_time) / 60
                        print(f"\n{'='*80}")
                        print(f"✅ Target reached: {current_packets:,} packets in {total_time:.1f} minutes!")
                        print(f"{'='*80}\n")
                        break

                    # Wait before next check
                    time.sleep(check_interval)

                except Exception as e:
                    print(f"⚠️  Error reading packet count: {e}")
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        print(f"\n⚠️  Too many failures ({consecutive_failures}), stopping packet monitoring")
                        break
                    time.sleep(check_interval)

            driver.save_screenshot('step4_notify_target_reached.png')
            print("✅ Packet monitoring complete!")
        else:
            # Default: Just observe for 10 seconds
            print("⏳ Observing data for 10 seconds...")
            time.sleep(10)

        driver.save_screenshot('step4_notify_active_data.png')
        print("✅ STEP 4 Complete - Data Streams Verified")

        # =================================================================
        # STEP 5: WriteSet - Stop Measurement
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 5: WriteSet - Stop Measurement")
        print("="*80)

        print("\n📖 Returning to WriteSet screen...")
        writeset_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteSet']")
        writeset_button.click()
        time.sleep(3)

        print("\n⏹️  Clicking STOP button...")
        stop_button = driver.find_element(AppiumBy.XPATH, "//*[@text='STOP']")
        stop_button.click()

        print("⏳ Waiting for measurement to stop (5 seconds)...")
        time.sleep(5)

        driver.save_screenshot('step5_writeset_stop.png')
        print("✅ STEP 5 Complete - Measurement Stopped")

        # =================================================================
        # STEP 6: Reset Device
        # =================================================================
        print("\n" + "="*80)
        print("📍 STEP 6: Reset Device")
        print("="*80)

        print("\n🔄 Clicking RESET DEVICE button...")
        reset_button = driver.find_element(AppiumBy.XPATH, "//*[@text='RESET DEVICE']")
        reset_button.click()

        print("⏳ Waiting for device reset (5 seconds)...")
        time.sleep(5)

        driver.save_screenshot('step6_reset_device.png')
        print("✅ STEP 6 Complete - Device Reset")

        # =================================================================
        # Final Verification
        # =================================================================
        print("\n" + "="*80)
        print("🎉 WORKFLOW TEST COMPLETE!")
        print("="*80)

        assert len(found_elements) == len(expected_elements), \
            f"Missing data streams: {set(expected_elements) - set(found_elements)}"

        print("\n✅ All steps passed successfully!")
        print("✅ Data collection workflow is working correctly!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
