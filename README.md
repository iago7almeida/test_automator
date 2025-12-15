# 🎭 Gestão Automation - Playwright

Framework de automação de testes para **Gestão Pigz** usando Playwright + Pytest.

**Multi-ambiente** (HML/PROD) | **Tokens dinâmicos** | **Config centralizada** | **Bem documentado**

## 🚀 Quick Start (3 minutos)

```bash
# 1. Ativar virtual environment
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate.ps1         # Windows

# 2. Configurar variáveis
cp .env.example .env
# Editar .env com suas credenciais

# 3. Validar
python validate_config.py
python validate_api_auth.py

# 4. Rodar testes
pytest -v
```

## 📚 Documentação

Toda documentação está em `docs/`:

| Arquivo | Descrição |
|---------|-----------|
| [00-venv-setup.md](docs/00-venv-setup.md) | Setup do virtual environment |
| [01-api-authentication.md](docs/01-api-authentication.md) | Sistema de autenticação de APIs |
| [02-configuration.md](docs/02-configuration.md) | Configuração centralizada (HML/PROD) |
| [03-project-structure.md](docs/03-project-structure.md) | Estrutura do projeto |
| [04-best-practices.md](docs/04-best-practices.md) | Boas práticas |
| [07-test-architecture.md](docs/07-test-architecture.md) | Estrutura de testes (backend/frontend/mobile) |

**👉 Comece por:** [`docs/00-venv-setup.md`](docs/00-venv-setup.md)

## 🎯 Features Principais

### ✅ Autenticação Dinâmica
Tokens JWT gerados automaticamente, renovam quando expiram:

```python
from config.api_auth import APIAuthManager
auth = APIAuthManager()
response = auth.get(f"{config.API_ADMIN_BASE}/users")
```

### ✅ Multi-Ambiente
Alterne entre HML e PROD com uma variável:

```bash
ENVIRONMENT=hml pytest -v    # Homologação
ENVIRONMENT=prod pytest -v   # Produção
```

### ✅ Config Centralizada
Uma única fonte de verdade para URLs, credenciais, timeouts:

```python
from config.settings import get_config
config = get_config()
print(config.BASE_URL)           # URL web
print(config.API_ADMIN_BASE)     # URL API
print(config.USERNAME)           # Credenciais
```

### ✅ Page Object Model
Organiza elementos e ações por página:

```python
from pages.login_page import LoginPage
login = LoginPage(page)
login.navigate()
login.login("email@test.com", "senha")
```

### ✅ Fixtures Pytest
Setup/teardown compartilhado:

```python
@pytest.fixture
def logged_in_page():
    # Lógica de login aqui

def test_dashboard(logged_in_page):
    # Teste com usuário logado
```

## 📁 Estrutura

```
.
├── docs/                    # 📚 Documentação
├── config/                  # ⚙️ Configuração centralizada
│   ├── settings.py          # Config por ambiente
│   └── api_auth.py          # Autenticação dinâmica
├── pages/                   # 🖼️ Page Objects
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── ...
├── tests/                   # 🧪 Testes
│   ├── conftest.py          # Fixtures
│   ├── test_main_flow.py
│   └── ...
├── .env.example             # Template variáveis
├── requirements.txt         # Dependências
├── README.md                # Este arquivo
└── .venv/                   # Virtual environment
```

## 🔧 Comandos Úteis

```bash
# Ativar virtual environment
source .venv/bin/activate

# Instalar/atualizar dependências
pip install -r requirements.txt

# Validar setup
python validate_config.py
python validate_api_auth.py

# Rodar todos os testes
pytest -v

# Rodar um teste específico
pytest tests/test_main_flow.py::test_login -v

# Modo headless (sem interface)
HEADLESS=true pytest -v

# Com cobertura
pytest --cov=pages --cov=tests -v

# Ambiente produção
ENVIRONMENT=prod pytest -v
```

## 🔐 Segurança

- ✅ Credenciais em `.env` (não versionado)
- ✅ Tokens gerados dinamicamente
- ✅ URLs variáveis por ambiente
- ✅ Sem hardcodes de secretos
- ✅ `.gitignore` protege dados sensíveis

## 📦 Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| python | 3.13 | Versão do python de uso |
| playwright | 1.40.0 | Automação web |
| pytest | 7.4.3 | Framework de testes |
| python-dotenv | 1.0.0 | Variáveis de ambiente |
| requests | 2.31.0 | Requisições HTTP |
| pandas | 2.1.3 | Processamento de dados |

Ver `requirements.txt` para lista completa.

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| "ModuleNotFoundError" | Ativar .venv: `source .venv/bin/activate` |
| "401 Unauthorized" | Verificar credenciais em `.env` |
| Testes lentos | Usar `HEADLESS=true` |
| Falhas aleatórias | Aumentar timeouts em `.env` |

**Mais problemas?** Veja [docs/04-best-practices.md](docs/04-best-practices.md#troubleshooting)

## 🚀 Próximos Passos

1. **Setup**: Siga [00-venv-setup.md](docs/00-venv-setup.md)
2. **APIs**: Leia [01-api-authentication.md](docs/01-api-authentication.md)
3. **Config**: Entenda [02-configuration.md](docs/02-configuration.md)
4. **Estrutura**: Explore [03-project-structure.md](docs/03-project-structure.md)
5. **Práticas**: Estude [04-best-practices.md](docs/04-best-practices.md)

## 👥 Contribuições

Ao adicionar novo código:
- [ ] Use `get_config()` para URLs
- [ ] Use `APIAuthManager` para APIs
- [ ] Siga [Best Practices](docs/04-best-practices.md)
- [ ] Testes passam: `pytest -v`
- [ ] Sem credenciais em commits

## 📞 Suporte

- 📖 Leia a [documentação em docs/](docs/)
- 🐛 Verifique [04-best-practices.md#troubleshooting](docs/04-best-practices.md#troubleshooting)

---
