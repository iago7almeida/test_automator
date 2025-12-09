# 📚 Documentação - Índice

Bem-vindo à documentação do **Gestão Automation Playwright**!

## 🗂️ Estrutura

Esta pasta contém toda a documentação do projeto, organizada por tópico:

| # | Arquivo | Descrição | Para Quem? |
|---|---------|-----------|-----------|
| **00** | [venv-setup.md](00-venv-setup.md) | 🐍 Virtual Environment | Todos (primeiro) |
| **01** | [api-authentication.md](01-api-authentication.md) | 🔐 Autenticação de APIs | Quem usa APIs |
| **02** | [configuration.md](02-configuration.md) | ⚙️ Configuração Centralizada | Quem configura |
| **03** | [project-structure.md](03-project-structure.md) | 📁 Estrutura do Projeto | Quem explora código |
| **04** | [best-practices.md](04-best-practices.md) | ✨ Boas Práticas | Quem escreve código |
| **05** | [pre-commit-hooks.md](05-pre-commit-hooks.md) | 🔧 Pre-commit + Quickstart | Quem faz commits |
| **06** | [executando-testes.md](06-executando-testes.md) | 🧪 Executando Testes | Quem roda testes |

## 🎯 Por Onde Começar?

### 👤 Sou novo no projeto
1. Leia: [`README.md`](../README.md) (visão geral)
2. Leia: [`00-venv-setup.md`](00-venv-setup.md) (setup)
3. Rode: `python validate_config.py`
4. Rode: `bash setup_pre_commit.sh` (pre-commit)
5. Rode: `pytest -v` (testes)

### 👨‍💻 Vou escrever testes
1. Leia: [`04-best-practices.md`](04-best-practices.md)
2. Explore: [`03-project-structure.md`](03-project-structure.md)
3. Veja: exemplos em `tests/`
4. Rode: [`06-executando-testes.md`](06-executando-testes.md) para debug
5. Use: [`05-pre-commit-hooks.md`](05-pre-commit-hooks.md) para commit com validação

