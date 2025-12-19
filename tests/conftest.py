# conftest.py
import pytest
from playwright.sync_api import sync_playwright

from config.settings import get_config
from models.web.login_page import LoginPage

cfg = get_config()


@pytest.fixture
def logged_in_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Faz login
        login = LoginPage(page)
        login.navigate()
        login.login(cfg.USERNAME, cfg.PASSWORD)

        yield page  # entrega a página para os testes

        browser.close()  # fecha ao final do teste
