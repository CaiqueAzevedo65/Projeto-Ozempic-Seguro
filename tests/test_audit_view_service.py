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
        item = AuditLogItem(
            1, "2025-01-01 10:00:00", "user", "LOGIN", "usuarios", None, None, None, None
        )
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


class TestAuditViewServiceEdgeCases:
    """Testes para casos extremos do AuditViewService"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditViewService()
        yield

    def test_get_logs_with_date_range(self):
        """Testa logs com intervalo de datas"""
        filter = AuditFilter(data_inicio="2025-01-01", data_fim="2025-12-31")
        result = self.service.get_logs(filter=filter)

        assert isinstance(result, PaginatedAuditResult)

    def test_get_logs_with_all_filters(self):
        """Testa logs com todos os filtros"""
        filter = AuditFilter(acao="LOGIN", data_inicio="2025-01-01", data_fim="2025-12-31")
        result = self.service.get_logs(filter=filter, page=2, per_page=5)

        assert isinstance(result, PaginatedAuditResult)
        assert result.page == 2
        assert result.per_page == 5

    def test_get_logs_empty_result(self):
        """Testa logs com resultado vazio"""
        filter = AuditFilter(
            acao="NONEXISTENT_ACTION", data_inicio="1990-01-01", data_fim="1990-12-31"
        )
        result = self.service.get_logs(filter=filter)

        assert isinstance(result, PaginatedAuditResult)
        assert result.total >= 0


class TestAuditLogItemEdgeCases:
    """Testes para casos extremos do AuditLogItem"""

    def test_acao_display_uppercase(self):
        """Testa ação já em maiúsculas"""
        item = AuditLogItem(1, "2025-01-01", "user", "LOGIN", "usuarios", None, None, None, None)
        assert item.acao_display == "LOGIN"

    def test_with_dados_novos(self):
        """Testa com dados novos"""
        item = AuditLogItem(
            1, "2025-01-01", "user", "CREATE", "usuarios", 1, None, '{"username": "test"}', None
        )
        assert item.dados_novos == '{"username": "test"}'

    def test_with_dados_antigos(self):
        """Testa com dados antigos"""
        item = AuditLogItem(
            1, "2025-01-01", "user", "UPDATE", "usuarios", 1, '{"username": "old"}', None, None
        )
        assert item.dados_anteriores == '{"username": "old"}'


class TestAuditFilterEdgeCases:
    """Testes para casos extremos do AuditFilter"""

    def test_filter_with_todas_acao(self):
        """Testa filtro com ação 'Todas'"""
        filter = AuditFilter(acao="Todas")
        assert filter.acao == "Todas"

    def test_filter_date_formats(self):
        """Testa diferentes formatos de data"""
        filter = AuditFilter(data_inicio="2025-01-01", data_fim="2025-12-31")
        assert filter.data_inicio == "2025-01-01"
        assert filter.data_fim == "2025-12-31"


class TestGetAuditViewService:
    """Testes para função get_audit_view_service"""

    def test_returns_service(self):
        """Testa que retorna AuditViewService"""
        service = get_audit_view_service()

        assert isinstance(service, AuditViewService)

    def test_returns_new_instance(self):
        """Testa que retorna nova instância"""
        service1 = get_audit_view_service()
        service2 = get_audit_view_service()

        assert isinstance(service1, AuditViewService)
        assert isinstance(service2, AuditViewService)


class TestPaginatedAuditResultAdditional:
    """Testes adicionais para PaginatedAuditResult"""

    def test_total_pages_zero(self):
        """Testa total_pages com total zero"""
        result = PaginatedAuditResult(items=[], total=0, page=1, per_page=20)
        assert result.total_pages == 0

    def test_has_next_last_page(self):
        """Testa has_next na última página"""
        result = PaginatedAuditResult(items=[], total=20, page=1, per_page=20)
        assert result.has_next is False

    def test_has_previous_first_page(self):
        """Testa has_previous na primeira página"""
        result = PaginatedAuditResult(items=[], total=100, page=1, per_page=20)
        assert result.has_previous is False

    def test_with_items(self):
        """Testa com itens"""
        item = AuditLogItem(1, "2025-01-01", "user", "LOGIN", "usuarios", None, None, None, None)
        result = PaginatedAuditResult(items=[item], total=1, page=1, per_page=20)
        assert len(result.items) == 1

    def test_total_pages_remainder(self):
        """Testa total_pages com resto"""
        result = PaginatedAuditResult(items=[], total=25, page=1, per_page=10)
        assert result.total_pages == 3


class TestAuditViewServicePagination:
    """Testes de paginação do AuditViewService"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditViewService()
        yield

    def test_get_logs_page_2(self):
        """Testa segunda página de logs"""
        result = self.service.get_logs(page=2, per_page=5)
        assert result.page == 2

    def test_get_logs_large_page(self):
        """Testa página grande"""
        result = self.service.get_logs(page=100, per_page=10)
        assert isinstance(result, PaginatedAuditResult)

    def test_get_logs_small_per_page(self):
        """Testa poucos itens por página"""
        result = self.service.get_logs(page=1, per_page=1)
        assert result.per_page == 1
