import os
import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


# 🔐 Gera senha segura (para senha provisória)
def gerar_senha_provisoria(tamanho=10):
    caracteres = string.ascii_letters + string.digits + '@#_!'
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))


# 📬 Função de envio de e-mail com suporte a HTML
def enviar_email(destinatario, assunto, mensagem):
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT", 587))
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem, "html"))

    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
        print(f"[✔] E-mail enviado com sucesso para {destinatario}")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")
        return False


# 🔐 Geração de token seguro com tempo de expiração
def gerar_token_email(email):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="recuperar-senha")


def verificar_token_email(token, max_age=3600):  # 1 hora
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="recuperar-senha", max_age=max_age)
        return email
    except Exception:
        return None
