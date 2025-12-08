# 📁 Estrutura do Projeto

## Visão Geral

```
gestao_automation_playwright/
├── docs/                          # 📚 Documentação centralizada
├── config/                        # ⚙️ Configuração
├── pages/                         # 🖼️ Page Objects
├── tests/                         # 🧪 Testes
├── data/                          # 📊 Dados de teste
├── .venv/                         # 🐍 Virtual environment
├── .env                           # 🔐 Variáveis (não versionado)
├── .env.example                   # 📋 Template
├── .gitignore                     # 🚫 Arquivos ignorados
├── requirements.txt               # 📦 Dependências
├── README.md                      # 🎯 Guia principal
└── setup.py                       # 🔧 Setup automático
```

## Pastas Principais

### `docs/` - Documentação
```
docs/
├── 00-venv-setup.md               # Setup do virtual environment
├── 01-api-authentication.md       # Sistema de autenticação
├── 02-configuration.md            # Configuração centralizada
├── 03-project-structure.md        # Esta documentação
└── 04-best-practices.md           # Boas práticas
```

### `config/` - Configuração
```
config/
├── __init__.py
├── settings.py                    # ⚙️ Config centralizada (HML/PROD)
├── api_auth.py                    # 🔐 Gerenciador de autenticação
└── __pycache__/
```

**Usar em todo projeto:**
```python
from config.settings import get_config
config = get_config()  # Retorna HMLConfig ou ProdConfig
```

### `pages/` - Page Object Model
```
pages/
├── __init__.py
├── base_page.py                   # Classe base (comum a todas)
├── login_page.py                  # Login
├── client_list_page.py            # Listagem de clientes
├── client_details_page.py         # Detalhes do cliente
├── new_order_page.py              # Criar pedido
├── order_sheet_page.py            # Folha de pedido
├── payment_page.py                # Pagamentos
├── tables_page.py                 # Tabelas
├── dashboard_page.py              # Dashboard
├── modal_handler.py               # Modais
└── blo.py                         # APIs de teste
```

**Pattern - Page Object:**
```python
from playwright.sync_api import Page
from config.settings import get_config

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()
        # Localizadores aqui
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Senha")
        self.submit_button = page.get_by_role("button", name="Login")

    def navigate(self):
        self.page.goto(f"{self.config.BASE_URL}/sign-in")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
```

### `tests/` - Testes
```
tests/
├── __init__.py
├── conftest.py                    # 🔧 Fixtures compartilhadas
├── test_main_flow.py              # Fluxo principal
├── test_client_detail.py          # Detalhes do cliente
├── test_client_payments.py        # Pagamentos
├── test_single_orders.py          # Pedidos unitários
├── test_table_operations.py       # Operações em tabelas
└── test_api_auth_examples.py      # Exemplos de API auth
```

**Pattern - Teste com Fixture:**
```python
def test_login_success(logged_in_page):
    """Teste assumindo que usuário já está logado"""
    # logged_in_page vem de conftest.py
    assert logged_in_page.page.url.includes("dashboard")
```

### `data/` - Dados de Teste
```
data/
└── data.py                        # Dados compartilhados
```

## Arquivos de Configuração

### `.env` (Local - Não versionado)
```dotenv
ENVIRONMENT=hml
HML_API_USER=seu_email@pigz.com.br
HML_API_PASSWORD=sua_senha
# ... outras variáveis
```

### `.env.example` (Template - Versionado)
Template com todas as variáveis possíveis.

```bash
# Usar:
cp .env.example .env
# ... editar .env com seus dados
```

### `requirements.txt` (Dependências)
Todas as dependências com versões fixas.

```bash
# Instalar:
pip install -r requirements.txt

# Adicionar novo pacote:
pip install novo_pacote
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: add novo_pacote"
```

## Como Trabalhar

### 1. Setup Inicial
```bash
# Ativar venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# ... editar .env
```

### 2. Criar Novo Teste
```python
# tests/test_new_feature.py
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_new_feature(logged_in_page):
    """Seu teste aqui"""
    dashboard = DashboardPage(logged_in_page.page)
    # ... test code
```

### 3. Criar Nova Página
```python
# pages/new_page.py
from playwright.sync_api import Page
from config.settings import get_config

class NewPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()
        # Localizadores

    def navigate(self):
        self.page.goto(f"{self.config.BASE_URL}/novo-endpoint")
```

### 4. Rodar Testes
```bash
# Todos
pytest -v

# Um arquivo
pytest tests/test_main_flow.py -v

# Um teste
pytest tests/test_main_flow.py::test_login -v

# Com cobertura
pytest --cov=pages --cov=tests

# Modo headless (sem interface)
HEADLESS=true pytest -v
```

## Imports Comuns

```python
# Configuração
from config.settings import get_config
config = get_config()

# Autenticação API
from config.api_auth import APIAuthManager
auth = APIAuthManager()

# Páginas
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Playwright
from playwright.sync_api import Page, expect

# Pytest
import pytest
```

## Padrões Usados

| Padrão | Arquivo | Descrição |
|--------|---------|-----------|
| Page Object Model | `pages/` | Organiza elementos e ações |
| Factory | `config/settings.py` | Cria config por ambiente |
| Singleton | `get_config()` | Uma única instância global |
| Fixture | `tests/conftest.py` | Setup/teardown compartilhado |

## Próximas Etapas

1. Leia [Best Practices](./04-best-practices.md)
2. Explore a pasta `pages/` para entender Page Objects
3. Veja `tests/test_api_auth_examples.py` para exemplos
4. Crie seu primeiro teste

---

**Anterior:** [Configuração](./02-configuration.md)
**Próximo:** [Boas Práticas](./04-best-practices.md)
