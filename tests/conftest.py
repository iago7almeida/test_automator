# conftest.py
import pytest
import time
from playwright.sync_api import sync_playwright

from config.settings import get_config
from models.web.login_page import LoginPage
from utils.perfomance_tracker import PerformanceTracker

cfg = get_config()


@pytest.fixture
def logged_in_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Faz login
        login = LoginPage(page)
        login.navigate()
        login.login(cfg.USERNAME, cfg.PASSWORD)

        yield page

        page.close()
        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    start = time.time()
    yield
    duration = time.time() - start

    PerformanceTracker.record(f"TESTE: {item.nodeid}", duration)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    PerformanceTracker.generate_report("relatorio_completo_projeto.csv")
