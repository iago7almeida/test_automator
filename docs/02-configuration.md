# ⚙️ Configuração Centralizada

## Visão Geral

Todo projeto usa **uma única fonte de verdade** para configuração: `config/settings.py`

```python
from config.settings import get_config

config = get_config()
print(config.BASE_URL)        # https://homolog.pigz.com.br
print(config.API_ADMIN_BASE)  # https://test.pigz.dev/admin/api
print(config.ENVIRONMENT)     # HML ou PROD
```

## Ambientes (HML vs PROD)

A configuração muda automaticamente baseado em `ENVIRONMENT`:

```bash
# Homologação (padrão)
ENVIRONMENT=hml
HML_BASE_URL=https://homolog.pigz.com.br
HML_API_BASE_URL=https://test.pigz.dev

# Produção
ENVIRONMENT=prod
PROD_BASE_URL=https://gestor.pigz.com.br
PROD_API_BASE_URL=https://api.pigz.com.br
```

## Estrutura de Configuração

```
BaseConfig (comum a todos)
├── HEADLESS = false
├── BROWSER_CHANNEL = "chromium"
├── DEFAULT_TIMEOUT = 5000
├── LOG_LEVEL = "INFO"
└── ...

HMLConfig (herda de BaseConfig)
├── BASE_URL = "https://homolog.pigz.com.br"
├── API_BASE_URL = "https://test.pigz.dev"
├── API_ADMIN_BASE = "https://test.pigz.dev/admin/api"
├── USERNAME = "email@test.com"
├── API_USERNAME = "email@test.com"
└── ...

ProdConfig (herda de BaseConfig)
├── BASE_URL = "https://gestor.pigz.com.br"
├── API_BASE_URL = "https://api.pigz.com.br"
├── API_ADMIN_BASE = "https://api.pigz.com.br/admin/api"
├── USERNAME = "email@prod.com"
├── API_USERNAME = "email@prod.com"
└── ...
```

## Variáveis Disponíveis

### URLs Web
```python
config.BASE_URL              # URL principal (ex: https://homolog.pigz.com.br)
```

### APIs
```python
config.API_BASE_URL          # Base (ex: https://test.pigz.dev)
config.API_ADMIN_BASE        # Admin (ex: https://test.pigz.dev/admin/api)
config.API_USERS_ENDPOINT    # "/partner/users"
config.API_AUTH_ENDPOINT     # "/auth/login"
config.API_ORDERS_ENDPOINT   # "/orders"
```

### Credenciais
```python
config.USERNAME              # Email web (ex: teste@test.com)
config.PASSWORD              # Senha web
config.API_USERNAME          # Email API
config.API_PASSWORD          # Senha API
config.API_TOKEN             # Token (gerado automaticamente)
```

### Browser
```python
config.HEADLESS              # true/false (interface gráfica)
config.BROWSER_CHANNEL       # "chromium", "firefox", etc
config.START_MAXIMIZED       # Maximizar janela
config.PAGE_ZOOM             # Zoom da página (%)
```

### Timeouts
```python
config.DEFAULT_TIMEOUT       # 5000 ms (padrão)
config.LONG_TIMEOUT          # 15000 ms (esperas longas)
config.SHORT_TIMEOUT         # 2000 ms (cliques rápidos)
```

### Logging
```python
config.LOG_LEVEL             # "DEBUG", "INFO", "WARNING", "ERROR"
config.SCREENSHOT_ON_FAILURE # true/false
config.SCREENSHOT_PATH       # "./tests/screenshots"
```

### Testes
```python
config.PYTEST_WORKERS        # Número de workers paralelos
config.STOP_ON_FIRST_FAILURE # Parar na primeira falha
```

### Ambiente
```python
config.ENVIRONMENT           # Environment.HML ou Environment.PROD
```

## Como Mudar Configuração

### Option 1: Variável de Ambiente
```bash
HEADLESS=true pytest tests/
ENVIRONMENT=prod pytest tests/
BROWSER_CHANNEL=firefox pytest tests/
```

### Option 2: Arquivo .env
```dotenv
HEADLESS=true
ENVIRONMENT=prod
BROWSER_CHANNEL=firefox
```

### Option 3: Dentro do Código
```python
from config.settings import get_config
import os

# Mudar antes de importar config
os.environ['ENVIRONMENT'] = 'prod'
config = get_config()
```

## Usando em Páginas

```python
from playwright.sync_api import Page
from config.settings import get_config

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = get_config()

    def navigate(self):
        url = f"{self.config.BASE_URL}/sign-in"
        self.page.goto(url)
```

## Usando em Testes

```python
from config.settings import get_config

def test_login():
    config = get_config()

    # Verificar ambiente
    assert config.ENVIRONMENT.value == "hml"

    # Usar URLs
    assert config.BASE_URL == "https://homolog.pigz.com.br"

    # Usar credenciais
    username = config.USERNAME
    password = config.PASSWORD
```

## Usando com APIs

```python
from config.api_auth import APIAuthManager
from config.settings import get_config

config = get_config()
auth = APIAuthManager()

# Endpoint com URL centralizada
url = f"{config.API_ADMIN_BASE}{config.API_USERS_ENDPOINT}"
response = auth.get(url)
```

## Arquivo de Variáveis

Ver `.env.example` para template com todas as variáveis disponíveis.

```bash
# Ver todas as variáveis
cat .env.example
```

## Padrão: Factory + Singleton

```python
# Factory (cria config por ambiente)
from config.settings import ConfigFactory
config = ConfigFactory.get_config()

# Singleton (global - reutiliza)
from config.settings import get_config
config = get_config()
config2 = get_config()  # Mesma instância!
```

## Validar Configuração

```bash
# Script de validação
python validate_config.py

# Ou manual
python -c "from config.settings import get_config; print(get_config().BASE_URL)"
```

## Próximas Etapas

1. Configure `.env` com seus dados
2. Use `config.BASE_URL` em páginas
3. Use `config.API_BASE_URL` em APIs
4. Mude `ENVIRONMENT=prod` para testar produção

---

**Anterior:** [API Authentication](./01-api-authentication.md)
**Próximo:** [Estrutura do Projeto](./03-project-structure.md)
