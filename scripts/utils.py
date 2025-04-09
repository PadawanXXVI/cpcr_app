import secrets
import string

def gerar_senha_provisoria(tamanho=8):
    """
    Gera uma senha segura, aleatória e provisória.
    Inclui letras maiúsculas, minúsculas, números e símbolos.
    """
    caracteres = string.ascii_letters + string.digits + '@#_!'
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha
