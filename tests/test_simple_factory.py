"""
Testes para SimpleServiceFactory - Factory simplificado.
"""
import pytest

from ozempic_seguro.services.simple_factory import (
    SimpleServiceFactory,
    get_user_service,
    get_audit_service,
)


class TestSimpleServiceFactory:
    """Testes para SimpleServiceFactory"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        SimpleServiceFactory.reset()
        yield
        SimpleServiceFactory.reset()
    
    def test_get_service_creates_instance(self):
        """Testa que get_service cria instância"""
        from ozempic_seguro.services.user_service import UserService
        
        service = SimpleServiceFactory.get_service(UserService)
        
        assert service is not None
        assert isinstance(service, UserService)
    
    def test_get_service_returns_singleton(self):
        """Testa que get_service retorna singleton"""
        from ozempic_seguro.services.user_service import UserService
        
        service1 = SimpleServiceFactory.get_service(UserService)
        service2 = SimpleServiceFactory.get_service(UserService)
        
        assert service1 is service2
    
    def test_reset_clears_instances(self):
        """Testa que reset limpa instâncias"""
        from ozempic_seguro.services.user_service import UserService
        
        service1 = SimpleServiceFactory.get_service(UserService)
        SimpleServiceFactory.reset()
        service2 = SimpleServiceFactory.get_service(UserService)
        
        # Após reset, deve ser uma nova instância
        assert service1 is not service2
    
    def test_register_instance(self):
        """Testa registro de instância customizada"""
        class MockService:
            pass
        
        mock = MockService()
        SimpleServiceFactory.register_instance(MockService, mock)
        
        result = SimpleServiceFactory.get_service(MockService)
        
        assert result is mock


class TestConvenienceFunctions:
    """Testes para funções de conveniência"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        SimpleServiceFactory.reset()
        yield
        SimpleServiceFactory.reset()
    
    def test_get_user_service(self):
        """Testa função get_user_service"""
        service = get_user_service()
        
        assert service is not None
    
    def test_get_audit_service(self):
        """Testa função get_audit_service"""
        service = get_audit_service()
        
        assert service is not None
