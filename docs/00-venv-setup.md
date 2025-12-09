# 🐍 Virtual Environment (.venv)

## Setup Rápido

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

## O que é .venv?

Um **ambiente isolado do Python** para este projeto que:
- ✅ Instala pacotes sem conflitar com outros projetos
- ✅ Usa versões específicas de dependências
- ✅ Funciona em Windows, Mac e Linux
- ✅ Facilita CI/CD e deployment

## Após Ativar

```bash
# Ver versão
python --version

# Listar pacotes
pip list

# Instalar novo pacote (se necessário)
pip install nome_do_pacote

# Congelar dependências
pip freeze > requirements.txt
```

## Workflows Comuns

**Primeira vez:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

**Uso diário:**
```bash
source .venv/bin/activate
pytest tests/test_main_flow.py -v
```

**Com novo pacote:**
```bash
source .venv/bin/activate
pip install novo_pacote
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: add new_pacote"
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| "command not found: python" | Ativar venv: `source .venv/bin/activate` |
| "ModuleNotFoundError" | Instalar deps: `pip install -r requirements.txt` |
| "Permission denied" | Linux/Mac: `chmod +x activate.sh` |
| Criar novo .venv | `python -m venv .venv` |

## Info Técnica

- **Localização:** `.venv/` (raiz do projeto)
- **Arquivo de config:** `.env` (não versionado)
- **Dependências:** `requirements.txt` (versionado)
- **Compatibilidade:** Python 3.8+
- **Tamanho:** ~500MB

---

**Próximo:** Leia [API Authentication](./01-api-authentication.md) para usar APIs dinâmicas.
