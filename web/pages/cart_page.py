from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web.pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_CONTAINER = (By.CLASS_NAME, "cart_contents_container")

    def get_item_count(self):
        self.wait.until(EC.presence_of_element_located(self.CART_CONTAINER))
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self