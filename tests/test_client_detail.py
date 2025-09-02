import os
import pytest
from dotenv import load_dotenv
from data.data import Customers
from playwright.sync_api import Page, expect
from pages.client_list_page import ClientListPage 
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

load_dotenv()

def test_go_to_client_detail(page: Page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    client_list_page = ClientListPage(page)

    # --- PRÉ-CONDIÇÃO: FAZER LOGIN ---
    username = os.getenv("HOMOLOG_USER")
    password = os.getenv("HOMOLOG_PASSWORD")

    login_page.navigate()
    login_page.login(username, password)    

    dashboard_page.login_verification_sucessfull()
    dashboard_page.handle_payment_modal_if_appears() 
    dashboard_page.go_to_clients()

    customer_name = Customers.DEFAULT_CUSTOMER
    client_list_page.select_client_by_name(customer_name)
    page.screenshot(path="tests/pay_debt.png")