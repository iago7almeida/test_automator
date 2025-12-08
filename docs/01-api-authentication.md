# 🔐 API Authentication System

## Visão Geral

Sistema de **tokens dinâmicos** que gera automaticamente novos tokens, renovando quando expiram.

### Antes vs Depois

```python
# ❌ ANTES - Inseguro (Hardcoded)
Authorization: "Bearer eyJ0eXAi..."  # Token no código!
BASE_URL = "https://test.pigz.dev"  # URL no código!

# ✅ DEPOIS - Seguro (Dinâmico)
auth = APIAuthManager()
response = auth.get(f"{config.API_ADMIN_BASE}/users")  # Tudo automático!
```

## Setup em 2 Minutos

1. **Configure .env:**
```bash
cp .env.example .env
# Editar com suas credenciais:
HML_API_USER=seu_email@pigz.com.br
HML_API_PASSWORD=sua_senha
```

2. **Use em seu código:**
```python
from config.api_auth import APIAuthManager
from config.settings import get_config

auth = APIAuthManager()
config = get_config()

# GET automático com token
response = auth.get(f"{config.API_ADMIN_BASE}/partner/users")
```

## Funcionalidades

| Feature | Descrição |
|---------|-----------|
| 🔐 Token Automático | Gera novo token na primeira requisição |
| 🔄 Renovação Auto | Renova quando expira (sem intervenção) |
| 📍 URLs Dinâmicas | Muda conforme ambiente (HML/PROD) |
| 🔁 Retry em 401 | Tenta automaticamente com novo token |
| 📝 Logging | Registra todas as operações |
| 🛡️ Multi-Ambiente | Suporta HML e PROD |

## Métodos Disponíveis

```python
auth = APIAuthManager()

# HTTP básico (token automático)
auth.get(url)           # GET
auth.post(url, json={}) # POST
auth.put(url, json={})  # PUT
auth.delete(url)        # DELETE

# Token manual
token = auth.generate_token()              # Gera novo
token = auth.get_valid_token()             # Obtém válido
headers = auth.get_auth_headers(token)     # Headers com Bearer

# Sessão reutilizável
session = auth.get_authenticated_session()
session.get(url)
session.post(url, json={})
```

## Em Testes (Pytest)

```python
import pytest
from config.api_auth import APIAuthManager

@pytest.fixture
def api():
    """Fixture que fornece auth com token fresco"""
    auth = APIAuthManager()
    auth.generate_token()
    return auth

def test_list_users(api):
    response = api.get(f"{config.API_ADMIN_BASE}/partner/users")
    assert response.status_code == 200
    assert 'users' in response.json()
```

## Variáveis de Ambiente

```dotenv
# Obrigatório - Credenciais
HML_API_USER=seu_email@pigz.com.br
HML_API_PASSWORD=sua_senha

# Automático - URLs (já configuradas)
HML_API_BASE_URL=https://test.pigz.dev
HML_API_ADMIN_BASE=https://test.pigz.dev/admin/api

# Opcional - Token pré-gerado (deixar vazio)
HML_API_TOKEN=

# Ambiente (padrão: hml)
ENVIRONMENT=hml  # ou 'prod'
```

## Troubleshooting

| Erro | Solução |
|------|---------|
| "Credenciais não configuradas" | Preencher HML_API_USER e HML_API_PASSWORD |
| "401 Unauthorized" | Verificar credenciais em .env |
| "Connection timeout" | Verificar URL em .env e internet |
| "Token não encontrado" | Credenciais inválidas ou API offline |

## Arquivos Relacionados

- `config/api_auth.py` - Gerenciador de autenticação
- `config/settings.py` - Configuração centralizada
- `tests/test_api_auth_examples.py` - 8 exemplos práticos
- `.env.example` - Template de variáveis

## Validar Instalação

```bash
# Script de validação completo
python validate_api_auth.py

# Rodar exemplos
pytest tests/test_api_auth_examples.py -v
```

## Próximas Etapas

1. Configure `.env` com suas credenciais
2. Rode: `python validate_api_auth.py`
3. Execute: `pytest tests/test_api_auth_examples.py -v`
4. Use em seus testes conforme exemplos acima

---

**Anterior:** [Virtual Environment](./00-venv-setup.md)
**Próximo:** [Configuração Centralizada](./02-configuration.md)
