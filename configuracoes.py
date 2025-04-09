import sys
import os
from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao sys.path (opcional, útil em scripts)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Carrega as variáveis do .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Classes de configuração
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'cpcr')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
