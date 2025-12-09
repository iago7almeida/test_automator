# 🧪 Executando Testes

Guia completo sobre como executar e debugar testes do projeto.

## 🚀 Quick Start

```bash
# Ativar .venv
source .venv/bin/activate

# Executar todos os testes
pytest -v

# Executar com Playwright visível
HEADLESS=false pytest -v

# Executar teste específico
pytest tests/test_client_detail.py -v
```

## 📋 Estrutura de Testes

```
tests/
├── conftest.py                    # Fixtures compartilhadas
├── test_api_auth_examples.py      # Exemplos de autenticação
├── test_client_detail.py          # Detalhes do cliente
├── test_client_payments.py        # Pagamentos
├── test_main_flow.py              # Fluxo principal
├── test_single_orders.py          # Pedidos avulsos
└── test_table_operations.py       # Operações em mesas
```

## 🎯 Executar Testes Específicos

### Todos os testes

```bash
pytest -v
```

### Um arquivo específico

```bash
pytest tests/test_client_detail.py -v
```

### Uma função específica

```bash
pytest tests/test_client_detail.py::test_client_detail_validation -v
```

### Por padrão de nome

```bash
# Testes que contêm "client" no nome
pytest -k "client" -v

# Testes que contêm "payment" no nome
pytest -k "payment" -v
```

## 🎮 Modos de Execução

### Headed (vê o navegador)

```bash
HEADLESS=false pytest -v
```

### Headless (sem janela do navegador)

```bash
HEADLESS=true pytest -v
# ou
pytest -v  # padrão é headless
```

### Com output visual

```bash
# Mais verboso
pytest -vv tests/test_client_detail.py

# Com prints visíveis
pytest -s tests/test_client_detail.py

# Combinado
pytest -vv -s tests/test_client_detail.py
```

### Com falha rápida

```bash
# Para no primeiro erro
pytest -x tests/

# Para com N erros
pytest --maxfail=3 tests/
```

## 🌍 Por Ambiente

### HML (Homologação - Padrão)

```bash
ENVIRONMENT=hml pytest -v
# ou apenas:
pytest -v
```

### PROD (Produção)

```bash
ENVIRONMENT=prod pytest -v
```

⚠️ **Cuidado!** Prod usa URLs e credenciais reais!

## 🔍 Debug e Investigação

### Ver todos os logs

```bash
pytest -v --tb=long tests/test_client_detail.py
```

### Drop para debugger em erro

```bash
pytest --pdb tests/test_client_detail.py
```

Quando parar no erro:
- `c` = continuar
- `n` = próxima linha
- `s` = step into
- `l` = listar código
- `p variavel` = print variável
- `q` = sair

### Ver código fonte durante teste

```bash
pytest --showlocals tests/test_client_detail.py
```

### Apenas teste com keyword

```bash
# Todos com "login" no nome
pytest -k "login" -v

# Todos com "login" mas não "logout"
pytest -k "login and not logout" -v
```

## ⚡ Atalhos de Velocidade

### Rodar último teste que falhou

```bash
pytest --lf -v
```

### Rodar apenas testes que falharam

```bash
pytest --ff -v
```

### Rodar com paralelização (requer pytest-xdist)

```bash
# Instalar: pip install pytest-xdist
pytest -n auto -v  # auto = número de CPUs
pytest -n 4 -v     # 4 processos
```

## 📊 Relatórios

### Cobertura de código

```bash
# Instalar: pip install pytest-cov
pytest --cov=pages --cov=config tests/

# Gerar HTML
pytest --cov=pages --cov=config --cov-report=html tests/
# Abrir: htmlcov/index.html
```

### Teste por categoria

```bash
# Marcar testes em conftest.py:
# @pytest.mark.slow
# @pytest.mark.integration
# @pytest.mark.api

# Rodar apenas rápidos
pytest -m "not slow" -v

# Rodar apenas lentos
pytest -m "slow" -v

# Rodar apenas API
pytest -m "api" -v
```

## 🐛 Troubleshooting

### Erro: "import config failed"

```bash
# Verificar instalação
python validate_config.py

# Reinstalar .venv
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Playwright browsers not found"

```bash
# Instalar browsers
playwright install
# ou
python -m playwright install
```

### Erro: "timeout on page.goto"

Aumentar timeout em `.env`:
```
PAGE_LOAD_TIMEOUT=60000
```

Ou no teste:
```python
page.goto(url, timeout=60000)
```

### Erro: "element not found"

1. Aumentar timeout (`.env`):
   ```
   ELEMENT_TIMEOUT=30000
   ```

2. Ou aguardar elemento:
   ```python
   page.wait_for_selector('.elemento', timeout=30000)
   ```

3. Ou usar wait_for:
   ```python
   page.wait_for_load_state('networkidle')
   ```

### Teste funciona local mas falha em CI

- Verificar `.env` em CI
- Aumentar timeouts
- Adicionar `page.wait_for_load_state()`
- Usar `page.screenshot()` para debug

## 📝 Fixtures Disponíveis

Em `tests/conftest.py`:

```python
# Navegador Chromium
def test_with_browser(browser):
    page = browser.new_page()
    # usar page

# Página nova para cada teste
def test_with_page(page):
    page.goto(url)
    # usar page

# API com autenticação
def test_with_api_auth(api_auth):
    response = api_auth.get(url)
    # usar response

# Sessão de API reutilizável
def test_with_session(api_auth_session):
    response = api_auth_session.get(url)
    # usar response
```

## ✅ Checklist de Teste

Antes de fazer commit:

```bash
# 1. Ativar .venv
source .venv/bin/activate

# 2. Validar config
python validate_config.py

# 3. Rodar pre-commit
pre-commit run --all-files

# 4. Rodar todos os testes
pytest -v

# 5. Verificar cobertura
pytest --cov=pages --cov=config tests/

# 6. Commit
git add .
git commit -m "Feature"
```

## 🎓 Exemplos Práticos

### Rodar teste de autenticação

```bash
pytest tests/test_api_auth_examples.py -v
```

### Debug de elemento não encontrado

```bash
# Parar no erro e investigar
HEADLESS=false pytest tests/test_client_detail.py::test_something -vv -s --pdb
```

### Verificar se login funciona

```bash
# Apenas testes que contêm "login"
pytest -k "login" -v
```

### Otimizar testes lentos

```bash
# Ver quanto tempo cada teste leva
pytest --durations=10 tests/

# Rodar em paralelo
pytest -n auto tests/
```

## 📖 Veja Também

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Python](https://playwright.dev/python/)
- [fixtures em conftest.py](../tests/conftest.py)
- [Exemplos de API](../tests/test_api_auth_examples.py)

---

**Status:** ✅ Completo
**Última atualização:** 8 de Dezembro de 2025

Comece: `pytest -v`
