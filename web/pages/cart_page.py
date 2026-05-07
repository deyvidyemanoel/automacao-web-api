from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_count(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.CART_ITEMS))
        except Exception:
            pass
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
