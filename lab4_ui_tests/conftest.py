import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.contact_page import ContactPage


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # HEADLESS=1 запускает браузер без окна (удобно для CI)
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        # нужны для запуска Chrome в контейнерах и на Linux-раннерах CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1200,1000")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    yield driver
    driver.quit()


@pytest.fixture
def contact_page(driver):
    return ContactPage(driver).open()
