"""
Serviço de gavetas - Lógica de gerenciamento de gavetas separada das views.

Responsabilidades:
- Obter estado das gavetas
- Alterar estado das gavetas
- Obter histórico de ações
- Paginação de histórico
"""
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from ..repositories.gaveta_repository import GavetaRepository
from ..core.logger import logger


@dataclass
class DrawerHistoryItem:
    """Item do histórico de gaveta"""
    data_hora: str
    gaveta_id: int
    acao: str
    usuario: str
    
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
        acoes = {
            'aberta': 'Abriu',
            'fechada': 'Fechou',
            'abrir': 'Abriu',
            'fechar': 'Fechou',
        }
        return acoes.get(self.acao.lower(), self.acao.capitalize())


@dataclass
class PaginatedResult:
    """Resultado paginado"""
    items: List[Any]
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


@dataclass
class DrawerState:
    """Estado de uma gaveta"""
    numero: int
    esta_aberta: bool
    ultimo_usuario: Optional[str] = None
    ultima_acao: Optional[str] = None
    
    @property
    def status_display(self) -> str:
        """Retorna status formatado"""
        return "Aberta" if self.esta_aberta else "Fechada"


class DrawerService:
    """
    Serviço de gavetas.
    
    Encapsula toda a lógica de gavetas que estava nas views.
    """
    
    DEFAULT_PAGE_SIZE = 20
    
    def __init__(self):
        self._repo = GavetaRepository()
    
    def get_drawer_state(self, drawer_number: int) -> Optional[DrawerState]:
        """
        Obtém estado de uma gaveta.
        
        Args:
            drawer_number: Número da gaveta
            
        Returns:
            DrawerState ou None
        """
        try:
            is_open = self._repo.get_state(drawer_number)
            return DrawerState(
                numero=drawer_number,
                esta_aberta=is_open
            )
        except Exception as e:
            logger.error(f"Error getting drawer state: {e}")
            return None
    
    def get_all_drawer_states(self, count: int = 10) -> List[DrawerState]:
        """
        Obtém estado de todas as gavetas.
        
        Args:
            count: Número de gavetas
            
        Returns:
            Lista de DrawerState
        """
        states = []
        for i in range(1, count + 1):
            state = self.get_drawer_state(i)
            if state:
                states.append(state)
            else:
                states.append(DrawerState(numero=i, esta_aberta=False))
        return states
    
    def set_drawer_state(
        self,
        drawer_number: int,
        is_open: bool,
        user_type: str,
        user_id: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Define estado de uma gaveta.
        
        Args:
            drawer_number: Número da gaveta
            is_open: Se está aberta
            user_type: Tipo do usuário
            user_id: ID do usuário (opcional)
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            estado = 'aberta' if is_open else 'fechada'
            success = self._repo.set_state(drawer_number, estado, user_type, user_id)
            
            if success:
                action = "aberta" if is_open else "fechada"
                logger.info(f"Drawer {drawer_number} {action} by user type {user_type}")
                return True, f"Gaveta {drawer_number} {action} com sucesso"
            else:
                return False, "Erro ao alterar estado da gaveta"
                
        except Exception as e:
            logger.error(f"Error setting drawer state: {e}")
            return False, f"Erro: {str(e)}"
    
    def get_drawer_history(
        self,
        drawer_number: int,
        page: int = 1,
        per_page: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Obtém histórico de uma gaveta com paginação.
        
        Args:
            drawer_number: Número da gaveta
            page: Página atual
            per_page: Itens por página
            
        Returns:
            PaginatedResult com histórico
        """
        try:
            offset = (page - 1) * per_page
            
            history_raw = self._repo.get_history_paginated(drawer_number, offset, per_page)
            total = self._repo.count_history(drawer_number)
            
            items = [
                DrawerHistoryItem(
                    data_hora=h[0],
                    gaveta_id=h[1] if len(h) > 1 else drawer_number,
                    acao=h[2] if len(h) > 2 else '',
                    usuario=h[3] if len(h) > 3 else ''
                )
                for h in history_raw
            ]
            
            return PaginatedResult(
                items=items,
                total=total,
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            logger.error(f"Error getting drawer history: {e}")
            return PaginatedResult(items=[], total=0, page=page, per_page=per_page)
    
    def get_all_history(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Obtém histórico de todas as gavetas com paginação.
        
        Args:
            page: Página atual
            per_page: Itens por página
            
        Returns:
            PaginatedResult com histórico
        """
        try:
            offset = (page - 1) * per_page
            
            history_raw = self._repo.get_all_history_paginated(offset, per_page)
            total = self._repo.count_all_history()
            
            items = [
                DrawerHistoryItem(
                    data_hora=h[0],
                    gaveta_id=h[1],
                    acao=h[2],
                    usuario=h[3]
                )
                for h in history_raw
            ]
            
            return PaginatedResult(
                items=items,
                total=total,
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            logger.error(f"Error getting all history: {e}")
            return PaginatedResult(items=[], total=0, page=page, per_page=per_page)
    
    def toggle_drawer(
        self,
        drawer_number: int,
        user_type: str,
        user_id: Optional[int] = None
    ) -> Tuple[bool, str, bool]:
        """
        Alterna estado de uma gaveta.
        
        Args:
            drawer_number: Número da gaveta
            user_type: Tipo do usuário
            user_id: ID do usuário (opcional)
            
        Returns:
            Tuple (sucesso, mensagem, novo_estado)
        """
        current_state = self.get_drawer_state(drawer_number)
        if not current_state:
            return False, "Gaveta não encontrada", False
        
        new_state = not current_state.esta_aberta
        success, message = self.set_drawer_state(
            drawer_number, new_state, user_type, user_id
        )
        
        return success, message, new_state


def get_drawer_service() -> DrawerService:
    """Retorna instância do DrawerService"""
    return DrawerService()
