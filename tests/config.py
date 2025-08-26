import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Lê as credenciais do ambiente, com valores padrão caso não sejam encontradas
USER_EMAIL = os.getenv("USER_EMAIL", "default_email@example.com")
USER_PASSWORD = os.getenv("USER_PASSWORD", "default_password")