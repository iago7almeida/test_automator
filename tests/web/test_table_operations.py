import time

import pytest
from playwright.sync_api import Page

from config.settings import get_config
from models.web.dashboard_page import DashboardPage
from models.web.login_page import LoginPage
from models.web.order_sheet_page import OrderSheetPage
from models.web.tables_page import TablesPage



@pytest.mark.frontend
def test_create_orders_on_multiple_tables(logged_in_page):
    dashboard = DashboardPage(logged_in_page)
    order_sheet = OrderSheetPage(logged_in_page)
    time.sleep(2)
    dashboard.go_to_tables()    
    for i in range(1, 12):
        print(f"Processando Mesa: {i}")
        order_sheet.add_item_to_table(i)
        time.sleep(2)


@pytest.mark.frontend
def test_cancel_order_on_table_1(page: Page):
    login_page = LoginPage(page)
    order_sheet = OrderSheetPage(page)

    login_page.navigate_to_login_page()
    login_page.login("teste_teste@gmail.com", "123")

    time.sleep(2)
    order_sheet.cancel_order_sheet(1)
    time.sleep(2)


@pytest.mark.frontend
def test_transfer_order_sheets(page: Page):
    login_page = LoginPage(page)
    _ = DashboardPage(page)
    order_sheet = OrderSheetPage(page)

    login_page.navigate_to_login_page()
    login_page.login("teste_teste@gmail.com", "123")
    for _ in range(1, 10):
        order_sheet.transfer_order_sheet(2)
        time.sleep(2)


@pytest.mark.frontend
def test_receive_payment(page: Page):
    login_page = LoginPage(page)
    _ = DashboardPage(page)
    _ = OrderSheetPage(page)

    login_page.navigate()


@pytest.mark.frontend
def test_merge_tabs(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    tables_page = TablesPage(logged_in_page)

    dashboard_page.go_to_tables()

    tables_page.join_tabs_in_a_table()
