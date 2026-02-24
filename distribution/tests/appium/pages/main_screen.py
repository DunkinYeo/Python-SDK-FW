"""Main screen page object for SDK Sample app."""
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class MainScreen(BasePage):
    """Page object for main screen of SDK Sample app (automation-sdk2.1.5.apk)."""

    # ==================================================
    # SDK Sample app - Jetpack Compose UI
    # Package: com.wellysis.spatch.sdk.sample
    # ==================================================

    # Main menu buttons (always visible at top)
    LINK_BUTTON = (AppiumBy.XPATH, "//*[@text='Link']")
    READ_BUTTON = (AppiumBy.XPATH, "//*[@text='Read']")
    WRITESET_BUTTON = (AppiumBy.XPATH, "//*[@text='WriteSet']")
    WRITEGET_BUTTON = (AppiumBy.XPATH, "//*[@text='WriteGet']")
    NOTIFY_BUTTON = (AppiumBy.XPATH, "//*[@text='Notify']")

    # Connection status elements (in Link screen)
    CONNECTION_STATUS_LABEL = (AppiumBy.XPATH, "//*[@text='Connection Status']")
    CONNECTION_STATUS_TEXT = (AppiumBy.XPATH, "//*[@text='DISCONNECTED' or @text='CONNECTED']")
    RSSI_LABEL = (AppiumBy.XPATH, "//*[@text='RSSI']")

    # Link screen elements
    SERIAL_NUMBER_INPUT = (AppiumBy.XPATH, "//android.widget.EditText")
    SERIAL_NUMBER_PLACEHOLDER = (AppiumBy.XPATH, "//*[@text='Input Serial Number']")
    CONNECT_BUTTON = (AppiumBy.XPATH, "//*[@text='CONNECT']")
    DISCONNECT_BUTTON = (AppiumBy.XPATH, "//*[@text='DISCONNECT']")
    SENSOR_TOGGLE = (AppiumBy.XPATH, "//*[@text='Sensor']")
    RESTART_APP_BUTTON = (AppiumBy.XPATH, "//*[@text='CLIENT-EX APP RESTART']")

    def __init__(self, driver):
        """Initialize main screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized MainScreen page object for SDK Sample app")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if main screen is loaded by looking for top menu buttons.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if main screen is loaded")
        try:
            # Check for any of the main menu buttons
            return (self.is_element_present(self.LINK_BUTTON, timeout) or
                    self.is_element_present(self.READ_BUTTON, timeout))
        except Exception as e:
            self.logger.error(f"Failed to verify main screen loaded: {e}")
            self.take_screenshot("main_screen_not_loaded")
            return False

    def get_app_version(self) -> str:
        """
        Get app version.

        Returns:
            App version string (2.1.5 from APK)
        """
        self.logger.info("Getting app version")
        return "2.1.5"

    def navigate_to_link(self) -> bool:
        """
        Navigate to LINK section (BLE connection management).

        Returns:
            True if navigation successful
        """
        self.logger.info("Navigating to LINK section")
        return self.safe_click(self.LINK_BUTTON)

    def navigate_to_read(self) -> bool:
        """
        Navigate to READ section.

        This section contains Firmware version and other read operations.

        Returns:
            True if navigation successful
        """
        self.logger.info("Navigating to READ section")
        return self.safe_click(self.READ_BUTTON)

    def navigate_to_writeset(self) -> bool:
        """Navigate to WRITESET section."""
        self.logger.info("Navigating to WRITESET section")
        return self.safe_click(self.WRITESET_BUTTON)

    def navigate_to_writeget(self) -> bool:
        """Navigate to WRITEGET section."""
        self.logger.info("Navigating to WRITEGET section")
        return self.safe_click(self.WRITEGET_BUTTON)

    def navigate_to_notify(self) -> bool:
        """Navigate to NOTIFY section."""
        self.logger.info("Navigating to NOTIFY section")
        return self.safe_click(self.NOTIFY_BUTTON)

    def is_device_connected(self) -> bool:
        """
        Check if BLE device is currently connected.

        Returns:
            True if device connected
        """
        self.logger.info("Checking BLE device connection status")
        try:
            status_text = self.safe_get_text(self.CONNECTION_STATUS_TEXT, timeout=3)
            if status_text:
                is_connected = "CONNECTED" in status_text.upper()
                self.logger.info(f"Device {'connected' if is_connected else 'disconnected'} (status: {status_text})")
                return is_connected

            self.logger.warning("Could not read connection status")
            return False

        except Exception as e:
            self.logger.error(f"Error checking connection status: {e}")
            return False

    def enter_serial_number(self, serial_number: str) -> bool:
        """
        Enter serial number in the input field.

        Args:
            serial_number: Serial number to enter

        Returns:
            True if successful
        """
        self.logger.info(f"Entering serial number: {serial_number}")
        try:
            # Click on the input field
            if not self.safe_click(self.SERIAL_NUMBER_INPUT):
                self.logger.error("Failed to click serial number input")
                return False

            # Enter text
            elem = self.driver.find_element(*self.SERIAL_NUMBER_INPUT)
            elem.clear()
            elem.send_keys(serial_number)

            self.logger.info("Serial number entered successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error entering serial number: {e}")
            return False

    def click_connect(self) -> bool:
        """Click CONNECT button."""
        self.logger.info("Clicking CONNECT button")
        return self.safe_click(self.CONNECT_BUTTON)

    def click_disconnect(self) -> bool:
        """Click DISCONNECT button."""
        self.logger.info("Clicking DISCONNECT button")
        return self.safe_click(self.DISCONNECT_BUTTON)

    def click_restart_app(self) -> bool:
        """Click CLIENT-EX APP RESTART button."""
        self.logger.info("Clicking restart app button")
        return self.safe_click(self.RESTART_APP_BUTTON)

    def get_rssi_value(self) -> str:
        """
        Get RSSI value.

        Returns:
            RSSI value as string
        """
        self.logger.info("Getting RSSI value")
        try:
            # RSSI value is the text element right after RSSI label
            rssi_value = self.driver.find_element(
                AppiumBy.XPATH,
                "//*[@text='RSSI']/following-sibling::android.widget.TextView[1]"
            )
            value = rssi_value.text
            self.logger.info(f"RSSI value: {value}")
            return value
        except Exception as e:
            self.logger.error(f"Error getting RSSI value: {e}")
            return "0"

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
            # Wait for any top menu button
            if self.wait_for_element(self.LINK_BUTTON, timeout):
                self.logger.info("Main screen is ready")
                return True

            self.logger.error("Main screen did not load in time")
            return False

        except Exception as e:
            self.logger.error(f"Main screen not ready: {e}")
            self.take_screenshot("main_screen_not_ready")
            return False
