import logging

import pytest

from config.api_auth import APIAuthManager
from config.settings import get_config

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def api_auth():
    auth = APIAuthManager()
    token = auth.generate_token()
    logger.debug("Fixture api_auth token: %s", token[:50] if token else None)
    return auth


@pytest.fixture(scope="session")
def api_auth_session():
    auth = APIAuthManager()
    token = auth.generate_token()
    logger.debug("Fixture api_auth_session token: %s", token[:50] if token else None)
    return auth


@pytest.mark.backend
def test_gerar_novo_token():
    config = get_config()
    logger.debug("Config API_USERNAME present: %s", bool(config.API_USERNAME))
    logger.debug("Config API_PASSWORD present: %s", bool(config.API_PASSWORD))
    if not (config.API_USERNAME and config.API_PASSWORD):
        pytest.skip("API credentials not configured; skipping token generation test")

    auth = APIAuthManager()
    token = auth.generate_token()
    logger.debug("Generated token: %s", token[:100] if token else None)

    assert token is not None
    assert len(token) > 50
    assert token.startswith("eyJ")


@pytest.mark.backend
def test_token_automatico_em_requisicao():
    config = get_config()
    if not (config.API_USERNAME and config.API_PASSWORD):
        pytest.skip("API credentials not configured; skipping integration test")

    auth = APIAuthManager()
    url = f"{config.API_ADMIN_BASE}/partner/users?limit=5"
    logger.debug("Requesting URL: %s", url)
    response = auth.get(url)
    if response is None:
        logger.error("Authenticated request returned None; headers: %s", auth.get_auth_headers())
        pytest.fail("Authenticated request failed; see logs for details")

    logger.debug("Response status: %s | body: %s", response.status_code, response.text[:500])
    assert response.status_code == 200
