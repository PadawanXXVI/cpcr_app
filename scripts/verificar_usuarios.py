# scripts/verificar_usuarios.py

import os
import sys
from dotenv import load_dotenv

# Garante que o diretório raiz esteja no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracoes import DevelopmentConfig
from modelos import db, Usuario
from flask import Flask

# Carrega variáveis do .env
load_dotenv()

# Inicializa o app e o banco
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("📋 Lista de usuários cadastrados:\n")
    usuarios = Usuario.query.order_by(Usuario.criado_em.desc()).all()

    for usuario in usuarios:
        status = "✅ Aprovado" if usuario.aprovado else "⏳ Pendente"
        admin = "👑 Admin" if usuario.is_admin else ""
        print(f"{usuario.id_usuario}: {usuario.nome} ({usuario.usuario}) - {usuario.email} - {status} {admin}")

    resposta = input("\nDeseja aprovar algum usuário? (s/n): ").strip().lower()
    if resposta == 's':
        try:
            id_escolhido = int(input("Informe o ID do usuário que deseja aprovar: "))
            usuario = Usuario.query.get(id_escolhido)
            if usuario:
                usuario.aprovado = True
                db.session.commit()
                print(f"\n✔️ Usuário ID {id_escolhido} aprovado com sucesso!")
            else:
                print("Usuário não encontrado.")
        except Exception as e:
            print(f"\n[✘] Erro ao aprovar o usuário: {e}")
