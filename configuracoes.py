import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class DevelopmentConfig:
    DEBUG = True

    # Chave secreta usada para sessões, autenticação etc.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # URI de conexão com o banco de dados MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
