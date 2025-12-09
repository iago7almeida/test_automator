from playwright.sync_api import sync_playwright

from pages.client_list_page import ClientListPage
from pages.login_page import LoginPage
from pages.new_order_page import NewOrderPage
from pages.order_sheet_page import OrderSheetPage
from pages.tables_page import TablesPage


def test_main_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
        _ = browser.new_context()
        page = browser.new_page()

        login = LoginPage(page)
        _ = TablesPage(page)
        _ = NewOrderPage(page)
        _ = OrderSheetPage(page)
        _ = ClientListPage(page)

        try:
            login.login("teste_teste@gmail.com", "123")
            # table._get_table_selector()

            # table.create_orders(10)
            # table.process_table_payments(10)
            # single.create_all_orders()
            # client_payment.process_client_payments()

            # order_sheet.open_order(1)
            # order_sheet.cancel_order()
            # order_sheet.transfer_order(3)
            # client_payment.delete_all_payments()
        except Exception as e:
            print(f"Erro na automação: {e}")
        finally:
            browser.close()
