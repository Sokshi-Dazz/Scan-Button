import time
from utils.logger import log_step

class ScanPage:

    def __init__(self, desktop):
        self.desktop = desktop
        self.win = desktop.window(title_re=".*HP Smart.*")

    def open_scan(self):
        self.win.wait("visible ready", timeout=30)
        self.win.set_focus()
        log_step("HP Smart focused before clicking Scan")

        btn = self.win.child_window(title="Scan", control_type="Button")
        btn.wait("visible ready", timeout=20)
        btn.click_input()
        log_step("Clicked Scan button")
        time.sleep(3)

    def return_home(self):
        btn = self.win.child_window(title="Return Home", control_type="Button")
        btn.wait("visible ready", timeout=20)
        btn.click_input()
        log_step("Clicked Return Home")
        time.sleep(3)

    def click_get_more_help(self):
        self.open_scan()
        help_btn = self.win.child_window(
            auto_id="NoContentGridGetMoreHelpBtn",
            control_type="Button"
        )
        help_btn.wait("visible ready", timeout=20)
        help_btn.click_input()
        log_step("Clicked Get More Help")
