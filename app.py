from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from modelos import db, Usuario, Processo, Movimentacao, Status, Demanda, RegiaoAdministrativa
from configuracoes import DevelopmentConfig
from utils import criar_log
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

# -------------------------
# Decorators
# -------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# -------------------------
# Rotas
# -------------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and check_password_hash(user.senha_hash, senha):
            if not user.aprovado:
                return "Usuário ainda não aprovado pelo administrador."

            if not user.ativo:
                return "Usuário inativo. Entre em contato com a administração."

            session['usuario'] = user.usuario
            session['id_usuario'] = user.id_usuario

            criar_log("Login realizado com sucesso", id_usuario=user.id_usuario)
            return redirect(url_for('dashboard'))

        return "Usuário ou senha incorretos."

    return render_template("login.html")

@app.route('/logout')
def logout():
    criar_log("Logout efetuado", id_usuario=session.get("id_usuario"))
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    usuario = Usuario.query.filter_by(id_usuario=session['id_usuario']).first()

    total_processos = Processo.query.count()
    total_secre = Processo.query.filter_by(tramite_inicial="SECRE").count()
    total_cr = Processo.query.filter_by(tramite_inicial="CR").count()
    total_do = Processo.query.filter_by(diretoria_destino="DO").count()
    total_dc = Processo.query.filter_by(diretoria_destino="DC").count()
    total_sgia = Processo.query.filter(Processo.tipo_demanda.like('%Árvore%')).count()
    total_devolvidos_vistoria = Processo.query.filter(Processo.status_demanda.like('%ausência de vistoria%')).count()
    total_devolvidos_implantacao = Processo.query.filter(Processo.status_demanda.like('%implantação%')).count()
    total_devolvidos_continuado = Processo.query.filter(Processo.status_demanda.like('%continuada%')).count()
    total_atendidos = Processo.query.filter_by(status_demanda="Atendido").count()

    pendentes = Usuario.query.filter_by(aprovado=False).count() if usuario.is_admin else 0

    return render_template("dashboard.html",
        total_processos=total_processos,
        total_secre=total_secre,
        total_cr=total_cr,
        total_do=total_do,
        total_dc=total_dc,
        total_sgia=total_sgia,
        total_devolvidos_vistoria=total_devolvidos_vistoria,
        total_devolvidos_implantacao=total_devolvidos_implantacao,
        total_devolvidos_continuado=total_devolvidos_continuado,
        total_atendidos=total_atendidos,
        pendentes=pendentes,
        usuario_logado=usuario.usuario
    )

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome_completo']
        usuario = request.form['nome_usuario']
        email = request.form['email']
        celular = request.form['numero_celular']
        senha = generate_password_hash(request.form['senha'])

        if Usuario.query.filter_by(usuario=usuario).first():
            return "Nome de usuário já está em uso."

        novo = Usuario(
            nome=nome,
            usuario=usuario,
            email=email,
            numero_celular=celular,
            senha_hash=senha,
            aprovado=False
        )
        db.session.add(novo)
        db.session.commit()

        criar_log(f"Usuário cadastrado: {usuario}", id_usuario=novo.id_usuario)
        return "Usuário cadastrado. Aguarde autorização do administrador."

    return render_template("cadastro_usuario.html")

@app.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
    if request.method == 'POST':
        nova = request.form['nova_senha']
        confirmar = request.form['confirmar_senha']

        if nova != confirmar:
            return render_template("trocar_senha.html", mensagem="As senhas não coincidem.")

        usuario = Usuario.query.get(session['id_usuario'])
        usuario.senha_hash = generate_password_hash(nova)
        db.session.commit()

        criar_log("Senha alterada com sucesso", id_usuario=usuario.id_usuario)
        return redirect(url_for('dashboard'))

    return render_template("trocar_senha.html")

