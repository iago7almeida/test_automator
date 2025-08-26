# tests/test_single_orders.py
import pytest
import time
from pages.login_page import LoginPage
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.new_order_page import NewOrderPage 


# Dados de teste
SINGLE_ORDER_PAYMENT_METHODS = [
    "OnCustomerAccount", "MealVoucher", "MealGift", "Courtesy",
    "Cash", "Debit", "Pix", "Credit"
]

pytestmark = pytest.mark.single_orders # Marcador para rodar apenas estes testes
class TestSingleOrders:

    @pytest.fixture(autouse=True)
    def setup_teardown_test(self, page: Page):
        self.page = page
        self.login_page = LoginPage(self.page)
        self.dashboard_page = DashboardPage(self.page)
        self.new_order_page = NewOrderPage(self.page) 

        # Setup comum para cada teste
        self.login_page.navigate_to_login_page()
        self.login_page.login("teste_teste@gmail.com", "123")
        # Navegar para a tela de novo pedido é comum a todos os testes aqui
        self.dashboard_page.navigate_to_new_order()
        yield
        # Teardown (se necessário após cada teste)
        print("Teste de pedido avulso concluído.")

    def test_create_single_order_retirada(self):
        """
        Testa a criação de um pedido avulso para retirada.
        Baseado em singleOrder.py > single_order_retirada
        e main.py > process_single_orders (parte)
        """
        print("Iniciando teste de pedido avulso para RETIRADA.")

        self.new_order_page.select_client_for_order() # Método em NewOrderPage
        time.sleep(1) # Do script original
        self.new_order_page.set_order_type_retirada() # Método em NewOrderPage
        time.sleep(1)
        self.new_order_page.add_default_product_to_order() # Ex: clica categoria, clica produto
        time.sleep(1)
        self.new_order_page.proceed_to_payment_or_send_order() # No caso de retirada/delivery sem pagamento obrigatório na tela
        time.sleep(1) # Do script original
        self.new_order_page.confirm_send_order() # Clica em "Enviar Pedido"

        # Adicionar asserções aqui para verificar se o pedido foi criado.
        print("Pedido avulso para RETIRADA processado (simulado).")

    def test_create_single_order_delivery(self):
        """
        Testa a criação de um pedido avulso para delivery.
        Baseado em singleOrder.py > single_order_delivery
        e main.py > process_single_orders (parte)
        """
        print("Iniciando teste de pedido avulso para DELIVERY.")

        self.new_order_page.select_client_for_order()
        time.sleep(0.5) # Do script original
        self.new_order_page.set_order_type_delivery()
        self.new_order_page.add_default_product_to_order()
        #self.new_order_page.proceed_to_payment_or_send_order()
        time.sleep(1) # Do script original
        self.new_order_page.confirm_send_order()

        # Adicionar asserções aqui.
        print("Pedido avulso para DELIVERY processado (simulado).")


    @pytest.mark.parametrize("payment_type", SINGLE_ORDER_PAYMENT_METHODS)
    def test_create_single_order_with_payment(self, payment_type: str):
        """
        Testa a criação de um pedido avulso com diferentes métodos de pagamento.
        Baseado em singleOrder.py > single_order
        e main.py > process_single_orders
        """
        print(f"Iniciando teste de pedido avulso com pagamento: {payment_type}")

        # A lógica de single_order.py para adicionar produto e ir para pagamento
        self.new_order_page.add_default_product_to_order() # Adiciona produto padrão
        self.new_order_page.go_to_payment_screen_single_order() # Clica no botão "Pagamento"

        if payment_type == "OnCustomerAccount":
            time.sleep(0.5) # Do script original
            self.new_order_page.select_client_for_order() # Seleciona cliente se for "Na conta"

        # Selecionar o método de pagamento
        self.new_order_page.select_payment_method_single_order(payment_type) # Método que lida com "OTHERS" também
        time.sleep(0.5) # Do script original

        self.new_order_page.click_launch_payment_button() # Clica em "Lançar"
        self.new_order_page.confirm_send_order() # Clica em "Enviar Pedido"
        time.sleep(1) # Do script original

        # Adicionar asserções aqui.
        print(f"Pedido avulso com pagamento {payment_type} processado (simulado).")