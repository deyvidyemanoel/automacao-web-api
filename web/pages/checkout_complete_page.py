from selenium.webdriver.common.by import By
from web.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_BUTTON = (By.ID, "back-to-products")

    def get_confirmation_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def back_to_products(self):
        self.click(self.BACK_BUTTON)
        return self
