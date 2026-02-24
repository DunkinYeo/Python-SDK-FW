"""Utility to automatically handle Android permission dialogs."""
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy


logger = logging.getLogger(__name__)


def handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=3):
    """
    Automatically click 'Allow' on Android permission dialogs.

    Args:
        driver: Appium WebDriver instance
        max_dialogs: Maximum number of permission dialogs to handle
        timeout_per_dialog: Seconds to wait for each dialog

    Returns:
        Number of permission dialogs handled
    """
    logger.info("Starting permission dialog handler...")

    dialogs_handled = 0

    # Common "Allow" button text in different languages
    allow_texts = [
        "Allow",  # English
        "ALLOW",  # English uppercase
        "허용",    # Korean
        "OK",     # Sometimes used
        "확인"     # Korean OK
    ]

    for i in range(max_dialogs):
        logger.info(f"Checking for permission dialog {i+1}/{max_dialogs}...")

        try:
            # Check if we're on a permission activity
            current_activity = driver.current_activity

            if "permission" in current_activity.lower():
                logger.info(f"Permission activity detected: {current_activity}")

                # Try to find and click Allow button
                for allow_text in allow_texts:
                    try:
                        allow_button = driver.find_element(
                            AppiumBy.XPATH,
                            f"//*[@text='{allow_text}']"
                        )

                        logger.info(f"Found '{allow_text}' button, clicking...")
                        allow_button.click()

                        logger.info(f"✅ Permission dialog {i+1} handled")
                        dialogs_handled += 1

                        # Wait a bit for next dialog to appear
                        time.sleep(2)
                        break

                    except Exception:
                        continue
            else:
                # No permission activity, we're done
                logger.info("No more permission dialogs detected")
                break

        except Exception as e:
            logger.debug(f"Error checking for permission dialog: {e}")

        # Brief pause before checking for next dialog
        time.sleep(timeout_per_dialog)

    logger.info(f"Permission handler complete. Handled {dialogs_handled} dialogs.")
    return dialogs_handled


def grant_permissions_via_adb(package_name, device_id=None):
    """
    Grant all dangerous permissions to an app via adb.

    Args:
        package_name: App package name (e.g., 'com.wellysis.spatch.sdk.sample')
        device_id: Device ID (optional, uses default if not specified)

    Returns:
        True if successful
    """
    import subprocess

    logger.info(f"Granting permissions to {package_name} via adb...")

    # Common dangerous permissions
    permissions = [
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.BLUETOOTH_SCAN",
        "android.permission.BLUETOOTH_CONNECT",
        "android.permission.BLUETOOTH_ADVERTISE",
        "android.permission.POST_NOTIFICATIONS",
    ]

    device_arg = ["-s", device_id] if device_id else []

    try:
        for permission in permissions:
            cmd = ["adb"] + device_arg + ["shell", "pm", "grant", package_name, permission]

            logger.debug(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                logger.info(f"✅ Granted: {permission}")
            else:
                # Permission might not be declared in manifest, that's OK
                logger.debug(f"⚠️  Could not grant {permission}: {result.stderr.strip()}")

        logger.info("✅ Permission granting complete")
        return True

    except Exception as e:
        logger.error(f"❌ Error granting permissions via adb: {e}")
        return False
