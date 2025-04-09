# testar_env.py

import os
from dotenv import load_dotenv
from utils import enviar_email

# Carregar variáveis do .env
load_dotenv()

# Dados do teste
destinatario = os.getenv("EMAIL_USER")  # ou substitua por qualquer e-mail para teste
assunto = "Teste de envio de e-mail - Sistema CPCR"
mensagem = """
<p><strong>Este é um teste automático do sistema CPCR.</strong></p>
<p>Se você recebeu este e-mail, a configuração está correta.</p>
<p>Atenciosamente,<br>Sistema CPCR</p>
"""

# Enviar o e-mail
resultado = enviar_email(destinatario, assunto, mensagem)

if resultado:
    print("[OK] E-mail de teste enviado com sucesso!")
else:
    print("[ERRO] Falha ao enviar o e-mail.")
