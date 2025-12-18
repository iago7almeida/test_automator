import json
import logging
from urllib.parse import quote

import pandas as pd
import requests

from config.api_auth import APIAuthManager
from config.settings import get_config

logger = logging.getLogger(__name__)

config = get_config()
auth_manager = APIAuthManager()


def get_users_url():
    return f"{config.API_ADMIN_BASE}{config.API_USERS_ENDPOINT}"


def get_orders_url():
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


def construir_query_string(params):
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
    try:
        logger.info("📡 Buscando dados: %s", url)
        response = auth_manager.make_authenticated_request("GET", url, force_new_token=force_new_token)

        if response is None:
            logger.error("❌ Falha na requisição autenticada")
            return None

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
