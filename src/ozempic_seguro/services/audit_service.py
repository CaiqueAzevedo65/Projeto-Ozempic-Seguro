"""
Serviço de auditoria: camada de negócio isolada para logs de auditoria.
"""
from typing import Optional, List, Dict

from ..repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self):
        self.audit_repo = AuditRepository()

    def get_logs(
        self,
        offset: int = 0,
        limit: int = 50,
        filtro_usuario: Optional[int] = None,
        filtro_acao: Optional[str] = None,
        filtro_tabela: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
    ) -> List[Dict]:
        """Retorna logs de auditoria com filtros e paginação."""
        return self.audit_repo.get_logs(
            offset, limit, filtro_usuario, filtro_acao, filtro_tabela, data_inicio, data_fim
        )

    def count_logs(
        self,
        filtro_usuario: Optional[int] = None,
        filtro_acao: Optional[str] = None,
        filtro_tabela: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
    ) -> int:
        """Retorna o total de logs que correspondem aos filtros."""
        return self.audit_repo.count_logs(
            filtro_usuario, filtro_acao, filtro_tabela, data_inicio, data_fim
        )

    def create_log(
        self,
        usuario_id: Optional[int] = None,
        acao: Optional[str] = None,
        tabela_afetada: Optional[str] = None,
        id_afetado: Optional[int] = None,
        dados_anteriores: Optional[Dict] = None,
        dados_novos: Optional[Dict] = None,
        endereco_ip: Optional[str] = None,
    ) -> Optional[int]:
        """Registra um log de auditoria e retorna o ID do registro."""
        return self.audit_repo.create_log(
            usuario_id, acao, tabela_afetada, id_afetado, dados_anteriores, dados_novos, endereco_ip
        )
