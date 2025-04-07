from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig

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
            session['usuario'] = user['usuario']
            session['id_usuario'] = user['id_usuario']
            return redirect(url_for('cadastro'))
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
                INSERT INTO usuarios (nome, usuario, email, numero_celular, senha_hash)
                VALUES (%s, %s, %s, %s, %s)
            ''', (nome_completo, nome_usuario, email, numero_celular, senha_hash))
            conn.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Erro ao cadastrar usuário: {err}"

    return render_template('cadastro_usuario.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dados = (
            request.form['numero_processo'],
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
        return redirect(url_for('cadastro'))
    return render_template('cadastro.html')

@app.route('/atualizar', methods=['GET', 'POST'])
def atualizar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        numero_processo = request.form['numero_processo']
        novo_status = request.form['status_demanda']
        observacoes = request.form['observacoes']
        id_usuario = session['id_usuario']

        cursor.execute('''
            UPDATE processos
            SET status_atual = %s, data_ultima_atualizacao = NOW()
            WHERE numero_processo = %s
        ''', (novo_status, numero_processo))

        cursor.execute("SELECT id_processo FROM processos WHERE numero_processo = %s", (numero_processo,))
        processo = cursor.fetchone()
        if processo:
            id_processo = processo['id_processo']

            cursor.execute('''
                INSERT INTO movimentacoes (id_processo, data_movimentacao, status_movimentado, observacoes, id_usuario)
                VALUES (%s, CURDATE(), %s, %s, %s)
            ''', (id_processo, novo_status, observacoes, id_usuario))

            conn.commit()

        return redirect(url_for('visualizacao'))

    return render_template('atualizacao.html')

@app.route('/visualizacao')
def visualizacao():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    numero = request.args.get('numero_processo', '')
    cursor.execute("SELECT * FROM processos WHERE numero_processo LIKE %s", (f"%{numero}%",))
    processos = cursor.fetchall()
    return render_template('visualizacao.html', processos=processos)

@app.route('/detalhes/<numero_processo>')
def detalhes_processo(numero_processo):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM processos WHERE numero_processo = %s", (numero_processo,))
    processo = cursor.fetchone()

    cursor.execute('''
        SELECT m.data_movimentacao, m.status_movimentado, m.observacoes, u.nome AS responsavel
        FROM movimentacoes m
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        JOIN processos p ON m.id_processo = p.id_processo
        WHERE p.numero_processo = %s
        ORDER BY m.data_movimentacao DESC
    ''', (numero_processo,))
    movimentacoes = cursor.fetchall()

    return render_template('detalhes_processo.html', processo=processo, movimentacoes=movimentacoes)

if __name__ == '__main__':
    app.run(debug=True)
