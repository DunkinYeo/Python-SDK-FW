"""Main screen page object for RECORD-EX app."""
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class MainScreen(BasePage):
    """Page object for main screen of RECORD-EX app (samplingrecord2.1.5.apk)."""

    # ==================================================
    # Updated for RECORD-EX app - Jetpack Compose UI
    # Package: com.wellysis.spatch.tool.record.ex
    # ==================================================
    # TODO: Verify with Appium Inspector and update as needed

    # Main menu buttons (always visible)
    LINK_BUTTON = (AppiumBy.XPATH, "//*[@text='link' or @text='Link' or @text='LINK']")
    READ_BUTTON = (AppiumBy.XPATH, "//*[@text='read' or @text='Read' or @text='READ']")
    WRITESET_BUTTON = (AppiumBy.XPATH, "//*[@text='writeset' or @text='WriteSet' or @text='WRITESET']")
    WRITEGET_BUTTON = (AppiumBy.XPATH, "//*[@text='writeget' or @text='WriteGet' or @text='WRITEGET']")
    NOTIFY_BUTTON = (AppiumBy.XPATH, "//*[@text='notify' or @text='Notify' or @text='NOTIFY']")

    # Alternative: partial match for flexibility
    LINK_TEXT = (AppiumBy.XPATH, "//*[contains(translate(@text, 'LINK', 'link'), 'link')]")
    READ_TEXT = (AppiumBy.XPATH, "//*[contains(translate(@text, 'READ', 'read'), 'read')]")
    WRITESET_TEXT = (AppiumBy.XPATH, "//*[contains(translate(@text, 'WRITESET', 'writeset'), 'writeset')]")
    WRITEGET_TEXT = (AppiumBy.XPATH, "//*[contains(translate(@text, 'WRITEGET', 'writeget'), 'writeget')]")
    NOTIFY_TEXT = (AppiumBy.XPATH, "//*[contains(translate(@text, 'NOTIFY', 'notify'), 'notify')]")

    # Action buttons
    DONE_BUTTON = (AppiumBy.XPATH, "//*[@text='DONE']")
    NEXT_BUTTON = (AppiumBy.XPATH, "//*[@text='NEXT']")
    STOP_BUTTON = (AppiumBy.XPATH, "//*[@text='STOP']")
    RESET_BUTTON = (AppiumBy.XPATH, "//*[@text='RESET']")
    QUIT_BUTTON = (AppiumBy.XPATH, "//*[@text='QUIT']")

    # Dialog buttons
    YES_BUTTON = (AppiumBy.XPATH, "//*[@text='YES']")
    NO_BUTTON = (AppiumBy.XPATH, "//*[@text='NO']")
    RETRY_BUTTON = (AppiumBy.XPATH, "//*[@text='RETRY']")

    # Connection status (verify with Inspector)
    CONNECTION_STATUS = (AppiumBy.XPATH, "//*[contains(@text, 'connect') or contains(@text, 'Connect')]")
    DEVICE_NAME_LABEL = (AppiumBy.XPATH, "//*[contains(@resource-id, 'device')]")

    def __init__(self, driver):
        """Initialize main screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized MainScreen page object for RECORD-EX")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if main screen is loaded.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if main screen is loaded")
        try:
            # Check for main menu buttons
            if self.is_element_present(self.LINK_BUTTON, timeout):
                return True
            if self.is_element_present(self.READ_BUTTON, timeout):
                return True
            if self.is_element_present(self.LINK_TEXT, timeout):
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to verify main screen loaded: {e}")
            self.take_screenshot("main_screen_not_loaded")
            return False

    def get_app_version(self) -> str:
        """
        Get app version.

        Returns:
            App version string (2.1.5 from APK)

        Note: Use Appium Inspector to find if version is displayed in UI
        """
        self.logger.info("Getting app version")
        # For now, return known version from APK filename
        return "2.1.5"

    def navigate_to_link(self) -> bool:
        """
        Navigate to LINK section (BLE connection).

        Returns:
            True if navigation successful
        """
        self.logger.info("Navigating to LINK section")
        try:
            if self.safe_click(self.LINK_BUTTON):
                self.logger.info("Clicked LINK button")
                return True

            if self.safe_click(self.LINK_TEXT):
                self.logger.info("Clicked LINK (partial match)")
                return True

            self.logger.error("Failed to click LINK button")
            self.take_screenshot("link_button_not_found")
            return False

        except Exception as e:
            self.logger.error(f"Error navigating to LINK: {e}")
            self.take_screenshot("navigate_link_error")
            return False

    def navigate_to_read(self) -> bool:
        """
        Navigate to READ section.

        This section contains Firmware version and other read operations.

        Returns:
            True if navigation successful
        """
        self.logger.info("Navigating to READ section")
        if self.safe_click(self.READ_BUTTON):
            return True
        return self.safe_click(self.READ_TEXT)

    def navigate_to_writeset(self) -> bool:
        """Navigate to WRITESET section."""
        self.logger.info("Navigating to WRITESET section")
        if self.safe_click(self.WRITESET_BUTTON):
            return True
        return self.safe_click(self.WRITESET_TEXT)

    def navigate_to_writeget(self) -> bool:
        """Navigate to WRITEGET section."""
        self.logger.info("Navigating to WRITEGET section")
        if self.safe_click(self.WRITEGET_BUTTON):
            return True
        return self.safe_click(self.WRITEGET_TEXT)

    def navigate_to_notify(self) -> bool:
        """Navigate to NOTIFY section."""
        self.logger.info("Navigating to NOTIFY section")
        if self.safe_click(self.NOTIFY_BUTTON):
            return True
        return self.safe_click(self.NOTIFY_TEXT)

    def click_done(self) -> bool:
        """Click DONE button."""
        self.logger.info("Clicking DONE button")
        return self.safe_click(self.DONE_BUTTON)

    def click_next(self) -> bool:
        """Click NEXT button."""
        self.logger.info("Clicking NEXT button")
        return self.safe_click(self.NEXT_BUTTON)

    def click_stop(self) -> bool:
        """Click STOP button."""
        self.logger.info("Clicking STOP button")
        return self.safe_click(self.STOP_BUTTON)

    def click_reset(self) -> bool:
        """Click RESET button."""
        self.logger.info("Clicking RESET button")
        return self.safe_click(self.RESET_BUTTON)

    def is_device_connected(self) -> bool:
        """
        Check if BLE device is currently connected.

        Returns:
            True if device connected

        Note: Use Appium Inspector to find accurate connection indicator
        """
        self.logger.info("Checking BLE device connection status")
        try:
            # Look for connection-related text
            status_text = self.safe_get_text(self.CONNECTION_STATUS, timeout=3)
            if status_text:
                connected_indicators = ["connected", "연결됨", "연결"]
                if any(indicator in status_text.lower() for indicator in connected_indicators):
                    self.logger.info(f"Device connected (status: {status_text})")
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

    def confirm_dialog_yes(self) -> bool:
        """Click YES in confirmation dialog."""
        self.logger.info("Clicking YES in dialog")
        return self.safe_click(self.YES_BUTTON)

    def confirm_dialog_no(self) -> bool:
        """Click NO in confirmation dialog."""
        self.logger.info("Clicking NO in dialog")
        return self.safe_click(self.NO_BUTTON)

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
            # Wait for LINK or READ button as indicator
            if not self.wait_for_element(self.LINK_BUTTON, timeout):
                if not self.wait_for_element(self.LINK_TEXT, timeout):
                    if not self.wait_for_element(self.READ_BUTTON, timeout):
                        return False

            self.logger.info("Main screen is ready")
            return True
        except Exception as e:
            self.logger.error(f"Main screen not ready: {e}")
            self.take_screenshot("main_screen_not_ready")
            return False
