# scripts/verificar_usuarios.py

import sys
import os
# Garante que o diretório raiz esteja no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracoes import DevelopmentConfig
import mysql.connector

# Conectar ao banco de dados
conn = mysql.connector.connect(
    host=DevelopmentConfig.MYSQL_HOST,
    user=DevelopmentConfig.MYSQL_USER,
    password=DevelopmentConfig.MYSQL_PASSWORD,
    database=DevelopmentConfig.MYSQL_DATABASE
)

cursor = conn.cursor(dictionary=True)

print("📋 Lista de usuários cadastrados (aguardando aprovação):\n")

cursor.execute("SELECT id_usuario, nome, usuario, email, aprovado FROM usuarios ORDER BY data_criacao DESC")
usuarios = cursor.fetchall()

for usuario in usuarios:
    status = "✅ Aprovado" if usuario['aprovado'] else "⏳ Pendente"
    print(f"{usuario['id_usuario']}: {usuario['nome']} ({usuario['usuario']}) - {usuario['email']} - {status}")

# Opcional: permitir aprovar um usuário manualmente
resposta = input("\nDeseja aprovar algum usuário? (s/n): ").strip().lower()
if resposta == 's':
    try:
        id_escolhido = int(input("Informe o ID do usuário que deseja aprovar: "))
        cursor.execute("UPDATE usuarios SET aprovado = TRUE WHERE id_usuario = %s", (id_escolhido,))
        conn.commit()
        print(f"\n✔️ Usuário ID {id_escolhido} aprovado com sucesso!")
    except Exception as e:
        print(f"\n[✘] Erro ao aprovar o usuário: {e}")

cursor.close()
conn.close()
