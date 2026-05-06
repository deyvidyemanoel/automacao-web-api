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

        error = login_page.get_error_message()
        assert "Username and password do not match" in error

    def test_login_locked_user(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(LOCKED_USER, PASSWORD)

        error = login_page.get_error_message()
        assert "locked out" in error.lower()


class TestCheckoutFlow:
    """Full E2E: login → add to cart → checkout → order confirmation."""

    def test_login_navigates_to_inventory(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(VALID_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.get_title() == "Products"

    def test_add_products_to_cart(self, driver):
        inventory_page = InventoryPage(driver)
        inventory_page.add_items_to_cart(quantity=2)

        assert inventory_page.get_cart_count() == 2

    def test_cart_contains_added_items(self, driver):
        InventoryPage(driver).go_to_cart()
        cart_page = CartPage(driver)

        assert cart_page.get_item_count() == 2

    def test_checkout_step_one_fills_info(self, driver):
        CartPage(driver).proceed_to_checkout()
        CheckoutStepOnePage(driver).fill_info("Joao", "Silva", "01310100")

        # reaching step two validates step one succeeded
        step_two = CheckoutStepTwoPage(driver)
        assert step_two.get_item_count() == 2

    def test_order_summary_shows_total(self, driver):
        step_two = CheckoutStepTwoPage(driver)
        total = step_two.get_total()

        assert "Total:" in total

    def test_finish_order_shows_confirmation(self, driver):
        CheckoutStepTwoPage(driver).finish_order()
        complete_page = CheckoutCompletePage(driver)

        assert complete_page.get_confirmation_message() == "Thank you for your order!"

    def test_back_to_products_after_order(self, driver):
        CheckoutCompletePage(driver).back_to_products()
        inventory_page = InventoryPage(driver)

        assert inventory_page.get_title() == "Products"
