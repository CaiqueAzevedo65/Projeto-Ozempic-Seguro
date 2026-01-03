"""
Módulo de serviços - Camada de lógica de negócio.

Fornece serviços que encapsulam regras de negócio e orquestram repositórios.
"""
from .user_service import UserService
from .audit_service import AuditService
from .service_factory import get_user_service, get_audit_service

__all__ = [
    "UserService",
    "AuditService",
    "get_user_service",
    "get_audit_service",
]
