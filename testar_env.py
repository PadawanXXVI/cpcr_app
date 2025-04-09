# testar_env.py

from dotenv import load_dotenv
import os

# Carregar o .env
load_dotenv()

# Recuperar e exibir a senha de e-mail
email = os.getenv("EMAIL_USER")
senha = os.getenv("EMAIL_PASSWORD")

print(f"📧 E-mail configurado: {email}")
print(f"🔐 Senha lida do .env: {senha}")
