import os
import sys
from dotenv import load_dotenv

# Garante acesso à pasta scripts e à raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.utils import enviar_email

load_dotenv()

# Testa envio de e-mail com mensagem simples
assunto = "✅ Teste de E-mail - Sistema CPCR"
destinatario = os.getenv("EMAIL_TESTE") or os.getenv("EMAIL_USER")
mensagem = """
<p>Olá,</p>
<p>Este é um teste automático do envio de e-mails pelo sistema <strong>CPCR</strong>.</p>
<p>Se você recebeu este e-mail, está tudo funcionando corretamente! 🎉</p>
"""

if enviar_email(destinatario, assunto, mensagem):
    print("[✔] E-mail de teste enviado com sucesso!")
else:
    print("[✖] Falha no envio do e-mail.")
