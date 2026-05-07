from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web.pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    SUMMARY_ITEMS = (By.CLASS_NAME, "cart_item")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    def get_total(self):
        return self.get_text(self.TOTAL_LABEL)

    def get_item_count(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.SUMMARY_ITEMS))
        except Exception:
            pass
        return len(self.driver.find_elements(*self.SUMMARY_ITEMS))

    def finish_order(self):
        self.click(self.FINISH_BUTTON)
        return self
