from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web.pages.base_page import BasePage

URL = "https://www.saucedemo.com/inventory.html"

class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def wait_to_load(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))
        return self

    def add_items_to_cart(self, quantity=2):
        self.wait_to_load()
        for _ in range(quantity):
            buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
            buttons[0].click()
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return self

    def get_cart_count(self):
        return int(self.get_text(self.CART_BADGE))

    def get_title(self):
        self.wait_to_load()
        return self.get_text(self.TITLE)