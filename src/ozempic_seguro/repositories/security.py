"""
Módulo de segurança: funções de hash e verificação de senha com bcrypt.
"""
import bcrypt
import hashlib
import secrets


def hash_password(senha: str, rounds: int = 12) -> str:
    """
    Gera um hash seguro para a senha usando bcrypt.
    
    Args:
        senha (str): Senha a ser hasheada
        rounds (int): Número de rounds para bcrypt (padrão: 12)
    
    Returns:
        str: Hash da senha
    """
    # Converte senha para bytes
    senha_bytes = senha.encode('utf-8')
    # Gera salt e hash com bcrypt
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(senha_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(senha: str, senha_hash: str) -> bool:
    """
    Verifica se a senha corresponde ao hash fornecido.
    Suporta tanto bcrypt (novo) quanto SHA256+salt (legacy).
    
    Args:
        senha (str): Senha em texto plano
        senha_hash (str): Hash armazenado no banco
    
    Returns:
        bool: True se a senha corresponde ao hash
    """
    try:
        # Verifica se é bcrypt (começa com $2a$, $2b$, $2x$ ou $2y$)
        if senha_hash.startswith(('$2a$', '$2b$', '$2x$', '$2y$')):
            # Novo sistema bcrypt
            senha_bytes = senha.encode('utf-8')
            hash_bytes = senha_hash.encode('utf-8')
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        else:
            # Sistema legacy SHA256+salt (para compatibilidade)
            return _verify_legacy_password(senha, senha_hash)
    except Exception:
        return False


def _verify_legacy_password(senha: str, senha_hash: str) -> bool:
    """
    Verifica senha usando o sistema legacy SHA256+salt.
    Usado apenas para compatibilidade com senhas antigas.
    """
    try:
        salt, _ = senha_hash.split('$')
        senha_salt = f"{senha}{salt}".encode('utf-8')
        digest = hashlib.sha256(senha_salt).hexdigest()
        return f"{salt}${digest}" == senha_hash
    except Exception:
        return False


def is_bcrypt_hash(senha_hash: str) -> bool:
    """
    Verifica se um hash é do tipo bcrypt.
    
    Args:
        senha_hash (str): Hash a ser verificado
    
    Returns:
        bool: True se for bcrypt, False caso contrário
    """
    return senha_hash.startswith(('$2a$', '$2b$', '$2x$', '$2y$'))