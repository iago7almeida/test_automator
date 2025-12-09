# 🔧 Pre-commit Hooks

Sistema automático de validação de código antes de commits. Valida e formata Python automaticamente.

## ⚙️ Setup

### 1. Ativar o .venv

```bash
source .venv/bin/activate
```

### 2. Executar script de setup

```bash
bash setup_pre_commit.sh
```

Isso vai:
- ✅ Instalar `pre-commit` package
- ✅ Instalar hooks Git automaticamente
- ✅ Configurar para rodar em cada commit

## 🚀 Como Usar

### Automático (em cada commit)

Quando você fizer commit, os hooks rodarão **automaticamente**:

```bash
git add .
git commit -m "Minha mensagem"
# Hooks rodam aqui automaticamente
```

### Manual (antes de commit)

Rodar hooks em todos os arquivos:

```bash
pre-commit run --all-files
```

Rodar apenas um hook específico:

```bash
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files
```

## 📋 Hooks Instalados

| Hook | Descrição | Ação |
|------|-----------|------|
| **black** | Code formatter | Formata Python automaticamente |
| **flake8** | Linter | Verifica estilo e erros |
| **isort** | Import sorter | Ordena imports automaticamente |
| **pylint** | Advanced linter | Análise profunda de código |
| **trailing-whitespace** | Espaços extras | Remove espaços no fim das linhas |
| **end-of-file-fixer** | Fim de arquivo | Garante newline no final |
| **check-yaml** | Validador YAML | Valida sintaxe YAML |
| **check-json** | Validador JSON | Valida sintaxe JSON |
| **check-merge-conflict** | Merge conflicts | Detecta marcadores de conflito |
| **debug-statements** | Debug code | Detecta print/pdb esquecidos |
| **mixed-line-ending** | Line endings | Normaliza CRLF/LF |

## ⚙️ Configuração

Editar: `.pre-commit-config.yaml`

Opções úteis:
```yaml
args: ['--line-length=100']      # Comprimento máximo da linha
exclude: '^\.venv|setup.py'      # Excluir arquivos
stages: [commit]                  # Rodar em qual stage (commit/push)
```

## 🚀 Adicionar Mais Hooks

Você pode adicionar mais hooks editando `.pre-commit-config.yaml`:

```bash
# Atualizar repo
- repo: https://github.com/outro/repo
  rev: v1.0.0
  hooks:
    - id: nome-do-hook
      args: ['--option']
```

Depois:
```bash
pre-commit install
pre-commit run --all-files
```

## ⏭️ Pular Hooks (Não Recomendado)

Para um commit específico, usar `--no-verify`:

```bash
git commit --no-verify -m "Minha mensagem"
```

⚠️ Use apenas em emergências!

## 🔄 Reinstalar Hooks

Se os hooks não estão rodando:

```bash
pre-commit uninstall
pre-commit install
```

## 🐛 Troubleshooting

### Erro: "command not found: pre-commit"

```bash
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

### Erro: "hook failed"

Os hooks detectaram problemas. Opções:

1. **Black vai formatar automaticamente:**
   ```bash
   pre-commit run black --all-files
   git add .
   ```

2. **Flake8 detectou erros que precisam fix manual:**
   - Leia a mensagem de erro
   - Corrija manualmente
   - Execute novamente

3. **Pylint tem warnings:**
   - Corrija o código
   - Ou adicione comentário `# pylint: disable=C0111`

### Erro: ".venv/bin/python: No such file"

Reinstalar .venv:
```bash
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash setup_pre_commit.sh
```

## 📊 Performance

Primeira execução pode ser lenta (baixa hooks). Depois fica rápido.

Para otimizar:
```bash
# Cache
export PRE_COMMIT_ALLOW_RERUN_OF_FAILED_HOOKS=1

# Rodar em paralelo (se suportado)
pre-commit run --all-files --hook-stage push
```

## 🎓 Exemplos

### Exemplo 1: Commit com código desformatado

```bash
# Seu código tem espaços extras
echo "x = 1  " > test.py

git add test.py
git commit -m "Fix"

# ❌ FALHOU - trailing whitespace
# Pre-commit removeu espaços automaticamente
# ✅ Tente novamente
git add test.py
git commit -m "Fix"
```

### Exemplo 2: Imports fora de ordem

```python
# Seu código
import sys
import os
from pathlib import Path
```

```bash
git add test.py
git commit -m "Novo teste"

# ✅ isort ordena automaticamente:
# import os
# import sys
# from pathlib import Path

git add test.py
git commit -m "Novo teste"
```

### Exemplo 3: Linha muito longa

```python
# Seu código tem 150 caracteres
long_string = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```bash
git commit -m "Fix"

# ⚠️ black/flake8 detecta (máx 100)
# Você precisa dividir a linha manualmente
# ou aumentar o limite em .pre-commit-config.yaml
```

## 🔗 Links Úteis

- [Pre-commit Documentation](https://pre-commit.com/)
- [Pylint - Linter](https://pylint.pycqa.org/)

## ✅ Checklist

- [ ] `.venv` ativado
- [ ] `pre-commit` instalado (`pip install pre-commit`)
- [ ] Hooks instalados (`pre-commit install`)
- [ ] Testou em arquivo (`pre-commit run --all-files`)
- [ ] Fez commit e funcionou

---

## 🚀 Quickstart Rápido

**3 comandos para começar:**

```bash
# 1. Ativar .venv
source .venv/bin/activate

# 2. Instalar hooks
bash setup_pre_commit.sh

# 3. Testar
pre-commit run --all-files
```

Pronto! Nos próximos commits, hooks rodam automaticamente.

---

## ⌨️ Atalhos Úteis

```bash
# Setup (primeira vez)
source .venv/bin/activate && bash setup_pre_commit.sh

# Testar todos os hooks em todos os arquivos
pre-commit run --all-files

# Testar hook específico
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files

# Pular hooks (emergência)
git commit --no-verify -m "Mensagem"

# Reinstalar hooks (se quebrado)
pre-commit uninstall && pre-commit install
```

---

## 📊 Resumo de Implementação

### Sistema Criado

| Item | Status | Descrição |
|------|--------|-----------|
| `.pre-commit-config.yaml` | ✅ | 11 hooks configurados |
| `setup_pre_commit.sh` | ✅ | Script de instalação |
| Documentação | ✅ | Este arquivo |

### Hooks Configurados

**Formatação (automático):**
- 🎨 black - Formata Python
- 📚 isort - Ordena imports
- 🧹 trailing-whitespace - Remove espaços extras
- ✂️ end-of-file-fixer - Normaliza fim de arquivo
- 📏 mixed-line-ending - Normaliza CRLF/LF

**Linting (você corrige):**
- 📝 flake8 - Detecta erros
- 🔍 pylint - Análise avançada
- 🐛 debug-statements - Detecta print/pdb

**Validação:**
- ✓ check-yaml, check-json, check-merge-conflict

### O Que Acontece em Cada Commit

```bash
git add .
git commit -m "Sua mensagem"
# ↓ Hooks rodam automaticamente:
# ✅ Código formatado (black)
# ✅ Imports ordenados (isort)
# ✅ Erros detectados (flake8, pylint)
# ✅ Espaços extras removidos
# ✅ Sintaxe validada
```

---

**Status:** ✅ Documentado
**Última atualização:** 8 de Dezembro de 2025

Comece: `bash setup_pre_commit.sh`
