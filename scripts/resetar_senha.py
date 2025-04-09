from configuracoes import DevelopmentConfig
import mysql.connector
from utils import gerar_senha_provisoria
from werkzeug.security import generate_password_hash

# Conectar ao banco
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor(dictionary=True)

# Listar usuários
cursor.execute("SELECT id_usuario, usuario FROM usuarios")
usuarios = cursor.fetchall()

print("\nUsuários cadastrados:\n")
for u in usuarios:
    print(f"{u['id_usuario']}: {u['usuario']}")

usuario_id = input("\nInforme o ID do usuário para gerar nova senha provisória: ")

# Gerar e aplicar senha provisória
nova_senha = gerar_senha_provisoria()
senha_hash = generate_password_hash(nova_senha)

cursor.execute("""
    UPDATE usuarios SET senha_hash = %s, senha_provisoria = TRUE
    WHERE id_usuario = %s
""", (senha_hash, usuario_id))
conn.commit()

print(f"\n==============================")
print(f"Senha provisória gerada para o usuário ID {usuario_id}:")
print(f"\n🔐 {nova_senha}")
print(f"\nInforme esta senha ao usuário e oriente a trocar no primeiro acesso.")
print(f"==============================")
