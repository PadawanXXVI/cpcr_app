from flask import Flask
from configuracoes import DevelopmentConfig
from modelos import db, Processo, Movimentacao, LogSistema, Demanda, Status, RegiaoAdministrativa

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("🧼 Limpando dados das tabelas (exceto usuários)...")

    tabelas = [Movimentacao, Processo, LogSistema, Status, Demanda, RegiaoAdministrativa]
    
    for tabela in tabelas:
        registros = db.session.query(tabela).delete()
        print(f"→ {registros} registros apagados da tabela {tabela.__tablename__}")

    db.session.commit()
    print("✅ Limpeza concluída com sucesso.")
