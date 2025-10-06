"""
Factory simplificado para gerenciamento de serviços.
Substitui o ServiceFactory complexo por uma implementação mais limpa.
"""
from typing import Dict, Any, Type, TypeVar, Optional
import threading

T = TypeVar('T')


class SimpleServiceFactory:
    """Factory simples com singleton thread-safe"""
    
    _instances: Dict[Type, Any] = {}
    _lock = threading.Lock()
    
    @classmethod
    def get_service(cls, service_class: Type[T]) -> T:
        """
        Obtém instância singleton de um serviço.
        
        Args:
            service_class: Classe do serviço desejado
            
        Returns:
            Instância singleton do serviço
        """
        if service_class not in cls._instances:
            with cls._lock:
                # Double-check locking pattern
                if service_class not in cls._instances:
                    cls._instances[service_class] = service_class()
        
        return cls._instances[service_class]
    
    @classmethod
    def reset(cls) -> None:
        """Limpa todas as instâncias (útil para testes)"""
        with cls._lock:
            cls._instances.clear()
    
    @classmethod
    def register_instance(cls, service_class: Type[T], instance: T) -> None:
        """
        Registra uma instância específica (útil para mocks em testes).
        
        Args:
            service_class: Classe do serviço
            instance: Instância a ser registrada
        """
        with cls._lock:
            cls._instances[service_class] = instance


# Funções de conveniência mantendo compatibilidade
def get_user_service():
    """Obtém instância do UserService"""
    from .user_service import UserService
    return SimpleServiceFactory.get_service(UserService)


def get_audit_service():
    """Obtém instância do AuditService"""
    from .audit_service import AuditService
    return SimpleServiceFactory.get_service(AuditService)
