from pywinauto import keyboard
from pywinauto import Application
import time
import selenium.webdriver as driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
# Launch HP Smart App
keyboard.send_keys("{VK_LWIN}")
keyboard.send_keys("HP Smart")
keyboard.send_keys("{ENTER}")
time.sleep(15)
 
# Connect to HP Smart Main Window
app = Application(backend="uia").connect(title_re="HP Smart")
 
# Get TOP-LEVEL window only
main = app.window(title_re="HP Smart", control_type="Window")
 
main.wait("visible", timeout=40)
main.set_focus()
main.maximize()
 
# Manage HP Account Button
manage_account_btn = main.child_window(
    title="Manage HP Account",
    control_type="Button"
)
manage_account_btn.wait("ready", timeout=30)
manage_account_btn.click_input()
time.sleep(3)  
# Sign Up Button
Sign_in_btn = main.child_window(
    title="Sign in",
    control_type="Button"
 
)
Sign_in_btn.wait("ready", timeout=30)
Sign_in_btn.click_input()
time.sleep(3)  
 
# driver = driver.Chrome()
# driver.switch_to.window(driver.window_handles[-1])
 
 
time.sleep(10)
 
 
 
username_edit = main.child_window(
    title="Username or Email Address",  # text shown in your screenshot
    control_type="Edit"
)
 
# Set text
username_edit.set_edit_text("testqama24+test2911@gmail.com")
# OR: send_keys("testqama24+test2911@gmail.com")
 
print("Username entered successfully!")
time.sleep(2)
use_password_btn = main.child_window(title="Use password", control_type="Button")
use_password_btn.click_input()