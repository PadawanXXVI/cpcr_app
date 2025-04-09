from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from configuracoes import DevelopmentConfig
from utils import gerar_senha_provisoria, enviar_email, gerar_token_email, verificar_token_email
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

# Decorator: força troca de senha se for provisória
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
            return redirect(url_for('index'))
        else:
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
        usuario_existente = cursor.fetchone()
        if usuario_existente:
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
        email = request.form['email']
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            token = gerar_token_email(usuario['email'])
            link = f"http://127.0.0.1:5000/redefinir_senha/{token}"

            corpo_email = f"""
            <p>Olá {usuario['nome']},</p>

            <p>Você solicitou uma redefinição de senha para acessar o sistema CPCR da Novacap.</p>

            <p>Acesse o link abaixo para criar uma nova senha. Este link expira em 1 hora:</p>

            <p><a href="{link}">{link}</a></p>

            <p>Se você não solicitou esta redefinição, ignore este e-mail.</p>

            <p>Atenciosamente,<br>Sistema CPCR - Novacap</p>
            """

            enviar_email(
                destinatario=usuario['email'],
                assunto="Redefinição de Senha - Sistema CPCR",
                mensagem=corpo_email
            )

        mensagem = "Se o e-mail informado estiver cadastrado, você receberá instruções para redefinir sua senha."
        return render_template('recuperacao.html', mensagem=mensagem)

    return render_template('recuperacao.html')

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
        confirmar_senha = request.form['confirmar_senha']

        if nova_senha != confirmar_senha:
            mensagem = "As senhas não coincidem. Tente novamente."
            return render_template('trocar_senha.html', mensagem=mensagem)

        nova_senha_hash = generate_password_hash(nova_senha)
        id_usuario = session['id_usuario']

        cursor.execute("""
            UPDATE usuarios
            SET senha_hash = %s, senha_provisoria = FALSE
            WHERE id_usuario = %s
        """, (nova_senha_hash, id_usuario))
        conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        user = cursor.fetchone()
        session['usuario'] = user['usuario']

        return redirect(url_for('index'))

    return render_template('trocar_senha.html')

if __name__ == '__main__':
    app.run(debug=True)
