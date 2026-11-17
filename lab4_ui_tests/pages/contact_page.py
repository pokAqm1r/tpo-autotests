from pathlib import Path

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Page Object для страницы «Обратная связь» (contact.html)."""

    URL = (Path(__file__).parent.parent / "contact.html").resolve().as_uri()

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    SUBJECT = (By.ID, "subject")
    MESSAGE = (By.ID, "message")
    AGREE = (By.ID, "agree")
    SUBMIT = (By.ID, "submit-button")
    FORM = (By.ID, "contact-form")
    SUCCESS = (By.ID, "success-message")

    def open(self):
        super().open(self.URL)
        return self

    def fill_form(self, name="", email="", phone="", subject="",
                  message="", agree=False):
        self.type(self.NAME, name)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        self.select_by_value(self.SUBJECT, subject)
        self.type(self.MESSAGE, message)
        if agree != self.find(self.AGREE).is_selected():
            self.click(self.AGREE)
        return self

    def submit(self):
        self.click(self.SUBMIT)
        return self

    def get_success_message(self):
        return self.find_visible(self.SUCCESS).text

    def get_error(self, field):
        return self.get_text((By.ID, f"{field}-error"))

    def get_all_errors(self):
        fields = ["name", "email", "phone", "subject", "message", "agree"]
        return {field: self.get_error(field) for field in fields}

    def is_form_visible(self):
        return self.find(self.FORM).is_displayed()
