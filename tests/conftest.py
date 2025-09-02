# tests/conftest.py
import pytest
from playwright.sync_api import Page, sync_playwright, Browser
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    # Headless=False para ver a execução, True para rodar em background
    browser = playwright_instance.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.evaluate("document.body.style.zoom='80%'")
    yield page
    context.close()

# --- NOVA FIXTURE DE LOGIN ---
@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """
    Uma fixture que realiza o login e retorna a página já logada.
    Os testes que usarem esta fixture já começarão na dashboard.
    """
    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    # Usa as credenciais importadas do arquivo de configuração
    login_page.login(USER_EMAIL, USER_PASSWORD)
    
    # É uma boa prática esperar por um elemento da página seguinte para garantir que o login funcionou
    page.wait_for_selector('div[hoverlabel="Clientes"]') # Espera por um item do menu do dashboard
    
    yield page
    # O teardown (fechar a página) já é feito pela fixture 'page'
