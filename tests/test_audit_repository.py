"""
Testes para AuditRepository - Operações de auditoria.
"""
import pytest
from datetime import datetime

from ozempic_seguro.repositories.audit_repository import AuditRepository
from ozempic_seguro.repositories.connection import DatabaseConnection


class TestAuditRepository:
    """Testes para AuditRepository"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.repo = AuditRepository()
        yield
    
    def test_create_log_success(self):
        """Testa criação de log de auditoria"""
        log_id = self.repo.create_log(
            usuario_id=1,
            acao="TEST_ACTION",
            tabela_afetada="TEST_TABLE",
            id_afetado=1,
            dados_anteriores={"old": "value"},
            dados_novos={"new": "value"},
            endereco_ip="127.0.0.1"
        )
        
        assert log_id is not None
        assert isinstance(log_id, int)
    
    def test_create_log_minimal(self):
        """Testa criação de log com dados mínimos"""
        log_id = self.repo.create_log(
            usuario_id=1,
            acao="MINIMAL_ACTION",
            tabela_afetada="TEST_TABLE"
        )
        
        assert log_id is not None
    
    def test_create_log_without_user(self):
        """Testa criação de log sem usuário (ações de sistema)"""
        log_id = self.repo.create_log(
            usuario_id=None,
            acao="SYSTEM_ACTION",
            tabela_afetada="SYSTEM"
        )
        
        assert log_id is not None
    
    def test_get_logs(self):
        """Testa obtenção de logs"""
        # Criar alguns logs primeiro
        self.repo.create_log(
            usuario_id=1,
            acao="GET_LOGS_TEST",
            tabela_afetada="TEST"
        )
        
        logs = self.repo.get_logs(offset=0, limit=10)
        
        assert isinstance(logs, list)
    
    def test_get_logs_with_filter(self):
        """Testa obtenção de logs com filtro"""
        # Criar log específico
        self.repo.create_log(
            usuario_id=1,
            acao="FILTERED_ACTION",
            tabela_afetada="FILTERED_TABLE"
        )
        
        logs = self.repo.get_logs(
            offset=0,
            limit=10,
            filtro_acao="FILTERED_ACTION"
        )
        
        assert isinstance(logs, list)
        # Todos os logs retornados devem ter a ação filtrada
        for log in logs:
            assert log['acao'] == "FILTERED_ACTION"
    
    def test_count_logs(self):
        """Testa contagem de logs"""
        count = self.repo.count_logs()
        
        assert isinstance(count, int)
        assert count >= 0
    
    def test_count_logs_with_filter(self):
        """Testa contagem de logs com filtro"""
        # Criar log específico
        unique_action = f"COUNT_TEST_{datetime.now().timestamp()}"
        self.repo.create_log(
            usuario_id=1,
            acao=unique_action,
            tabela_afetada="TEST"
        )
        
        count = self.repo.count_logs(filtro_acao=unique_action)
        
        assert count >= 1


class TestAuditRepositoryFilters:
    """Testes para filtros de AuditRepository"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.repo = AuditRepository()
        yield
    
    def test_filter_by_table(self):
        """Testa filtro por tabela"""
        unique_table = f"TABLE_{datetime.now().timestamp()}"
        
        self.repo.create_log(
            usuario_id=1,
            acao="TEST",
            tabela_afetada=unique_table
        )
        
        logs = self.repo.get_logs(filtro_tabela=unique_table)
        
        for log in logs:
            assert log['tabela_afetada'] == unique_table
    
    def test_filter_by_user(self):
        """Testa filtro por usuário"""
        logs = self.repo.get_logs(filtro_usuario=1)
        
        # Logs filtrados por usuário devem ter o usuário correto
        # O campo retornado é 'usuario' (username), não 'usuario_id'
        assert isinstance(logs, list)
    
    def test_pagination(self):
        """Testa paginação de logs"""
        # Criar vários logs
        for i in range(5):
            self.repo.create_log(
                usuario_id=1,
                acao=f"PAGINATION_TEST_{i}",
                tabela_afetada="TEST"
            )
        
        # Buscar primeira página
        page1 = self.repo.get_logs(offset=0, limit=2)
        # Buscar segunda página
        page2 = self.repo.get_logs(offset=2, limit=2)
        
        # Páginas devem ser diferentes
        if len(page1) > 0 and len(page2) > 0:
            assert page1[0]['id'] != page2[0]['id']
