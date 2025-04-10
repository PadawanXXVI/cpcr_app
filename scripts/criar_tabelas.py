import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracoes import DevelopmentConfig
import mysql.connector

conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS processos (
    id_processo INT AUTO_INCREMENT PRIMARY KEY,
    numero_processo VARCHAR(25) NOT NULL UNIQUE,
    data_criacao_ra DATE NOT NULL,
    data_entrada_cpcr DATE NOT NULL,
    admin_regional VARCHAR(100) NOT NULL,
    tipo_demanda VARCHAR(100) NOT NULL,
    vistoria_completa TEXT,
    diretoria_destino VARCHAR(10),
    status_demanda VARCHAR(100) NOT NULL,
    descricao_processo TEXT,
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
''')

print("✅ Tabela 'processos' criada com sucesso.")
conn.commit()
cursor.close()
conn.close()
