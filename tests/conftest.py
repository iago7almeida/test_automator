import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import os
import dotenv
dotenv.load_dotenv()  # Carrega variáveis de ambiente do arquivo .env



@pytest.fixture
def logged_in_page(page: Page) -> Page:
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    username = os.getenv("HOMOLOG_USER")
    password = os.getenv("HOMOLOG_PASSWORD")

    login_page.navigate()
    login_page.login(username, password)
    
    dashboard_page.login_verification_sucessfull()
    dashboard_page.handle_payment_modal_if_appears()






    yield page  # Fornece a página autenticada para o testes