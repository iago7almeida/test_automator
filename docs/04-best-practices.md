# ✨ Boas Práticas

## Geral

### 1. Sempre Ativar .venv
Veja detalhes completos em [00-venv-setup.md](00-venv-setup.md)

```bash
# Antes de qualquer comando Python
source .venv/bin/activate
```

### 2. Usar Configuração Centralizada
```python
# ✅ BOM
from config.settings import get_config
config = get_config()
url = f"{config.BASE_URL}/signin"

# ❌ RUIM
url = "https://homolog.pigz.com.br/signin"  # Hardcoded!
```

### 3. Credenciais em .env
Veja mais em [02-configuration.md](02-configuration.md)

```python
# ✅ BOM
username = config.USERNAME  # De .env

# ❌ RUIM
username = "teste@test.com"  # No código!
```

## Testes (Pytest)

### 1. Use Fixtures
```python
# ✅ BOM
@pytest.fixture
def api():
    auth = APIAuthManager()
    auth.generate_token()
    return auth

def test_users(api):
    response = api.get(url)
    assert response.status_code == 200

# ❌ RUIM
def test_users():
    auth = APIAuthManager()
    auth.generate_token()
    # Repetir em cada teste
```

### 2. Nomes Descritivos
```python
# ✅ BOM
def test_login_with_valid_credentials():
    """Usuário consegue fazer login com email e senha válidos"""

# ❌ RUIM
def test_login():
    """Testa login"""
```

### 3. Uma Coisa Por Teste
```python
# ✅ BOM
def test_login_success():
    """Login com sucesso"""

def test_login_invalid_password():
    """Login com senha inválida mostra erro"""

# ❌ RUIM
def test_login():
    """Testa login com vários cenários"""
    # Múltiplos cenários em um teste
```

### 4. Assertions Claras
```python
# ✅ BOM
assert len(users) > 0, "Deve retornar pelo menos 1 usuário"
assert response.status_code == 200

# ❌ RUIM
assert len(users)
assert response
```

## Page Objects

### 1. Um Arquivo Por Página
```python
# ✅ BOM
pages/login_page.py       # Login
pages/dashboard_page.py   # Dashboard

# ❌ RUIM
pages/pages.py            # Tudo junto
```

### 2. Localizadores no __init__
```python
# ✅ BOM
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Senha")

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)

# ❌ RUIM
def login(page, email, password):
    page.get_by_label("Email").fill(email)  # Repetir localizadores
```

### 3. Métodos por Ação
```python
# ✅ BOM
page.search_user("João")
page.filter_by_status("active")
page.sort_by_date()

# ❌ RUIM
page.click_search()
page.fill_input("João")
page.select_filter("status")
page.click_sort()
```

### 4. Use Config
```python
# ✅ BOM
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()

    def navigate(self):
        self.page.goto(f"{self.config.BASE_URL}/signin")

# ❌ RUIM
def navigate(page):
    page.goto("https://homolog.pigz.com.br/signin")  # Hardcoded
```

## APIs

### 1. Use APIAuthManager
```python
# ✅ BOM
from config.api_auth import APIAuthManager
auth = APIAuthManager()
response = auth.get(url)  # Token automático

# ❌ RUIM
import requests
headers = {"Authorization": "Bearer eyJ..."}  # Hardcoded
response = requests.get(url, headers=headers)
```

### 2. URLs Dinâmicas
```python
# ✅ BOM
url = f"{config.API_ADMIN_BASE}/partner/users"

# ❌ RUIM
url = "https://test.pigz.dev/admin/api/partner/users"  # Hardcoded
```

### 3. Verificar Resposta
```python
# ✅ BOM
response = auth.get(url)
if response:
    data = response.json()
else:
    print("Erro na requisição")

# ❌ RUIM
response = auth.get(url)
data = response.json()  # Pode quebrar se response for None
```

## Logging

### 1. Use Logging
```python
# ✅ BOM
import logging
logger = logging.getLogger(__name__)

logger.info("🔐 Fazendo login")
logger.error("❌ Erro ao fazer login")

# ❌ RUIM
print("Login")     # Muito simples
print("ERROR")     # Não há contexto
```

### 2. Níveis Corretos
```python
logger.debug("Detalhe técnico")           # Muito detalhado
logger.info("Operação executada")         # Info importante
logger.warning("Algo estranho")           # Atenção
logger.error("Erro, mas continua")        # Erro
logger.critical("Erro crítico, stop")     # Parar tudo
```

## Commits & Git

### 1. Commits Descritivos
```bash
# ✅ BOM
git commit -m "feat: add login page automation"
git commit -m "fix: resolve timeout on payment"
git commit -m "chore: update requirements.txt"

# ❌ RUIM
git commit -m "fix"
git commit -m "atualizar"
git commit -m "stuff"
```

### 2. Nunca Commit de Segredo
```bash
# ✅ Seguro (já em .gitignore)
.env              # Credenciais
.venv/            # Virtual env
__pycache__/      # Cache

# ❌ NUNCA
Token Bearer eyJ...  # No código
senha123             # No código
```

## Performance

### 1. Use Implicitly Wait
```python
# ✅ BOM (Playwright espera até 5s por default)
page.get_by_text("Usuário").click()

# ❌ RUIM
import time
time.sleep(5)  # Espera sempre 5s
page.get_by_text("Usuário").click()
```

### 2. Reutilize Page Objects
```python
# ✅ BOM
def test_feature(logged_in_page):
    """Usa fixture que já faz login"""
    dashboard = DashboardPage(logged_in_page.page)

# ❌ RUIM
def test_feature():
    """Faz login de novo"""
    page.goto(url)
    page.fill_email()
    page.fill_password()
    page.click_login()
```

## Estrutura

### 1. Imports Organizados
```python
# ✅ BOM
# 1. Standard library
import logging
from pathlib import Path

# 2. Third party
import pytest
from playwright.sync_api import Page

# 3. Local
from config.settings import get_config
from pages.login_page import LoginPage

# ❌ RUIM
from pages.login_page import LoginPage
import pytest
from config.settings import get_config
import logging
```

### 2. Docstrings
```python
# ✅ BOM
def login(self, email: str, password: str) -> None:
    """
    Faz login com email e senha.

    Args:
        email: Email do usuário
        password: Senha do usuário

    Raises:
        AssertionError: Se login falhar
    """

# ❌ RUIM
def login(self, email, password):
    """Faz login"""
```

## Checklist Antes de Commit

- [ ] Código segue as práticas acima
- [ ] Testes passam: `pytest -v`
- [ ] Sem hardcodes de URL/senha/token
- [ ] Usa `get_config()` para URLs
- [ ] Usa `APIAuthManager` para APIs
- [ ] Logging adequado
- [ ] Docstrings nas funções
- [ ] Imports organizados
- [ ] Commit message descritiva

## Referências Rápidas

```bash
# Validar projeto
python validate_config.py
python validate_api_auth.py

# Rodar testes
pytest -v
pytest tests/test_main_flow.py::test_login -v
pytest --cov=pages --cov=tests

# Rodar com configuração
ENVIRONMENT=prod pytest -v
HEADLESS=true pytest -v
HEADLESS=true ENVIRONMENT=prod pytest -v
```

---

**Anterior:** [Estrutura do Projeto](./03-project-structure.md)
**Próximo:** [README Principal](../README.md)
