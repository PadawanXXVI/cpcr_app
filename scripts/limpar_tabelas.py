import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from configuracoes import DevelopmentConfig
from modelos import db, Processo, Movimentacao, LogSistema, Status, Demanda, RegiaoAdministrativa
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("🧹 Limpando tabelas do banco de dados (exceto usuários)...")

    # Ordem de deleção (respeitando dependências por chave estrangeira)
    tabelas_para_limpar = [Movimentacao, Processo, LogSistema, Status, Demanda, RegiaoAdministrativa]

    for tabela in tabelas_para_limpar:
        print(f"❌ Apagando tabela: {tabela.__tablename__}")
        try:
            with db.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {tabela.__tablename__} CASCADE"))
        except Exception as e:
            print(f"⚠️ Erro ao apagar {tabela.__tablename__}: {e}")

    print("✅ Tabelas removidas com sucesso!")
