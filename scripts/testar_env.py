# testar_env.py

import os
from dotenv import load_dotenv
from utils import enviar_email

# Carrega as variáveis do .env (na raiz do projeto)
load_dotenv()

# E-mail de destino (pode ser o próprio remetente para teste)
destinatario = os.getenv("EMAIL_USER")
assunto = "🔐 Teste de envio de e-mail - Sistema CPCR"
mensagem = """
<p><strong>Este é um teste automático do sistema CPCR.</strong></p>
<p>Se você recebeu este e-mail, o envio via SMTP iCloud está funcionando corretamente.</p>
<p>Atenciosamente,<br>Sistema CPCR</p>
"""

# Envia o e-mail
enviado = enviar_email(destinatario, assunto, mensagem)

if enviado:
    print("[✔] E-mail de teste enviado com sucesso!")
else:
    print("[✖] Erro ao enviar e-mail. Verifique o .env ou a senha do app.")
