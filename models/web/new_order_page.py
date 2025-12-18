import logging

from playwright.sync_api import Page, expect

from config.settings import get_config

logger = logging.getLogger(__name__)


class NewOrderPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()

        self.search_product_input = page.get_by_placeholder("Busque por produto")
        self.payments_buttons = page.get_by_role("button", name="Pagamentos")
        self.submit_payment_button = page.get_by_role("button", name="Lançar")
        self.customer_search_input = page.get_by_role("complementary").get_by_role("textbox").first

    def navigate(self):
        url = f"{self.config.BASE_URL}/createSingleOrder"
        logger.info("📍 Navegando para: %s", url)
        self.page.goto(url)

    def select_order_type_balcony(self):
        pass

    def select_order_type_withdrawal(self):
        self.page.get_by_text("Retirada").click()

    def select_order_type_delivery(self):
        self.page.get_by_text("Delivery").click()

    def search_and_select_customer(self, customer_name: str):
        self.customer_search_input.click()
        self.customer_search_input.fill(customer_name)
        customer_result = self.page.locator("div.sc-cfd510a4-8.fNDSsg").filter(has_text=customer_name)
        self.customer_search_input.click()
        expect(customer_result).to_be_visible(timeout=6000)
        customer_result.hover()
        customer_result.click()

    def add_product_to_order(self, product_name: str):
        self.search_product_input.fill(product_name)
        product_result = self.page.get_by_role("button").filter(has_text=product_name)
        expect(product_result).to_be_visible()
        product_result.click()

    def proceed_to_payment(self):
        self.page.get_by_role("button", name="pagamento").click()
