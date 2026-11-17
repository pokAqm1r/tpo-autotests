from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    """Общие действия, которые нужны любой странице."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(
            expected_conditions.presence_of_element_located(locator)
        )

    def find_visible(self, locator):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def click(self, locator):
        self.wait.until(expected_conditions.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_value(self, locator, value):
        Select(self.find(locator)).select_by_value(value)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        return self.find(locator).is_displayed()
