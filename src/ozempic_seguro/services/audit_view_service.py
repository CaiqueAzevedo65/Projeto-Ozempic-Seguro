"""
Serviço de visualização de auditoria - Lógica de auditoria separada das views.

Responsabilidades:
- Obter logs de auditoria
- Filtrar logs
- Paginar resultados
- Formatar dados para exibição
"""
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .audit_service import AuditService
from ..core.logger import logger


@dataclass
class AuditLogItem:
    """Item de log de auditoria"""
    id: int
    data_hora: str
    usuario: str
    acao: str
    tabela: str
    id_afetado: Optional[int]
    dados_anteriores: Optional[str]
    dados_novos: Optional[str]
    ip: Optional[str]
    
    @property
    def data_hora_display(self) -> str:
        """Retorna data/hora formatada"""
        try:
            if isinstance(self.data_hora, str):
                return self.data_hora
            return str(self.data_hora)
        except Exception:
            return "N/A"
    
    @property
    def acao_display(self) -> str:
        """Retorna ação formatada"""
        return self.acao.upper() if self.acao else "N/A"


@dataclass
class AuditFilter:
    """Filtros para busca de auditoria"""
    acao: Optional[str] = None
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None
    usuario: Optional[str] = None
    tabela: Optional[str] = None
    
    @classmethod
    def default_last_7_days(cls) -> 'AuditFilter':
        """Cria filtro padrão dos últimos 7 dias"""
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=7)
        return cls(
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )


@dataclass
class PaginatedAuditResult:
    """Resultado paginado de auditoria"""
    items: List[AuditLogItem]
    total: int
    page: int
    per_page: int
    
    @property
    def total_pages(self) -> int:
        """Calcula total de páginas"""
        if self.per_page <= 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page
    
    @property
    def has_next(self) -> bool:
        """Verifica se há próxima página"""
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        """Verifica se há página anterior"""
        return self.page > 1


class AuditViewService:
    """
    Serviço de visualização de auditoria.
    
    Encapsula toda a lógica de auditoria que estava nas views.
    """
    
    DEFAULT_PAGE_SIZE = 50
    AVAILABLE_ACTIONS = ["Todas", "LOGIN", "LOGOUT", "CRIAR", "ATUALIZAR", "EXCLUIR"]
    
    def __init__(self):
        self._audit_service = AuditService()
    
    def get_logs(
        self,
        filter: Optional[AuditFilter] = None,
        page: int = 1,
        per_page: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedAuditResult:
        """
        Obtém logs de auditoria com filtros e paginação.
        
        Args:
            filter: Filtros a aplicar
            page: Página atual
            per_page: Itens por página
            
        Returns:
            PaginatedAuditResult com logs
        """
        try:
            offset = (page - 1) * per_page
            
            # Preparar filtros
            filtro_acao = None
            data_inicio = None
            data_fim = None
            
            if filter:
                if filter.acao and filter.acao != "Todas":
                    filtro_acao = filter.acao
                data_inicio = filter.data_inicio
                data_fim = filter.data_fim
            
            # Obter logs
            logs = self._audit_service.get_logs(
                offset=offset,
                limit=per_page,
                filtro_acao=filtro_acao,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            # Contar total
            total = self._audit_service.count_logs(
                filtro_acao=filtro_acao,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            # Converter para AuditLogItem
            items = []
            for log in logs:
                try:
                    items.append(AuditLogItem(
                        id=log.get('id', 0),
                        data_hora=log.get('data_hora', ''),
                        usuario=log.get('usuario', ''),
                        acao=log.get('acao', ''),
                        tabela=log.get('tabela_afetada', ''),
                        id_afetado=log.get('id_afetado'),
                        dados_anteriores=log.get('dados_anteriores'),
                        dados_novos=log.get('dados_novos'),
                        ip=log.get('endereco_ip')
                    ))
                except Exception as e:
                    logger.warning(f"Error parsing audit log: {e}")
                    continue
            
            return PaginatedAuditResult(
                items=items,
                total=total,
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            logger.error(f"Error getting audit logs: {e}")
            return PaginatedAuditResult(items=[], total=0, page=page, per_page=per_page)
    
    def get_available_actions(self) -> List[str]:
        """Retorna lista de ações disponíveis para filtro"""
        return self.AVAILABLE_ACTIONS.copy()
    
    def get_default_filter(self) -> AuditFilter:
        """Retorna filtro padrão (últimos 7 dias)"""
        return AuditFilter.default_last_7_days()


def get_audit_view_service() -> AuditViewService:
    """Retorna instância do AuditViewService"""
    return AuditViewService()
