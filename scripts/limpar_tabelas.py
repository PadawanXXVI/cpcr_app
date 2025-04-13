from flask import Flask
from configuracoes import DevelopmentConfig
from modelos import db, Processo, Movimentacao, LogSistema, Status, Demanda, RegiaoAdministrativa
from sqlalchemy import text

# Inicializa o app Flask
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("🧹 Limpando tabelas do banco de dados...")

    # Ordem correta para remoção (tabelas com FK dependentes vêm primeiro)
    tabelas = [Movimentacao, Processo, LogSistema, Status, Demanda, RegiaoAdministrativa]

    for tabela in tabelas:
        print(f"❌ Apagando tabela: {tabela.__tablename__}")
        with db.engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {tabela.__tablename__} CASCADE"))

    db.session.commit()
    print("✅ Tabelas removidas com sucesso!")
