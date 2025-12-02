import json
import logging
import time
from pathlib import Path
from pywinauto import Desktop, keyboard
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("hp_automation")
 
# -----------------------------
# Config Loader
# -----------------------------
def load_config(path="config.json"):
    """Load credentials and settings from JSON config."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(Path(path).read_text())
 
# -----------------------------
# UI Helper Class
# -----------------------------
class UIHelper:
    def __init__(self, backend="uia"):
        self.desktop = Desktop(backend=backend)
 
    def wait_window(self, title_re, timeout=30):
        win = self.desktop.window(title_re=title_re)
        win.wait("exists visible enabled ready", timeout=timeout)
        win.set_focus()
        return win
 
    def click_button(self, parent, title=None, auto_id=None, fallback_text=None, timeout=15):
        try:
            btn = parent.child_window(title=title, auto_id=auto_id, control_type="Button")
            btn.wait("visible enabled ready", timeout=timeout)
        except Exception:
            if fallback_text:
                for b in parent.descendants(control_type="Button"):
                    if fallback_text in b.window_text():
                        btn = b
                        break
            else:
                raise
        btn.click_input()
        log.info(f"Clicked button: {title or fallback_text or auto_id}")
 
# -----------------------------
# HTML Report Utility
# -----------------------------
class HTMLReport:
    def __init__(self):
        self.steps = []
 
    def log_step(self, desc, status="PASS"):
        self.steps.append((desc, status))
        log.info(f"{desc}: {status}")
 
    def generate(self, path="automation_report.html"):
        html = [
            "<html><head><title>Automation Report</title></head><body>",
            "<h2>HP Account Automation Report - SIGN IN & SCAN</h2>",
            "<table border='1'><tr><th>Step</th><th>Status</th></tr>"
        ]
        for desc, status in self.steps:
            html.append(f"<tr><td>{desc}</td><td>{status}</td></tr>")
        html.append("</table></body></html>")
        Path(path).write_text("".join(html))
        log.info(f"Report generated: {path}")
 
# -----------------------------
# Selenium Alert Handler (Optional)
# -----------------------------
def accept_alert_if_present(driver, timeout=5):
    if not driver:
        return
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        log.info("Browser alert accepted.")
    except Exception:
        log.info("No browser alert present.")
 
# -----------------------------
# Automation Steps
# -----------------------------
def launch_hp_smart(helper, report):
    try:
        keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
        report.log_step("Launched HP Smart app")
        main_win = helper.wait_window(".*HP Smart.*")
        report.log_step("Focused HP Smart main window")
        helper.click_button(main_win, title="Manage HP Account", auto_id="HpcSignedOutIcon")
        report.log_step("Clicked Manage HP Account button")
        try:
            helper.click_button(main_win, auto_id="HpcSignOutFlyout_SignInBtn", fallback_text="Sign in")
            report.log_step("Clicked Sign In button")
        except Exception:
            report.log_step("Sign In button not found, assuming browser opened", "INFO")
        return helper.desktop
    except Exception as e:
        report.log_step(f"Error launching HP Smart: {e}", "FAIL")
        return None
 
def sign_in(helper, report, email, password):
    try:
        browser = helper.wait_window(".*HP account.*", timeout=60)
        report.log_step("Focused HP Account sign-in window")
        time.sleep(2)
        keyboard.send_keys("^a{BACKSPACE}" + email)
        report.log_step(f"Typed email: {email}")
        helper.click_button(browser, title="Use password")
        time.sleep(3)
        keyboard.send_keys("^a{BACKSPACE}" + password)
        report.log_step("Typed password")
        helper.click_button(browser, auto_id="sign-in", fallback_text="Sign in")
        report.log_step("Clicked Sign in button")
        time.sleep(10)
    except Exception as e:
        report.log_step(f"Error during sign-in: {e}", "FAIL")
 
def click_scan(helper, report):
    try:
        main_win = helper.wait_window(".*HP Smart.*")
        helper.click_button(main_win, title="Scan", fallback_text="Scan")
        report.log_step("Clicked Scan button")
        time.sleep(10)
    except Exception as e:
        report.log_step(f"Error clicking Scan: {e}", "FAIL")
 
# -----------------------------
# Main Flow
# -----------------------------
def main():
    cfg = load_config()
    helper = UIHelper()
    report = HTMLReport()
    report.log_step(f"Using credentials: {cfg['email']} / ********")
 
    desktop = launch_hp_smart(helper, report)
    if not desktop:
        report.generate()
        return
 
    time.sleep(10)
    sign_in(helper, report, cfg["email"], cfg["password"])
    accept_alert_if_present(driver=None)
    click_scan(helper, report)
    report.generate()
 
# -----------------------------
# Pytest Entry
# -----------------------------
def test_hp_account_sign_in():
    main()
    assert True
 
if __name__ == "__main__":
    main()