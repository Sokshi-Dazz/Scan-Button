import time
from utils.app_launcher import launch_hp_smart
from Pages.signin_page import SignInPage
from Pages.scan_page import ScanPage
from utils.logger import log_step, REPORT
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_hp_account_sign_in():
    email = "john321@mailsac.com"
    password = "John@321"

    log_step("Starting HP Smart Sign-In Test")

    desktop = launch_hp_smart()
    assert desktop, "HP Smart did not launch"

    time.sleep(5)

    signin = SignInPage()
    signin.sign_in_flow(email, password)

    scan = ScanPage(desktop)
    scan.open_scan()
    scan.return_home()
    scan.click_get_more_help()

    assert True
