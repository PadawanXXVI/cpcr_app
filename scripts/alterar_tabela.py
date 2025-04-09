from configuracoes import DevelopmentConfig
import mysql.connector

# Conectar ao banco
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor()

# Adicionar coluna data_criacao
try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP;")
    conn.commit()
    print("Coluna 'data_criacao' adicionada com sucesso.")
except mysql.connector.Error as err:
    print(f"Erro ao adicionar coluna: {err}")
finally:
    cursor.close()
    conn.close()
