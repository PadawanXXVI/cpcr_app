from modelos import db, Usuario, Status, Demanda, RegiaoAdministrativa
from flask import Flask
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Nuncy2403@localhost/cpcr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("\n🛠️  Iniciando recriação do banco de dados...")

    # DROP de tabelas exceto usuários
    print("🔁 Removendo tabelas antigas (exceto 'usuarios')...")
    db.reflect()
    for table in reversed(db.metadata.sorted_tables):
        if table.name != "usuarios":
            print(f"   ➤ Drop: {table.name}")
            db.engine.execute(f"DROP TABLE IF EXISTS {table.name} CASCADE")

    # Criação das tabelas
    print("✅ Criando novas tabelas...")
    db.create_all()

    # Garantir admin com ID 1
    admin = Usuario.query.get(1)
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("✅ Admin com ID 1 mantido como administrador.")
    else:
        print("⚠️ Nenhum usuário com ID 1 encontrado. Verifique o banco de dados.")

    # STATUS oficiais
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

    # DEMANDAS oficiais
    demandas_reais = [
        "Alambrado (Cercamento)",
        "Boca de Lobo",
        "Bueiro",
        "Calçada",
        "Doação de Mudas",
        "Estacionamentos",
        "Galeria de Água Potável",
        "Galeria de Águas Pluviais",
        "Implantação (calçada, quadra, praça, estacionamento etc.)",
        "Jardim",
        "Mato Alto",
        "Meio-fio",
        "Parque Infantil",
        "Passagem Subterrânea",
        "Passarela",
        "Pisos Articulados",
        "Pista de Skate",
        "Poda / Supressão de Árvore",
        "Ponto de Encontro Comunitário – PEC",
        "Praça",
        "Quadra de Esporte",
        "Rampa",
        "Rua, Via ou Rodovia (pista urbana)",
        "Tapa-Buraco"
    ]
    for nome in demandas_reais:
        if not Demanda.query.filter_by(nome=nome).first():
            db.session.add(Demanda(nome=nome))

    # RAs oficiais
    ras_completas = [
        ("RA I", "Plano Piloto"),
        ("RA II", "Gama"),
        ("RA III", "Taguatinga"),
        ("RA IV", "Brazlândia"),
        ("RA V", "Sobradinho"),
        ("RA VI", "Planaltina"),
        ("RA VII", "Paranoá"),
        ("RA VIII", "Núcleo Bandeirante"),
        ("RA IX", "Ceilândia"),
        ("RA X", "Guará"),
        ("RA XI", "Cruzeiro"),
        ("RA XII", "Samambaia"),
        ("RA XIII", "Santa Maria"),
        ("RA XIV", "São Sebastião"),
        ("RA XV", "Recanto das Emas"),
        ("RA XVI", "Lago Sul"),
        ("RA XVII", "Riacho Fundo"),
        ("RA XVIII", "Lago Norte"),
        ("RA XIX", "Candangolândia"),
        ("RA XX", "Águas Claras"),
        ("RA XXI", "Riacho Fundo II"),
        ("RA XXII", "Sudoeste/Octogonal"),
        ("RA XXIII", "Varjão"),
        ("RA XXIV", "Park Way"),
        ("RA XXV", "SCIA/Estrutural"),
        ("RA XXVI", "Sobradinho II"),
        ("RA XXVII", "Jardim Botânico"),
        ("RA XXVIII", "Itapoã"),
        ("RA XXIX", "SIA"),
        ("RA XXX", "Vicente Pires"),
        ("RA XXXI", "Fercal"),
        ("RA XXXII", "Sol Nascente e Pôr do Sol"),
        ("RA XXXIII", "Arniqueira"),
        ("RA XXXIV", "Arapoanga"),
        ("RA XXXV", "Água Quente")
    ]
    for codigo, nome in ras_completas:
        if not RegiaoAdministrativa.query.filter_by(codigo=codigo).first():
            db.session.add(RegiaoAdministrativa(codigo=codigo, nome=nome))

    db.session.commit()
    print("✅ Banco de dados recriado e atualizado com sucesso.")
