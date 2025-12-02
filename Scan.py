from pywinauto import keyboard
from pywinauto import Application
import time
 
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

# CLICK THE SCAN BUTTON (purple button on your screenshot)

scan_btn = main.child_window(title="Scan", control_type="Button")

# Fallback if needed
if not scan_btn.exists():
    scan_btn = main.child_window(title_re=".*Scan.*", control_type="Button")

scan_btn.wait("ready", timeout=20)
scan_btn.click_input()
time.sleep(3)


# CLICK THE "Return Home" BUTTON

time.sleep(3)  # allow page to load

return_home_btn = main.child_window(title="Return Home", control_type="Button")

# Fallback option using regex
if not return_home_btn.exists():
    return_home_btn = main.child_window(title_re=".*Return Home.*", control_type="Button")

return_home_btn.wait("ready", timeout=20)
return_home_btn.click_input()
time.sleep(3)


# CLICK THE SCAN BUTTON (

scan_btn = main.child_window(title="Scan", control_type="Button")

# Fallback if needed
if not scan_btn.exists():
    scan_btn = main.child_window(title_re=".*Scan.*", control_type="Button")

scan_btn.wait("ready", timeout=20)
scan_btn.click_input()
time.sleep(3)

# CLICK THE "Get More Help" BUTTON

time.sleep(3)  # allow page elements to load

get_help_btn = main.child_window(title="Get More Help", control_type="Button")

# Fallback using regex
if not get_help_btn.exists():
    get_help_btn = main.child_window(title_re=".*More Help.*", control_type="Button")

get_help_btn.wait("ready", timeout=20)
get_help_btn.click_input()
time.sleep(5)  # new tab/popup usually loads

# CLOSE the new help/support window

try:
    # Find any new HP Smart sub-window
    help_win = app.window(title_re=".*Help.*|.*Support.*")

    help_win.wait("visible", timeout=10)
    help_win.set_focus()

    # Click the close button (X)
    help_win.close()
    time.sleep(2)

except:
    print("No help window detected or already closed.")


# Connect to the web browser (Chrome / Edge)
browser = Application(backend="uia").connect(title_re=".*HP.*|.*Support.*|.*Microsoft Edge.*|.*Chrome.*")

# DEFINE win (FIXED)
win = browser.top_window()
win.set_focus()

# Try to locate the X close button on the popup
x_btn = win.child_window(title="Close", control_type="Button")

# If not found, try other possible names
if not x_btn.exists():
    x_btn = win.child_window(title="Dismiss", control_type="Button")

# If still not found, search for the X symbol (× or X)
if not x_btn.exists():
    x_btn = win.child_window(title_re=".*×.*|.*X.*", control_type="Button")

# Final fallback: the first button in the popup
if not x_btn.exists():
    x_btn = win.child_window(control_type="Button", found_index=0)

x_btn.wait("ready", timeout=10)
x_btn.click_input()
time.sleep(1)


# CLICK THE "Import" TAB 

time.sleep(2)

import_tab = main.child_window(title="Import", control_type="TabItem")

# If HP Smart exposes it differently, use fallback
if not import_tab.exists():
    import_tab = main.child_window(title_re=".*Import.*", control_type="TabItem")

import_tab.wait("ready", timeout=20)
import_tab.click_input()
time.sleep(2)




