import pytest
from playwright.sync_api import Page

from config.settings import get_config
from data.data import Customers
from models.web.client_list_page import ClientListPage
from models.web.dashboard_page import DashboardPage

cfg = get_config()


@pytest.mark.frontend
def test_go_to_client_detail(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    client_list_page = ClientListPage(logged_in_page)

    dashboard_page.handle_payment_modal_if_appears()
    # extra debug context
    dashboard_page.page.wait_for_load_state("networkidle")
    dashboard_page.page.context.clear_cookies()  # ensure clean between steps
    dashboard_page.go_to_clients()

    customer_name = Customers.DEFAULT_CUSTOMER
    client_list_page.select_client_by_name(customer_name)
    logged_in_page.screenshot(path="tests/pay_debt.png")
