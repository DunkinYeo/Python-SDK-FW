#!/usr/bin/env python3
"""Inspect WriteGet screen UI structure to find correct XPaths."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import time
from tests.appium.driver import get_driver
from appium.webdriver.common.appiumby import AppiumBy
from xml.dom import minidom

def inspect_writeget_screen():
    """Navigate to WriteGet screen and dump UI structure."""
    print("🔍 Starting UI inspection...")

    driver = get_driver()

    try:
        # Wait for app to load
        time.sleep(5)

        # Navigate to WriteGet screen
        print("\n📖 Navigating to WriteGet screen...")
        writeget_button = driver.find_element(AppiumBy.XPATH, "//*[@text='WriteGet']")
        writeget_button.click()
        time.sleep(3)

        # Get page source
        print("\n📄 Getting page source...")
        page_source = driver.page_source

        # Save full page source
        with open('writeget_page_source.xml', 'w', encoding='utf-8') as f:
            # Pretty print XML
            dom = minidom.parseString(page_source)
            f.write(dom.toprettyxml())

        print("✅ Page source saved to: writeget_page_source.xml")

        # Look for Memory Packet Number related elements
        print("\n🔍 Searching for Memory Packet Number elements...")
        print("="*60)

        # Find all elements containing "Memory Packet Number"
        elements = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Memory Packet Number')]")
        for i, elem in enumerate(elements):
            print(f"\nElement {i+1}:")
            print(f"  Text: {elem.text}")
            print(f"  Class: {elem.get_attribute('class')}")
            print(f"  Resource ID: {elem.get_attribute('resource-id')}")
            print(f"  Clickable: {elem.get_attribute('clickable')}")

        # Find all EditText elements
        print("\n🔍 Searching for EditText elements...")
        print("="*60)
        edit_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        for i, edit_text in enumerate(edit_texts):
            print(f"\nEditText {i+1}:")
            print(f"  Text: {edit_text.text}")
            print(f"  Hint: {edit_text.get_attribute('hint')}")
            print(f"  Resource ID: {edit_text.get_attribute('resource-id')}")
            print(f"  Content Description: {edit_text.get_attribute('content-desc')}")

        # Find all Button elements
        print("\n🔍 Searching for Button elements...")
        print("="*60)
        buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        for i, button in enumerate(buttons):
            print(f"\nButton {i+1}:")
            print(f"  Text: {button.text}")
            print(f"  Resource ID: {button.get_attribute('resource-id')}")
            print(f"  Content Description: {button.get_attribute('content-desc')}")

        # Find elements with "WRITE" text
        print("\n🔍 Searching for WRITE elements...")
        print("="*60)
        write_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text='WRITE']")
        for i, elem in enumerate(write_elements):
            print(f"\nWRITE Element {i+1}:")
            print(f"  Class: {elem.get_attribute('class')}")
            print(f"  Resource ID: {elem.get_attribute('resource-id')}")
            print(f"  Clickable: {elem.get_attribute('clickable')}")

        print("\n" + "="*60)
        print("✅ UI inspection complete!")
        print(f"📄 Full page source saved to: writeget_page_source.xml")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n🛑 Closing driver...")
        driver.quit()

if __name__ == "__main__":
    inspect_writeget_screen()
