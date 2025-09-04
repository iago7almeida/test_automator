# tests/test_table_operations.py
import pytest
import time
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.tables_page import TablesPage
from pages.order_sheet_page import OrderSheetPage
import os
import dotenv

dotenv.load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

# @pytest.mark.usefixtures("page") # Não é mais necessário se 'page' for um argumento da fixture

def test_create_orders_on_multiple_tables(page: Page): # 'page' vem da fixture em conftest.py
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    #tables_page = TablesPage(page)
    order_sheet = OrderSheetPage(page)

    login_page.navigate_to_login_page()
    login_page.login("teste_teste@gmail.com", "123")
    
    # Esperar que o login seja bem-sucedido navegando para o dashboard
    # e verificando um elemento lá, se necessário (adicionar em LoginPage.login)
    time.sleep(7)
    dashboard_page.navigate_to_tables()

    for i in range(1, 12): # Teste com 2 mesas para ser mais rápido
        print(f"Processando Mesa: {i}")
        order_sheet.add_order_to_table(i)
        # assert tables_page.is_item_added_to_order_sheet(i)
        time.sleep(2)

def test_cancel_order_on_table_1(page: Page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    order_sheet = OrderSheetPage(page)

    login_page.navigate_to_login_page() # Re-login ou assumir estado logado de teste anterior (não ideal para testes unitários)
    login_page.login("teste_teste@gmail.com", "123")
    dashboard_page.navigate_to_tables()

    
    order_sheet._click_table(1) # Abre ou adiciona se já aberta
    time.sleep(2)
    order_sheet.cancel_order_sheet(1)
    # Adicionar asserções para verificar se a comanda foi cancelada
    time.sleep(2)
    
def test_transfer_order_sheets(page: Page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    order_sheet = OrderSheetPage(page)
    
    login_page.navigate_to_login_page() # Re-login ou assumir estado logado de teste anterior (não ideal para testes unitários)
    login_page.login("teste_teste@gmail.com", "123")
    dashboard_page.navigate_to_tables()
    for i in range(1, 10):
        order_sheet.transfer_order_sheet(2)
        time.sleep(2)
        
def test_receive_payment(page: Page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    order_sheet = OrderSheetPage(page)
    
    login_page.navigate()


def test_merge_tabs(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    tables_page = TablesPage(logged_in_page)

    dashboard_page.go_to_tables()

    tables_page.join_tabs_in_a_table()
