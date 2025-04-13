from flask import request
from modelos import db, LogSistema
from datetime import datetime

def get_ip_usuario():
    """Retorna o IP real do usuário, mesmo se estiver atrás de proxy."""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.remote_addr
    return ip

def criar_log(acao, id_usuario=None):
    """Registra uma ação no sistema."""
    log = LogSistema(
        id_usuario=id_usuario,
        acao=acao,
        ip_maquina=get_ip_usuario(),
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()

def formatar_numero_processo(numero):
    """Aplica a máscara padrão ao número do processo."""
    import re
    match = re.match(r"^(\d{5})(\d{8})/(\d{4})-(\d{2})$", numero)
    if match:
        return f"{match.group(1)}-{match.group(2)}/{match.group(3)}-{match.group(4)}"
    return numero
