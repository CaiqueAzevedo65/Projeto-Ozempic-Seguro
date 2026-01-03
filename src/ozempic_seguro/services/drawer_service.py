"""
Serviço de gavetas - View Service para componentes de UI.

.. deprecated:: 1.3.4
    Este módulo delega para GavetaService.
    Para novos desenvolvimentos, use GavetaService diretamente.

Mantido para compatibilidade com views existentes.
"""
from typing import Optional, List, Tuple

from .gaveta_service import (
    GavetaService,
    DrawerState,
    DrawerHistoryItem,
    PaginatedResult,
)
from ..core.logger import logger


class DrawerService:
    """
    Serviço de gavetas (View Service).
    
    .. deprecated:: 1.3.4
        Delega para GavetaService. Use GavetaService diretamente.
    """
    
    DEFAULT_PAGE_SIZE = 20
    
    def __init__(self):
        self._service = GavetaService.get_instance()
    
    def get_drawer_state(self, drawer_number: int) -> Optional[DrawerState]:
        """Obtém estado de uma gaveta."""
        try:
            is_open = self._service.get_state(drawer_number)
            return DrawerState(numero=drawer_number, esta_aberta=is_open)
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
        """Define estado de uma gaveta."""
        if is_open:
            return self._service.open_drawer(drawer_number, user_type, user_id)
        else:
            return self._service.close_drawer(drawer_number, user_type, user_id)
    
    def get_drawer_history(
        self,
        drawer_number: int,
        page: int = 1,
        per_page: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """Obtém histórico de uma gaveta com paginação."""
        try:
            offset = (page - 1) * per_page
            
            history_raw = self._service.get_history_paginated(drawer_number, offset, per_page)
            total = self._service.count_history(drawer_number)
            
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
        """Obtém histórico de todas as gavetas com paginação."""
        try:
            offset = (page - 1) * per_page
            
            history_raw = self._service.get_all_history_paginated(offset, per_page)
            total = self._service.count_all_history()
            
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
