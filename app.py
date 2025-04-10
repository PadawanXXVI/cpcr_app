from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from configuracoes import DevelopmentConfig
from scripts.utils import gerar_senha_provisoria, enviar_email, gerar_token_email, verificar_token_email
from functools import wraps

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DATABASE']
)
cursor = conn.cursor(dictionary=True)

# Decorador: redireciona para troca de senha se for provisória
def verificar_senha_provisoria(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' in session:
            cursor.execute("SELECT senha_provisoria FROM usuarios WHERE id_usuario = %s", (session['id_usuario'],))
            resultado = cursor.fetchone()
            if resultado and resultado['senha_provisoria']:
                return redirect(url_for('trocar_senha'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador: exige login ativo
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        user = cursor.fetchone()

        if user and check_password_hash(user['senha_hash'], senha):
            if not user.get('aprovado', True):
                return "Usuário ainda não aprovado pelo administrador."

            session['usuario'] = user['usuario']
            session['id_usuario'] = user['id_usuario']

            if user.get('senha_provisoria', False):
                return redirect(url_for('trocar_senha'))

            return redirect(url_for('cadastro_processo'))

        return "Usuário ou senha incorretos"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        nome_usuario = request.form['nome_usuario']
        email = request.form['email']
        numero_celular = request.form['numero_celular']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)

        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (nome_usuario,))
        if cursor.fetchone():
            return "Nome de usuário já está em uso. Escolha outro."

        try:
            cursor.execute('''
                INSERT INTO usuarios (nome, usuario, email, numero_celular, senha_hash, aprovado)
                VALUES (%s, %s, %s, %s, %s, FALSE)
            ''', (nome_completo, nome_usuario, email, numero_celular, senha_hash))
            conn.commit()
            return "Usuário cadastrado com sucesso. Aguarde autorização do administrador."
        except mysql.connector.Error as err:
            return f"Erro ao cadastrar usuário: {err}"

    return render_template('cadastro_usuario.html')

@app.route('/recuperar_acesso', methods=['GET', 'POST'])
def recuperar_acesso():
    if request.method == 'POST':
        nome = request.form['nome_completo'].strip()
        email = request.form['email'].strip()
        nova_senha = request.form['nova_senha']
        confirmar = request.form['confirmar_senha']

        if nova_senha != confirmar:
            mensagem = "As senhas não coincidem. Tente novamente."
            return render_template("recuperacao.html", mensagem=mensagem)

        # Verifica se existe usuário com nome + email
        cursor.execute("""
            SELECT * FROM usuarios WHERE nome = %s AND email = %s
        """, (nome, email))
        usuario = cursor.fetchone()

        if not usuario:
            mensagem = "Usuário não encontrado com os dados informados."
            return render_template("recuperacao.html", mensagem=mensagem)

        # Atualiza a senha
        nova_hash = generate_password_hash(nova_senha)
        cursor.execute("""
            UPDATE usuarios
            SET senha_hash = %s, senha_provisoria = FALSE
            WHERE id_usuario = %s
        """, (nova_hash, usuario['id_usuario']))
        conn.commit()

        return render_template("recuperacao.html", mensagem="Senha redefinida com sucesso. Você já pode fazer login.")

    return render_template("recuperacao.html")

@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    email = verificar_token_email(token)
    if not email:
        return "Este link expirou ou é inválido."

    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmar = request.form['confirmar_senha']

        if nova_senha != confirmar:
            return render_template("trocar_senha.html", mensagem="As senhas não coincidem.")

        nova_hash = generate_password_hash(nova_senha)
        cursor.execute("""
            UPDATE usuarios SET senha_hash = %s, senha_provisoria = FALSE
            WHERE email = %s
        """, (nova_hash, email))
        conn.commit()

        return redirect(url_for('login'))

    return render_template("trocar_senha.html")

@app.route('/trocar_senha', methods=['GET', 'POST'])
def trocar_senha():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmar = request.form['confirmar_senha']

        if nova_senha != confirmar:
            return render_template('trocar_senha.html', mensagem="As senhas não coincidem.")

        nova_hash = generate_password_hash(nova_senha)
        cursor.execute("""
            UPDATE usuarios SET senha_hash = %s, senha_provisoria = FALSE
            WHERE id_usuario = %s
        """, (nova_hash, session['id_usuario']))
        conn.commit()

        return redirect(url_for('index'))

    return render_template('trocar_senha.html')

@app.route('/cadastro_processo', methods=['GET', 'POST'])
@verificar_senha_provisoria
@login_required
def cadastro_processo():
    if request.method == 'POST':
        numero = request.form['numero_processo']
        cursor.execute("SELECT id_processo FROM processos WHERE numero_processo = %s", (numero,))
        existente = cursor.fetchone()

        if existente:
            return redirect(url_for('atualizar_processo', id=existente['id_processo']))

        dados = (
            numero,
            request.form['data_criacao_ra'],
            request.form['data_entrada_cpcr'],
            request.form['admin_regional'],
            request.form['tipo_demanda'],
            request.form['vistoria_completa'],
            request.form['diretoria_destino'],
            request.form['status_demanda'],
            request.form['descricao_processo']
        )

        cursor.execute('''
            INSERT INTO processos
            (numero_processo, data_criacao_ra, data_entrada_cpcr, admin_regional,
             tipo_demanda, vistoria_completa, diretoria_destino, status_demanda, descricao_processo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', dados)
        conn.commit()

        return redirect(url_for('cadastro_processo'))

    # Listas de apoio
    lista_ras = [ ... ]  # mesmas RAs
    lista_demandas = [ ... ]  # mesmas demandas
    lista_status = [ ... ]  # mesmos status
    totais = { ... }  # painel de totais (simulado)

    return render_template("cadastro_processo.html",
                           lista_ras=lista_ras,
                           lista_demandas=lista_demandas,
                           lista_status=lista_status,
                           totais=totais)

@app.route('/atualizar_processo/<int:id>', methods=['GET', 'POST'])
@verificar_senha_provisoria
@login_required
def atualizar_processo(id):
    cursor.execute("SELECT * FROM processos WHERE id_processo = %s", (id,))
    processo = cursor.fetchone()

    if not processo:
        return "Processo não encontrado", 404

    if request.method == 'POST':
        novo_status = request.form['status_demanda']
        nova_diretoria = request.form['diretoria_destino']
        observacoes = request.form['observacoes']
        id_usuario = session['id_usuario']

        cursor.execute("""
            UPDATE processos SET status_demanda = %s, diretoria_destino = %s,
            data_ultima_atualizacao = NOW() WHERE id_processo = %s
        """, (novo_status, nova_diretoria, id))

        cursor.execute("""
            INSERT INTO movimentacoes (id_processo, data_movimentacao, status_movimentado, observacoes, id_usuario)
            VALUES (%s, NOW(), %s, %s, %s)
        """, (id, novo_status, observacoes, id_usuario))

        conn.commit()
        return redirect(url_for('atualizar_processo', id=id))

    lista_status = [ ... ]
    lista_diretorias = ["DC", "DO", "N/A"]

    cursor.execute("""
        SELECT m.data_movimentacao, m.status_movimentado, m.observacoes, u.nome AS responsavel
        FROM movimentacoes m
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        WHERE m.id_processo = %s
        ORDER BY m.data_movimentacao DESC
    """, (id,))
    historico = cursor.fetchall()

    return render_template("atualizar_processo.html",
                           processo=processo,
                           lista_status=lista_status,
                           lista_diretorias=lista_diretorias,
                           historico=historico)

@app.route('/visualizacao')
@verificar_senha_provisoria
def visualizacao():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Filtros
    numero = request.args.get('numero_processo', '')
    ra = request.args.get('admin_regional', '')
    demanda = request.args.get('tipo_demanda', '')
    status = request.args.get('status_demanda', '')

    # Query base
    query = "SELECT * FROM processos WHERE 1=1"
    params = []

    if numero:
        query += " AND numero_processo LIKE %s"
        params.append(f"%{numero}%")
    if ra:
        query += " AND admin_regional = %s"
        params.append(ra)
    if demanda:
        query += " AND tipo_demanda = %s"
        params.append(demanda)
    if status:
        query += " AND status_demanda = %s"
        params.append(status)

    cursor.execute(query, tuple(params))
    processos = cursor.fetchall()

    # Reutilizamos listas para filtros (já usadas em cadastro_processo)
    lista_ras = [
        "RA I - Plano Piloto", "RA II - Gama", "RA III - Taguatinga", "RA IV - Brazlândia", "RA V - Sobradinho",
        "RA VI - Planaltina", "RA VII - Paranoá", "RA VIII - Núcleo Bandeirante", "RA IX - Ceilândia", "RA X - Guará",
        "RA XI - Cruzeiro", "RA XII - Samambaia", "RA XIII - Santa Maria", "RA XIV - São Sebastião", "RA XV - Recanto das Emas",
        "RA XVI - Lago Sul", "RA XVII - Riacho Fundo", "RA XVIII - Lago Norte", "RA XIX - Candangolândia", "RA XX - Águas Claras",
        "RA XXI - Riacho Fundo II", "RA XXII - Sudoeste/Octogonal", "RA XXIII - Varjão", "RA XXIV - Park Way",
        "RA XXV - SCIA/Estrutural", "RA XXVI - Sobradinho II", "RA XXVII - Jardim Botânico", "RA XXVIII - Itapoã",
        "RA XXIX - SIA", "RA XXX - Vicente Pires", "RA XXXI - Fercal", "RA XXXII - Sol Nascente e Pôr do Sol",
        "RA XXXIII - Arniqueira", "RA XXXIV - Arapoanga", "RA XXXV - Água Quente"
    ]

    lista_demandas = [
        "Tapa-buraco", "Boca de Lobo", "Bueiro", "Calçada", "Estacionamentos",
        "Galeria de Águas Pluviais", "Jardim", "Mato Alto", "Meio-fio", "Parque Infantil",
        "Passagem Subterrânea", "Passarela", "Pisos Articulados", "Pista de Skate",
        "Ponto de Encontro Comunitário (PEC)", "Praça", "Quadra de Esporte", "Rampa",
        "Alambrado (Cercamento)", "Implantação (calçada, quadra, praça, estacionamento etc.)",
        "Recapeamento Asfáltico", "Poda / supressão de árvore", "Doação de mudas"
    ]

    lista_status = [
        "Em atendimento", "Atendido", "Enviado à Diretoria das Cidades",
        "Enviado à Diretoria de Obras", "Devolvido à RA de origem",
        "Improcedente - tramitação pelo SGIA", "Improcedente - necessita de orçamento próprio",
        "Concluído"
    ]

    return render_template('visualizacao.html',
                           processos=processos,
                           lista_ras=lista_ras,
                           lista_demandas=lista_demandas,
                           lista_status=lista_status)

if __name__ == '__main__':
    app.run(debug=True)
