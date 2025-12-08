import json
import logging
from urllib.parse import quote

import pandas as pd
import requests

# Importar gerenciador de autenticação
from config.api_auth import APIAuthManager
from config.settings import get_config

# Configurar logger
logger = logging.getLogger(__name__)

# ===================================================================================
# 1. CONFIGURAÇÕES GERAIS E REGRAS DE NEGÓCIO
# ===================================================================================

# Obter configuração centralizada
config = get_config()
auth_manager = APIAuthManager()


# URLs são construídas dinamicamente a partir da config
def get_users_url():
    """Constrói URL de usuários dinamicamente."""
    return f"{config.API_ADMIN_BASE}{config.API_USERS_ENDPOINT}"


def get_orders_url():
    """Constrói URL de pedidos dinamicamente."""
    return f"{config.API_ADMIN_BASE}{config.API_ORDERS_ENDPOINT}"


MAPA_COLUNAS_USERS = {
    "status": "status",
    "roles": "accessProfile.type",
    "types": "accessProfile.name",
    "states": "partner.locality",
    "createdStart": "createdAt",
    "createdEnd": "createdAt",
    "loginStart": "lastLogin",
    "loginEnd": "lastLogin",
}

STATE_ID_MAP = {23: "RR", 21: "RS", 26: "SP"}

# <<< NOVO: Dicionário com as regras de negócio para validação >>>
VALID_ROLE_TYPE_COMBINATIONS = {
    "MERCHANT": ["Basic", "Manager", "Administrator"],
    "PARTNER": ["Agent", "Administrator"],
    "ADMIN": ["Commercial", "Administrator"],
}


# ===================================================================================
# 2. CASOS DE TESTE ATUALIZADOS COM BASE NAS REGRAS
# ===================================================================================
casos_de_teste_users = [
    # --- Testes de Status (simples) ---
    {
        "descricao": "Teste 1 (Status): Apenas usuários Ativos (status=1)",
        "filtros": {"status": 1},
    },
    {
        "descricao": "Teste 2 (Status): Apenas usuários Inativos (status=0)",
        "filtros": {"status": 0},
    },
    # --- Testes de Data: Última Atividade ---
    {
        "descricao": "Teste 3 (Data - Última Atividade): Usuários ativos com atividade nos últimos 7 dias",
        "filtros": {
            "status": 1,
            "loginStart": "01%2F08%2F2025",
            "loginEnd": "07%2F08%2F2025",
        },
    },
    {
        "descricao": "Teste 4 (Data - Última Atividade): Usuários inativos com atividade em julho",
        "filtros": {
            "status": 0,
            "loginStart": "01%2F07%2F2025",
            "loginEnd": "31%2F07%2F2025",
        },
    },
    # --- Testes de Perfil (roles) ---
    {
        "descricao": "Teste 9 (Perfil): Apenas usuários Comerciantes",
        "filtros": {"roles": "MERCHANT"},
    },
    {
        "descricao": "Teste 10 (Perfil Múltiplo): Usuários MERCHANT e PARTNER",
        "filtros": {"roles": ["MERCHANT", "PARTNER"]},
    },
    # --- Testes de Acesso VÁLIDOS ---
    {
        "descricao": "Teste 11 (Acesso Válido): MERCHANT com Manager",
        "filtros": {"roles": "MERCHANT", "types": "Manager"},
    },
    {
        "descricao": "Teste 12 (Acesso Válido): MERCHANT com Basic",
        "filtros": {"roles": "MERCHANT", "types": "Basic"},
    },
    {
        "descricao": "Teste 13 (Acesso Válido): PARTNER com Agent",
        "filtros": {"roles": "PARTNER", "types": "Agent"},
    },
    {
        "descricao": "Teste 14 (Acesso Válido): ADMIN com Commercial",
        "filtros": {"roles": "ADMIN", "types": "Commercial"},
    },
    {
        "descricao": "Teste 15 (Acesso Válido): ADMIN com Admin",
        "filtros": {"roles": "ADMIN", "types": "Administrator"},
    },
    # --- Testes de Acesso INVÁLIDOS ---
    {
        "descricao": "Teste 16 (Acesso Inválido): MERCHANT com Agent",
        "filtros": {"roles": "MERCHANT", "types": "Agent"},
    },
    {
        "descricao": "Teste 17 (Acesso Inválido): PARTNER com Basic",
        "filtros": {"roles": "PARTNER", "types": "Basic"},
    },
    {
        "descricao": "Teste 18 (Acesso Inválido): ADMIN com Manager",
        "filtros": {"roles": "ADMIN", "types": "Manager"},
    },
    # --- Testes de Combinação Data + Perfil + Status ---
    {
        "descricao": "Teste 19 (Combinado): ADMIN ativos logados no último mês",
        "filtros": {
            "roles": "ADMIN",
            "status": 1,
            "loginStart": "01%2F07%2F2025",
            "loginEnd": "31%2F07%2F2025",
        },
    },
    {
        "descricao": "Teste 20 (Combinado): MERCHANT inativos com login nos últimos 30 dias",
        "filtros": {
            "roles": "MERCHANT",
            "status": 0,
            "loginStart": "10%2F07%2F2025",
            "loginEnd": "10%2F08%2F2025",
        },
    },
    # --- Testes de Localização ---
    {
        "descricao": "Teste 21 (Localização): Usuários de Roraima (states=23)",
        "filtros": {"states": 23},
    },
    {
        "descricao": "Teste 22 (Localização + Perfil): Comerciantes ativos em São Paulo (states=35)",
        "filtros": {"roles": "MERCHANT", "status": 1, "states": 35},
    },
    # --- Testes Negativos ---
    {
        "descricao": "Teste 23 (Negativo): Período inválido (data início > data fim)",
        "filtros": {"loginStart": "11%2F08%2F2025", "loginEnd": "01%2F08%2F2025"},
    },
    {
        "descricao": "Teste 24 (Negativo): Perfil inexistente",
        "filtros": {"roles": "INVALIDO"},
    },
    {
        "descricao": "Teste 25 (Negativo): Acesso inexistente",
        "filtros": {"types": "SuperUser"},
    },
]


