import mysql.connector

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='novacap',     
)

cursor = conn.cursor()

# Criação do banco e da tabela de usuários
cursor.execute("CREATE DATABASE IF NOT EXISTS cpcr;")
cursor.execute("USE cpcr;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        usuario VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        numero_celular VARCHAR(20),
        senha_hash TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        senha_expira_em DATE
    );
""")

conn.commit()
cursor.close()
conn.close()

print("Banco de dados 'cpcr' e tabela 'usuarios' criados com sucesso.")
