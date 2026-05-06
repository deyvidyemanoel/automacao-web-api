import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Selenium 4.6+ Selenium Manager handles ChromeDriver automatically
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()
