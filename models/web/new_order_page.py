import logging
from playwright.sync_api import Page, expect
from config.settings import get_config


class NewOrderPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()

        self.search_product_input = page.get_by_placeholder("Busque por produto")
        self.payments_buttons = page.get_by_role("button", name="Pagamentos")
        self.submit_payment_button = page.get_by_role("button", name="Lançar")
        self.customer_search_input = self.page.locator("label").filter(has_text="Nome do cliente").locator("..").locator("input").first

        self.asside_side = page.locator("aside", has_text="Balcão")


    def navigate(self):
        url = f"{self.config.BASE_URL}/createSingleOrder"
        logging.info("📍 Navegando para: %s", url)
        self.page.goto(url)

    def select_order_type_balcony(self):
        pass

    def select_order_type_withdrawal(self):
        self.page.get_by_text("Retirada", exact=True).click()
        


    def select_order_type_delivery(self):
        self.page.get_by_text("Delivery", exact=True).click()

    def search_and_select_customer(self, customer_name: str):
        self.customer_search_input.click()
        self.customer_search_input.fill(customer_name)
        customer_result = self.asside_side.locator("div")\
            .filter(has_text=customer_name)\
            .filter(has_text="Saldo")\
            .last
        self.customer_search_input.click()
        expect(customer_result).to_be_visible(timeout=60000)
        customer_result.hover()
        customer_result.click()

    def add_product_to_order(self, product_name: str):
        self.search_product_input.wait_for(state="visible")
        self.search_product_input.click()
        self.search_product_input.fill(product_name)
        self.product_result = self.page.locator("button").filter(has_text=product_name)
        
        self.product_result.click()
        self.page.wait_for_timeout(300)

    def proceed_to_payment(self):
        self.page.get_by_role("button", name="pagamento").click()
