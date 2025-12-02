import time
from pywinauto import keyboard, Application
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


# Launch HP Smart App

keyboard.send_keys("{VK_LWIN}")
keyboard.send_keys("HP Smart")
keyboard.send_keys("{ENTER}")
time.sleep(15)
 
# Connect to main HP Smart window
app = Application(backend="uia").connect(title_re="HP Smart")
main = app.window(title_re="HP Smart")
main.wait("visible", timeout=40)
main.set_focus()


# CLICK SCAN

main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
time.sleep(2)

# RETURN HOME
main.child_window(title_re=".*Return Home.*", control_type="Button").click_input()
time.sleep(2)

# SCAN AGAIN
main.child_window(title_re=".*Scan.*", control_type="Button").click_input()
time.sleep(2)

# CLICK MORE HELP
main.child_window(title_re=".*More Help.*", control_type="Button").click_input()
time.sleep(7)



# OPEN CHROME

chrome_driver = r"C:\webdrivers\chromedriver.exe"
service = ChromeService(chrome_driver)
driver = webdriver.Chrome(service=service)

time.sleep(5)

parent = driver.current_window_handle

# Switch to newly opened tab
for w in driver.window_handles:
    if w != parent:
        driver.switch_to.window(w)
        break

print("Switched to HP help page")

time.sleep(3)



# ACCEPT ALERT (IF ANY)

try:
    alert = Alert(driver)
    print("Alert text:", alert.text)
    alert.accept()
    print("Browser alert accepted.")
except NoAlertPresentException:
    print("No browser alert appeared.")



# (NO POPUP-CLOSE BUTTON CLICKING ANYMORE)

print("Skipping popup X button close as requested.")

time.sleep(2)



# SWITCH BACK TO HP SMART

main.set_focus()

# CLICK IMPORT TAB
main.child_window(title_re=".*Import.*", control_type="TabItem").click_input()
time.sleep(2)

print("Script completed successfully.")
