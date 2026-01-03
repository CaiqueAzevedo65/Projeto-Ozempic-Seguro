"""
Módulo de segurança: funções de hash e verificação de senha com bcrypt.
Sistema 100% bcrypt - sem suporte legacy.
"""
import bcrypt


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
    senha_bytes = senha.encode("utf-8")
    # Gera salt e hash com bcrypt
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(senha_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(senha: str, senha_hash: str) -> bool:
    """
    Verifica se a senha corresponde ao hash fornecido.
    Usa apenas bcrypt para máxima segurança.

    Args:
        senha (str): Senha em texto plano
        senha_hash (str): Hash armazenado no banco

    Returns:
        bool: True se a senha corresponde ao hash
    """
    try:
        # Verifica se é bcrypt (começa com $2a$, $2b$, $2x$ ou $2y$)
        if not senha_hash.startswith(("$2a$", "$2b$", "$2x$", "$2y$")):
            # Hash inválido ou formato desconhecido
            return False

        # Sistema bcrypt apenas
        senha_bytes = senha.encode("utf-8")
        hash_bytes = senha_hash.encode("utf-8")
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except (ValueError, TypeError):
        # Invalid hash format or encoding error
        return False


def is_bcrypt_hash(senha_hash: str) -> bool:
    """
    Verifica se um hash é do tipo bcrypt.

    Args:
        senha_hash (str): Hash a ser verificado

    Returns:
        bool: True se for bcrypt, False caso contrário
    """
    return senha_hash.startswith(("$2a$", "$2b$", "$2x$", "$2y$"))
