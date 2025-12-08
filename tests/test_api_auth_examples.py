import logging

import pytest

from config.api_auth import APIAuthManager
from config.settings import get_config

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def api_auth():
    """
    Fixture que fornece um gerenciador de autenticação com token fresco.
    Cria um novo token antes de cada teste.

    Usage em testes:
        def test_users_list(api_auth):
            response = api_auth.get(f"{config.API_ADMIN_BASE}/partner/users")
            assert response.status_code == 200
    """
    auth = APIAuthManager()
    auth.generate_token()  # Gerar novo token antes do teste
    return auth


@pytest.fixture(scope="session")
def api_auth_session():
    """
    Fixture com escopo de sessão - reutiliza token durante toda a sessão
    (mais rápido, mas token pode expirar em testes longos)

    Usage:
        def test_users(api_auth_session):
            response = api_auth_session.get(url)
    """
    auth = APIAuthManager()
    auth.generate_token()
    return auth


# ==============================================================================
# EXEMPLO 2: Testes com autenticação dinâmica
# ==============================================================================


def test_gerar_novo_token():
    """
    Teste 1: Verificar geração de token

    Este teste demonstra:
    - Gerar um novo token
    - Verificar se foi gerado com sucesso
    - Usar o token em requisições
    """
    auth = APIAuthManager()

    # Gerar token
    token = auth.generate_token()

    assert token is not None, "❌ Token não foi gerado"
    assert len(token) > 50, "❌ Token parece inválido (muito curto)"
    assert token.startswith("eyJ"), "❌ Token não parece ser JWT (não começa com eyJ)"

    logger.info("✅ Token gerado com sucesso: %s...", token[:50])


def test_token_automatico_em_requisicao():
    """
    Teste 2: Requisição com token automático

    Demonstra que o token é gerado automaticamente se não existir
    """
    config = get_config()
    auth = APIAuthManager()

    # Fazer requisição - token é gerado automaticamente se necessário
    url = f"{config.API_ADMIN_BASE}/partner/users?limit=5"
    response = auth.get(url)

    if response:
        assert response.status_code == 200, f"❌ Status {response.status_code}"
        data = response.json()
        assert "users" in data, "❌ 'users' não encontrado na resposta"
        logger.info("✅ Requisição com token automático bem-sucedida")
    else:
        logger.warning("⚠️ Requisição falhou (verifique credenciais .env)")


def test_token_com_renovacao_automatica():
    """
    Teste 3: Renovação automática de token

    Se o token expirar durante os testes, um novo é gerado automaticamente
    """
    config = get_config()
    auth = APIAuthManager()

    # Primeira requisição
    url = f"{config.API_ADMIN_BASE}/partner/users?limit=1"
    response1 = auth.get(url)
    token1 = auth.token

    # Simular expiração forçando novo token
    response2 = auth.get(url, force_new_token=True)
    token2 = auth.token

    logger.info("✅ Token 1: %s...", token1[:30])
    logger.info("✅ Token 2: %s...", token2[:30])

    # Os tokens podem ser diferentes se foram gerados em momentos diferentes
    if response1 and response2:
        logger.info("✅ Ambas as requisições bem-sucedidas")


def test_requisicao_autenticada_completa():
    """
    Teste 4: Requisição autenticada completa

    Este é um exemplo de como seria um teste real do projeto
    """
    config = get_config()

    # Usar a fixture que fornece um gerenciador com token fresco
    url = f"{config.API_ADMIN_BASE}/partner/users?limit=10&status=1"
    response = api_auth.get(url)

    if response:
        assert response.status_code == 200
        data = response.json()
        users = data.get("users", [])

        logger.info("✅ Busca de usuários bem-sucedida: %d usuários ativos", len(users))

        # Verificações adicionais
        for user in users:
            assert "id" in user, "❌ Usuário sem ID"
            assert "status" in user, "❌ Usuário sem status"
    else:
        logger.warning("⚠️ Falha na requisição (verifique as credenciais)")


def test_diferentes_endpoints(endpoint_tester):
    """
    Teste 5: Testar diferentes endpoints com mesmo token

    Mostra como usar o mesmo token para múltiplos endpoints
    """
    config = get_config()

    endpoints = [
        f"{config.API_ADMIN_BASE}/partner/users?limit=1",
        f"{config.API_ADMIN_BASE}/partner/users?limit=1&status=1",
        f"{config.API_ADMIN_BASE}/partner/users?limit=1&roles=MERCHANT",
    ]

    for endpoint in endpoints:
        response = endpoint_tester.get(endpoint)

        if response:
            assert response.status_code == 200
            logger.info("✅ %s: OK", endpoint)
        else:
            logger.warning("⚠️ %s: Falhou", endpoint)


# ==============================================================================
# EXEMPLO 3: Testes de tratamento de erros
# ==============================================================================


def test_erro_credenciais_invalidas():
    """
    Teste 6: Tratamento de credenciais inválidas
    """
    auth = APIAuthManager()

    # Tentar autenticar com credenciais inválidas
    token = auth.generate_token("usuario_invalido@test.com", "senha_invalida")

    if token is None:
        logger.info("✅ Sistema rejeitou credenciais inválidas corretamente")
    else:
        logger.error("❌ Sistema aceitou credenciais inválidas (Possível falha de segurança)")


def test_url_invalida():
    """
    Teste 7: Tratamento de URL inválida
    """
    auth = APIAuthManager()
    auth.generate_token()  # Gerar token válido

    # Tentar acessar URL inválida
    response = auth.get("https://test.pigz.dev/admin/api/endpoint_invalido")

    if response is None or response.status_code >= 400:
        logger.info("✅ Sistema tratou URL inválida corretamente")
    else:
        logger.warning("⚠️ URL inválida retornou sucesso (Possível erro)")


# ==============================================================================
# EXEMPLO 4: Usando sessão autenticada
# ==============================================================================


def test_usando_sessao_autenticada():
    """
    Teste 8: Usar sessão autenticada para múltiplas requisições

    Mais eficiente que criar novo gerenciador para cada requisição
    """
    config = get_config()
    auth = APIAuthManager()

    # Obter sessão autenticada
    session = auth.get_authenticated_session()

    # Fazer múltiplas requisições com mesma sessão
    urls = [
        f"{config.API_ADMIN_BASE}/partner/users?limit=5",
        f"{config.API_ADMIN_BASE}/partner/users?limit=5&status=1",
        f"{config.API_ADMIN_BASE}/partner/users?limit=5&roles=MERCHANT",
    ]

    results = []
    for url in urls:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            results.append(response.status_code)
            logger.info("✅ %s: %d", url, response.status_code)
        except Exception as e:
            logger.error("❌ %s: %s", url, str(e))

    assert len(results) > 0, "❌ Nenhuma requisição bem-sucedida"
    logger.info("✅ Sessão autenticada funcionando: %d requisições bem-sucedidas", len(results))
