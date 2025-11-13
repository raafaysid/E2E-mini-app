import os
import pathlib
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# where failure artifacts go
ARTIFACT_DIR = pathlib.Path("reports") / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    "On test failure, save a screenshot (if UI) and browser console logs (Chrome)."
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or rep.passed:
        return

    #try to get driver if this is a UI test
    driver = item.funcargs.get("driver")
    test_name = item.name.replace("/", "_").replace("\\", "_")

    if driver:
        #screenshot
        png_path = ARTIFACT_DIR / f"{test_name}.png"
        try:
            driver.save_screenshot(str(png_path))
            rep.sections.append(("screenshot", f"Saved: {png_path}"))
        except Exception as e:
            rep.sections.append(("screenshot_error", str(e)))

        #browser console logs (Chrome supports this)
        log_path = ARTIFACT_DIR / f"{test_name}.browser.log"
        try:
            logs = []
            try:
                logs = driver.get_log("browser")
            except Exception:
                #not supported by current browser/driver (like: Safari)
                pass
            with open(log_path, "w", encoding="utf-8") as f:
                for entry in logs:
                    f.write(f"[{entry.get('level')}] {entry.get('message')}\n")
            if logs:
                rep.sections.append(("browser_logs", f"Saved: {log_path}"))
        except Exception as e:
            rep.sections.append(("browser_logs_error", str(e)))

@pytest.fixture
def driver():
    opts = ChromeOptions()
    if os.getenv("HEADED", "0") != "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    # for CI runners
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # enable console log capture for the failure hook
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    opts.set_capability("unhandledPromptBehavior", "dismiss")

    drv = webdriver.Chrome(options=opts)
    try:
        yield drv
    finally:
        drv.quit()
