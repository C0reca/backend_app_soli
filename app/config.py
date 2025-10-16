# app/config.py

import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv()

# Configuração da Base de Dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/gestao_app")

# Configuração JWT (para uso futuro com autenticação)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 60 * 24  # 1 dia

# Configurações de Email (opcional)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.exemplo.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "no-reply@exemplo.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "password")
