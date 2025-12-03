import time
from pywinauto import Desktop, keyboard
from utils.logger import log_step
from Pages.homepage import HomePage

def launch_hp_smart():
    try:
        keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
        log_step("Launching HP Smart app")

        desktop = Desktop(backend="uia")
        win = desktop.window(title_re=".*HP Smart.*")
        win.wait("exists visible ready", timeout=30)
        win.set_focus()

        log_step("HP Smart Main window focused")

        btn = win.child_window(**HomePage.manage_hp_account)
        btn.wait("visible ready", timeout=20)
        btn.click_input()
        log_step("Clicked Manage HP Account")

        return desktop

    except Exception as e:
        log_step(f"Launch error: {e}", "FAIL")
        return None
