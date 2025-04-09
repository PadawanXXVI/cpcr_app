import secrets
import string

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def gerar_senha_provisoria(tamanho=8):
    """
    Gera uma senha segura, aleatória e provisória.
    Inclui letras maiúsculas, minúsculas, números e símbolos.
    """
    caracteres = string.ascii_letters + string.digits + '@#_!'
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha


def enviar_email(destinatario, assunto, mensagem):
    email_host = os.getenv('EMAIL_HOST')
    email_port = int(os.getenv('EMAIL_PORT'))
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'html'))

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")
        return False

def gerar_token_email(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='recuperar-senha')

def verificar_token_email(token, max_age=3600):  # 1 hora = 3600 segundos
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='recuperar-senha', max_age=max_age)
        return email
    except Exception:
        return None
