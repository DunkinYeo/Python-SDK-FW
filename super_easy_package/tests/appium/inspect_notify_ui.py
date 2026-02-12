#!/usr/bin/env python3
"""Inspect Notify screen UI structure to find Packet Number element."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import time
from tests.appium.driver import get_driver
from appium.webdriver.common.appiumby import AppiumBy
from xml.dom import minidom

def inspect_notify_screen():
    """Navigate to Notify screen and dump UI structure."""
    print("🔍 Starting UI inspection...")

    driver = get_driver()

    try:
        # Wait for app to load
        print("\n📱 Waiting for app to load...")
        time.sleep(5)

        # Navigate to Notify screen
        print("\n📖 Navigating to Notify screen...")
        notify_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Notify']")
        notify_button.click()
        time.sleep(5)

        # Get page source
        print("\n📄 Dumping page source...")
        page_source = driver.page_source

        # Pretty print XML
        dom = minidom.parseString(page_source)
        pretty_xml = dom.toprettyxml(indent="  ")

        # Save to file
        output_file = "notify_screen_ui.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"\n✅ UI structure saved to: {output_file}")

        # Search for "Packet Number" in the XML
        print("\n🔍 Searching for 'Packet Number' elements...")
        lines = pretty_xml.split('\n')
        packet_lines = [line for line in lines if 'Packet Number' in line or 'packet' in line.lower()]

        if packet_lines:
            print("\n📦 Found lines containing 'Packet Number':")
            for i, line in enumerate(packet_lines, 1):
                print(f"\n{i}. {line.strip()}")
        else:
            print("\n⚠️  No 'Packet Number' elements found in current view")
            print("   The element might be off-screen. Try scrolling first.")

        # Also try to find all TextViews with numbers
        print("\n🔍 Searching for TextViews with numbers...")
        try:
            all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            print(f"\n📋 Found {len(all_texts)} TextViews on screen:")
            for i, elem in enumerate(all_texts[:30], 1):  # Show first 30
                try:
                    text = elem.text
                    if text:
                        print(f"{i}. '{text}'")
                except:
                    pass
        except Exception as e:
            print(f"⚠️  Error getting TextViews: {e}")

    finally:
        print("\n🛑 Closing driver...")
        driver.quit()

if __name__ == "__main__":
    inspect_notify_screen()
