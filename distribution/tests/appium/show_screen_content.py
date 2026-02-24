"""Show all content on current screen."""
from tests.appium.driver import get_driver
from tests.appium.utils.permission_handler import handle_permission_dialogs
from appium.webdriver.common.appiumby import AppiumBy
import time


driver = get_driver()

print("\n🔐 Handling permissions...")
handle_permission_dialogs(driver, max_dialogs=5, timeout_per_dialog=2)

print("\n⏳ Waiting 5 seconds...")
time.sleep(5)

print("\n📝 All text elements on screen:")
print("="*60)

all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
for i, elem in enumerate(all_texts):
    text = elem.text
    if text:
        print(f"{i+1:3}. {text}")

print("="*60)
print(f"\nTotal: {len(all_texts)} text elements")

# Take screenshot
driver.save_screenshot('current_screen.png')
print("\n📸 Screenshot: current_screen.png")

# Save page source
page_source = driver.page_source
with open('current_screen.xml', 'w', encoding='utf-8') as f:
    f.write(page_source)
print("📄 Page source: current_screen.xml")

driver.quit()
