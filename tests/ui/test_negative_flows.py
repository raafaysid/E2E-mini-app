import os, uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:5137")

def _wait_for(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def _wait_for_alert_and_accept(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        text = alert.text  # e.g., "Login failed"
        alert.accept()
        return text
    except Exception:
        return None
    
def login(driver, username="admin", password="fakepass"):
    driver.get(FRONTEND)
    _wait_for(driver, (By.ID, "login-form"))
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-btn").click()

def test_login_invalid_credentials_stays_on_form(driver):
    login(driver, password="wrongpass")
    #expect a JS alert and clear it so Selenium can continue
    msg = _wait_for_alert_and_accept(driver, timeout=5)
    assert msg is None or "failed" in msg.lower()

    #still on login screen
    _wait_for(driver, (By.ID, "login-form"))
def test_item_required_fields_not_added(driver):
    login(driver)
    _wait_for(driver, (By.ID, "logged-in"))
    items_el = driver.find_element(By.ID, "items")
    before = items_el.text

    driver.find_element(By.ID, "add-btn").click()  # submit with no fields

    # Give the UI a moment if it would have added something (shouldn't)
    WebDriverWait(driver, 1).until(lambda d: True)
    after = driver.find_element(By.ID, "items").text

    assert after == before, "Items list changed even though required fields were empty"

def test_price_must_be_numeric(driver):
    login(driver)
    _wait_for(driver, (By.ID, "logged-in"))
    bogus = "BadPrice-" + uuid.uuid4().hex[:4]
    driver.find_element(By.ID, "item-name").send_keys(bogus)
    driver.find_element(By.ID, "item-price").send_keys("ten dollars")
    driver.find_element(By.ID, "add-btn").click()
    items_text = driver.find_element(By.ID, "items").text
    assert bogus not in items_text
