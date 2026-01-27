#!/bin/bash
# ==============================================================================
# Quick Activation Script for .venv
# ==============================================================================
# Facilita a ativação do virtual environment
#
# Uso:
#   source activate.sh    # Ativa o venv
#   source deactivate.sh  # Desativa (ou use: deactivate)
# ==============================================================================

if [ -z "$BASH_SOURCE" ]; then
    echo "❌ Este script deve ser executado com 'source', não diretamente!"
    echo ""
    echo "Uso correto:"
    echo "  source activate.sh"
    exit 1
fi

# Detectar o sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    VENV_ACTIVATE=".venv/bin/activate"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    VENV_ACTIVATE=".venv\\Scripts\\activate"
else
    echo "❌ Sistema operacional não suportado: $OSTYPE"
    exit 1
fi

# Verificar se o venv existe
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "❌ Virtual environment não encontrado em $VENV_ACTIVATE"
    echo ""
    echo "Criando um novo venv:"
    python -m venv .venv
fi

# Ativar o venv
echo "Ativando o virtual environment..."
source "$VENV_ACTIVATE"

echo "✅ Virtual environment ativado!"

echo "Próximos passos:"
echo "  1. Instalando dependências..."
pip install -r requirements.txt
echo "  2. Instalando ferramentas de teste"
playwright install
echo "Finalizado"
