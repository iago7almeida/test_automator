import requests
import pandas as pd
from urllib.parse import quote # Usaremos para codificar os valores
import json
from datetime import datetime, timedelta
# ===================================================================================
# 1. CONFIGURAÇÕES GERAIS E REGRAS DE NEGÓCIO
# ===================================================================================
BASE_URL_USERS = "https://test.pigz.dev/admin/api/partner/users"
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTk0OCwidXNlcm5hbWUiOiJpYWdvLmFsbWVpZGFAcGlnei5jb20uYnIiLCJleHAiOjE3NTYwNDgzODEsImNvbW1lcmNlcyI6W10sImJldGEiOmZhbHNlfQ.M6nxbX-95aisn8H9ZVb5oDyMFt89tlXmD77xPrOU3TA",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

MAPA_COLUNAS_USERS = {
    'status': 'status',
    'roles': 'accessProfile.type',
    'types': 'accessProfile.name',
    'states': 'partner.locality',
    'createdStart': 'createdAt',
    'createdEnd': 'createdAt',
    'loginStart': 'lastLogin',
    'loginEnd': 'lastLogin'
}

STATE_ID_MAP = { 23: "RR", 21: "RS", 26: "SP" }

# <<< NOVO: Dicionário com as regras de negócio para validação >>>
VALID_ROLE_TYPE_COMBINATIONS = {
    "MERCHANT": ["Basic", "Manager", "Administrator"],
    "PARTNER": ["Agent", "Administrator"],
    "ADMIN": ["Commercial", "Administrator"]
}


