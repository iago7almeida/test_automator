# ==============================================================================
# API Authentication Manager
# ==============================================================================
# Gerencia autenticação de APIs, geração de tokens e requisições autenticadas
# ==============================================================================

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

import requests

from config.settings import get_config

logger = logging.getLogger(__name__)


class APIAuthManager:
    """
    Gerencia autenticação para APIs.
    - Gera novos tokens
    - Faz requisições autenticadas
    - Gerencia renovação de tokens
    """

    def __init__(self):
        """Inicializa o gerenciador de autenticação."""
        self.config = get_config()
        self.token = None
        self.token_expiry = None
        self.session = requests.Session()
        self._setup_default_headers()

    def _setup_default_headers(self):
        """Configura headers padrão para requisições."""
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "Automation-Test/1.0 (Gestao-Pigz)",
                "Accept": "application/json",
            }
        )

    def generate_token(self, username: Optional[str] = None, password: Optional[str] = None) -> Optional[str]:
        """
        Gera um novo token de autenticação.

        Args:
            username: Username para autenticação (usa config se não fornecido)
            password: Password para autenticação (usa config se não fornecido)

        Returns:
            str: Token JWT gerado
            None: Se falhar na autenticação

        Example:
            >>> auth = APIAuthManager()
            >>> token = auth.generate_token()
            >>> print(f"Token gerado: {token[:50]}...")
        """
        username = username or self.config.API_USERNAME
        password = password or self.config.API_PASSWORD

        if not username or not password:
            logger.error("❌ Credenciais API não configuradas no .env")
            return None

        auth_url = f"{self.config.API_ADMIN_BASE}{self.config.API_AUTH_ENDPOINT}"
        payload = {"username": username, "password": password}

        try:
            logger.info("🔐 Gerando novo token para: %s", username)
            response = self.session.post(auth_url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")

            if not self.token:
                logger.error("❌ Token não encontrado na resposta: %s", data)
                return None

            # Calcular expiração (JWT típico expira em 24h, usar 23h por segurança)
            self.token_expiry = datetime.now() + timedelta(hours=23)

            logger.info("✅ Token gerado com sucesso")
            logger.debug("   Token: %s...", self.token[:50])
            logger.debug("   Expira em: %s", self.token_expiry)

            return self.token

        except requests.exceptions.Timeout:
            logger.error("❌ Timeout ao tentar gerar token: %s", auth_url)
            return None
        except requests.exceptions.HTTPError as e:
            logger.error("❌ Erro HTTP ao gerar token: %s - %s", e.response.status_code, e.response.text)
            return None
        except Exception as e:
            logger.error("❌ Erro ao gerar token: %s", str(e))
            return None

    def get_valid_token(self, force_refresh: bool = False) -> Optional[str]:
        """
        Retorna um token válido, gerando um novo se necessário.

        Args:
            force_refresh: Força geração de novo token mesmo que o atual seja válido

        Returns:
            str: Token válido
            None: Se não conseguir gerar token

        Example:
            >>> auth = APIAuthManager()
            >>> token = auth.get_valid_token()
            >>> # Se token expirou, gera automaticamente um novo
        """
        # Se força refresh ou não tem token ou token expirou
        if force_refresh or not self.token or (self.token_expiry and datetime.now() >= self.token_expiry):
            logger.info("🔄 Token inválido ou expirado, gerando novo...")
            return self.generate_token()

        logger.debug("✅ Token ainda válido")
        return self.token

    def get_auth_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """
        Retorna headers de autenticação com token.

        Args:
            token: Token a usar (usa o gerenciado se não fornecido)

        Returns:
            dict: Headers com Authorization Bearer

        Example:
            >>> auth = APIAuthManager()
            >>> headers = auth.get_auth_headers()
            >>> # Usar em requests: requests.get(url, headers=headers)
        """
        token = token or self.get_valid_token()

        if not token:
            logger.warning("⚠️ Nenhum token disponível")
            return {}

        return {"Authorization": f"Bearer {token}", **self.session.headers}

    def get_authenticated_session(self) -> requests.Session:
        """
        Retorna uma sessão pré-configurada com autenticação.

        Returns:
            requests.Session: Sessão com headers de auth já configurados

        Example:
            >>> auth = APIAuthManager()
            >>> session = auth.get_authenticated_session()
            >>> response = session.get(f"{config.API_ADMIN_BASE}/partner/users")
        """
        session = requests.Session()
        session.headers.update(self.get_auth_headers())
        return session

    def make_authenticated_request(self, method: str, url: str, force_new_token: bool = False, **kwargs) -> Optional[requests.Response]:
        """
        Faz uma requisição autenticada, gerando novo token se necessário.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc)
            url: URL completa para fazer a requisição
            force_new_token: Força geração de novo token antes da requisição
            **kwargs: Args adicionais para requests (json, params, data, etc)

        Returns:
            requests.Response: Resposta da requisição
            None: Se falhar

        Example:
            >>> auth = APIAuthManager()
            >>> response = auth.make_authenticated_request(
            ...     'GET',
            ...     f"{config.API_ADMIN_BASE}/partner/users?limit=10"
            ... )
            >>> if response:
            ...     users = response.json().get('users', [])
        """
        token = self.get_valid_token(force_refresh=force_new_token)

        if not token:
            logger.error("❌ Não conseguiu obter token para autenticação")
            return None

        headers = self.get_auth_headers(token)

        try:
            logger.debug("📡 %s %s", method, url)
            response = self.session.request(method, url, headers=headers, timeout=10, **kwargs)
            response.raise_for_status()

            logger.debug("✅ Resposta: %s", response.status_code)
            return response

        except requests.exceptions.Timeout:
            logger.error("❌ Timeout: %s %s", method, url)
            return None
        except requests.exceptions.HTTPError as e:
            # Se 401 (Unauthorized), tenta com novo token
            if e.response.status_code == 401 and not force_new_token:
                logger.warning("⚠️ Token expirado, tentando com novo token...")
                return self.make_authenticated_request(method, url, force_new_token=True, **kwargs)

            logger.error("❌ Erro HTTP %s: %s", e.response.status_code, e.response.text)
            return None
        except Exception as e:
            logger.error("❌ Erro na requisição: %s", str(e))
            return None

    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """GET autenticado."""
        return self.make_authenticated_request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Optional[requests.Response]:
        """POST autenticado."""
        return self.make_authenticated_request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Optional[requests.Response]:
        """PUT autenticado."""
        return self.make_authenticated_request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Optional[requests.Response]:
        """DELETE autenticado."""
        return self.make_authenticated_request("DELETE", url, **kwargs)
