"""Read screen page object for SDK validation app."""
import re
from appium.webdriver.common.appiumby import AppiumBy
from tests.appium.pages.base_page import BasePage


class ReadScreen(BasePage):
    """Page object for Read screen where FW version can be read."""

    # ==================================================
    # IMPORTANT: Customize these locators for your app!
    # ==================================================
    # Use Appium Inspector to identify the correct elements

    # Read screen title/header
    READ_TITLE = (AppiumBy.ID, "com.yourapp:id/read_title")
    READ_TITLE_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'Read')]")

    # Option list items (customize based on your app's structure)
    # Example: ListView, RecyclerView items
    OPTION_LIST = (AppiumBy.ID, "com.yourapp:id/option_list")

    # Firmware version option
    FW_VERSION_OPTION = (AppiumBy.XPATH, "//*[@text='Firmware version']")
    FW_VERSION_OPTION_KR = (AppiumBy.XPATH, "//*[@text='펌웨어 버전']")
    FW_VERSION_OPTION_ID = (AppiumBy.ID, "com.yourapp:id/fw_version_option")

    # Alternative patterns to find firmware option
    FW_OPTION_CONTAINS = (AppiumBy.XPATH, "//*[contains(@text, 'Firmware')]")
    FW_OPTION_CONTAINS_KR = (AppiumBy.XPATH, "//*[contains(@text, '펌웨어')]")

    # Version display (after selecting firmware version)
    VERSION_DISPLAY = (AppiumBy.ID, "com.yourapp:id/version_value")
    VERSION_TEXT = (AppiumBy.ID, "com.yourapp:id/version_text")
    RESULT_TEXT = (AppiumBy.ID, "com.yourapp:id/result_text")

    # Alternative: Generic text view that displays result
    GENERIC_TEXT_VIEW = (AppiumBy.CLASS_NAME, "android.widget.TextView")

    # Buttons
    READ_EXECUTE_BUTTON = (AppiumBy.ID, "com.yourapp:id/read_button")
    BACK_BUTTON = (AppiumBy.ID, "com.yourapp:id/back_button")
    CLOSE_BUTTON = (AppiumBy.XPATH, "//*[@text='Close']")

    # Sampling rate related
    SAMPLING_RATE_OPTION = (AppiumBy.XPATH, "//*[@text='Sampling rate']")
    SAMPLING_RATE_VALUE = (AppiumBy.ID, "com.yourapp:id/sampling_rate_value")

    def __init__(self, driver):
        """Initialize read screen page object."""
        super().__init__(driver)
        self.logger.info("Initialized ReadScreen page object")

    def is_screen_loaded(self, timeout: int = 10) -> bool:
        """
        Check if Read screen is loaded.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if screen loaded
        """
        self.logger.info("Checking if Read screen is loaded")
        try:
            # Try to find Read screen title or option list
            if self.is_element_present(self.READ_TITLE, timeout):
                return True
            if self.is_element_present(self.READ_TITLE_TEXT, timeout):
                return True
            # Check if option list is present
            return self.is_element_present(self.OPTION_LIST, timeout)
        except Exception as e:
            self.logger.error(f"Read screen not loaded: {e}")
            self.take_screenshot("read_screen_not_loaded")
            return False

    def select_firmware_version(self) -> bool:
        """
        Select 'Firmware version' option from the Read menu.

        Returns:
            True if selection successful
        """
        self.logger.info("Selecting Firmware version option")
        try:
            # Try different ways to find and click firmware version option

            # Method 1: Try exact text match (English)
            if self.safe_click(self.FW_VERSION_OPTION):
                self.logger.info("Selected FW version option (exact text)")
                return True

            # Method 2: Try exact text match (Korean)
            if self.safe_click(self.FW_VERSION_OPTION_KR):
                self.logger.info("Selected FW version option (Korean text)")
                return True

            # Method 3: Try by ID
            if self.safe_click(self.FW_VERSION_OPTION_ID):
                self.logger.info("Selected FW version option (by ID)")
                return True

            # Method 4: Try contains text (English)
            if self.safe_click(self.FW_OPTION_CONTAINS):
                self.logger.info("Selected FW version option (contains text)")
                return True

            # Method 5: Try contains text (Korean)
            if self.safe_click(self.FW_OPTION_CONTAINS_KR):
                self.logger.info("Selected FW version option (contains Korean)")
                return True

            # Method 6: Try scrolling to find it
            self.logger.info("Trying to scroll to find FW version option")
            if self.scroll_to_element(self.FW_VERSION_OPTION):
                if self.safe_click(self.FW_VERSION_OPTION):
                    return True

            self.logger.error("Failed to find and click Firmware version option")
            self.take_screenshot("fw_option_not_found")
            return False

        except Exception as e:
            self.logger.error(f"Error selecting firmware version: {e}")
            self.take_screenshot("select_fw_error")
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
        Read the displayed firmware version.

        Args:
            wait_time: Time to wait for version to appear

        Returns:
            Firmware version string or empty string if not found
        """
        self.logger.info("Reading firmware version from display")
        try:
            # Give device time to respond
            import time
            time.sleep(wait_time)

            # Try different ways to find version display

            # Method 1: Dedicated version display element
            version_text = self.safe_get_text(self.VERSION_DISPLAY, timeout=5)
            if version_text:
                fw_version = self._extract_version_from_text(version_text)
                if fw_version:
                    self.logger.info(f"Found FW version: {fw_version}")
                    return fw_version

            # Method 2: Generic version text element
            version_text = self.safe_get_text(self.VERSION_TEXT, timeout=3)
            if version_text:
                fw_version = self._extract_version_from_text(version_text)
                if fw_version:
                    self.logger.info(f"Found FW version in text: {fw_version}")
                    return fw_version

            # Method 3: Result text element
            version_text = self.safe_get_text(self.RESULT_TEXT, timeout=3)
            if version_text:
                fw_version = self._extract_version_from_text(version_text)
                if fw_version:
                    self.logger.info(f"Found FW version in result: {fw_version}")
                    return fw_version

            # Method 4: Search all TextViews for version pattern
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
