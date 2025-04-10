# scripts/resetar_senha.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracoes import DevelopmentConfig
from scripts.utils import gerar_senha_provisoria
import mysql.connector
from werkzeug.security import generate_password_hash

# Conectar ao banco de dados
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor(dictionary=True)

id_usuario = input("Digite o ID do usuário para redefinir a senha: ")

nova_senha = gerar_senha_provisoria()
senha_hash = generate_password_hash(nova_senha)

cursor.execute("""
    UPDATE usuarios
    SET senha_hash = %s, senha_provisoria = TRUE
    WHERE id_usuario = %s
""", (senha_hash, id_usuario))
conn.commit()

print("="*50)
print(f"Senha provisória gerada para o usuário ID {id_usuario}:")
print(f">>> {nova_senha}")
print("Informe esta senha ao usuário e oriente a trocar no primeiro acesso.")
print("="*50)
