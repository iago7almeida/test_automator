# conftest.py
import pytest
from playwright.async_api import async_playwright

from config.settings import get_config
from models.web.login_page import LoginPage

cfg = get_config()


@pytest.fixture
async def logged_in_page():
    async with async_playwright() as p:
        # Lançar navegador
        browser = await p.chromium.launch(headless=cfg.HEADLESS, channel=cfg.BROWSER_CHANNEL)
        context = await browser.new_context(viewport=None if cfg.START_MAXIMIZED else {"width": 1280, "height": 720})
        page = await context.new_page()

        # Login
        login = LoginPage(page)
        await login.navigate()
        await login.login(cfg.USERNAME, cfg.PASSWORD)

        yield page  # entrega a página para os testes

        # Fechar navegador no final
        await browser.close()
