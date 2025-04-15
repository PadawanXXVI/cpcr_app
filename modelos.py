from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------------
# USUÁRIOS DO SISTEMA
# ---------------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    numero_celular = db.Column(db.String(20))
    senha_hash = db.Column(db.Text, nullable=False)
    senha_provisoria = db.Column(db.Boolean, default=False)
    aprovado = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('Movimentacao', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'

# ---------------------
# PROCESSOS
# ---------------------
class Processo(db.Model):
    __tablename__ = 'processos'

    id_processo = db.Column(db.Integer, primary_key=True)
    numero_processo = db.Column(db.String(25), unique=True, nullable=False)
    data_criacao_ra = db.Column(db.Date, nullable=False)
    tramite_inicial = db.Column(db.String(10), nullable=False)
    data_entrada = db.Column(db.Date, nullable=False)

    admin_regional = db.Column(db.String(100), nullable=False)
    tipo_demanda = db.Column(db.String(100), nullable=False)
    vistoria_completa = db.Column(db.String(10))
    diretoria_destino = db.Column(db.String(10))
    status_demanda = db.Column(db.String(100), nullable=False)
    descricao_processo = db.Column(db.Text)
    data_ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data_cadastro = db.Column(db.Date)  # ✅ Data real de cadastro do processo

    movimentacoes = db.relationship('Movimentacao', backref='processo', lazy=True)

    def __repr__(self):
        return f'<Processo {self.numero_processo}>'

# ---------------------
# MOVIMENTAÇÕES (HISTÓRICO)
# ---------------------
class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'

    id_movimentacao = db.Column(db.Integer, primary_key=True)
    id_processo = db.Column(db.Integer, db.ForeignKey('processos.id_processo'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    status_movimentado = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)
    data_movimentacao_real = db.Column(db.Date)  # ✅ Data real da movimentação

    def __repr__(self):
        return f'<Movimentacao Processo {self.id_processo}>'

# ---------------------
# LOGS DO SISTEMA
# ---------------------
class LogSistema(db.Model):
    __tablename__ = 'logs'

    id_log = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    acao = db.Column(db.String(200))
    ip_maquina = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.id_log}>'

# ---------------------
# TABELAS DINÂMICAS: STATUS / DEMANDAS / RAs
# ---------------------
class Status(db.Model):
    __tablename__ = 'status'

    id_status = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Status {self.nome}>'

class Demanda(db.Model):
    __tablename__ = 'demandas'

    id_demanda = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Demanda {self.nome}>'

class RegiaoAdministrativa(db.Model):
    __tablename__ = 'regioes_administrativas'

    id_ra = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<RA {self.nome}>'
