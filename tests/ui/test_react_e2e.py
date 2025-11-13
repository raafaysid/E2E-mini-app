import os, uuid, requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:5137")
BACKEND  = os.getenv("BACKEND_URL",  "http://127.0.0.1:8000")  # FastAPI

def test_react_login_and_add_item(driver):
    driver.get(FRONTEND)
    wait = WebDriverWait(driver, 20)

    # Login (UI) 
    wait.until(EC.visibility_of_element_located((By.ID, "login-form")))
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("fakepass")
    driver.find_element(By.ID, "login-btn").click()
    wait.until(EC.visibility_of_element_located((By.ID, "logged-in")))

    #create a UNIQUE item (UI) 
    name = f"Notebook-{uuid.uuid4().hex[:6]}"
    driver.find_element(By.ID, "item-name").send_keys(name)
    driver.find_element(By.ID, "item-price").send_keys("10.5")
    driver.find_element(By.ID, "add-btn").click()

    #DOM oracle: UI shows the new item
    wait.until(EC.text_to_be_present_in_element((By.ID, "items"), name))

    #backend oracle: verify it on the server (API) 
    r = requests.get(f"{BACKEND}/items", timeout=5)
    r.raise_for_status()
    items = r.json()
    assert any(i.get("name") == name and float(i.get("price", 0)) == 10.5 for i in items), \
        "Item not found on server; UI may have updated without real persistence"
