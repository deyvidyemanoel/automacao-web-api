cat > web/tests/test_checkout_flow.py << 'EOF'
import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_step_one_page import CheckoutStepOnePage
from web.pages.checkout_step_two_page import CheckoutStepTwoPage
from web.pages.checkout_complete_page import CheckoutCompletePage

pytestmark = pytest.mark.web

VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"


class TestLoginPage:
    def test_login_with_invalid_credentials(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login("invalid_user", "wrong_password")
        assert "Username and password do not match" in login_page.get_error_message()

    def test_login_locked_user(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(LOCKED_USER, PASSWORD)
        assert "locked out" in login_page.get_error_message().lower()

    def test_login_empty_credentials(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login("", "")
        assert "Username is required" in login_page.get_error_message()

    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(VALID_USER, "")
        assert "Password is required" in login_page.get_error_message()

    def test_login_valid_user(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(VALID_USER, PASSWORD)
        assert InventoryPage(driver).get_title() == "Products"


class TestInventory:
    def test_inventory_title(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        assert InventoryPage(driver).get_title() == "Products"

    def test_add_one_item_to_cart(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=1)
        assert inventory_page.get_cart_count() == 1

    def test_cart_badge_updates(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=1)
        assert inventory_page.get_cart_count() >= 1

    def test_go_to_cart(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=1)
        inventory_page.go_to_cart()
        assert CartPage(driver).get_item_count() >= 1


class TestCheckoutFlow:
    def test_login_navigates_to_inventory(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        assert InventoryPage(driver).get_title() == "Products"

    def test_add_products_to_cart(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        assert inventory_page.get_cart_count() == 2

    def test_cart_contains_added_items(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        inventory_page.go_to_cart()
        assert CartPage(driver).get_item_count() == 2

    def test_checkout_step_one_fills_info(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        inventory_page.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        CheckoutStepOnePage(driver).fill_info("Joao", "Silva", "01310100")
        assert CheckoutStepTwoPage(driver).get_item_count() == 2

    def test_order_summary_shows_total(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        inventory_page.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        CheckoutStepOnePage(driver).fill_info("Joao", "Silva", "01310100")
        assert "Total:" in CheckoutStepTwoPage(driver).get_total()

    def test_finish_order_shows_confirmation(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        inventory_page.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        CheckoutStepOnePage(driver).fill_info("Joao", "Silva", "01310100")
        CheckoutStepTwoPage(driver).finish_order()
        assert CheckoutCompletePage(driver).get_confirmation_message() == "Thank you for your order!"

    def test_back_to_products_after_order(self, driver):
        LoginPage(driver).open().login(VALID_USER, PASSWORD)
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)
        inventory_page.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        CheckoutStepOnePage(driver).fill_info("Joao", "Silva", "01310100")
        CheckoutStepTwoPage(driver).finish_order()
        CheckoutCompletePage(driver).back_to_products()
        assert InventoryPage(driver).get_title() == "Products"
EOF