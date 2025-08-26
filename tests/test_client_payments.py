# tests/test_client_payments.py
import pytest
from playwright.sync_api import Page
import time
from pages.dashboard_page import DashboardPage
from pages.client_list_page import ClientListPage
from pages.client_details_page import ClientDetailsPage

# Dados de teste
CLIENT_PAYMENT_METHODS = ["Cash", "Pix", "Debit", "Credit"]
DEFAULT_PAYMENT_AMOUNT = "3550"

@pytest.mark.client_payments
class TestClientPayments:

    @pytest.fixture(autouse=True)
    def setup_test(self, logged_in_page: Page):
        """
        Setup que usa a fixture logged_in_page.
        O teste já começa logado e na página do dashboard.
        """
        self.page = logged_in_page # A página já está logada
        self.dashboard_page = DashboardPage(self.page)
        self.client_list_page = ClientListPage(self.page)
        self.client_details_page = ClientDetailsPage(self.page)

        # O login já foi feito pela fixture, então só precisamos navegar para a área de clientes
        self.dashboard_page.navigate_to_clients()
        assert self.client_list_page.select_first_client(), "Nenhum cliente encontrado para selecionar."
        # 'yield' não é necessário aqui, pois não há teardown específico
    
    @pytest.mark.parametrize("payment_type", CLIENT_PAYMENT_METHODS)
    def test_receive_client_payment(self, payment_type: str):
        """
        Testa o recebimento de pagamento do cliente com diferentes métodos.
        """
        print(f"Iniciando teste de recebimento de pagamento do cliente com: {payment_type}")

        self.client_details_page.open_receive_payment_modal()
        self.client_details_page.fill_payment_amount(DEFAULT_PAYMENT_AMOUNT)
        self.client_details_page.select_payment_method_client(payment_type)
        self.client_details_page.confirm_receive_payment()
        self.client_details_page.select_do_not_print_receipt()

        print(f"Pagamento do cliente com {payment_type} processado.")
        self.client_details_page.close_client_area_or_modal()

    def test_delete_client_payments(self):
        """
        Testa a exclusão de pagamentos do cliente.
        """
        print("Iniciando teste de exclusão de pagamentos do cliente.")

        deleted_count = self.client_details_page.delete_all_listed_payments()

        if deleted_count > 0:
            print(f"{deleted_count} pagamentos do cliente foram excluídos.")
        else:
            print("Nenhum pagamento do cliente encontrado para exclusão.")

        self.client_details_page.close_client_area_or_modal()
