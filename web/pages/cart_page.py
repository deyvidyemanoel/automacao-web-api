from selenium.webdriver.common.by import By
from web.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