# ===================================================================================
# 3. FUNÇÕES DE ANÁLISE E VALIDAÇÃO (ATUALIZADAS)
# ===================================================================================


def construir_query_string(params):
    """
    Constrói a string de query, adicionando '[]' aos parâmetros 'roles' e 'types'.
    """
    parts = []
    for key, value in params.items():
        if key in ["roles", "types"]:
            if isinstance(value, list):
                for item in value:
                    parts.append(f"{key}[]={quote(str(item))}")
            else:
                parts.append(f"{key}[]={quote(str(value))}")
        else:
            parts.append(f"{key}={quote(str(value))}")
    return "&".join(parts)


def processar_usuarios(users_list):
    """Processa a lista de usuários do JSON para um formato plano e útil."""
    processed_list = []
    for user in users_list:
        states = set()
        if user.get("merchant") and user["merchant"].get("merchantCommerces"):
            for commerce in user["merchant"]["merchantCommerces"]:
                if commerce.get("merchantAddress") and commerce["merchantAddress"].get("state"):
                    states.add(commerce["merchantAddress"]["state"])

        access_profile = user.get("accessProfile")
        access_profile_name = access_profile.get("name") if access_profile else None
        access_profile_type = access_profile.get("type") if access_profile else None

        user_data = {
            "id": user.get("id"),
            "status": user.get("status"),
            "accessProfile.type": access_profile_type,
            "accessProfile.name": access_profile_name,
            "createdAt": user.get("createdAt"),
            "merchant_states": list(states),
        }
        processed_list.append(user_data)
    return processed_list


def buscar_dataframe(url, json_key, force_new_token=False):
    """
    Faz a requisição autenticada, processa o JSON e retorna um DataFrame.

    Args:
        url: URL completa para fazer a requisição
        json_key: Chave do JSON que contém os dados (ex: 'users')
        force_new_token: Força geração de novo token

    Returns:
        pd.DataFrame: DataFrame com os dados processados
        None: Se houver erro na requisição
    """
    try:
        # Usar o gerenciador de autenticação para fazer a requisição
        logger.info("📡 Buscando dados: %s", url)
        response = auth_manager.make_authenticated_request("GET", url, force_new_token=force_new_token)

        if response is None:
            logger.error("❌ Falha na requisição autenticada")
            return None

        logger.debug("✅ Status: %s", response.status_code)
        logger.debug("   Resposta: %s...", response.text[:300])

        items = response.json().get(json_key, [])
        if not items:
            logger.warning("⚠️ Nenhum item encontrado com chave '%s'", json_key)
            return pd.DataFrame()

        processed_items = processar_usuarios(items)
        df = pd.DataFrame(processed_items)
        if "createdAt" in df.columns:
            df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

        logger.info("✅ %d registros carregados com sucesso", len(df))
        return df

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error("❌ Erro na requisição: %s", str(e))
        return None


