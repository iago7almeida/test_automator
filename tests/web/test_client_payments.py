import pytest
import logging
from playwright.sync_api import Page
from models.web.client_details_page import ClientDetailsPage
from models.web.client_list_page import ClientListPage
from models.web.dashboard_page import DashboardPage

CLIENT_PAYMENT_METHODS = ["Cash", "Pix", "Debit", "Credit"]
DEFAULT_PAYMENT_AMOUNT = "3550"


@pytest.mark.frontend
class TestClientPayments:
    def __init__(self):
        self.page: Page = None
        self.dashboard_page = DashboardPage(self.page)
        self.client_list_page = ClientListPage(self.page)
        self.client_details_page = ClientDetailsPage(self.page)

    @pytest.fixture(autouse=True)
    def setup_test(self, logged_in_page: Page):
        self.page = logged_in_page
        self.dashboard_page = DashboardPage(self.page)
        self.client_list_page = ClientListPage(self.page)
        self.client_details_page = ClientDetailsPage(self.page)

        assert self.client_list_page.select_first_client(), "Nenhum cliente encontrado para selecionar."

    @pytest.mark.parametrize("payment_type", CLIENT_PAYMENT_METHODS)
    def test_receive_client_payment(self, payment_type: str):
        self.client_details_page.open_receive_payment_modal()
        self.client_details_page.fill_payment_amount(DEFAULT_PAYMENT_AMOUNT)
        self.client_details_page.select_payment_method_client(payment_type)
        self.client_details_page.confirm_receive_payment()
        self.client_details_page.select_do_not_print_receipt()

        self.client_details_page.close_client_area_or_modal()

    def test_delete_client_payments(self):
        deleted_count = self.client_details_page.delete_all_listed_payments()

        if deleted_count > 0:
            logging.info(f"{deleted_count} pagamentos do cliente foram excluídos.")
        else:
            logging.info("Nenhum pagamento do cliente encontrado para exclusão.")

        self.client_details_page.close_client_area_or_modal()
