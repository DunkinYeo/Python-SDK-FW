"""Utility for extracting version information from SDK validation app."""
import logging
from typing import Dict, Optional

from tests.sampling.sampling_utils import parse_version
from tests.appium.pages.main_screen import MainScreen
from tests.appium.pages.read_screen import ReadScreen


class VersionExtractor:
    """Extracts FW/SDK/App version information from the app UI."""

    def __init__(self, driver):
        """
        Initialize version extractor.

        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.main_screen = MainScreen(driver)
        self.read_screen = ReadScreen(driver)

    def extract_fw_version(self) -> str:
        """
        Extract firmware version from app.

        Flow:
        1. Navigate to Read screen
        2. Select "Firmware version" option
        3. Read displayed version

        Returns:
            Firmware version string or "unknown" if extraction fails
        """
        self.logger.info("Extracting firmware version")
        try:
            # Navigate to Read section from main screen
            if not self.main_screen.navigate_to_read_section():
                self.logger.error("Failed to navigate to Read section")
                return "unknown"

            # Wait for Read screen to load
            if not self.read_screen.is_screen_loaded(timeout=10):
                self.logger.error("Read screen did not load")
                return "unknown"

            # Execute full FW version read flow
            fw_version = self.read_screen.get_fw_version_full_flow()

            if fw_version and self.validate_version_format(fw_version):
                self.logger.info(f"Successfully extracted FW version: {fw_version}")
                return fw_version

            self.logger.warning(f"FW version extraction returned invalid value: {fw_version}")
            return "unknown"

        except Exception as e:
            self.logger.error(f"Error extracting FW version: {e}")
            return "unknown"

    def extract_sdk_version(self) -> str:
        """
        Extract SDK version from app.

        Note: SDK version might be same as app version or displayed separately.
        Customize this based on your app's behavior.

        Returns:
            SDK version string or "unknown"
        """
        self.logger.info("Extracting SDK version")
        try:
            # For most apps, SDK version = app version
            # If your app displays SDK version separately, customize this method

            # Method 1: Try to get from app version
            app_version = self.extract_app_version()
            if app_version != "unknown":
                self.logger.info(f"Using app version as SDK version: {app_version}")
                return app_version

            # Method 2: Try to read from Read section if there's a separate option
            # (Uncomment and customize if your app has separate SDK version option)
            # if self.main_screen.navigate_to_read_section():
            #     if self.read_screen.is_screen_loaded():
            #         # Add logic to select and read SDK version
            #         pass

            self.logger.warning("Could not extract SDK version")
            return "unknown"

        except Exception as e:
            self.logger.error(f"Error extracting SDK version: {e}")
            return "unknown"

    def extract_app_version(self) -> str:
        """
        Extract app version from main screen.

        Returns:
            App version string or "unknown"
        """
        self.logger.info("Extracting app version")
        try:
            # Ensure we're on main screen
            if not self.main_screen.is_screen_loaded(timeout=10):
                self.logger.warning("Main screen not loaded, attempting to navigate")
                # Try going back to main screen
                self.driver.back()
                if not self.main_screen.is_screen_loaded(timeout=5):
                    self.logger.error("Cannot load main screen")
                    return "unknown"

            # Get app version from main screen
            app_version = self.main_screen.get_app_version()

            if app_version and app_version != "unknown":
                self.logger.info(f"Successfully extracted app version: {app_version}")
                return app_version

            self.logger.warning("App version not found on main screen")
            return "unknown"

        except Exception as e:
            self.logger.error(f"Error extracting app version: {e}")
            return "unknown"

    def validate_version_format(self, version: str) -> bool:
        """
        Validate that version string is in correct format.

        Args:
            version: Version string to validate

        Returns:
            True if valid version format
        """
        if not version or version == "unknown":
            return False

        try:
            # Try to parse using existing utility
            parse_version(version)
            return True
        except Exception as e:
            self.logger.warning(f"Invalid version format '{version}': {e}")
            return False

    def extract_all_versions(self) -> Dict[str, str]:
        """
        Extract all version information (FW, SDK, App).

        This is the main method to use for complete version extraction.

        Returns:
            Dictionary with platform, fw_version, sdk_version, app_version
        """
        self.logger.info("Extracting all version information")

        versions = {
            "platform": "Android",
            "fw_version": "unknown",
            "sdk_version": "unknown",
            "app_version": "unknown"
        }

        try:
            # Step 1: Extract app version first (less intrusive)
            versions["app_version"] = self.extract_app_version()

            # Step 2: Extract FW version (requires navigation)
            versions["fw_version"] = self.extract_fw_version()

            # Step 3: Extract SDK version (might use app version)
            versions["sdk_version"] = self.extract_sdk_version()

            # Log results
            self.logger.info("Version extraction complete:")
            for key, value in versions.items():
                self.logger.info(f"  {key}: {value}")

            return versions

        except Exception as e:
            self.logger.error(f"Error during version extraction: {e}")
            return versions

    def get_version_dict(self) -> Dict[str, str]:
        """
        Get version dictionary compatible with conftest.py app_env fixture.

        This is an alias for extract_all_versions() for compatibility.

        Returns:
            Dictionary with platform, fw_version, sdk_version, app_version
        """
        return self.extract_all_versions()

    def save_versions_to_file(self, filepath: str) -> bool:
        """
        Extract versions and save to JSON file.

        Args:
            filepath: Path to output JSON file

        Returns:
            True if successful
        """
        import json

        self.logger.info(f"Saving versions to {filepath}")
        try:
            versions = self.extract_all_versions()

            with open(filepath, 'w') as f:
                json.dump(versions, f, indent=2)

            self.logger.info(f"Versions saved successfully to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving versions to file: {e}")
            return False


def extract_versions_from_driver(driver) -> Dict[str, str]:
    """
    Convenience function to extract versions from a driver instance.

    Args:
        driver: Appium WebDriver instance

    Returns:
        Dictionary with version information
    """
    extractor = VersionExtractor(driver)
    return extractor.extract_all_versions()