# ===================================================================================
# 2. CASOS DE TESTE ATUALIZADOS COM BASE NAS REGRAS
# ===================================================================================
casos_de_teste_users = [
    # --- Testes de Status (simples) ---
    {"descricao": "Teste 1 (Status): Apenas usuários Ativos (status=1)", "filtros": {"status": 1}},
    {"descricao": "Teste 2 (Status): Apenas usuários Inativos (status=0)", "filtros": {"status": 0}},

    # --- Testes de Data: Última Atividade ---
    {"descricao": "Teste 3 (Data - Última Atividade): Usuários ativos com atividade nos últimos 7 dias",
     "filtros": {"status": 1, "loginStart": "01%2F08%2F2025", "loginEnd": "07%2F08%2F2025"}},
    {"descricao": "Teste 4 (Data - Última Atividade): Usuários inativos com atividade em julho",
     "filtros": {"status": 0, "loginStart": "01%2F07%2F2025", "loginEnd": "31%2F07%2F2025"}},

    # --- Testes de Perfil (roles) ---
    {"descricao": "Teste 9 (Perfil): Apenas usuários Comerciantes", "filtros": {"roles": "MERCHANT"}},
    {"descricao": "Teste 10 (Perfil Múltiplo): Usuários MERCHANT e PARTNER", "filtros": {"roles": ["MERCHANT", "PARTNER"]}},

    # --- Testes de Acesso VÁLIDOS ---
    {"descricao": "Teste 11 (Acesso Válido): MERCHANT com Manager", "filtros": {"roles": "MERCHANT", "types": "Manager"}},
    {"descricao": "Teste 12 (Acesso Válido): MERCHANT com Basic", "filtros": {"roles": "MERCHANT", "types": "Basic"}},
    {"descricao": "Teste 13 (Acesso Válido): PARTNER com Agent", "filtros": {"roles": "PARTNER", "types": "Agent"}},
    {"descricao": "Teste 14 (Acesso Válido): ADMIN com Commercial", "filtros": {"roles": "ADMIN", "types": "Commercial"}},
    {"descricao": "Teste 15 (Acesso Válido): ADMIN com Admin", "filtros": {"roles": "ADMIN", "types": "Administrator"}},

    # --- Testes de Acesso INVÁLIDOS ---
    {"descricao": "Teste 16 (Acesso Inválido): MERCHANT com Agent", "filtros": {"roles": "MERCHANT", "types": "Agent"}},
    {"descricao": "Teste 17 (Acesso Inválido): PARTNER com Basic", "filtros": {"roles": "PARTNER", "types": "Basic"}},
    {"descricao": "Teste 18 (Acesso Inválido): ADMIN com Manager", "filtros": {"roles": "ADMIN", "types": "Manager"}},

    # --- Testes de Combinação Data + Perfil + Status ---
    {"descricao": "Teste 19 (Combinado): ADMIN ativos logados no último mês",
     "filtros": {"roles": "ADMIN", "status": 1, "loginStart": "01%2F07%2F2025", "loginEnd": "31%2F07%2F2025"}},
    {"descricao": "Teste 20 (Combinado): MERCHANT inativos com login nos últimos 30 dias",
     "filtros": {"roles": "MERCHANT", "status": 0, "loginStart": "10%2F07%2F2025", "loginEnd": "10%2F08%2F2025"}},

    # --- Testes de Localização ---
    {"descricao": "Teste 21 (Localização): Usuários de Roraima (states=23)", "filtros": {"states": 23}},
    {"descricao": "Teste 22 (Localização + Perfil): Comerciantes ativos em São Paulo (states=35)",
     "filtros": {"roles": "MERCHANT", "status": 1, "states": 35}},

    # --- Testes Negativos ---
    {"descricao": "Teste 23 (Negativo): Período inválido (data início > data fim)",
     "filtros": {"loginStart": "11%2F08%2F2025", "loginEnd": "01%2F08%2F2025"}},
    {"descricao": "Teste 24 (Negativo): Perfil inexistente",
     "filtros": {"roles": "INVALIDO"}},
    {"descricao": "Teste 25 (Negativo): Acesso inexistente",
     "filtros": {"types": "SuperUser"}}
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
        if key in ['roles', 'types']:
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
        if user.get('merchant') and user['merchant'].get('merchantCommerces'):
            for commerce in user['merchant']['merchantCommerces']:
                if commerce.get('merchantAddress') and commerce['merchantAddress'].get('state'):
                    states.add(commerce['merchantAddress']['state'])

        access_profile = user.get('accessProfile')
        access_profile_name = access_profile.get('name') if access_profile else None
        access_profile_type = access_profile.get('type') if access_profile else None

        user_data = {
            'id': user.get('id'),
            'status': user.get('status'),
            'accessProfile.type': access_profile_type,
            'accessProfile.name': access_profile_name,
            'createdAt': user.get('createdAt'),
            'merchant_states': list(states)
        }
        processed_list.append(user_data)
    return processed_list

def buscar_dataframe(url, json_key):
    """Faz a requisição, processa o JSON e retorna um DataFrame."""
    try:
        response = requests.get(url, headers=headers)
        print("DEBUG Status:", response.status_code)
        print("DEBUG Conteúdo:", response.text[:300])  # Mostra parte da resposta

        response.raise_for_status()
        items = response.json().get(json_key, [])
        if not items: 
            return pd.DataFrame()

        processed_items = processar_usuarios(items)
        df = pd.DataFrame(processed_items)
        if 'createdAt' in df.columns:
            df['createdAt'] = pd.to_datetime(df['createdAt'], errors='coerce')
        return df

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"  [ERRO] Falha na requisição ou ao processar JSON. Erro: {e}")
        return None


