"""
UIAutomator2-based driver (No Appium server required!)
Appium 서버 없이 순수 Python으로 Android 제어
"""
import uiautomator2 as u2
import time
import os
from typing import Optional


class U2Driver:
    """Wrapper for uiautomator2 that mimics Appium driver interface."""

    def __init__(self, device_serial: Optional[str] = None):
        """Initialize U2 driver.

        Args:
            device_serial: Android device serial number (optional)
        """
        self.device_serial = device_serial
        self.driver = None

    def connect(self):
        """Connect to Android device."""
        print(f"🔗 Connecting to device...")

        if self.device_serial:
            self.driver = u2.connect(self.device_serial)
        else:
            self.driver = u2.connect()

        print(f"✅ Connected to: {self.driver.info['productName']}")
        return self.driver

    def start_app(self, package_name: str, activity: str):
        """Start Android app."""
        print(f"🚀 Starting app: {package_name}")
        self.driver.app_start(package_name, activity)
        time.sleep(3)  # Wait for app to start

    def stop_app(self, package_name: str):
        """Stop Android app."""
        print(f"🛑 Stopping app: {package_name}")
        self.driver.app_stop(package_name)

    def find_element_by_text(self, text: str, timeout: int = 10):
        """Find element by text."""
        return self.driver(text=text, timeout=timeout)

    def find_element_by_resource_id(self, resource_id: str, timeout: int = 10):
        """Find element by resource ID."""
        return self.driver(resourceId=resource_id, timeout=timeout)

    def find_element_by_xpath(self, xpath: str, timeout: int = 10):
        """Find element by XPath (approximate - u2 doesn't support XPath directly)."""
        # Note: u2 doesn't support XPath, need to convert to u2 selector
        # This is a simplified version
        return None

    def click_by_text(self, text: str, timeout: int = 10):
        """Click element by text."""
        element = self.driver(text=text, timeout=timeout)
        if element.exists:
            element.click()
            return True
        return False

    def click_by_contains_text(self, text: str, timeout: int = 10):
        """Click element that contains text."""
        element = self.driver(textContains=text, timeout=timeout)
        if element.exists:
            element.click()
            return True
        return False

    def get_text(self, selector):
        """Get text from element."""
        if selector.exists:
            return selector.info.get('text', '')
        return ''

    def wait_for_text(self, text: str, timeout: int = 10):
        """Wait for text to appear."""
        return self.driver(text=text).wait(timeout=timeout)

    def screenshot(self, filename: str):
        """Take screenshot."""
        self.driver.screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")

    def press_back(self):
        """Press back button."""
        self.driver.press("back")

    def swipe(self, fx, fy, tx, ty, duration=0.5):
        """Swipe gesture."""
        self.driver.swipe(fx, fy, tx, ty, duration)

    def quit(self):
        """Close connection."""
        if self.driver:
            print("👋 Disconnecting...")
            # U2 doesn't need explicit quit
            self.driver = None


def get_u2_driver(device_serial: Optional[str] = None) -> U2Driver:
    """Get U2 driver instance.

    Args:
        device_serial: Android device serial (optional)

    Returns:
        U2Driver instance
    """
    driver = U2Driver(device_serial)
    driver.connect()
    return driver