def _validar_consistencia_interna(df_filtrado, teste):
    """Helper: Valida se os dados filtrados respeitam os critérios do teste."""
    logger.info("1️⃣ Validando Consistência Interna...")
    erros_consistencia = 0
    if df_filtrado.empty:
        return erros_consistencia

    for param, valor_esperado in teste["filtros"].items():
        coluna = MAPA_COLUNAS_USERS.get(param)
        if not coluna or coluna not in df_filtrado.columns:
            continue

        if param in ["roles", "types"]:
            valores_permitidos = valor_esperado if isinstance(valor_esperado, list) else [valor_esperado]
            inconsistentes = df_filtrado[~df_filtrado[coluna].isin(valores_permitidos)]
        elif param == "states":
            inconsistentes = df_filtrado[df_filtrado[coluna].apply(lambda x, val=valor_esperado: val not in x)]
        else:
            inconsistentes = df_filtrado[df_filtrado[coluna] != valor_esperado]

        if not inconsistentes.empty:
            logger.warning("  ❌ FALHA: %d usuários não cumprem '%s=%s'", len(inconsistentes), param, valor_esperado)
            erros_consistencia += 1

    if erros_consistencia == 0:
        logger.info("  ✅ Consistência validada com sucesso")
    return erros_consistencia


def _validar_abrangencia(df_filtrado, df_master, teste):
    """Helper: Valida se a API retornou exatamente os dados esperados."""
    logger.info("\n2️⃣ Validando Abrangência (vs lista completa)...")
    df_esperado = df_master.copy()

    for param, valor in teste["filtros"].items():
        coluna = MAPA_COLUNAS_USERS.get(param)
        if not coluna or df_esperado.empty or coluna not in df_esperado.columns:
            continue

        if param in ["roles", "types"]:
            valores_permitidos = valor if isinstance(valor, list) else [valor]
            df_esperado = df_esperado[df_esperado[coluna].isin(valores_permitidos)]
        elif param == "states":
            df_esperado = df_esperado[df_esperado[coluna].apply(lambda x, v=valor: v in x)]
        else:
            df_esperado = df_esperado[df_esperado[coluna].notna() & (df_esperado[coluna] == valor)]

    ids_esperados = set(df_esperado["id"]) if not df_esperado.empty else set()
    ids_retornados = set(df_filtrado["id"]) if not df_filtrado.empty else set()

    if ids_esperados == ids_retornados:
        logger.info("  ✅ Abrangência validada - Resultados corretos!")
    else:
        faltantes = ids_esperados - ids_retornados
        extras = ids_retornados - ids_esperados
        if faltantes:
            logger.error("  ❌ %d usuários esperados não foram retornados", len(faltantes))
        if extras:
            logger.error("  ❌ %d usuários retornados incorretamente", len(extras))
    logger.info("")


def analisar_teste_usuario(teste, df_master):
    """Executa um único caso de teste, validando consistência e abrangência."""
    descricao = teste["descricao"]
    filtros = teste["filtros"].copy()
    logger.info("=" * 70)
    logger.info("🧪 %s", descricao)
    logger.info("=" * 70)

    filtros["limit"] = 1000
    query_string = construir_query_string(filtros)
    url_filtrada = f"{get_users_url()}?{query_string}"
    df_filtrado = buscar_dataframe(url_filtrada, json_key="users")
    if df_filtrado is None:
        logger.error("❌ Não conseguiu buscar dados filtrados")
        return

    logger.debug("URL de Teste: %s", url_filtrada)
    logger.info("✅ API retornou %d usuários\n", len(df_filtrado))

    # Executar validações
    _validar_consistencia_interna(df_filtrado, teste)
    _validar_abrangencia(df_filtrado, df_master, teste)


# ===================================================================================
# 4. ROTEIRO DE EXECUÇÃO PRINCIPAL
# ===================================================================================
def executar_suite_testes():  # pylint: disable=too-many-branches,too-many-statements
    """Executa a suite completa de testes."""
    logger.info("🚀 Iniciando Suite de Testes de Filtro de Usuários")
    logger.info("📍 Ambiente: %s", config.ENVIRONMENT.value.upper())
    logger.info("📍 API Base: %s", config.API_ADMIN_BASE)

    # Gerar novo token antes de começar
    token = auth_manager.get_valid_token(force_refresh=True)
    if not token:
        logger.error("❌ Falha ao gerar token. Aborte dos testes.")
        return

    logger.info("✅ Token gerado com sucesso: %s...\n", token[:50])

    # Buscar lista de referência
    url_master = f"{get_users_url()}?limit=1000"
    logger.info("📋 Buscando lista de referência: %s", url_master)
    df_master_users = buscar_dataframe(url_master, json_key="users")

    if df_master_users is not None and not df_master_users.empty:
        logger.info("✅ Lista de referência carregada: %d usuários\n", len(df_master_users))
        for teste in casos_de_teste_users:
            analisar_teste_usuario(teste, df_master_users)
    else:
        logger.error("❌ Não foi possível carregar a lista de referência. Testes abortados.")

    logger.info("🏁 Suite de Testes Concluída\n")


# Se executar como script
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    executar_suite_testes()
