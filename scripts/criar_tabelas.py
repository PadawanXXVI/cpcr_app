import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from configuracoes import DevelopmentConfig
from modelos import db, Usuario, Processo, Movimentacao, LogSistema, Status, Demanda, RegiaoAdministrativa
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("🔄 Iniciando criação do banco de dados 'cr_novacap'...")

    # Tabelas que podem ser removidas (exceto usuários)
    tabelas_para_apagar = [Movimentacao, Processo, LogSistema, Status, Demanda, RegiaoAdministrativa]

    for tabela in tabelas_para_apagar:
        print(f"🧨 Apagando tabela: {tabela.__tablename__}")
        with db.engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {tabela.__tablename__} CASCADE"))

    db.create_all()
    print("✅ Tabelas criadas com sucesso.")

    # Regiões Administrativas
    if not RegiaoAdministrativa.query.first():
        ras = [
            ("RA I", "Plano Piloto"), ("RA II", "Gama"), ("RA III", "Taguatinga"),
            ("RA IV", "Brazlândia"), ("RA V", "Sobradinho"), ("RA VI", "Planaltina"),
            ("RA VII", "Paranoá"), ("RA VIII", "Núcleo Bandeirante"), ("RA IX", "Ceilândia"),
            ("RA X", "Guará"), ("RA XI", "Cruzeiro"), ("RA XII", "Samambaia"),
            ("RA XIII", "Santa Maria"), ("RA XIV", "São Sebastião"), ("RA XV", "Recanto das Emas"),
            ("RA XVI", "Lago Sul"), ("RA XVII", "Riacho Fundo"), ("RA XVIII", "Lago Norte"),
            ("RA XIX", "Candangolândia"), ("RA XX", "Águas Claras"), ("RA XXI", "Riacho Fundo II"),
            ("RA XXII", "Sudoeste/Octogonal"), ("RA XXIII", "Varjão"), ("RA XXIV", "Park Way"),
            ("RA XXV", "SCIA/Estrutural"), ("RA XXVI", "Sobradinho II"), ("RA XXVII", "Jardim Botânico"),
            ("RA XXVIII", "Itapoã"), ("RA XXIX", "SIA"), ("RA XXX", "Vicente Pires"),
            ("RA XXXI", "Fercal"), ("RA XXXII", "Sol Nascente e Pôr do Sol"),
            ("RA XXXIII", "Arniqueira"), ("RA XXXIV", "Arapoanga"), ("RA XXXV", "Água Quente")
        ]
        for cod, nome in ras:
            db.session.add(RegiaoAdministrativa(codigo=cod, nome=nome))

    # Demandas
    if not Demanda.query.first():
        demandas = sorted([
            "Alambrado (Cercamento)",
            "Boca de Lobo",
            "Bueiro",
            "Calçada",
            "Doação de Mudas",
            "Estacionamentos",
            "Galeria de Água Potável",
            "Galeria de Águas Pluviais",
            "Jardim",
            "Mato Alto",
            "Meio-fio",
            "Parque Infantil",
            "Passagem Subterrânea",
            "Passarela",
            "Pisos Articulados",
            "Pista de Skate",
            "Poda / Supressão de Árvore",
            "Ponto de Encontro Comunitário (PEC)",
            "Praça",
            "Quadra de Esporte",
            "Rampa",
            "Recapeamento Asfáltico",
            "Tapa-buraco"
        ])
        for d in demandas:
            db.session.add(Demanda(nome=d))

    # Status
    if not Status.query.first():
        status = sorted([
            "Atendido",
            "Devolvido à RA de origem - ausência de vistoria / fotogeorreferenciada",
            "Devolvido à RA de origem - serviço de implantação",
            "Devolvido à RA de origem - serviço de natureza continuada pela diretoria",
            "Enviado à Diretoria das Cidades",
            "Enviado à Diretoria de Obras",
            "Improcedente - tramitação pelo SGIA"
        ])
        for s in status:
            db.session.add(Status(nome=s))

    db.session.commit()
    print("✅ Dados dinâmicos inseridos com sucesso (se estavam ausentes).")
