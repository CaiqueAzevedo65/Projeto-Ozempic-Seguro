"""
Testes para AuditViewService - Serviço de visualização de auditoria.
"""
import pytest

from ozempic_seguro.services.audit_view_service import (
    AuditViewService,
    AuditLogItem,
    AuditFilter,
    PaginatedAuditResult,
    get_audit_view_service,
)


class TestAuditLogItem:
    """Testes para AuditLogItem"""
    
    def test_data_hora_display(self):
        """Testa formatação de data"""
        item = AuditLogItem(1, "2025-01-01 10:00:00", "user", "LOGIN", "usuarios", None, None, None, None)
        assert item.data_hora_display == "2025-01-01 10:00:00"
    
    def test_acao_display(self):
        """Testa formatação de ação"""
        item = AuditLogItem(1, "2025-01-01", "user", "login", "usuarios", None, None, None, None)
        assert item.acao_display == "LOGIN"


class TestAuditFilter:
    """Testes para AuditFilter"""
    
    def test_default_last_7_days(self):
        """Testa filtro padrão de 7 dias"""
        filter = AuditFilter.default_last_7_days()
        
        assert filter.data_inicio is not None
        assert filter.data_fim is not None
    
    def test_empty_filter(self):
        """Testa filtro vazio"""
        filter = AuditFilter()
        
        assert filter.acao is None
        assert filter.data_inicio is None


class TestPaginatedAuditResult:
    """Testes para PaginatedAuditResult"""
    
    def test_total_pages(self):
        """Testa cálculo de páginas"""
        result = PaginatedAuditResult(items=[], total=100, page=1, per_page=20)
        assert result.total_pages == 5
    
    def test_has_next(self):
        """Testa has_next"""
        result = PaginatedAuditResult(items=[], total=100, page=1, per_page=20)
        assert result.has_next is True
    
    def test_has_previous(self):
        """Testa has_previous"""
        result = PaginatedAuditResult(items=[], total=100, page=2, per_page=20)
        assert result.has_previous is True


class TestAuditViewService:
    """Testes para AuditViewService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditViewService()
        yield
    
    def test_get_logs_no_filter(self):
        """Testa obtenção de logs sem filtro"""
        result = self.service.get_logs()
        
        assert isinstance(result, PaginatedAuditResult)
        assert isinstance(result.items, list)
    
    def test_get_logs_with_filter(self):
        """Testa obtenção de logs com filtro"""
        filter = AuditFilter(acao="LOGIN")
        result = self.service.get_logs(filter=filter)
        
        assert isinstance(result, PaginatedAuditResult)
    
    def test_get_logs_pagination(self):
        """Testa paginação"""
        result = self.service.get_logs(page=1, per_page=10)
        
        assert result.page == 1
        assert result.per_page == 10
    
    def test_get_available_actions(self):
        """Testa obtenção de ações disponíveis"""
        actions = self.service.get_available_actions()
        
        assert isinstance(actions, list)
        assert "Todas" in actions
        assert "LOGIN" in actions
    
    def test_get_default_filter(self):
        """Testa obtenção de filtro padrão"""
        filter = self.service.get_default_filter()
        
        assert isinstance(filter, AuditFilter)
        assert filter.data_inicio is not None


class TestGetAuditViewService:
    """Testes para função get_audit_view_service"""
    
    def test_returns_service(self):
        """Testa que retorna AuditViewService"""
        service = get_audit_view_service()
        
        assert isinstance(service, AuditViewService)
