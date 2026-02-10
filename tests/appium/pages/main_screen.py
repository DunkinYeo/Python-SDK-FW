"""Main screen page object for SDK validation app."""
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class MainScreen(BasePage):
    """Page object for main screen of SDK validation app."""

    # ==================================================
    # IMPORTANT: Customize these locators for your app!
    # ==================================================
    # Use Appium Inspector to find the correct IDs/XPaths
    # Examples below are placeholders

    # Main UI elements
    APP_TITLE = (AppiumBy.ID, "com.yourapp:id/app_title")
    APP_VERSION_TEXT = (AppiumBy.ID, "com.yourapp:id/version_text")

    # Navigation buttons
    READ_BUTTON = (AppiumBy.ID, "com.yourapp:id/read_button")
    WRITE_BUTTON = (AppiumBy.ID, "com.yourapp:id/write_button")
    SCAN_BUTTON = (AppiumBy.ID, "com.yourapp:id/scan_button")
    CONNECT_BUTTON = (AppiumBy.ID, "com.yourapp:id/connect_button")
    SETTINGS_BUTTON = (AppiumBy.ID, "com.yourapp:id/settings_button")

    # Alternative: Find by text
    READ_BUTTON_TEXT = (AppiumBy.XPATH, "//*[@text='Read']")
    WRITE_BUTTON_TEXT = (AppiumBy.XPATH, "//*[@text='Write']")
    SCAN_BUTTON_TEXT = (AppiumBy.XPATH, "//*[@text='Scan']")
    CONNECT_BUTTON_TEXT = (AppiumBy.XPATH, "//*[@text='Connect']")

    # Connection status
    CONNECTION_STATUS = (AppiumBy.ID, "com.yourapp:id/connection_status")
    DEVICE_NAME_LABEL = (AppiumBy.ID, "com.yourapp:id/device_name")

    def __init__(self, driver):
        """Initialize main screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized MainScreen page object")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if main screen is loaded.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if main screen is loaded")
        # Try to find any characteristic element of main screen
        # Customize this check based on your app
        try:
            # Try by ID first
            if self.is_element_present(self.APP_TITLE, timeout):
                return True
            # Fallback: try to find Read button
            if self.is_element_present(self.READ_BUTTON, timeout):
                return True
            # Last resort: try by text
            return self.is_element_present(self.READ_BUTTON_TEXT, timeout)
        except Exception as e:
            self.logger.error(f"Failed to verify main screen loaded: {e}")
            self.take_screenshot("main_screen_not_loaded")
            return False

    def get_app_version(self) -> str:
        """
        Get app version displayed on main screen.

        Returns:
            App version string or "unknown" if not found
        """
        self.logger.info("Getting app version from main screen")
        try:
            # Try to find version text element
            version_text = self.safe_get_text(self.APP_VERSION_TEXT, timeout=5)
            if version_text:
                self.logger.info(f"Found app version: {version_text}")
                return version_text

            # Alternative: Try to find version in other locations
            # Add your app-specific logic here
            self.logger.warning("App version not found on main screen")
            return "unknown"

        except Exception as e:
            self.logger.error(f"Error getting app version: {e}")
            return "unknown"

    def navigate_to_read_section(self) -> bool:
        """
        Navigate to Read section.

        Returns:
            True if navigation successful
        """
        self.logger.info("Navigating to Read section")
        try:
            # Try clicking Read button by ID
            if self.safe_click(self.READ_BUTTON):
                self.logger.info("Clicked Read button (by ID)")
                return True

            # Fallback: Try by text
            if self.safe_click(self.READ_BUTTON_TEXT):
                self.logger.info("Clicked Read button (by text)")
                return True

            self.logger.error("Failed to click Read button")
            self.take_screenshot("read_button_not_found")
            return False

        except Exception as e:
            self.logger.error(f"Error navigating to Read section: {e}")
            self.take_screenshot("navigate_read_error")
            return False

    def navigate_to_write_section(self) -> bool:
        """Navigate to Write section."""
        self.logger.info("Navigating to Write section")
        if self.safe_click(self.WRITE_BUTTON):
            return True
        return self.safe_click(self.WRITE_BUTTON_TEXT)

    def navigate_to_scan(self) -> bool:
        """Navigate to Scan screen."""
        self.logger.info("Navigating to Scan screen")
        if self.safe_click(self.SCAN_BUTTON):
            return True
        return self.safe_click(self.SCAN_BUTTON_TEXT)

    def click_connect(self) -> bool:
        """Click Connect button."""
        self.logger.info("Clicking Connect button")
        if self.safe_click(self.CONNECT_BUTTON):
            return True
        return self.safe_click(self.CONNECT_BUTTON_TEXT)

    def is_device_connected(self) -> bool:
        """
        Check if BLE device is currently connected.

        Returns:
            True if device connected

        Note: Customize this based on your app's connection indicator
        """
        self.logger.info("Checking BLE device connection status")
        try:
            # Method 1: Check connection status text
            status_text = self.safe_get_text(self.CONNECTION_STATUS, timeout=3)
            if status_text:
                # Customize these checks for your app
                connected_indicators = ["connected", "연결됨", "연결"]
                if any(indicator in status_text.lower() for indicator in connected_indicators):
                    self.logger.info(f"Device connected (status: {status_text})")
                    return True

            # Method 2: Check if device name is displayed
            if self.is_element_visible(self.DEVICE_NAME_LABEL, timeout=2):
                device_name = self.safe_get_text(self.DEVICE_NAME_LABEL)
                if device_name and device_name != "":
                    self.logger.info(f"Device connected (name: {device_name})")
                    return True

            self.logger.info("Device not connected")
            return False

        except Exception as e:
            self.logger.error(f"Error checking connection status: {e}")
            return False

    def get_connected_device_name(self) -> str:
        """
        Get name of connected BLE device.

        Returns:
            Device name or empty string
        """
        self.logger.info("Getting connected device name")
        try:
            device_name = self.safe_get_text(self.DEVICE_NAME_LABEL, timeout=3)
            if device_name:
                self.logger.info(f"Connected device: {device_name}")
                return device_name
            return ""
        except Exception as e:
            self.logger.error(f"Error getting device name: {e}")
            return ""

    def wait_for_screen_ready(self, timeout: int = 15) -> bool:
        """
        Wait for main screen to be fully loaded and ready.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if screen is ready
        """
        self.logger.info("Waiting for main screen to be ready")
        try:
            # Wait for key UI elements to be present
            if not self.wait_for_element(self.READ_BUTTON, timeout):
                if not self.wait_for_element(self.READ_BUTTON_TEXT, timeout):
                    return False

            self.logger.info("Main screen is ready")
            return True
        except Exception as e:
            self.logger.error(f"Main screen not ready: {e}")
            self.take_screenshot("main_screen_not_ready")
            return False
