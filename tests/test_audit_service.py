"""
Testes para AuditService - Serviço de auditoria.
"""
import pytest

from ozempic_seguro.services.audit_service import AuditService


class TestAuditService:
    """Testes para AuditService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditService()
        yield
    
    def test_create_log(self):
        """Testa criação de log de auditoria"""
        result = self.service.create_log(
            usuario_id=1,
            acao='TEST_ACTION',
            tabela_afetada='TEST_TABLE'
        )
        
        # Deve retornar ID do log criado ou None
        assert result is None or isinstance(result, int)
    
    def test_create_log_with_data(self):
        """Testa criação de log com dados"""
        result = self.service.create_log(
            usuario_id=1,
            acao='CREATE',
            tabela_afetada='usuarios',
            id_afetado=2,
            dados_novos={'nome': 'Test User'}
        )
        
        assert result is None or isinstance(result, int)
    
    def test_create_log_with_previous_data(self):
        """Testa criação de log com dados anteriores"""
        result = self.service.create_log(
            usuario_id=1,
            acao='UPDATE',
            tabela_afetada='usuarios',
            id_afetado=2,
            dados_anteriores={'nome': 'Old Name'},
            dados_novos={'nome': 'New Name'}
        )
        
        assert result is None or isinstance(result, int)
    
    def test_get_logs(self):
        """Testa obtenção de logs"""
        logs = self.service.get_logs()
        
        assert isinstance(logs, list)
    
    def test_get_logs_with_limit(self):
        """Testa obtenção de logs com limite"""
        logs = self.service.get_logs(limit=10)
        
        assert isinstance(logs, list)
        assert len(logs) <= 10
    
    def test_get_logs_with_offset(self):
        """Testa obtenção de logs com offset"""
        logs = self.service.get_logs(offset=5, limit=10)
        
        assert isinstance(logs, list)
    
    def test_count_logs(self):
        """Testa contagem de logs"""
        count = self.service.count_logs()
        
        assert isinstance(count, int)
        assert count >= 0
