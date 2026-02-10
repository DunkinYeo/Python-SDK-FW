"""Base page object with common utilities for all page objects."""
import logging
import os
from datetime import datetime
from typing import Tuple, Optional

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException
)


class BasePage:
    """Base class for all page objects with common utilities."""

    def __init__(self, driver, timeout: int = 10):
        """
        Initialize base page.

        Args:
            driver: Appium WebDriver instance
            timeout: Default timeout in seconds for waits
        """
        self.driver = driver
        self.default_timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screenshot_dir = "screenshots"
        self._ensure_screenshot_dir()

    def _ensure_screenshot_dir(self):
        """Ensure screenshot directory exists."""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    # ========== Wait Strategies ==========

    def wait_for_element(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ):
        """
        Wait for element to be present in DOM.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Custom timeout in seconds

        Returns:
            WebElement if found

        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self.default_timeout
        try:
            self.logger.debug(f"Waiting for element: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {locator}")
            self.take_screenshot(f"timeout_{locator[1]}")
            raise

    def wait_for_element_visible(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ):
        """
        Wait for element to be visible.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Custom timeout in seconds

        Returns:
            WebElement if visible
        """
        timeout = timeout or self.default_timeout
        try:
            self.logger.debug(f"Waiting for element to be visible: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            self.take_screenshot(f"not_visible_{locator[1]}")
            raise

    def wait_for_element_clickable(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ):
        """
        Wait for element to be clickable.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Custom timeout in seconds

        Returns:
            WebElement if clickable
        """
        timeout = timeout or self.default_timeout
        try:
            self.logger.debug(f"Waiting for element to be clickable: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            self.logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            self.take_screenshot(f"not_clickable_{locator[1]}")
            raise

    def wait_for_text_in_element(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for specific text to appear in element.

        Args:
            locator: Tuple of (By strategy, value)
            text: Expected text
            timeout: Custom timeout in seconds

        Returns:
            True if text found within timeout
        """
        timeout = timeout or self.default_timeout
        try:
            self.logger.debug(f"Waiting for text '{text}' in element: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.text_to_be_present_in_element(locator, text))
            self.logger.debug(f"Text '{text}' found in element: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Text '{text}' not found in element: {locator}")
            return False

    # ========== Element Finding ==========

    def find_element_by_id(self, element_id: str):
        """Find element by resource ID."""
        locator = (AppiumBy.ID, element_id)
        return self.wait_for_element(locator)

    def find_element_by_xpath(self, xpath: str):
        """Find element by XPath."""
        locator = (AppiumBy.XPATH, xpath)
        return self.wait_for_element(locator)

    def find_element_by_accessibility_id(self, accessibility_id: str):
        """Find element by accessibility ID."""
        locator = (AppiumBy.ACCESSIBILITY_ID, accessibility_id)
        return self.wait_for_element(locator)

    def find_element_by_text(self, text: str, exact: bool = True):
        """
        Find element by text content.

        Args:
            text: Text to search for
            exact: If True, match exact text. If False, match contains.

        Returns:
            WebElement
        """
        if exact:
            xpath = f"//*[@text='{text}']"
        else:
            xpath = f"//*[contains(@text, '{text}')]"
        locator = (AppiumBy.XPATH, xpath)
        return self.wait_for_element(locator)

    def find_elements_by_class(self, class_name: str):
        """Find all elements with given class name."""
        return self.driver.find_elements(AppiumBy.CLASS_NAME, class_name)

    # ========== Safe Interactions ==========

    def safe_click(
        self,
        locator: Tuple[str, str],
        retries: int = 3,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Safely click element with retry logic.

        Args:
            locator: Tuple of (By strategy, value)
            retries: Number of retry attempts
            timeout: Custom timeout in seconds

        Returns:
            True if click succeeded, False otherwise
        """
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                element.click()
                self.logger.info(f"Clicked element: {locator}")
                return True
            except (StaleElementReferenceException, WebDriverException) as e:
                self.logger.warning(
                    f"Click attempt {attempt + 1}/{retries} failed: {e}"
                )
                if attempt == retries - 1:
                    self.logger.error(f"Failed to click after {retries} attempts")
                    self.take_screenshot(f"click_failed_{locator[1]}")
                    return False
        return False

    def safe_send_keys(
        self,
        locator: Tuple[str, str],
        text: str,
        clear_first: bool = True
    ) -> bool:
        """
        Safely send keys to element.

        Args:
            locator: Tuple of (By strategy, value)
            text: Text to send
            clear_first: Whether to clear field before sending keys

        Returns:
            True if successful
        """
        try:
            element = self.wait_for_element_visible(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys to element: {locator}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send keys: {e}")
            self.take_screenshot(f"sendkeys_failed_{locator[1]}")
            return False

    def safe_get_text(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> Optional[str]:
        """
        Safely get text from element.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Custom timeout in seconds

        Returns:
            Element text or None if failed
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            text = element.text
            self.logger.debug(f"Got text from {locator}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            self.take_screenshot(f"gettext_failed_{locator[1]}")
            return None

    def is_element_present(
        self,
        locator: Tuple[str, str],
        timeout: int = 3
    ) -> bool:
        """
        Check if element is present without throwing exception.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Timeout in seconds

        Returns:
            True if element present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_visible(
        self,
        locator: Tuple[str, str],
        timeout: int = 3
    ) -> bool:
        """
        Check if element is visible without throwing exception.

        Args:
            locator: Tuple of (By strategy, value)
            timeout: Timeout in seconds

        Returns:
            True if element visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ========== Screenshot Utilities ==========

    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot with timestamp.

        Args:
            name: Base name for screenshot

        Returns:
            Path to screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save screenshot: {e}")
            return ""

    # ========== Scroll Utilities ==========

    def scroll_down(self, duration: int = 500):
        """
        Scroll down on screen.

        Args:
            duration: Duration of scroll in milliseconds
        """
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.8
            end_y = size['height'] * 0.2

            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            self.logger.debug("Scrolled down")
        except Exception as e:
            self.logger.error(f"Failed to scroll down: {e}")

    def scroll_up(self, duration: int = 500):
        """
        Scroll up on screen.

        Args:
            duration: Duration of scroll in milliseconds
        """
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.2
            end_y = size['height'] * 0.8

            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            self.logger.debug("Scrolled up")
        except Exception as e:
            self.logger.error(f"Failed to scroll up: {e}")

    def scroll_to_element(
        self,
        locator: Tuple[str, str],
        max_scrolls: int = 5
    ) -> bool:
        """
        Scroll until element is visible.

        Args:
            locator: Tuple of (By strategy, value)
            max_scrolls: Maximum number of scroll attempts

        Returns:
            True if element found, False otherwise
        """
        for i in range(max_scrolls):
            if self.is_element_visible(locator, timeout=2):
                self.logger.info(f"Element found after {i} scrolls")
                return True
            self.scroll_down()

        self.logger.warning(f"Element not found after {max_scrolls} scrolls")
        return False
