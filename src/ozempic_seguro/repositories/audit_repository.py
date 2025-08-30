"""
Repositório de auditoria: registros de ações do sistema.
"""
from .database import DatabaseManager
import json

class AuditRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def create_log(self, usuario_id=None, acao: str = None, tabela_afetada: str = None,
                   id_afetado=None, dados_anteriores: dict = None, dados_novos: dict = None,
                   endereco_ip: str = None) -> int | None:
        """Registra um log de auditoria e retorna o ID do registro."""
        prev = json.dumps(dados_anteriores, ensure_ascii=False) if dados_anteriores else None
        new = json.dumps(dados_novos, ensure_ascii=False) if dados_novos else None
        return self.db.registrar_auditoria(
            usuario_id, acao, tabela_afetada, id_afetado, prev, new, endereco_ip
        )

    def get_logs(self, offset: int = 0, limit: int = 50,
                 filtro_usuario=None, filtro_acao=None, filtro_tabela=None,
                 data_inicio=None, data_fim=None) -> list[dict]:
        """Retorna logs de auditoria com filtros e paginação."""
        return self.db.buscar_logs_auditoria(
            offset, limit, filtro_usuario, filtro_acao, filtro_tabela, data_inicio, data_fim
        )

    def count_logs(self, filtro_usuario=None, filtro_acao=None,
                   filtro_tabela=None, data_inicio=None, data_fim=None) -> int:
        """Retorna o total de logs que correspondem aos filtros."""
        return self.db.contar_logs_auditoria(
            filtro_usuario, filtro_acao, filtro_tabela, data_inicio, data_fim
        )
