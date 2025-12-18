# ==============================================================================
# Configuration Settings
# ==============================================================================
# Centraliza toda configuração do projeto baseada em ambiente
# Padrão: Strategy Pattern + Singleton
# ==============================================================================

import os
import pathlib
from enum import Enum

from dotenv import load_dotenv

# Carregar variáveis de ambiente
# Prefer env file under envs/hml/.env if present (pytest may not load env_files option).
root = pathlib.Path(__file__).resolve().parents[1]
default_env = root / "envs" / "hml" / ".env"
if default_env.exists():
    load_dotenv(default_env)
else:
    # fallback: load .env at project root if present
    load_dotenv()


class Environment(Enum):
    """Ambientes suportados pelo projeto."""

    HML = "hml"
    PROD = "prod"


class BaseConfig:
    API_USERNAME = os.getenv("API_USERNAME", "")
    API_PASSWORD = os.getenv("API_PASSWORD", "")

    BASE_URL = os.getenv("BASE_URL", "https://gestor.pigz.com.br")

    # URLs APIs
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.pigz.com.br")
    API_ADMIN_BASE = os.getenv("API_ADMIN_BASE", "https://api.pigz.com.br/admin/api")

    # Endpoints específicos
    API_USERS_ENDPOINT = "/partner/users"
    API_ORDERS_ENDPOINT = "/orders"

    # Credenciais Web
    USERNAME = os.getenv("USER_WEB", "")
    PASSWORD = os.getenv("PASSWORD_WEB", "")

    # Credenciais API
    API_USERNAME = os.getenv("API_USER", "")
    API_PASSWORD = os.getenv("API_PASSWORD", "")

    # Token (será gerado dinamicamente)
    API_TOKEN = os.getenv("API_TOKEN", "")

    ENVIRONMENT = Environment.PROD

    # Comportamento geral
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", "chromium")
    START_MAXIMIZED = os.getenv("START_MAXIMIZED", "true").lower() == "true"
    PAGE_ZOOM = int(os.getenv("PAGE_ZOOM", "80"))

    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "5000"))
    LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", "15000"))
    SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", "2000"))

    # Logging & Debug
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "./tests/screenshots")

    # Teste
    PYTEST_WORKERS = int(os.getenv("PYTEST_WORKERS", "1"))
    STOP_ON_FIRST_FAILURE = os.getenv("STOP_ON_FIRST_FAILURE", "false").lower() == "true"


def get_config() -> BaseConfig:
    """
    Retorna a configuração global (Singleton).

    Returns:
        BaseConfig: Configuração do ambiente
    """
    return BaseConfig()
