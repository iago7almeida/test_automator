@echo off
REM ==============================================================================
REM Quick Activation Script for .venv (Windows)
REM ==============================================================================
REM Facilita a ativação do virtual environment no Windows
REM
REM Uso:
REM   activate.bat    - Ativa o venv
REM   deactivate      - Desativa
REM ==============================================================================

setlocal enabledelayedexpansion

REM Verificar se o venv existe
if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo ❌ Virtual environment nao encontrado em .venv\Scripts\activate.bat
    echo.
    echo Criar um novo venv:
    echo   python -m venv .venv
    echo   activate.bat
    echo.
    pause
    exit /b 1
)

REM Ativar o venv
call ".venv\Scripts\activate.bat"

echo.
echo ✅ Virtual environment ativado!
echo.
echo Proximos passos:
echo   1. pip install -r requirements.txt
echo   2. playwright install
echo   3. pre-commit install
echo   4. pytest -v
echo.

endlocal
