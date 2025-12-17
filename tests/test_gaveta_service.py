"""
Testes para GavetaService - Cobertura de operações de gavetas.
"""
import pytest
from unittest.mock import patch, MagicMock

from ozempic_seguro.services.gaveta_service import GavetaService


class TestGavetaService:
    """Testes para GavetaService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        # Reset singleton para testes isolados
        GavetaService._instance = None
        self.service = GavetaService.get_instance()
        yield
        GavetaService._instance = None
    
    def test_singleton_pattern(self):
        """Testa que GavetaService é singleton"""
        service1 = GavetaService.get_instance()
        service2 = GavetaService.get_instance()
        assert service1 is service2
    
    def test_get_estado_gaveta(self):
        """Testa obtenção do estado de uma gaveta"""
        estado = self.service.get_estado(1)
        # Estado pode ser True ou False
        assert isinstance(estado, bool)
    
    def test_get_historico(self):
        """Testa obtenção de histórico de gaveta"""
        historico = self.service.get_historico(1, limite=10)
        assert isinstance(historico, list)
    
    def test_get_historico_paginado(self):
        """Testa obtenção de histórico paginado"""
        historico = self.service.get_historico_paginado(1, offset=0, limit=20)
        assert isinstance(historico, list)
    
    def test_get_total_historico(self):
        """Testa contagem de histórico"""
        total = self.service.get_total_historico(1)
        assert isinstance(total, int)
        assert total >= 0
    
    def test_get_todo_historico(self):
        """Testa obtenção de todo histórico"""
        historico = self.service.get_todo_historico()
        assert isinstance(historico, list)
    
    def test_get_todo_historico_paginado(self):
        """Testa obtenção de todo histórico paginado"""
        historico = self.service.get_todo_historico_paginado(offset=0, limit=20)
        assert isinstance(historico, list)
    
    def test_get_total_todo_historico(self):
        """Testa contagem de todo histórico"""
        total = self.service.get_total_todo_historico()
        assert isinstance(total, int)
        assert total >= 0
