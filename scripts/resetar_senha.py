import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import gerar_senha_provisoria

from werkzeug.security import generate_password_hash
import mysql.connector
from configuracoes import DevelopmentConfig

# Conectar ao banco de dados
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor()

# ID do usuário a redefinir (altere este valor conforme o usuário)
id_usuario = 1  # ← Substitua pelo ID real do usuário

# Gerar senha provisória e hash
senha_provisoria = gerar_senha_provisoria()
senha_hash = generate_password_hash(senha_provisoria)

# Atualizar no banco
cursor.execute("""
    UPDATE usuarios
    SET senha_hash = %s, senha_provisoria = TRUE
    WHERE id_usuario = %s
""", (senha_hash, id_usuario))
conn.commit()

# Encerrar conexão
cursor.close()
conn.close()

# Mostrar senha gerada
print("=" * 50)
print(f"Senha provisória gerada para o usuário ID {id_usuario}:")
print(f"🔐 {senha_provisoria}")
print("Informe esta senha ao usuário e oriente a trocar no primeiro acesso.")
print("=" * 50)