### 🔌 Vou usar APIs
1. Leia: [`01-api-authentication.md`](01-api-authentication.md)
2. Leia: [`02-configuration.md`](02-configuration.md)
3. Veja: exemplos em `tests/test_api_auth_examples.py`
4. Adapte para seus testes
5. Use: [`05-pre-commit-hooks.md#-atalhos-úteis`](05-pre-commit-hooks.md#️-atalhos-úteis) para validar antes de commit

### ⚙️ Vou configurar ambiente
1. Leia: [`02-configuration.md`](02-configuration.md)
2. Verifique: variáveis em `.env`
3. Rode: `python validate_config.py`
4. Teste: com `ENVIRONMENT=prod pytest`
5. Setup pre-commit: `bash setup_pre_commit.sh`

## 🚀 Comandos Rápidos

```bash
# Setup
source .venv/bin/activate
cp .env.example .env
# Editar .env com credenciais

# Validar
python validate_config.py
python validate_api_auth.py

# Testes
pytest -v
pytest tests/test_main_flow.py -v
HEADLESS=true pytest -v
ENVIRONMENT=prod pytest -v

# Help
python validate_config.py --help
@@# Pre-commit
@@bash setup_pre_commit.sh
@@pre-commit run --all-files
```

## 📖 Guia Completo

### 1. Setup (Primeira Vez)
[→ Leia 00-venv-setup.md](00-venv-setup.md)

Tópicos:
- O que é .venv
- Setup rápido
- Workflows comuns
- Troubleshooting

### 2. Autenticação de APIs
[→ Leia 01-api-authentication.md](01-api-authentication.md)

Tópicos:
- Tokens dinâmicos
- Como usar
- Em testes
- Troubleshooting

### 3. Configuração
[→ Leia 02-configuration.md](02-configuration.md)

Tópicos:
- Ambientes (HML/PROD)
- Variáveis disponíveis
- Como mudar configuração
- Usando em código

### 4. Estrutura do Projeto
[→ Leia 03-project-structure.md](03-project-structure.md)

Tópicos:
- Estrutura de pastas
- Page Object Model
- Como adicionar código
- Arquivos importantes

### 5. Boas Práticas
[→ Leia 04-best-practices.md](04-best-practices.md)

Tópicos:
- Geral
- Testes (Pytest)
- Page Objects
- APIs
- Logging
- Git
- Performance

### 6. Pre-commit Hooks + Quickstart
[→ Leia 05-pre-commit-hooks.md](05-pre-commit-hooks.md)

Tópicos:
- Setup automático (3 linhas!)
- Como rodar
- Hooks disponíveis
- Quickstart rápido
- Atalhos úteis
- Resumo de implementação

### 7. Executando Testes
[→ Leia 06-executando-testes.md](06-executando-testes.md)

Tópicos:
- Quick start
- Modos de execução
- Debug e investigação
- Relatórios
- Troubleshooting

## 🔍 Procurando por...?

| Preciso de... | Arquivo | Seção |
|---|---|---|
| Setup inicial | 00-venv-setup.md | - |
| Usar APIs | 01-api-authentication.md | Como usar |
| Tokens dinâmicos | 01-api-authentication.md | O que é |
| URLs variáveis | 02-configuration.md | Variáveis |
| Multi-ambiente | 02-configuration.md | Ambientes |
| Page Objects | 03-project-structure.md | Pattern |
| Fixtures | 03-project-structure.md | tests/ |
| Escrever testes | 04-best-practices.md | Testes |
| Logging | 04-best-practices.md | Logging |
| Git | 04-best-practices.md | Commits |
| Pre-commit setup | 05-pre-commit-hooks.md | Quickstart Rápido |
| Executar testes | 06-executando-testes.md | Quick Start |
| Debug testes | 06-executando-testes.md | Debug |
| Relatórios testes | 06-executando-testes.md | Relatórios |

## 💡 Dicas Importantes

✅ **Sempre ativar .venv antes de trabalhar**
```bash
source .venv/bin/activate
```

✅ **Usar `get_config()` para URLs**
```python
from config.settings import get_config
config = get_config()
url = f"{config.BASE_URL}/path"
```

✅ **Usar `APIAuthManager` para APIs**
```python
from config.api_auth import APIAuthManager
auth = APIAuthManager()
response = auth.get(url)  # Token automático
```

✅ **Seguir estrutura de pastas**
- Uma página = um arquivo em `pages/`
- Um teste = um arquivo em `tests/`
- Config = sempre usar `config/`

✅ **Nunca versionar segredos**
- `.env` → nunca commit
- Tokens → nunca hardcode
- Senhas → sempre em `.env`
@@
@@✅ **Setup pre-commit na primeira vez**
@@```bash
@@bash setup_pre_commit.sh
@@# Hooks rodarão automaticamente em cada commit
@@```

## 📞 Suporte

- 💬 Pergunta comum? Verifique [04-best-practices.md#troubleshooting](04-best-practices.md#troubleshooting)
- 🐛 Erro técnico? Rode `python validate_config.py`
- 📖 Dúvida? Leia o arquivo correspondente acima
- 🔗 Link quebrado? Reporte a issue

## 🎓 Aprenda Mais

### Recursos Externos
- [Playwright Python](https://playwright.dev/python/)
- [Pytest Docs](https://docs.pytest.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Código de Exemplo
- `tests/test_api_auth_examples.py` - 8 exemplos de API
- `tests/conftest.py` - Fixtures prontas
- `pages/login_page.py` - Page Object exemplo
- `config/settings.py` - Config centralizada

## 📝 Changelog

**8 de Dezembro de 2025**
- ✅ Reorganizou docs em pasta centralizada
- ✅ Consolidou duplicações (VENV, API_AUTH)
- ✅ Criou README.md conciso
- ✅ Estrutura final: 5 arquivos bem organizados

---

**Status:** ✅ Documentação Completa
**Última atualização:** 8 de Dezembro de 2025

Comece por: [README.md](../README.md) → [00-venv-setup.md](00-venv-setup.md)

---

## 📦 Arquivo (Histórico)

A pasta `docs/archive/` contém documentos históricos de limpeza e consolidação. Você pode consultá-los se precisar de referência sobre o que foi feito, mas não são necessários para usar o projeto.
