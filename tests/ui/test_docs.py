import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:8000"

def test_fastapi_docs_loads(driver):
    driver.get(f"{BASE_URL}/docs")

    # wait until the Swagger UI header is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.swagger-ui"))
    )

    page = driver.page_source
    assert "/health" in page
    assert "/login" in page
    assert "/items" in page

    #simple title/content sanity checks
    assert "Swagger UI" in driver.title or "FastAPI" in driver.title
    # verify that the health endpoint appears on the page somewhere
    page_text = driver.page_source
    assert "/health" in page_text

    #save a screenshot artifact
    os.makedirs("reports/screenshots", exist_ok=True)
    driver.save_screenshot("reports/screenshots/docs.png") 