def analisar_teste_usuario(teste, df_master):
    """Executa um único caso de teste, validando consistência e abrangência."""
    descricao = teste['descricao']
    filtros = teste['filtros'].copy()
    print("=" * 70)
    print(f"Executando: {descricao}")
    print("=" * 70)

    filtros['limit'] = 1000
    query_string = construir_query_string(filtros)
    url_filtrada = f"{BASE_URL_USERS}?{query_string}"
    df_filtrado = buscar_dataframe(url_filtrada, json_key='users')
    if df_filtrado is None: return

    print(f"URL de Teste: {url_filtrada}")
    print(f"API retornou {len(df_filtrado)} usuários para este filtro.\n")

    # --- VALIDAÇÃO 1: CONSISTÊNCIA INTERNA ---
    print("1. Validando Consistência Interna...")
    erros_consistencia = 0
    if not df_filtrado.empty:
        for param, valor_esperado in teste['filtros'].items():
            coluna = MAPA_COLUNAS_USERS.get(param)
            if not coluna or coluna not in df_filtrado.columns: continue

            if param in ['roles', 'types']:
                valores_permitidos = valor_esperado if isinstance(valor_esperado, list) else [valor_esperado]
                inconsistentes = df_filtrado[~df_filtrado[coluna].isin(valores_permitidos)]
            elif param == 'states':
                sigla_estado = STATE_ID_MAP.get(valor_esperado)
                inconsistentes = df_filtrado[df_filtrado[coluna].apply(lambda x: sigla_estado not in x)]
            else:
                inconsistentes = df_filtrado[df_filtrado[coluna] != valor_esperado]

            if not inconsistentes.empty:
                print(f"  ❌ FALHA: {len(inconsistentes)} usuários não cumprem o critério '{param}={valor_esperado}'.")
                erros_consistencia += 1

    if erros_consistencia == 0:
        print("  ✅ SUCESSO: Todos os usuários retornados são consistentes com os filtros.")

    # --- VALIDAÇÃO 2: ABRANGÊNCIA ---
    print("\n2. Validando Abrangência (vs lista completa)...")
    df_esperado = df_master.copy()
    for param, valor in teste['filtros'].items():
        coluna = MAPA_COLUNAS_USERS.get(param)
        if not coluna or df_esperado.empty or coluna not in df_esperado.columns: continue

        if param in ['roles', 'types']:
            valores_permitidos = valor if isinstance(valor, list) else [valor]
            df_esperado = df_esperado[df_esperado[coluna].isin(valores_permitidos)]
        elif param == 'states':
            sigla_estado = STATE_ID_MAP.get(valor)
            # A regra de negócio é que o filtro de estado só se aplica a usuários que têm endereços.
            # Os outros são ignorados pelo filtro.
            df_esperado = df_esperado[df_esperado[coluna].apply(lambda x: sigla_estado in x)]
        else:
            df_esperado = df_esperado[df_esperado[coluna].notna() & (df_esperado[coluna] == valor)]

    # <<< CORREÇÃO APLICADA AQUI >>>
    # Garante que só tentamos acessar a coluna 'id' se o DataFrame não estiver vazio.
    ids_esperados = set(df_esperado['id']) if not df_esperado.empty else set()
    ids_retornados = set(df_filtrado['id']) if not df_filtrado.empty else set()

    if ids_esperados == ids_retornados:
        print("  ✅ SUCESSO: A lista da API corresponde perfeitamente ao esperado.")
    else:
        faltantes = ids_esperados - ids_retornados
        extras = ids_retornados - ids_esperados
        if faltantes: print(f"  ❌ FALHA: {len(faltantes)} usuários esperados NÃO foram retornados. IDs: {list(faltantes)[:5]}...")
        if extras: print(f"  ❌ FALHA: {len(extras)} usuários foram retornados INCORRETAMENTE. IDs: {list(extras)[:5]}...")
    print("\n")

# ===================================================================================
# 4. ROTEIRO DE EXECUÇÃO PRINCIPAL
# ===================================================================================
print("Iniciando Roteiro de Testes para a API de Filtro de Usuários...")
url_master = f"{BASE_URL_USERS}?limit=1000"
print(f"Buscando a lista de referência completa em: {url_master}")
df_master_users = buscar_dataframe(url_master, json_key='users')

if df_master_users is not None and not df_master_users.empty:
    print(f"Lista de referência carregada com {len(df_master_users)} usuários.\n")
    for teste in casos_de_teste_users:
        analisar_teste_usuario(teste, df_master_users)
else:
    print("Não foi possível carregar a lista de referência de usuários. Abortando testes.")

print("Roteiro de Testes Concluído.")
