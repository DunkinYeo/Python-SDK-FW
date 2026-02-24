"""BLE connection screen page object for SDK validation app."""
import os
from typing import List, Optional
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class BLEScreen(BasePage):
    """Page object for BLE scanning and connection screen."""

    # ==================================================
    # IMPORTANT: Customize these locators for your app!
    # ==================================================

    # Scan screen elements
    SCAN_TITLE = (AppiumBy.XPATH, "//*[contains(@text, 'Scan')]")
    SCAN_BUTTON = (AppiumBy.ID, "com.yourapp:id/scan_button")
    STOP_SCAN_BUTTON = (AppiumBy.ID, "com.yourapp:id/stop_scan_button")

    # Device list
    DEVICE_LIST = (AppiumBy.ID, "com.yourapp:id/device_list")
    DEVICE_ITEM = (AppiumBy.ID, "com.yourapp:id/device_item")
    DEVICE_NAME_TEXT = (AppiumBy.ID, "com.yourapp:id/device_name")
    DEVICE_MAC_TEXT = (AppiumBy.ID, "com.yourapp:id/device_mac")
    DEVICE_RSSI_TEXT = (AppiumBy.ID, "com.yourapp:id/device_rssi")

    # Connection controls
    CONNECT_BUTTON = (AppiumBy.ID, "com.yourapp:id/connect_button")
    DISCONNECT_BUTTON = (AppiumBy.ID, "com.yourapp:id/disconnect_button")
    CONNECTION_STATUS = (AppiumBy.ID, "com.yourapp:id/connection_status")

    # Status messages
    SCANNING_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Scanning')]")
    CONNECTED_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Connected')]")
    DISCONNECTED_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Disconnected')]")

    # Permission dialogs (Android)
    PERMISSION_ALLOW_BUTTON = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
    PERMISSION_ALLOW_FOREGROUND = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")

    def __init__(self, driver):
        """Initialize BLE screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized BLEScreen page object")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if BLE/Scan screen is loaded.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if BLE screen is loaded")
        try:
            # Check for scan button or title
            if self.is_element_present(self.SCAN_BUTTON, timeout):
                return True
            if self.is_element_present(self.SCAN_TITLE, timeout):
                return True
            return self.is_element_present(self.DEVICE_LIST, timeout)
        except Exception as e:
            self.logger.error(f"BLE screen not loaded: {e}")
            return False

    def handle_permissions(self) -> bool:
        """
        Handle BLE permission dialogs if they appear.

        Returns:
            True if permissions handled or not needed
        """
        self.logger.info("Checking for permission dialogs")
        try:
            # Check for location permission (required for BLE on Android)
            if self.is_element_present(self.PERMISSION_ALLOW_BUTTON, timeout=3):
                self.logger.info("Permission dialog detected, allowing...")
                self.safe_click(self.PERMISSION_ALLOW_BUTTON)
                return True

            # Alternative permission button
            if self.is_element_present(self.PERMISSION_ALLOW_FOREGROUND, timeout=2):
                self.logger.info("Foreground permission dialog detected")
                self.safe_click(self.PERMISSION_ALLOW_FOREGROUND)
                return True

            self.logger.info("No permission dialogs detected")
            return True

        except Exception as e:
            self.logger.error(f"Error handling permissions: {e}")
            return False

    def start_scan(self) -> bool:
        """
        Start BLE device scan.

        Returns:
            True if scan started successfully
        """
        self.logger.info("Starting BLE scan")
        try:
            # Handle permissions first
            self.handle_permissions()

            # Click scan button
            if self.safe_click(self.SCAN_BUTTON):
                self.logger.info("Scan button clicked")

                # Wait for scanning indicator
                if self.wait_for_element(self.SCANNING_INDICATOR, timeout=5):
                    self.logger.info("Scan started successfully")
                    return True

                # Even if indicator not found, scan might have started
                self.logger.warning("Scanning indicator not found, but scan may be active")
                return True

            self.logger.error("Failed to click scan button")
            return False

        except Exception as e:
            self.logger.error(f"Error starting scan: {e}")
            self.take_screenshot("scan_start_error")
            return False

    def stop_scan(self) -> bool:
        """
        Stop BLE device scan.

        Returns:
            True if scan stopped
        """
        self.logger.info("Stopping BLE scan")
        try:
            if self.safe_click(self.STOP_SCAN_BUTTON):
                self.logger.info("Scan stopped")
                return True

            # Sometimes scan button toggles
            if self.safe_click(self.SCAN_BUTTON):
                self.logger.info("Scan stopped (via toggle)")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Error stopping scan: {e}")
            return False

    def wait_for_devices(self, timeout: int = 10) -> bool:
        """
        Wait for at least one device to appear in scan results.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if devices found
        """
        self.logger.info(f"Waiting up to {timeout}s for devices...")
        try:
            # Wait for device list to have items
            import time
            start_time = time.time()

            while time.time() - start_time < timeout:
                devices = self.get_scanned_devices()
                if len(devices) > 0:
                    self.logger.info(f"Found {len(devices)} device(s)")
                    return True
                time.sleep(1)

            self.logger.warning("No devices found within timeout")
            self.take_screenshot("no_devices_found")
            return False

        except Exception as e:
            self.logger.error(f"Error waiting for devices: {e}")
            return False

    def get_scanned_devices(self) -> List[dict]:
        """
        Get list of scanned BLE devices.

        Returns:
            List of device info dictionaries with name, mac, rssi
        """
        self.logger.info("Getting scanned devices")
        devices = []

        try:
            # Find all device items in list
            device_elements = self.driver.find_elements(*self.DEVICE_ITEM)

            if not device_elements:
                # Try finding by device name elements
                device_elements = self.driver.find_elements(*self.DEVICE_NAME_TEXT)

            self.logger.info(f"Found {len(device_elements)} device elements")

            for device_elem in device_elements:
                try:
                    # Extract device info
                    device_info = {
                        "name": "",
                        "mac": "",
                        "rssi": ""
                    }

                    # Try to get device name
                    try:
                        name_elem = device_elem.find_element(*self.DEVICE_NAME_TEXT)
                        device_info["name"] = name_elem.text
                    except:
                        # Fallback: use device element text
                        device_info["name"] = device_elem.text

                    # Try to get MAC address
                    try:
                        mac_elem = device_elem.find_element(*self.DEVICE_MAC_TEXT)
                        device_info["mac"] = mac_elem.text
                    except:
                        pass

                    # Try to get RSSI
                    try:
                        rssi_elem = device_elem.find_element(*self.DEVICE_RSSI_TEXT)
                        device_info["rssi"] = rssi_elem.text
                    except:
                        pass

                    if device_info["name"]:
                        devices.append(device_info)
                        self.logger.debug(f"Device: {device_info}")

                except Exception as e:
                    self.logger.debug(f"Error parsing device element: {e}")
                    continue

            return devices

        except Exception as e:
            self.logger.error(f"Error getting scanned devices: {e}")
            return []

    def find_device_by_name(self, device_name: str) -> Optional[dict]:
        """
        Find specific device by name in scan results.

        Args:
            device_name: Name to search for (supports partial match)

        Returns:
            Device info dict or None if not found
        """
        self.logger.info(f"Looking for device: {device_name}")
        devices = self.get_scanned_devices()

        for device in devices:
            if device_name.lower() in device["name"].lower():
                self.logger.info(f"Found device: {device}")
                return device

        self.logger.warning(f"Device '{device_name}' not found")
        return None

    def connect_to_device(self, device_name: Optional[str] = None) -> bool:
        """
        Connect to BLE device.

        Args:
            device_name: Device name to connect to. If None, uses env variable.

        Returns:
            True if connection successful
        """
        # Get device name from env if not provided
        if not device_name:
            device_name = os.getenv("BLE_DEVICE_NAME", "")

        if not device_name:
            self.logger.error("No device name provided")
            return False

        self.logger.info(f"Attempting to connect to device: {device_name}")

        try:
            # Step 1: Start scan
            if not self.start_scan():
                return False

            # Step 2: Wait for device to appear
            import time
            time.sleep(3)  # Give scan some time

            # Step 3: Find device
            device = self.find_device_by_name(device_name)
            if not device:
                self.logger.error(f"Device '{device_name}' not found in scan results")
                self.take_screenshot("device_not_found")
                return False

            # Step 4: Click on device (assuming clicking device connects)
            device_locator = (AppiumBy.XPATH, f"//*[contains(@text, '{device_name}')]")
            if not self.safe_click(device_locator):
                self.logger.error("Failed to click on device")
                return False

            # Step 5: Click connect button if it exists
            if self.is_element_present(self.CONNECT_BUTTON, timeout=3):
                if not self.safe_click(self.CONNECT_BUTTON):
                    return False

            # Step 6: Wait for connection confirmation
            time.sleep(2)

            if self.is_connected():
                self.logger.info(f"Successfully connected to {device_name}")
                return True

            self.logger.warning("Connection state unclear")
            return False

        except Exception as e:
            self.logger.error(f"Error connecting to device: {e}")
            self.take_screenshot("connect_error")
            return False

    def disconnect_device(self) -> bool:
        """
        Disconnect from current BLE device.

        Returns:
            True if disconnection successful
        """
        self.logger.info("Disconnecting from BLE device")
        try:
            if self.safe_click(self.DISCONNECT_BUTTON):
                import time
                time.sleep(2)

                if not self.is_connected():
                    self.logger.info("Device disconnected successfully")
                    return True

            self.logger.warning("Disconnection unclear")
            return False

        except Exception as e:
            self.logger.error(f"Error disconnecting: {e}")
            return False

    def is_connected(self) -> bool:
        """
        Check if BLE device is currently connected.

        Returns:
            True if connected
        """
        self.logger.info("Checking connection status")
        try:
            # Method 1: Check for "Connected" indicator
            if self.is_element_present(self.CONNECTED_INDICATOR, timeout=2):
                self.logger.info("Connected indicator found")
                return True

            # Method 2: Check connection status text
            status_text = self.safe_get_text(self.CONNECTION_STATUS, timeout=2)
            if status_text:
                connected_keywords = ["connected", "연결됨", "연결"]
                if any(keyword in status_text.lower() for keyword in connected_keywords):
                    self.logger.info(f"Connection status: {status_text}")
                    return True

            # Method 3: Check if disconnect button is present
            if self.is_element_present(self.DISCONNECT_BUTTON, timeout=2):
                self.logger.info("Disconnect button present, assuming connected")
                return True

            self.logger.info("Device not connected")
            return False

        except Exception as e:
            self.logger.error(f"Error checking connection: {e}")
            return False

    def scan_and_connect_full_flow(
        self,
        device_name: Optional[str] = None,
        scan_duration: int = 5
    ) -> bool:
        """
        Complete flow: Start scan, find device, and connect.

        Args:
            device_name: Device name to connect to
            scan_duration: How long to scan in seconds

        Returns:
            True if connected successfully
        """
        self.logger.info("Executing full scan and connect flow")
        try:
            # Start scanning
            if not self.start_scan():
                return False

            # Wait for devices
            import time
            time.sleep(scan_duration)

            # Stop scan
            self.stop_scan()

            # Connect to device
            return self.connect_to_device(device_name)

        except Exception as e:
            self.logger.error(f"Error in scan and connect flow: {e}")
            self.take_screenshot("scan_connect_flow_error")
            return False
