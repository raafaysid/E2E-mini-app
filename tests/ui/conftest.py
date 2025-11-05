import pytest
from selenium.webdriver import Safari
@pytest.fixture
def driver():
    drv = Safari()
    try:
        yield drv
    finally:
        drv.quit()