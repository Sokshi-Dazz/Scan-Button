import time
from pywinauto import Desktop, keyboard
from utils.logger import log_step

class SignInPage:

    def __init__(self):
        self.browser = Desktop(backend="uia").window(title_re=".*HP account.*")

    def wait_and_focus(self):
        self.browser.wait("exists visible ready", timeout=60)
        self.browser.set_focus()
        log_step("Focused HP Account browser window")

    def enter_email(self, email):
        keyboard.send_keys("^a{BACKSPACE}")
        keyboard.send_keys(email, with_spaces=True)
        log_step(f"Typed email: {email}")

    def click_use_password(self):
        btn = self.browser.child_window(title="Use password", control_type="Button")
        btn.wait("visible ready", timeout=30)
        btn.click_input()
        log_step("Clicked Use Password")

    def enter_password(self, password):
        try:
            pwd = self.browser.child_window(auto_id="password", control_type="Edit")
            pwd.wait("visible ready", timeout=20)
        except:
            edits = self.browser.descendants(control_type="Edit")
            pwd = edits[0]
            log_step("Fallback to first Edit for password", "INFO")

        pwd.click_input()
        keyboard.send_keys("^a{BACKSPACE}")
        keyboard.send_keys(password, with_spaces=True)
        log_step("Password typed")

    def click_sign_in(self):
        try:
            btn = self.browser.child_window(auto_id="sign-in", control_type="Button")
            btn.wait("visible ready", timeout=20)
            btn.click_input()
            log_step("Clicked Sign In")
        except:
            for b in self.browser.descendants(control_type="Button"):
                if "Sign in" in b.window_text():
                    b.click_input()
                    log_step("Clicked Sign In fallback")
                    break

        time.sleep(6)

    def sign_in_flow(self, email, password):
        self.wait_and_focus()
        time.sleep(2)
        self.enter_email(email)
        self.click_use_password()
        time.sleep(2)
        self.enter_password(password)
        self.click_sign_in()
