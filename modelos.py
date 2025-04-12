from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    nome_usuario = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    numero_celular = db.Column(db.String(20))
    senha_hash = db.Column(db.String(200), nullable=False)
    autorizado = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

class RegiaoAdministrativa(db.Model):
    __tablename__ = "regioes_administrativas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

class Demanda(db.Model):
    __tablename__ = "demandas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

class Processo(db.Model):
    __tablename__ = "processos"
    id_processo = db.Column(db.Integer, primary_key=True)
    numero_processo = db.Column(db.String(30), unique=True, nullable=False)
    data_criacao_ra = db.Column(db.Date, nullable=False)
    tramite_inicial = db.Column(db.String(10), nullable=False)
    data_entrada = db.Column(db.Date, nullable=False)
    admin_regional_id = db.Column(db.Integer, db.ForeignKey("regioes_administrativas.id"), nullable=False)
    tipo_demanda_id = db.Column(db.Integer, db.ForeignKey("demandas.id"), nullable=False)
    vistoria_completa = db.Column(db.String(10), nullable=False)
    diretoria_destino = db.Column(db.String(10), nullable=False)
    status_demanda_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    descricao_processo = db.Column(db.String(300))
    responsavel = db.Column(db.String(150), nullable=False)

    admin_regional = db.relationship("RegiaoAdministrativa")
    tipo_demanda = db.relationship("Demanda")
    status_demanda = db.relationship("Status")
    movimentacoes = db.relationship("Movimentacao", backref="processo", cascade="all, delete-orphan")

class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"
    id = db.Column(db.Integer, primary_key=True)
    id_processo = db.Column(db.Integer, db.ForeignKey("processos.id_processo"), nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    status_movimentado = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(150), nullable=False)
    observacoes = db.Column(db.Text)

class LogSistema(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    acao = db.Column(db.String(200), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    ip_maquina = db.Column(db.String(100))
    descricao = db.Column(db.Text)
