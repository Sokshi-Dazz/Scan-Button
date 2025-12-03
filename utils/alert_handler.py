from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log_step

def accept_alert_if_present(driver, timeout=5):
    if not driver:
        return
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        log_step("Browser alert detected.")
        alert.accept()
        log_step("Browser alert accepted.")
    except:
        log_step("No browser alert present", "INFO")
