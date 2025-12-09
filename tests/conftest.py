# ==============================================================================
# Pytest Configuration & Fixtures
# ==============================================================================
# Centraliza todas as configurações e fixtures do pytest para os testes
# ==============================================================================

import logging

import pytest
from playwright.sync_api import Page

from config.settings import get_config
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

# ==============================================================================
# Configuração de Logging
# ==============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ==============================================================================
# Pytest Hooks para Relatórios
# ==============================================================================


def pytest_configure(_):
    """Hook chamado após parsing de argumentos linha de comando."""
    config_obj = get_config()
    logger.info("Iniciando testes no ambiente: %s", config_obj.ENVIRONMENT.value.upper())
    logger.info("Base URL: %s", config_obj.BASE_URL)


def pytest_collection_modifyitems(_, items):
    """Hook para modificar items coletados."""
    # Adicionar marcador para testes que usam fixture 'page'
    for item in items:
        if "page" in item.fixturenames:
            item.add_marker(pytest.mark.browser)


# ==============================================================================
# Fixtures - Browser Configuration
# ==============================================================================


@pytest.fixture(scope="session")
def browser_context_args():
    """Configuração de contexto do navegador."""
    config = get_config()

    return {
        "no_viewport": not config.START_MAXIMIZED,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def playwright_context_args():
    """Argumentos passados ao playwright."""
    config = get_config()

    return {
        "headless": config.HEADLESS,
        "channel": config.BROWSER_CHANNEL,
    }


# ==============================================================================
# Fixtures - Page Setup
# ==============================================================================


@pytest.fixture(autouse=True)
def _setup_page_zoom(page: Page):
    """Fixture automática que ajusta o zoom da página para cada teste."""
    config = get_config()
    page.evaluate(f"document.body.style.zoom='{config.PAGE_ZOOM}%'")
    yield page


# ==============================================================================
# Fixtures - Authentication
# ==============================================================================


@pytest.fixture
def logged_in_page(page: Page):
    """
    Fixture que fornece uma página autenticada.

    Retorna a página já logada e pronta para usar nos testes.
    Exemplo:
        def test_example(logged_in_page: Page):
            dashboard_page = DashboardPage(logged_in_page)
            dashboard_page.go_to_new_order()
    """
    config = get_config()
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    logger.info("Iniciando login com usuário: %s", config.USERNAME)

    try:
        login_page.navigate()
        login_page.login(config.USERNAME, config.PASSWORD)

        dashboard_page.login_verification_sucessfull()
        dashboard_page.handle_payment_modal_if_appears()

        logger.info("Login realizado com sucesso")
    except Exception as e:
        logger.error("Erro durante login: %s", e)
        raise

    yield page  # Fornece a página autenticada para o testes
