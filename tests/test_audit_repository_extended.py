"""
Testes estendidos para AuditRepository - Cobertura adicional.
"""
import pytest

from ozempic_seguro.repositories.audit_repository import AuditRepository


class TestAuditRepositoryExtended:
    """Testes estendidos para AuditRepository"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.repo = AuditRepository()
        yield

    def test_create_log_minimal(self):
        """Testa criação de log mínimo"""
        result = self.repo.create_log(usuario_id=1, acao="TEST")

        assert result is None or isinstance(result, int)

    def test_create_log_full(self):
        """Testa criação de log completo"""
        result = self.repo.create_log(
            usuario_id=1,
            acao="CREATE",
            tabela_afetada="usuarios",
            id_afetado=2,
            dados_anteriores={"old": "data"},
            dados_novos={"new": "data"},
            endereco_ip="127.0.0.1",
        )

        assert result is None or isinstance(result, int)

    def test_get_logs_default(self):
        """Testa obtenção de logs com parâmetros default"""
        logs = self.repo.get_logs()

        assert isinstance(logs, list)

    def test_get_logs_with_limit(self):
        """Testa obtenção de logs com limite"""
        logs = self.repo.get_logs(limit=5)

        assert isinstance(logs, list)
        assert len(logs) <= 5

    def test_get_logs_with_offset(self):
        """Testa obtenção de logs com offset"""
        logs = self.repo.get_logs(offset=0, limit=10)

        assert isinstance(logs, list)

    def test_get_logs_filter_by_action(self):
        """Testa filtro por ação"""
        logs = self.repo.get_logs(filtro_acao="LOGIN")

        assert isinstance(logs, list)

    def test_get_logs_filter_by_table(self):
        """Testa filtro por tabela"""
        logs = self.repo.get_logs(filtro_tabela="usuarios")

        assert isinstance(logs, list)

    def test_get_logs_filter_by_date_range(self):
        """Testa filtro por período"""
        logs = self.repo.get_logs(data_inicio="2025-01-01", data_fim="2025-12-31")

        assert isinstance(logs, list)

    def test_count_logs_default(self):
        """Testa contagem de logs"""
        count = self.repo.count_logs()

        assert isinstance(count, int)
        assert count >= 0

    def test_count_logs_with_filter(self):
        """Testa contagem de logs com filtro"""
        count = self.repo.count_logs(filtro_acao="LOGIN")

        assert isinstance(count, int)
        assert count >= 0
