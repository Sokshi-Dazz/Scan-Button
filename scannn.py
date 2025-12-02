from pywinauto import keyboard, Application
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def log(step):
    print(f"\n=== {step} ===")

def pass_msg(msg):
    print(f"✔ PASS: {msg}")

def fail_msg(msg):
    print(f"❌ FAIL: {msg}")


# ==========================================================
# STEP 1: OPEN HP SMART
# ==========================================================
log("Opening HP Smart application")

try:
    keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
    time.sleep(10)

    app = Application(backend="uia").connect(title_re="HP Smart")
    main = app.window(title_re="HP Smart")
    main.set_focus()

    pass_msg("HP Smart launched successfully")
except:
    fail_msg("Failed to launch HP Smart")
    raise


# ==========================================================
# STEP 2: CLICK SCAN
# ==========================================================
log("Clicking SCAN button")

try:
    main.child_window(title_re=".*Scan.*", control_type="Button").wait("visible", timeout=10)
    main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
    pass_msg("Scan clicked successfully")
except:
    fail_msg("Scan button not found")
    raise

time.sleep(2)


# ==========================================================
# STEP 3: CLICK RETURN HOME
# ==========================================================
log("Clicking RETURN HOME button")

try:
    main.child_window(title_re=".*Return Home.*", control_type="Button").wait("visible", timeout=10)
    main.child_window(title_re=".*Return Home.*", control_type="Button").click_input()
    pass_msg("Return Home clicked successfully")
except:
    fail_msg("Return Home button not found")
    raise

time.sleep(2)


# ==========================================================
# STEP 4: CLICK SCAN AGAIN
# ==========================================================
log("Clicking SCAN again")

try:
    main.child_window(title_re=".*Scan.*", control_type="Button").wait("visible", timeout=10)
    main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
    pass_msg("Scan (second time) clicked successfully")
except:
    fail_msg("Scan button not found on second attempt")
    raise

time.sleep(2)



# STEP 5: CLICK GET MORE HELP

log("Clicking GET MORE HELP")

try:
    main.child_window(title_re=".*More Help.*", control_type="Button").wait("visible", timeout=10)
    main.child_window(title_re=".*More Help.*", control_type="Button").click_input()
    pass_msg("Get More Help clicked successfully")
except:
    fail_msg("Get More Help button not found")
    raise

time.sleep(5)



# STEP 6: HANDLE NEW BROWSER TAB (SELENIUM)

log("Switching to new browser tab")

try:
    driver = webdriver.Edge()
    parent = driver.current_window_handle
    time.sleep(2)

    for w in driver.window_handles:
        if w != parent:
            driver.switch_to.window(w)
            break

    pass_msg("Successfully switched to new browser tab")
except:
    fail_msg("Failed to switch to new browser tab")
    raise

# STEP 7: CLICK MODAL CLOSE (X)

log("Closing popup modal using Selenium")

try:
    close_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/ngb-modal-window/div/div/div[1]/button"))
    )
    close_btn.click()
    pass_msg("Close (X) icon clicked successfully")
except:
    fail_msg("Close button not found or not clickable")
    raise


# STEP 8: VALIDATE TEXT "Select your country/region and language"

log("Validating heading text on webpage")

try:
    heading = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Select your country/region and language')]"))
    )
    pass_msg("Heading validated: 'Select your country/region and language' is present")
except:
    fail_msg("Heading text not found")
    raise


# STEP 9: CLICK IMPORT TAB IN HP SMART

log("Switching back to HP Smart to click IMPORT")

try:
    main.set_focus()
    tab = main.child_window(title_re=".*Import.*", control_type="TabItem")
    tab.wait("visible", timeout=10)
    tab.click_input()
    pass_msg("Import tab clicked successfully")
except:
    fail_msg("Import tab not found in HP Smart")
    raise

log("TEST COMPLETED")

