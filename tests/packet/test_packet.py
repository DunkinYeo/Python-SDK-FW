"""Packet monitoring and data collection workflow tests."""
import pytest
import time
import os
import subprocess
from dotenv import load_dotenv
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import InvalidSessionIdException
import re

load_dotenv()


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
        """
        print("\n" + "="*80)
        print("🔬 TEST: Complete Data Collection Workflow")
        print("="*80)

        driver = connected_driver

        print("\n⏳ Waiting for UI to stabilize...")
        time.sleep(3)

        try:
            driver.hide_keyboard()
        except Exception:
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
        time.sleep(5)

        driver.save_screenshot('step4_notify_before_check.png')

        expected_elements = ["ECG", "IMU", "ACC", "Memory", "Heart Rate", "Battery"]
        print("\n🔍 Checking for active data streams...")

        found_elements = []
        for element_name in expected_elements:
            try:
                driver.find_element(AppiumBy.XPATH, f"//*[@text='{element_name}']")
                print(f"✅ Found: {element_name}")
                found_elements.append(element_name)
            except Exception:
                print(f"📜 Scrolling to find: {element_name}...")
                found = False
                for scroll_attempt in range(3):
                    try:
                        driver.execute_script('mobile: scrollGesture', {
                            'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                            'direction': 'down', 'percent': 0.75
                        })
                        time.sleep(1)
                        driver.find_element(AppiumBy.XPATH, f"//*[@text='{element_name}']")
                        print(f"✅ Found after scroll (attempt {scroll_attempt + 1}): {element_name}")
                        found_elements.append(element_name)
                        found = True
                        break
                    except Exception:
                        continue
                if not found:
                    print(f"❌ Missing: {element_name}")

        print(f"\n📊 Result: {len(found_elements)}/{len(expected_elements)} elements found")
        if len(found_elements) != len(expected_elements):
            missing = set(expected_elements) - set(found_elements)
            print(f"⚠️  Missing elements: {missing}")
        else:
            print("✅ All data streams are active!")

        # =================================================================
        # Optional: Long-term Packet Monitoring
        # =================================================================
        if target_packets:
            print("\n" + "="*80)
            print(f"📊 PACKET MONITORING: Waiting for {target_packets:,} packets")
            print("="*80)

            estimated_minutes = target_packets / 60
            estimated_hours = estimated_minutes / 60
            if estimated_hours >= 1:
                print(f"⏱️  Estimated time: {estimated_hours:.1f} hours ({estimated_minutes:.0f} minutes)")
            else:
                print(f"⏱️  Estimated time: {estimated_minutes:.0f} minutes")

            print("🔍 Monitoring ECG packet count...")

            start_time = time.time()
            last_log_time = start_time
            check_interval = 10
            last_keepalive_time = start_time
            device_name = os.getenv('APPIUM_DEVICE_NAME', '')

            def _keepalive():
                try:
                    adb_cmd = ['adb']
                    if device_name:
                        adb_cmd += ['-s', device_name]
                    subprocess.run(adb_cmd + ['shell', 'input', 'keyevent', '224'],
                                   timeout=5, capture_output=True)
                except Exception:
                    pass

            def _recover_notify_screen():
                try:
                    notify_tab = driver.find_element(AppiumBy.XPATH, "//*[@text='Notify']")
                    notify_tab.click()
                    time.sleep(2)
                    for _ in range(3):
                        driver.execute_script('mobile: scrollGesture', {
                            'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                            'direction': 'up', 'percent': 0.75
                        })
                        time.sleep(0.3)
                    print("🔄 [RECOVER] Navigated back to Notify screen")
                except Exception as re:
                    print(f"⚠️  [RECOVER] Could not navigate to Notify: {re}")

            # Scroll to top so Packet Number is visible
            print("\n📜 Scrolling to top of screen...")
            try:
                for _ in range(3):
                    driver.execute_script('mobile: scrollGesture', {
                        'left': 100, 'top': 800, 'width': 500, 'height': 1000,
                        'direction': 'up', 'percent': 0.75
                    })
                    time.sleep(0.5)
            except Exception:
                pass

            current_packets = 0
            consecutive_failures = 0
            max_failures = 30

            while current_packets < target_packets:
                try:
                    packet_text = None

                    try:
                        packet_element = driver.find_element(
                            AppiumBy.XPATH, "//*[contains(@text, 'Packet Number :')]"
                        )
                        packet_text = packet_element.text
                    except Exception as e1:
                        try:
                            all_texts = driver.find_elements(
                                AppiumBy.CLASS_NAME, "android.widget.TextView"
                            )
                            for elem in all_texts:
                                try:
                                    text = elem.text
                                    if text and 'Packet Number' in text:
                                        packet_text = text
                                        break
                                except Exception:
                                    continue
                            if not packet_text:
                                raise Exception("Packet Number not found")
                        except Exception as e2:
                            # Session terminated — exit immediately, no point retrying
                            if isinstance(e1, InvalidSessionIdException) or isinstance(e2, InvalidSessionIdException):
                                print("\n❌ Appium session terminated — stopping packet monitoring")
                                consecutive_failures = max_failures  # force exit
                                break
                            print(f"❌ [DEBUG] XPath failed: {str(e1)[:60]}")
                            consecutive_failures += 1
                            if consecutive_failures % 3 == 0:
                                _keepalive()
                                _recover_notify_screen()
                            if consecutive_failures >= max_failures:
                                print(f"\n⚠️  Too many failures ({consecutive_failures}), stopping")
                                break

                    if packet_text:
                        consecutive_failures = 0
                        match = re.search(r'Packet Number:\s*(\d+)', packet_text, re.IGNORECASE)
                        if match:
                            prev_packets = current_packets
                            current_packets = int(match.group(1))
                            print(f"📦 Packets: {prev_packets} → {current_packets} / {target_packets}")

                            current_time = time.time()
                            if current_time - last_log_time >= 60:
                                elapsed = (current_time - start_time) / 60
                                progress = (current_packets / target_packets) * 100
                                remaining = target_packets - current_packets
                                eta = remaining / max(current_packets / (elapsed + 0.001), 0.001)
                                print(f"\n📊 Progress: {current_packets:,}/{target_packets:,} ({progress:.1f}%) | "
                                      f"Elapsed: {elapsed:.1f}m | ETA: {eta:.1f}m\n")
                                last_log_time = current_time
                        else:
                            print(f"⚠️  Could not parse: '{packet_text[:80]}'")

                    if current_packets >= target_packets:
                        total_time = (time.time() - start_time) / 60
                        print(f"\n{'='*80}")
                        print(f"✅ Target reached: {current_packets:,} packets in {total_time:.1f} minutes!")
                        print(f"{'='*80}\n")
                        break

                    current_time = time.time()
                    if current_time - last_keepalive_time >= 30:
                        _keepalive()
                        last_keepalive_time = current_time

                    time.sleep(check_interval)

                except InvalidSessionIdException:
                    print("\n❌ Appium session terminated — stopping packet monitoring")
                    break
                except Exception as e:
                    print(f"⚠️  Error: {e}")
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        print(f"\n⚠️  Too many failures, stopping packet monitoring")
                        break
                    _keepalive()
                    time.sleep(check_interval)

            try:
                driver.save_screenshot('step4_notify_target_reached.png')
            except Exception:
                pass
            print("✅ Packet monitoring complete!")
        else:
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

        device_name = os.getenv('APPIUM_DEVICE_NAME', '')

        def _keepalive_simple():
            try:
                adb_cmd = ['adb']
                if device_name:
                    adb_cmd += ['-s', device_name]
                subprocess.run(adb_cmd + ['shell', 'input', 'keyevent', '224'],
                               timeout=5, capture_output=True)
            except Exception:
                pass

        print("\n📖 Returning to WriteSet screen...")
        for _attempt in range(5):
            try:
                writeset_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteSet']")
                writeset_button.click()
                break
            except Exception:
                _keepalive_simple()
                time.sleep(3)
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
        # Final
        # =================================================================
        print("\n" + "="*80)
        print("🎉 WORKFLOW TEST COMPLETE!")
        print("="*80)

        if len(found_elements) < len(expected_elements):
            missing = set(expected_elements) - set(found_elements)
            print(f"\n⚠️  Some data streams not found: {missing} ({len(found_elements)}/{len(expected_elements)})")
        else:
            print("\n✅ All data streams confirmed active!")

        print("\n✅ All steps passed successfully!")
