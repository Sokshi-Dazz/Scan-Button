import time
from selenium.webdriver.common.alert import Alert
import re
import random
import string
from pywinauto import Desktop, keyboard
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
 
REPORT = []
def log_step(desc, status="PASS"):
    REPORT.append((desc, status))
    print(f"{desc}: {status}")
 
# -------------------------------------------------------------
#  RANDOM MAILBOX GENERATOR
# -------------------------------------------------------------
def generate_random_mailbox():
    prefix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return prefix + "test"
 
# -------------------------------------------------------------
#  HP SMART LAUNCH & ACCOUNT CREATION
# -------------------------------------------------------------
def launch_hp_smart():
    try:
        keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
        log_step("Sent keys to launch HP Smart app.")
 
        desktop = Desktop(backend="uia")
        main_win = desktop.window(title_re=".*HP Smart.*")
        main_win.wait('exists visible enabled ready', timeout=30)
        main_win.set_focus()
        log_step("Focused HP Smart main window.")
 
        manage_account_btn = main_win.child_window(
            title="Manage HP Account", auto_id="HpcSignedOutIcon", control_type="Button")
        manage_account_btn.wait('visible enabled ready', timeout=15)
        manage_account_btn.click_input()
        log_step("Clicked Manage HP Account button.")
 
        create_account_btn = main_win.child_window(
            auto_id="HpcSignOutFlyout_CreateBtn", control_type="Button")
        create_account_btn.wait('visible enabled ready', timeout=15)
        create_account_btn.click_input()
        log_step("Clicked Create Account button.")
 
        return desktop
 
    except Exception as e:
        log_step(f"Error launching HP Smart: {e}", "FAIL")
        return None
 
def fill_account_form(desktop, email_id):
    try:
        browser_win = desktop.window(title_re=".*HP account.*")
        browser_win.wait('exists visible enabled ready', timeout=30)
        browser_win.set_focus()
        log_step("Focused HP Account browser window.")
 
        browser_win.child_window(auto_id="firstName", control_type="Edit").type_keys("John")
        browser_win.child_window(auto_id="lastName", control_type="Edit").type_keys("Doe")
        browser_win.child_window(auto_id="email", control_type="Edit").type_keys(email_id)
        browser_win.child_window(auto_id="password", control_type="Edit").type_keys("SecurePassword123")
 
        create_btn = browser_win.child_window(auto_id="sign-up-submit", control_type="Button")
        create_btn.wait('visible enabled ready', timeout=10)
        create_btn.click_input()
        log_step("Filled account form and clicked Create button.")
 
        time.sleep(6)
 
    except Exception as e:
        log_step(f"Error filling account form: {e}", "FAIL")
 
# -------------------------------------------------------------
#  FETCH OTP (SELENIUM)
# -------------------------------------------------------------
def fetch_otp_from_mailsac(mailbox_name, max_wait=30, poll_interval=3):
    otp = None
    driver = None
 
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
 
        driver.get("https://mailsac.com")
        log_step("Opened Mailsac website.")
 
        mailbox_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='mailbox']")))
        mailbox_field.send_keys(mailbox_name)
 
        check_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Check the mail!']")))
        check_btn.click()
        log_step("Opened Mailsac inbox.")
 
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                email_row = WebDriverWait(driver, poll_interval).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//table[contains(@class,'inbox-table')]/tbody/tr[contains(@class,'clickable')][1]"))
                )
                email_row.click()
                log_step("Clicked on first email row.")
                break
            except:
                driver.find_element(By.XPATH, "//button[normalize-space()='Check the mail!']").click()
                log_step("Refreshed Mailsac inbox.", "INFO")
 
        body_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#emailBody")))
        email_body = body_elem.text
 
        otp_match = re.search(r"\b(\d{6})\b", email_body)
        if otp_match:
            otp = otp_match.group(1)
            log_step(f"Extracted OTP: {otp}")
        else:
            log_step("OTP not found in email.", "FAIL")
 
        return otp, driver
 
    except Exception as e:
        log_step(f"Error fetching OTP: {e}", "FAIL")
        if driver:
            driver.quit()
        return None, None
 
# -------------------------------------------------------------
#  PASTE OTP USING PYWINAUTO
# -------------------------------------------------------------
def complete_web_verification_in_app(otp):
    try:
        desktop = Desktop(backend="uia")
        otp_window = desktop.window(title_re=".*HP account.*")
        otp_window.wait('exists visible enabled ready', timeout=20)
        otp_window.set_focus()
        log_step("Focused OTP input screen.")
 
        otp_box = otp_window.child_window(auto_id="code", control_type="Edit")
        otp_box.wait('visible enabled ready', timeout=10)
 
        pyperclip.copy(otp)
        time.sleep(1)
 
        otp_box.click_input()
        otp_box.type_keys("^v")
        log_step("OTP pasted successfully.")
 
        verify_btn = otp_window.child_window(auto_id="submit-code", control_type="Button")
        verify_btn.wait('visible enabled ready', timeout=10)
        verify_btn.click_input()
        log_step("Clicked Verify button.")
 
        time.sleep(4)
 
    except Exception as e:
        log_step(f"OTP verification failed: {e}", "FAIL")
 
# -------------------------------------------------------------
def generate_report():
    html = """<html><head><title>Automation Report</title></head><body>
<h2>HP Account Automation Report</h2><table border='1'>
<tr><th>Step</th><th>Status</th></tr>"""
    for desc, status in REPORT:
        html += f"<tr><td>{desc}</td><td>{status}</td></tr>"
    html += "</table></body></html>"
 
    with open("automation_report.html", "w") as f:
        f.write(html)
 
    print("Report generated: automation_report.html")
 
# -------------------------------------------------------------
def main():
    mailbox = generate_random_mailbox()
    email_id = f"{mailbox}@mailsac.com"
    log_step(f"Generated mailbox: {email_id}")
 
    desktop = launch_hp_smart()
    if desktop:
        fill_account_form(desktop, email_id)
 
    otp, driver = fetch_otp_from_mailsac(mailbox)
 
    if otp:
        complete_web_verification_in_app(otp)
 
    # ---------------------------------------------------------
    # FIXED ALERT HANDLING
    # ---------------------------------------------------------
    if driver:
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            log_step("Browser alert accepted.")
        except TimeoutException:
            log_step("No alert appeared in the browser.", "INFO")
        except NoAlertPresentException:
            log_step("Alert disappeared before handling.", "INFO")
        except Exception as e:
            log_step(f"Alert handling error: {e}", "FAIL")
 
        driver.quit()
 
    generate_report()
 
if __name__ == "__main__":
    main()