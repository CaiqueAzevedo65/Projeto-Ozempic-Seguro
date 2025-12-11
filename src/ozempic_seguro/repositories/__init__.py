"""
Módulo de repositórios - Camada de persistência de dados.

Fornece acesso ao banco de dados através de repositórios especializados.
"""
from .connection import DatabaseConnection
from .user_repository import UserRepository
from .audit_repository import AuditRepository
from .gaveta_repository import GavetaRepository
from .security import hash_password, verify_password
from .input_validator import InputValidator

# Mantido para compatibilidade
from .database import DatabaseManager

__all__ = [
    # Conexão
    'DatabaseConnection',
    
    # Repositórios
    'UserRepository',
    'AuditRepository',
    'GavetaRepository',
    
    # Segurança
    'hash_password',
    'verify_password',
    'InputValidator',
    
    # Compatibilidade (deprecated)
    'DatabaseManager',
]
