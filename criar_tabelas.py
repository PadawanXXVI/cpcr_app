from flask import Flask
from configuracoes import DevelopmentConfig
from modelos import db, Usuario, Processo, Movimentacao, LogSistema, Status, Demanda, RegiaoAdministrativa
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("🔄 Iniciando criação do banco de dados 'cr_novacap'...")

    # Tabelas em ordem para evitar conflitos com foreign keys
    tabelas = [Movimentacao, Processo, Usuario, LogSistema, Status, Demanda, RegiaoAdministrativa]

    for tabela in tabelas:
        print(f"🧨 Apagando tabela: {tabela.__tablename__}")
        with db.engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {tabela.__tablename__} CASCADE"))

    # Criação das tabelas
    db.create_all()
    print("✅ Tabelas criadas com sucesso.")

    # Dados iniciais para tabelas dinâmicas
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

    demandas = [
        "Tapa-buraco", "Boca de Lobo", "Bueiro", "Calçada", "Estacionamentos",
        "Galeria de Águas Pluviais", "Jardim", "Mato Alto", "Meio-fio", "Parque Infantil",
        "Passagem Subterrânea", "Passarela", "Pisos Articulados", "Pista de Skate",
        "Ponto de Encontro Comunitário (PEC)", "Praça", "Quadra de Esporte", "Rampa",
        "Alambrado (Cercamento)", "Implantação (calçada, quadra, praça, estacionamento etc.)",
        "Recapeamento Asfáltico", "Poda / Supressão de Árvore", "Doação de Mudas"
    ]
    for d in demandas:
        db.session.add(Demanda(nome=d))

    status = [
        "Enviado à Diretoria das Cidades",
        "Enviado à Diretoria de Obras",
        "Devolvido à RA de origem",
        "Improcedente - tramitação pelo SGIA",
        "Improcedente - necessita de orçamento próprio",
        "Improcedente - cronograma próprio da diretoria",
        "Concluído"
    ]
    for s in status:
        db.session.add(Status(nome=s))

    db.session.commit()
    print("✅ Dados iniciais inseridos com sucesso.")
