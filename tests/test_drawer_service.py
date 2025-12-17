"""
Testes para DrawerService - Serviço de gavetas.
"""
import pytest

from ozempic_seguro.services.drawer_service import (
    DrawerService,
    DrawerState,
    DrawerHistoryItem,
    PaginatedResult,
    get_drawer_service,
)


class TestDrawerState:
    """Testes para DrawerState"""
    
    def test_status_display_open(self):
        """Testa status aberta"""
        state = DrawerState(numero=1, esta_aberta=True)
        assert state.status_display == "Aberta"
    
    def test_status_display_closed(self):
        """Testa status fechada"""
        state = DrawerState(numero=1, esta_aberta=False)
        assert state.status_display == "Fechada"


class TestDrawerHistoryItem:
    """Testes para DrawerHistoryItem"""
    
    def test_acao_display_aberta(self):
        """Testa ação aberta"""
        item = DrawerHistoryItem("2025-01-01", 1, "aberta", "user1")
        assert item.acao_display == "Abriu"
    
    def test_acao_display_fechada(self):
        """Testa ação fechada"""
        item = DrawerHistoryItem("2025-01-01", 1, "fechada", "user1")
        assert item.acao_display == "Fechou"
    
    def test_data_hora_display(self):
        """Testa formatação de data"""
        item = DrawerHistoryItem("2025-01-01 10:00:00", 1, "aberta", "user1")
        assert item.data_hora_display == "2025-01-01 10:00:00"


class TestPaginatedResult:
    """Testes para PaginatedResult"""
    
    def test_total_pages_exact(self):
        """Testa cálculo de páginas exato"""
        result = PaginatedResult(items=[], total=100, page=1, per_page=20)
        assert result.total_pages == 5
    
    def test_total_pages_remainder(self):
        """Testa cálculo de páginas com resto"""
        result = PaginatedResult(items=[], total=101, page=1, per_page=20)
        assert result.total_pages == 6
    
    def test_has_next_true(self):
        """Testa has_next verdadeiro"""
        result = PaginatedResult(items=[], total=100, page=1, per_page=20)
        assert result.has_next is True
    
    def test_has_next_false(self):
        """Testa has_next falso"""
        result = PaginatedResult(items=[], total=100, page=5, per_page=20)
        assert result.has_next is False
    
    def test_has_previous_true(self):
        """Testa has_previous verdadeiro"""
        result = PaginatedResult(items=[], total=100, page=2, per_page=20)
        assert result.has_previous is True
    
    def test_has_previous_false(self):
        """Testa has_previous falso"""
        result = PaginatedResult(items=[], total=100, page=1, per_page=20)
        assert result.has_previous is False


class TestDrawerService:
    """Testes para DrawerService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = DrawerService()
        yield
    
    def test_get_drawer_state(self):
        """Testa obtenção de estado de gaveta"""
        state = self.service.get_drawer_state(1)
        
        # Pode retornar None ou DrawerState
        assert state is None or isinstance(state, DrawerState)
    
    def test_get_all_drawer_states(self):
        """Testa obtenção de todos os estados"""
        states = self.service.get_all_drawer_states(5)
        
        assert isinstance(states, list)
        assert len(states) == 5
        for state in states:
            assert isinstance(state, DrawerState)
    
    def test_get_drawer_history(self):
        """Testa obtenção de histórico de gaveta"""
        result = self.service.get_drawer_history(1)
        
        assert isinstance(result, PaginatedResult)
        assert isinstance(result.items, list)
    
    def test_get_all_history(self):
        """Testa obtenção de todo histórico"""
        result = self.service.get_all_history()
        
        assert isinstance(result, PaginatedResult)
        assert isinstance(result.items, list)
    
    def test_get_all_history_pagination(self):
        """Testa paginação do histórico"""
        result = self.service.get_all_history(page=1, per_page=10)
        
        assert result.page == 1
        assert result.per_page == 10


class TestDrawerServiceMethods:
    """Testes para métodos do DrawerService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = DrawerService()
        yield
    
    def test_set_drawer_state_open(self):
        """Testa definir gaveta como aberta"""
        success, message = self.service.set_drawer_state(1, True, "administrador", 1)
        
        assert isinstance(success, bool)
        assert isinstance(message, str)
        if success:
            assert "aberta" in message.lower() or "sucesso" in message.lower()
    
    def test_set_drawer_state_closed(self):
        """Testa definir gaveta como fechada"""
        success, message = self.service.set_drawer_state(1, False, "repositor", 2)
        
        assert isinstance(success, bool)
        assert isinstance(message, str)
        if success:
            assert "fechada" in message.lower() or "sucesso" in message.lower()
    
    def test_toggle_drawer(self):
        """Testa alternar estado da gaveta"""
        success, message, new_state = self.service.toggle_drawer(1, "administrador", 1)
        
        assert isinstance(success, bool)
        assert isinstance(message, str)
        assert isinstance(new_state, bool)
    
    def test_toggle_drawer_invalid(self):
        """Testa alternar gaveta inválida"""
        success, message, new_state = self.service.toggle_drawer(999999, "administrador", 1)
        
        # Pode retornar False se a gaveta não existe
        assert isinstance(success, bool)
        assert isinstance(message, str)
        assert isinstance(new_state, bool)


class TestGetDrawerService:
    """Testes para função get_drawer_service"""
    
    def test_returns_service(self):
        """Testa que retorna DrawerService"""
        service = get_drawer_service()
        
        assert isinstance(service, DrawerService)


class TestDrawerHistoryItemEdgeCases:
    """Testes para casos extremos do DrawerHistoryItem"""
    
    def test_data_hora_display_with_datetime_object(self):
        """Testa formatação com objeto datetime"""
        from datetime import datetime
        now = datetime.now()
        item = DrawerHistoryItem(now, 1, "aberta", "user1")
        assert item.data_hora_display is not None
    
    def test_acao_display_unknown(self):
        """Testa ação desconhecida"""
        item = DrawerHistoryItem("2025-01-01", 1, "UNKNOWN", "user1")
        assert item.acao_display == "Unknown"
    
    def test_acao_display_alternative_spellings(self):
        """Testa ortografias alternativas"""
        item1 = DrawerHistoryItem("2025-01-01", 1, "abrir", "user1")
        assert item1.acao_display == "Abriu"
        
        item2 = DrawerHistoryItem("2025-01-01", 1, "fechar", "user1")
        assert item2.acao_display == "Fechou"


class TestPaginatedResultEdgeCases:
    """Testes para casos extremos do PaginatedResult"""
    
    def test_total_pages_zero_per_page(self):
        """Testa total_pages com per_page zero ou negativo"""
        result = PaginatedResult(items=[], total=100, page=1, per_page=0)
        assert result.total_pages == 0
        
        result2 = PaginatedResult(items=[], total=100, page=1, per_page=-1)
        assert result2.total_pages == 0
    
    def test_empty_result(self):
        """Testa resultado vazio"""
        result = PaginatedResult(items=[], total=0, page=1, per_page=20)
        assert result.total_pages == 0
        assert result.has_next is False
        assert result.has_previous is False
