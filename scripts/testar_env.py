import os
from dotenv import load_dotenv
from configuracoes import DevelopmentConfig
from scripts.utils import enviar_email

# Carrega as variáveis do .env
load_dotenv()

print("\n✅ Variáveis carregadas do .env:")
print(f"EMAIL_HOST: {os.getenv('EMAIL_HOST')}")
print(f"EMAIL_PORT: {os.getenv('EMAIL_PORT')}")
print(f"EMAIL_USER: {os.getenv('EMAIL_USER')}")
print(f"EMAIL_SENDER: {os.getenv('EMAIL_SENDER')}")
print(f"EMAIL_PASSWORD: {'*' * len(os.getenv('EMAIL_PASSWORD', ''))}")  # Não exibe a senha

# Testa envio de e-mail
try:
    enviar_email(
        destinatario=os.getenv("EMAIL_USER"),
        assunto="🧪 Teste de envio - Sistema CPCR",
        mensagem="<p>Este é um teste de envio de e-mail automático pelo sistema CPCR da Novacap.</p>"
    )
    print("📧 E-mail de teste enviado com sucesso!")
except Exception as e:
    print(f"❌ Falha ao enviar e-mail: {e}")
