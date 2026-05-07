from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web.pages.base_page import BasePage

URL = "https://www.saucedemo.com/"

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container h3")

    def open(self):
        self.driver.get(URL)
        return self

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def login_and_wait(self, username, password):
        self.login(username, password)
        self.wait.until(EC.url_contains("inventory"))
        return self

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)