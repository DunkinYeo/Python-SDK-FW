"""Read screen page object for SDK Sample app."""
import re
import time
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class ReadScreen(BasePage):
    """Page object for Read screen where device information can be read."""

    # ==================================================
    # SDK Sample app - Read screen
    # ==================================================

    # Read options - Label (informational text)
    BATTERY_LABEL = (AppiumBy.XPATH, "//*[@text='Battery']")
    MODEL_NUMBER_LABEL = (AppiumBy.XPATH, "//*[@text='Model Number']")
    SERIAL_NUMBER_LABEL = (AppiumBy.XPATH, "//*[@text='Serial Number']")
    FW_VERSION_LABEL = (AppiumBy.XPATH, "//*[@text='Firmware Version']")
    HW_VERSION_LABEL = (AppiumBy.XPATH, "//*[@text='Hardware Version']")
    SW_VERSION_LABEL = (AppiumBy.XPATH, "//*[@text='Software Version']")

    # Read options - Buttons (clickable to execute read operation)
    BATTERY_BUTTON = (AppiumBy.XPATH, "//*[@text='BATTERY']")
    MODEL_NUMBER_BUTTON = (AppiumBy.XPATH, "//*[@text='MODEL NUMBER']")
    SERIAL_NUMBER_BUTTON = (AppiumBy.XPATH, "//*[@text='SERIAL NUMBER']")
    FW_VERSION_BUTTON = (AppiumBy.XPATH, "//*[@text='FIRMWARE VERSION']")
    HW_VERSION_BUTTON = (AppiumBy.XPATH, "//*[@text='HARDWARE VERSION']")
    SW_VERSION_BUTTON = (AppiumBy.XPATH, "//*[@text='SOFTWARE VERSION']")

    def __init__(self, driver):
        """Initialize read screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized ReadScreen page object")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if Read screen is loaded by looking for any read option labels.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if Read screen is loaded")
        try:
            # Check if any of the read option labels are present
            return (self.is_element_present(self.FW_VERSION_LABEL, timeout) or
                    self.is_element_present(self.BATTERY_LABEL, timeout) or
                    self.is_element_present(self.MODEL_NUMBER_LABEL, timeout))
        except Exception as e:
            self.logger.error(f"Read screen not loaded: {e}")
            self.take_screenshot("read_screen_not_loaded")
            return False

    def select_firmware_version(self) -> bool:
        """
        Click 'FIRMWARE VERSION' button to read firmware version from device.

        Note: This requires a BLE device to be connected.

        Returns:
            True if button click successful
        """
        self.logger.info("Clicking FIRMWARE VERSION button")
        try:
            # Click the FIRMWARE VERSION button
            if self.safe_click(self.FW_VERSION_BUTTON):
                self.logger.info("Clicked FIRMWARE VERSION button")
                return True

            # If direct click fails, try scrolling to find it
            self.logger.info("Trying to scroll to find FIRMWARE VERSION button")
            if self.scroll_to_element(self.FW_VERSION_BUTTON):
                if self.safe_click(self.FW_VERSION_BUTTON):
                    return True

            self.logger.error("Failed to click FIRMWARE VERSION button")
            self.take_screenshot("fw_button_not_found")
            return False

        except Exception as e:
            self.logger.error(f"Error clicking firmware version button: {e}")
            self.take_screenshot("click_fw_button_error")
            return False

    def execute_read(self) -> bool:
        """
        Execute the read operation (if there's a separate Read/Execute button).

        Returns:
            True if successful
        """
        self.logger.info("Executing read operation")
        try:
            # Some apps require clicking a "Read" or "Execute" button after selecting option
            if self.is_element_present(self.READ_EXECUTE_BUTTON, timeout=2):
                return self.safe_click(self.READ_EXECUTE_BUTTON)

            # If no execute button, selection itself triggers read
            self.logger.info("No separate execute button found, assuming auto-read")
            return True

        except Exception as e:
            self.logger.error(f"Error executing read: {e}")
            return False

    def read_fw_version(self, wait_time: int = 5) -> str:
        """
        Read the displayed firmware version after clicking FIRMWARE VERSION button.

        The version appears in a TextView immediately following the "Firmware Version" label.

        Args:
            wait_time: Time to wait for version to appear (device communication time)

        Returns:
            Firmware version string or empty string if not found
        """
        self.logger.info("Reading firmware version from display")
        try:
            # Give device time to communicate and respond
            time.sleep(wait_time)

            # Method 1: Find the TextView right after "Firmware Version" label
            # XPath: Get the next sibling TextView after Firmware Version label
            try:
                fw_value_elem = self.driver.find_element(
                    AppiumBy.XPATH,
                    "//*[@text='Firmware Version']/following-sibling::android.widget.TextView[1]"
                )
                version_text = fw_value_elem.text
                if version_text:
                    fw_version = self._extract_version_from_text(version_text)
                    if fw_version:
                        self.logger.info(f"Found FW version: {fw_version}")
                        return fw_version
                    # If no version pattern found, return the raw text
                    elif version_text.strip():
                        self.logger.info(f"Found FW version (raw): {version_text}")
                        return version_text.strip()
            except Exception as e:
                self.logger.debug(f"Method 1 failed: {e}")

            # Method 2: Search all TextViews for version pattern
            text_views = self.find_elements_by_class("android.widget.TextView")
            for tv in text_views:
                try:
                    text = tv.text
                    if text:
                        fw_version = self._extract_version_from_text(text)
                        if fw_version:
                            self.logger.info(f"Found FW version in TextView: {fw_version}")
                            return fw_version
                except:
                    continue

            self.logger.warning("Could not find firmware version display")
            self.take_screenshot("fw_version_not_found")
            return ""

        except Exception as e:
            self.logger.error(f"Error reading firmware version: {e}")
            self.take_screenshot("read_fw_error")
            return ""

    def _extract_version_from_text(self, text: str) -> str:
        """
        Extract version number from text using regex patterns.

        Args:
            text: Raw text containing version

        Returns:
            Version string (e.g., "2.2.6") or empty string
        """
        if not text:
            return ""

        # Common version patterns
        patterns = [
            r'(\d+\.\d+\.\d+)',  # Standard x.y.z
            r'v(\d+\.\d+\.\d+)',  # With 'v' prefix
            r'V(\d+\.\d+\.\d+)',  # With 'V' prefix
            r'version[:\s]+(\d+\.\d+\.\d+)',  # "version: x.y.z" or "version x.y.z"
            r'Version[:\s]+(\d+\.\d+\.\d+)',  # Capitalized
            r'(\d+\.\d+\.\d+\.\d+)',  # Quad version w.x.y.z
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                version = match.group(1) if match.lastindex else match.group(0)
                self.logger.debug(f"Extracted version '{version}' from text: {text}")
                return version

        # No version pattern found
        return ""

    def read_sampling_rate(self) -> str:
        """
        Read current sampling rate setting.

        Returns:
            Sampling rate as string
        """
        self.logger.info("Reading sampling rate")
        try:
            # Select sampling rate option
            if self.safe_click(self.SAMPLING_RATE_OPTION):
                self.execute_read()
                rate_text = self.safe_get_text(self.SAMPLING_RATE_VALUE, timeout=5)
                if rate_text:
                    self.logger.info(f"Sampling rate: {rate_text}")
                    return rate_text

            return ""
        except Exception as e:
            self.logger.error(f"Error reading sampling rate: {e}")
            return ""

    def go_back(self) -> bool:
        """
        Navigate back from Read screen.

        Returns:
            True if successful
        """
        self.logger.info("Navigating back from Read screen")
        try:
            # Try back button
            if self.safe_click(self.BACK_BUTTON):
                return True

            # Try close button
            if self.safe_click(self.CLOSE_BUTTON):
                return True

            # Try system back button
            self.driver.back()
            self.logger.info("Used system back button")
            return True

        except Exception as e:
            self.logger.error(f"Error going back: {e}")
            return False

    def get_fw_version_full_flow(self) -> str:
        """
        Complete flow: Select firmware version option and read the value.

        Returns:
            Firmware version string
        """
        self.logger.info("Executing full FW version read flow")
        try:
            # Step 1: Select firmware version option
            if not self.select_firmware_version():
                self.logger.error("Failed to select firmware version option")
                return ""

            # Step 2: Execute read (if needed)
            self.execute_read()

            # Step 3: Read and return version
            fw_version = self.read_fw_version()

            if fw_version:
                self.logger.info(f"Successfully read FW version: {fw_version}")
            else:
                self.logger.warning("FW version read returned empty")

            return fw_version

        except Exception as e:
            self.logger.error(f"Error in FW version full flow: {e}")
            self.take_screenshot("fw_full_flow_error")
            return ""
