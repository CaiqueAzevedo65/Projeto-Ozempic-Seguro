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
            usuario_id=1, acao="TEST_ACTION", tabela_afetada="TEST_TABLE"
        )

        # Deve retornar ID do log criado ou None
        assert result is None or isinstance(result, int)

    def test_create_log_with_data(self):
        """Testa criação de log com dados"""
        result = self.service.create_log(
            usuario_id=1,
            acao="CREATE",
            tabela_afetada="usuarios",
            id_afetado=2,
            dados_novos={"nome": "Test User"},
        )

        assert result is None or isinstance(result, int)

    def test_create_log_with_previous_data(self):
        """Testa criação de log com dados anteriores"""
        result = self.service.create_log(
            usuario_id=1,
            acao="UPDATE",
            tabela_afetada="usuarios",
            id_afetado=2,
            dados_anteriores={"nome": "Old Name"},
            dados_novos={"nome": "New Name"},
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


class TestAuditServiceFilters:
    """Testes para filtros do AuditService"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditService()
        yield

    def test_get_logs_by_action(self):
        """Testa obtenção de logs por ação"""
        logs = self.service.get_logs(filtro_acao="LOGIN")
        assert isinstance(logs, list)

    def test_get_logs_by_table(self):
        """Testa obtenção de logs por tabela"""
        logs = self.service.get_logs(filtro_tabela="usuarios")
        assert isinstance(logs, list)

    def test_get_logs_by_user(self):
        """Testa obtenção de logs por usuário"""
        logs = self.service.get_logs(filtro_usuario=1)
        assert isinstance(logs, list)

    def test_count_logs_with_filter(self):
        """Testa contagem de logs com filtro"""
        count = self.service.count_logs(filtro_acao="LOGIN")
        assert isinstance(count, int)

    def test_get_logs_empty_filter(self):
        """Testa logs com filtro vazio"""
        logs = self.service.get_logs(filtro_acao="NONEXISTENT_ACTION_XYZ")
        assert isinstance(logs, list)


class TestAuditServiceActions:
    """Testes para ações específicas do AuditService"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuditService()
        yield

    def test_log_login(self):
        """Testa log de login"""
        result = self.service.create_log(usuario_id=1, acao="LOGIN", tabela_afetada="usuarios")
        assert result is None or isinstance(result, int)

    def test_log_logout(self):
        """Testa log de logout"""
        result = self.service.create_log(usuario_id=1, acao="LOGOUT", tabela_afetada="usuarios")
        assert result is None or isinstance(result, int)

    def test_log_drawer_open(self):
        """Testa log de abertura de gaveta"""
        result = self.service.create_log(
            usuario_id=1, acao="GAVETA_ABERTA", tabela_afetada="gavetas", id_afetado=1
        )
        assert result is None or isinstance(result, int)

    def test_log_drawer_close(self):
        """Testa log de fechamento de gaveta"""
        result = self.service.create_log(
            usuario_id=1, acao="GAVETA_FECHADA", tabela_afetada="gavetas", id_afetado=1
        )
        assert result is None or isinstance(result, int)

    def test_log_user_create(self):
        """Testa log de criação de usuário"""
        result = self.service.create_log(
            usuario_id=1,
            acao="USUARIO_CRIADO",
            tabela_afetada="usuarios",
            id_afetado=5,
            dados_novos={"username": "newuser", "tipo": "vendedor"},
        )
        assert result is None or isinstance(result, int)

    def test_log_without_user(self):
        """Testa log sem usuário (ação de sistema)"""
        result = self.service.create_log(
            usuario_id=None, acao="SYSTEM_STARTUP", tabela_afetada="system"
        )
        assert result is None or isinstance(result, int)