@app.route('/cadastro_processo', methods=['GET', 'POST'])
@login_required
def cadastro_processo():
    if request.method == 'POST':
        numero = request.form['numero_processo'].strip()
        existente = Processo.query.filter_by(numero_processo=numero).first()

        if existente:
            flash("⚠️ Processo já cadastrado. Redirecionando...", "warning")
            return redirect(url_for('atualizar_processo', id=existente.id_processo))

        processo = Processo(
            numero_processo=numero,
            data_criacao_ra=request.form['data_criacao_ra'],
            tramite_inicial=request.form['tramite_inicial'],
            data_entrada=request.form['data_entrada'],
            admin_regional=request.form['admin_regional'],
            tipo_demanda=request.form['tipo_demanda'],
            vistoria_completa=request.form['vistoria_completa'],
            diretoria_destino=request.form['diretoria_destino'],
            status_demanda=request.form['status_demanda'],
            descricao_processo=request.form['descricao_processo'],
            data_cadastro=request.form['data_cadastro']
        )
        db.session.add(processo)

        movimentacao = Movimentacao(
            id_usuario=request.form['responsavel_cadastro'],
            processo=processo,
            status_movimentado=processo.status_demanda,
            observacoes="Cadastro inicial",
            data_movimentacao_real=request.form['data_cadastro']
        )
        db.session.add(movimentacao)
        db.session.commit()

        criar_log(f"Cadastro de novo processo: {numero}", id_usuario=request.form['responsavel_cadastro'])
        flash("✅ Processo cadastrado com sucesso!", "success")
        return redirect(url_for('cadastro_processo'))

    ras = [ra.nome for ra in RegiaoAdministrativa.query.order_by("nome")]
    demandas = [d.nome for d in Demanda.query.order_by("nome")]
    status = [s.nome for s in Status.query.order_by("nome")]
    usuarios = Usuario.query.filter_by(ativo=True).order_by(Usuario.nome).all()

    return render_template("cadastro_processo.html",
        lista_ras=ras,
        lista_demandas=demandas,
        lista_status=status,
        lista_usuarios=usuarios
    )

@app.route('/atualizar_processo/<int:id>', methods=['GET', 'POST'])
@login_required
def atualizar_processo(id):
    processo = Processo.query.get_or_404(id)

    if request.method == 'POST':
        novo_status = request.form['status_demanda']
        observacoes = request.form['observacoes']
        data_real = request.form['data_movimentacao']
        responsavel_id = request.form['responsavel_movimentacao']

        processo.status_demanda = novo_status
        processo.data_ultima_atualizacao = datetime.utcnow()

        nova_mov = Movimentacao(
            id_processo=processo.id_processo,
            id_usuario=responsavel_id,
            status_movimentado=novo_status,
            observacoes=observacoes,
            data_atualizacao_real=data_real
        )
        db.session.add(nova_mov)
        db.session.commit()

        criar_log(f"Processo {processo.numero_processo} atualizado: {novo_status}", id_usuario=responsavel_id)
        return redirect(url_for('atualizar_processo', id=id))

    status = [s.nome for s in Status.query.order_by("nome")]
    diretorias = ["DC", "DO"]
    historico = Movimentacao.query.filter_by(id_processo=id).order_by(Movimentacao.data_movimentacao.desc()).all()
    usuarios = Usuario.query.filter_by(ativo=True).order_by(Usuario.nome).all()

    return render_template("atualizar_processo.html",
        processo=processo,
        lista_status=status,
        lista_diretorias=diretorias,
        historico=historico,
        lista_usuarios=usuarios
    )

@app.route('/visualizacao')
@login_required
def visualizacao():
    filtros = {
        "numero": request.args.get("numero_processo", ""),
        "ra": request.args.get("admin_regional", ""),
        "demanda": request.args.get("tipo_demanda", ""),
        "status": request.args.get("status_demanda", "")
    }

    query = Processo.query
    if filtros["numero"]:
        query = query.filter(Processo.numero_processo.like(f"%{filtros['numero']}%"))
    if filtros["ra"]:
        query = query.filter(Processo.admin_regional == filtros["ra"])
    if filtros["demanda"]:
        query = query.filter(Processo.tipo_demanda == filtros["demanda"])
    if filtros["status"]:
        query = query.filter(Processo.status_demanda == filtros["status"])

    processos = query.order_by(Processo.data_entrada.desc()).all()

    ras = [ra.nome for ra in RegiaoAdministrativa.query.order_by("nome")]
    demandas = [d.nome for d in Demanda.query.order_by("nome")]
    status = [s.nome for s in Status.query.order_by("nome")]

    return render_template("visualizacao.html",
        processos=processos,
        lista_ras=ras,
        lista_demandas=demandas,
        lista_status=status
    )

@app.route('/verificar_processo', methods=['GET'])
@login_required
def verificar_processo():
    numero = request.args.get('numero_processo', '').strip()
    if not numero:
        return jsonify({"existe": False})

    existente = Processo.query.filter_by(numero_processo=numero).first()
    if existente:
        return jsonify({"existe": True, "id": existente.id_processo})
    return jsonify({"existe": False})

if __name__ == '__main__':
    app.run(debug=True)
