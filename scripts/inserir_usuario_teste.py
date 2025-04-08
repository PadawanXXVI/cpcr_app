from werkzeug.security import generate_password_hash
import mysql.connector
from config import DevelopmentConfig

# Conexão com o banco
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor()

# Dados do usuário
nome = "Usuário Teste"
usuario = "teste.usuario"
email = "teste@example.com"
numero_celular = "61999999999"
senha = "senha123"
senha_hash = generate_password_hash(senha)

# Inserção no banco
cursor.execute('''
    INSERT INTO usuarios (nome, usuario, email, numero_celular, senha_hash)
    VALUES (%s, %s, %s, %s, %s)
''', (nome, usuario, email, numero_celular, senha_hash))

conn.commit()
cursor.close()
conn.close()

print("Usuário inserido com sucesso!")
