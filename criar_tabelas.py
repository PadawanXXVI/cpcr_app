from flask import Flask
from modelos import db, Usuario, Processo, Movimentacao, LogSistema, Demanda, Status, RegiaoAdministrativa
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("\n🔧 Iniciando criação do banco de dados 'cr_novacap'...")

    # DROP das tabelas, mantendo apenas usuários existentes
    db.reflect()
    for table in reversed(db.metadata.sorted_tables):
        if table.name != "usuarios":
            print(f"❌ Apagando tabela: {table.name}")
            db.engine.execute(f"DROP TABLE IF EXISTS {table.name} CASCADE")

    # Criar todas as tabelas novamente
    db.create_all()
    print("✅ Tabelas criadas com sucesso.")

    # Garantir que o usuário admin (ID 1) continue com is_admin=True
    admin = Usuario.query.get(1)
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("🔐 Admin (ID 1) mantido como administrador.")
    else:
        print("⚠️ Nenhum usuário com ID 1 encontrado.")

    # Inserir STATUS
    status_oficiais = [
        "Enviado à Diretoria das Cidades",
        "Enviado à Diretoria de Obras",
        "Devolvido à RA de origem",
        "Improcedente - tramitação pelo SGIA",
        "Improcedente - implantação ou necessita de orçamento próprio",
        "Improcedente - cronograma próprio da Diretoria",
        "Concluído"
    ]
    for nome in status_oficiais:
        if not Status.query.filter_by(nome=nome).first():
            db.session.add(Status(nome=nome))

    # Inserir DEMANDAS
    demandas_reais = [
        "Alambrado (Cercamento)",
        "Boca de Lobo",
        "Bueiro",
        "Calçada",
        "Estacionamentos",
        "Jardim",
        "Mato Alto",
        "Meio-fio",
        "Parque Infantil",
        "Passarela",
        "Passagem Subterrânea",
        "Pisos Articulados",
        "Pista de Skate",
        "Ponto de Encontro Comunitário (PEC)",
        "Praça",
        "Quadra de Esporte",
        "Rampa",
        "Rua, Via ou Rodovia (pista urbana)",
        "Tapa-Buraco",
        "Galeria de Águas Pluviais",
        "Doação de Mudas",
        "Poda / Supressão de Árvore",
        "Implantação (calçada, quadra, praça, estacionamento etc.)",
        "Galeria de Água Potável"
    ]
    for nome in demandas_reais:
        if not Demanda.query.filter_by(nome=nome).first():
            db.session.add(Demanda(nome=nome))

    # Inserir REGIÕES ADMINISTRATIVAS
    ras_completas = [
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
    for codigo, nome in ras_completas:
        if not RegiaoAdministrativa.query.filter_by(codigo=codigo).first():
            db.session.add(RegiaoAdministrativa(codigo=codigo, nome=nome))

    db.session.commit()
    print("🚀 Banco de dados populado com sucesso!")
