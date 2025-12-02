import time
from pywinauto import keyboard, Application
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LAUNCH HP SMART

keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
time.sleep(10)

app = Application(backend="uia").connect(title_re="HP Smart")
main = app.window(title_re="HP Smart")
main.set_focus()


# CLICK SCAN

main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
time.sleep(2)


# CLICK RETURN HOME

main.child_window(title_re=".*Return Home.*", control_type="Button").click_input()
time.sleep(2)


# CLICK SCAN AGAIN

main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
time.sleep(2)


# CLICK MORE HELP

main.child_window(title_re=".*More Help.*", control_type="Button").click_input()
time.sleep(7)


# BROWSER HANDLING

driver = webdriver.Edge()      # or webdriver.Chrome()
time.sleep(5)

parent = driver.current_window_handle

# Switch to newly opened tab
for w in driver.window_handles:
    if w != parent:
        driver.switch_to.window(w)
        break

print("Switched to HP help page")

time.sleep(3)

# -------------------------------
# CLOSE REGION/LANGUAGE POPUP
# -------------------------------

try:
    close_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//button[@aria-label='Close' "
             "or contains(@class,'close') "
             "or .//*[text()='×']]")
        )
    )
    close_btn.click()
    print("Closed region/language selector popup successfully")

except Exception as e:
    print("Close button not found:", e)

time.sleep(3)

# -------------------------------
# SWITCH BACK TO HP SMART
# -------------------------------
main.set_focus()

# -------------------------------
# CLICK IMPORT TAB
# -------------------------------
main.child_window(title_re=".*Import.*", control_type="TabItem").click_input()
time.sleep(2)

print("Script completed successfully.")
