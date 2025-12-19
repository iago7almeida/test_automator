# pylint: disable=invalid-name, raise-missing-from, logging-fstring-interpolation, too-many-public-methods, global-statement
import logging
import os
import pathlib
from enum import Enum
from typing import Any, Callable, Optional, Union

from dotenv import load_dotenv

# Carregar variáveis de ambiente
root = pathlib.Path(__file__).resolve().parents[1]
default_env = root / "envs" / "hml" / ".env"

logger = logging.getLogger(__name__)

if default_env.exists():
    logger.info(f"Carregando variáveis de ambiente do arquivo padrão: {default_env}")
    load_dotenv(default_env)
else:
    load_dotenv()


class Environment(Enum):
    HML = "hml"
    PROD = "prod"


class BaseConfig:
    """
    Classe de configuração com validação, imutabilidade e conversão de tipos.
    """

    def __init__(self):
        # --- Definição de Ambiente ---
        self._environment = Environment.PROD

        # --- 1. Credenciais Web ---
        self._web_username = self._get_env("USER_WEB", required=True)
        self._web_password = self._get_env("PASSWORD_WEB", required=True)

        # --- 2. URLs Base ---
        self._base_url = self._get_env("BASE_URL", required=True)
        self._api_base_url = self._get_env("API_BASE_URL", required=True)
        self._api_admin_base = self._get_env("API_ADMIN_BASE", required=True)

        # --- 3. Credenciais API ---
        self._api_user = self._get_env("API_USER", required=True)
        self._api_password = self._get_env("API_PASSWORD", required=True)
        self._api_token = self._get_env("API_TOKEN", required=False)

        # --- 4. Endpoints ---
        self._api_users_endpoint = "/partner/users"
        self._api_orders_endpoint = "/orders"

        # --- 5. Comportamento Geral (Booleanos limpos) ---
        # Note que agora o default é False (bool) e o cast converte a string do .env
        self._headless = self._get_env("HEADLESS", default=False, cast=self._to_bool)
        self._browser_channel = self._get_env("BROWSER_CHANNEL", default="chrome")
        self._start_maximized = self._get_env("START_MAXIMIZED", default=False, cast=self._to_bool)
        self._page_zoom = self._get_env("PAGE_ZOOM", default=80, cast=int)

        # --- 6. Timeouts ---
        self._default_timeout = self._get_env("DEFAULT_TIMEOUT", default=5000, cast=int)
        self._long_timeout = self._get_env("LONG_TIMEOUT", default=15000, cast=int)
        self._short_timeout = self._get_env("SHORT_TIMEOUT", default=2000, cast=int)

        # --- 7. Logging & Teste ---
        self._log_level = self._get_env("LOG_LEVEL", default="INFO")
        self._screenshot_on_failure = self._get_env("SCREENSHOT_ON_FAILURE", default=True, cast=self._to_bool)
        self._screenshot_path = self._get_env("SCREENSHOT_PATH", default="./tests/screenshots")
        self._pytest_workers = self._get_env("PYTEST_WORKERS", default=1, cast=int)
        self._stop_on_first_failure = self._get_env("STOP_ON_FIRST_FAILURE", default=False, cast=self._to_bool)

    # --------------------------------------------------------------------------
    # Métodos Auxiliares
    # --------------------------------------------------------------------------

    @staticmethod
    def _to_bool(value: Union[str, bool]) -> bool:
        """
        Converte strings comuns de ambiente ("true", "1", "yes") para Booleano real.
        Evita o problema do bool("false") retornar True em Python.
        """
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "t", "yes", "on")

    def _get_env(self, key: str, default: Any = None, required: bool = False, cast: Callable = None) -> Any:
        """Busca variável, valida se vazia (se required) e converte tipo."""
        value = os.getenv(key)

        # Validação de campo vazio/inexistente se for obrigatório
        if required and (value is None or str(value).strip() == ""):
            raise ValueError(f"CRITICAL: Variável '{key}' é obrigatória, mas está vazia ou ausente.")

        if value is None:
            return default

        if cast:
            try:
                return cast(value)
            except ValueError as e:
                raise ValueError(f"Erro de conversão na variável '{key}': {e}")

        return value

    # --------------------------------------------------------------------------
    # Properties (Getters)
    # --------------------------------------------------------------------------

    @property
    def ENVIRONMENT(self) -> Environment:
        return self._environment

    @property
    def BASE_URL(self) -> str:
        return self._base_url

    @property
    def API_BASE_URL(self) -> str:
        return self._api_base_url

    @property
    def API_ADMIN_BASE(self) -> str:
        return self._api_admin_base

    @property
    def USERNAME(self) -> str:
        return self._web_username

    @property
    def PASSWORD(self) -> str:
        return self._web_password

    @property
    def API_USERNAME(self) -> str:
        return self._api_user

    @property
    def API_PASSWORD(self) -> str:
        return self._api_password

    @property
    def API_TOKEN(self) -> Optional[str]:
        return self._api_token

    @property
    def API_USERS_ENDPOINT(self) -> str:
        return self._api_users_endpoint

    @property
    def API_ORDERS_ENDPOINT(self) -> str:
        return self._api_orders_endpoint

    # Propriedades Booleanas
    @property
    def HEADLESS(self) -> bool:
        return self._headless

    @property
    def BROWSER_CHANNEL(self) -> str:
        return self._browser_channel

    @property
    def START_MAXIMIZED(self) -> bool:
        return self._start_maximized

    @property
    def PAGE_ZOOM(self) -> int:
        return self._page_zoom

    @property
    def DEFAULT_TIMEOUT(self) -> int:
        return self._default_timeout

    @property
    def LONG_TIMEOUT(self) -> int:
        return self._long_timeout

    @property
    def SHORT_TIMEOUT(self) -> int:
        return self._short_timeout

    @property
    def LOG_LEVEL(self) -> str:
        return self._log_level

    @property
    def SCREENSHOT_ON_FAILURE(self) -> bool:
        return self._screenshot_on_failure

    @property
    def SCREENSHOT_PATH(self) -> str:
        return self._screenshot_path

    @property
    def PYTEST_WORKERS(self) -> int:
        return self._pytest_workers

    @property
    def STOP_ON_FIRST_FAILURE(self) -> bool:
        return self._stop_on_first_failure


# Singleton
_config_instance = None


def get_config() -> BaseConfig:
    global _config_instance
    if _config_instance is None:
        _config_instance = BaseConfig()
    return _config_instance
