# pages/new_order_page.py
import logging

from playwright.sync_api import Page, expect

from config.settings import get_config

logger = logging.getLogger(__name__)


class NewOrderPage:
    """
    Representa a página de criação de um novo pedido no sistema.

    Esta classe encapsula todos os elementos e ações que podem ser realizados
    na tela de criação de pedido, como buscar produtos e avançar para o pagamento.
    """

    def __init__(self, page: Page):
        """
        Inicializa a NewOrderPage.

        Args:
            page: A instância do objeto Page do Playwright.
        """
        self.page = page
        self.config = get_config()

        # --- Localizadores de Elementos ---
        self.search_product_input = page.get_by_placeholder("Busque por produto")
        self.payments_buttons = page.get_by_role("button", name="Pagamentos")
        self.submit_payment_button = page.get_by_role("button", name="Lançar")
        self.customer_search_input = page.get_by_role("complementary").get_by_role("textbox").first

    def navigate(self):
        """
        Navega diretamente para a página de criação de um novo pedido.
        Usa URL centralizada da configuração.
        """
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
        """
        Busca um produto pelo nome e o adiciona ao pedido.

        Args:
            product_name: O nome exato do produto a ser buscado.
        """
        self.search_product_input.fill(product_name)

        # Localiza o resultado da busca que contém o nome do produto e clica nele
        product_result = self.page.get_by_role("button").filter(has_text=product_name)
        expect(product_result).to_be_visible()
        product_result.click()

    def proceed_to_payment(self):
        """
        Clica no botão 'Pagamento' para avançar para a próxima etapa do pedido.
        """
        self.page.get_by_role("button", name="pagamento").click()
