"""Link screen page object for RECORD-EX app (BLE connection)."""
import os
from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class LinkScreen(BasePage):
    """Page object for Link screen where BLE device connection is managed."""

    # ==================================================
    # Link screen - BLE connection management
    # TODO: Verify with Appium Inspector
    # ==================================================

    # Connection buttons
    CONNECT_BUTTON = (AppiumBy.XPATH, "//*[@text='connect' or @text='Connect' or @text='CONNECT']")
    DISCONNECT_BUTTON = (AppiumBy.XPATH, "//*[@text='disconnect' or @text='Disconnect' or @text='DISCONNECT']")
    SCAN_BUTTON = (AppiumBy.XPATH, "//*[@text='scan' or @text='Scan' or @text='SCAN']")

    # Device list/selection
    DEVICE_LIST = (AppiumBy.XPATH, "//*[contains(@resource-id, 'device') or contains(@resource-id, 'list')]")

    # Connection status
    CONNECTION_STATUS = (AppiumBy.XPATH, "//*[contains(@text, 'connected') or contains(@text, 'Connected')]")
    DISCONNECTED_STATUS = (AppiumBy.XPATH, "//*[contains(@text, 'disconnected') or contains(@text, 'Disconnected')]")

    # Dialog buttons (from strings.xml)
    YES_BUTTON = (AppiumBy.XPATH, "//*[@text='YES']")
    NO_BUTTON = (AppiumBy.XPATH, "//*[@text='NO']")

    def __init__(self, driver):
        """Initialize link screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized LinkScreen page object")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """Check if link screen is loaded."""
        self.logger.info("Checking if link screen is loaded")
        try:
            if self.is_element_present(self.CONNECT_BUTTON, timeout):
                return True
            if self.is_element_present(self.DISCONNECT_BUTTON, timeout):
                return True
            return False
        except Exception as e:
            self.logger.error(f"Link screen not loaded: {e}")
            return False

    def click_connect(self) -> bool:
        """
        Click connect button to initiate BLE connection.

        Returns:
            True if successful
        """
        self.logger.info("Clicking CONNECT button")
        return self.safe_click(self.CONNECT_BUTTON)

    def click_disconnect(self) -> bool:
        """
        Click disconnect button to disconnect BLE device.

        Returns:
            True if successful
        """
        self.logger.info("Clicking DISCONNECT button")
        return self.safe_click(self.DISCONNECT_BUTTON)

    def connect_to_device(self, device_name: Optional[str] = None, timeout: int = 30) -> bool:
        """
        Connect to spatch device via BLE.

        Args:
            device_name: Device name (from env if not provided)
            timeout: Connection timeout

        Returns:
            True if connected successfully
        """
        if not device_name:
            device_name = os.getenv("BLE_DEVICE_NAME", "")

        self.logger.info(f"Attempting to connect to device: {device_name}")

        try:
            # Step 1: Click connect button
            if not self.click_connect():
                self.logger.error("Failed to click connect button")
                return False

            # Step 2: Wait for connection (may need device selection in UI)
            import time
            time.sleep(3)  # Wait for scan/connection

            # Step 3: Check connection status
            if self.is_connected():
                self.logger.info("Successfully connected to BLE device")
                return True

            self.logger.warning("Connection status unclear")
            return False

        except Exception as e:
            self.logger.error(f"Error connecting to device: {e}")
            self.take_screenshot("connect_error")
            return False

    def disconnect_device(self) -> bool:
        """
        Disconnect from BLE device.

        Returns:
            True if disconnected successfully
        """
        self.logger.info("Disconnecting from BLE device")
        try:
            if not self.click_disconnect():
                return False

            import time
            time.sleep(2)

            # Confirm dialog if it appears
            if self.is_element_present(self.YES_BUTTON, timeout=2):
                self.safe_click(self.YES_BUTTON)

            if not self.is_connected():
                self.logger.info("Device disconnected successfully")
                return True

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
            # Method 1: Check for "connected" text
            if self.is_element_present(self.CONNECTION_STATUS, timeout=2):
                self.logger.info("Device is connected")
                return True

            # Method 2: Check if disconnect button is present
            if self.is_element_present(self.DISCONNECT_BUTTON, timeout=2):
                self.logger.info("Disconnect button present, assuming connected")
                return True

            self.logger.info("Device not connected")
            return False

        except Exception as e:
            self.logger.error(f"Error checking connection: {e}")
            return False

    def wait_for_connection(self, timeout: int = 30) -> bool:
        """
        Wait for BLE connection to complete.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if connected within timeout
        """
        self.logger.info(f"Waiting up to {timeout}s for connection")
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.is_connected():
                return True
            time.sleep(1)

        self.logger.warning("Connection timeout")
        self.take_screenshot("connection_timeout")
        return False
