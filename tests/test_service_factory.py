"""
Testes para ServiceFactory - Injeção de dependências.
"""
import pytest

from ozempic_seguro.services.service_factory import (
    ServiceFactory,
    ServiceRegistry,
    get_user_service,
    get_audit_service,
)


class TestServiceRegistry:
    """Testes para ServiceRegistry"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.registry = ServiceRegistry()
        yield
    
    def test_register_and_get_service(self):
        """Testa registro e obtenção de serviço"""
        mock_service = {"name": "test_service"}
        
        self.registry.register_service("test", mock_service)
        
        result = self.registry.get_service("test", lambda: None)
        assert result == mock_service
    
    def test_get_service_creates_if_not_exists(self):
        """Testa que serviço é criado se não existir"""
        created_service = {"created": True}
        
        result = self.registry.get_service("new_service", lambda: created_service)
        
        assert result == created_service
    
    def test_set_and_get_mock(self):
        """Testa definição e obtenção de mock"""
        mock = {"mock": True}
        
        self.registry.set_mock("service_name", mock)
        
        # Mock deve ter prioridade sobre serviço real
        result = self.registry.get_service("service_name", lambda: {"real": True})
        assert result == mock
    
    def test_clear_mocks(self):
        """Testa limpeza de mocks"""
        self.registry.set_mock("service", {"mock": True})
        
        self.registry.clear_mocks()
        
        # Agora deve criar serviço real
        result = self.registry.get_service("service", lambda: {"real": True})
        assert result == {"real": True}
    
    def test_reset_services(self):
        """Testa reset de todos os serviços"""
        self.registry.register_service("service1", {"s1": True})
        self.registry.set_mock("service2", {"s2": True})
        
        self.registry.reset_services()
        
        # Deve criar novos serviços
        result = self.registry.get_service("service1", lambda: {"new": True})
        assert result == {"new": True}


class TestServiceFactory:
    """Testes para ServiceFactory"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        ServiceFactory.reset_all_services()
        yield
        ServiceFactory.reset_all_services()
    
    def test_get_user_service(self):
        """Testa obtenção de UserService"""
        service = ServiceFactory.get_user_service()
        
        assert service is not None
        # Deve ser singleton
        service2 = ServiceFactory.get_user_service()
        assert service is service2
    
    def test_get_audit_service(self):
        """Testa obtenção de AuditService"""
        service = ServiceFactory.get_audit_service()
        
        assert service is not None
    
    def test_get_database_manager(self):
        """Testa obtenção de DatabaseManager"""
        manager = ServiceFactory.get_database_manager()
        
        assert manager is not None
    
    def test_get_session_manager(self):
        """Testa obtenção de SessionManager"""
        manager = ServiceFactory.get_session_manager()
        
        assert manager is not None
    
    def test_get_security_logger(self):
        """Testa obtenção de SecurityLogger"""
        logger = ServiceFactory.get_security_logger()
        
        assert logger is not None
    
    def test_set_mock_user_service(self):
        """Testa definição de mock para UserService"""
        mock = {"mock": True}
        
        ServiceFactory.set_mock_user_service(mock)
        
        result = ServiceFactory.get_user_service()
        assert result == mock
    
    def test_set_mock_audit_service(self):
        """Testa definição de mock para AuditService"""
        mock = {"mock": True}
        
        ServiceFactory.set_mock_audit_service(mock)
        
        result = ServiceFactory.get_audit_service()
        assert result == mock
    
    def test_clear_all_mocks(self):
        """Testa limpeza de todos os mocks"""
        ServiceFactory.set_mock_user_service({"mock": True})
        
        ServiceFactory.clear_all_mocks()
        
        # Deve retornar serviço real
        result = ServiceFactory.get_user_service()
        assert result is not None
        assert not isinstance(result, dict)
    
    def test_get_service_status(self):
        """Testa obtenção de status dos serviços"""
        # Carregar alguns serviços
        ServiceFactory.get_user_service()
        
        status = ServiceFactory.get_service_status()
        
        assert isinstance(status, dict)
        assert 'user_service' in status
        assert status['user_service'] is True


class TestConvenienceFunctions:
    """Testes para funções de conveniência"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        ServiceFactory.reset_all_services()
        yield
        ServiceFactory.reset_all_services()
    
    def test_get_user_service_function(self):
        """Testa função get_user_service"""
        service = get_user_service()
        
        assert service is not None
    
    def test_get_audit_service_function(self):
        """Testa função get_audit_service"""
        service = get_audit_service()
        
        assert service is not None
