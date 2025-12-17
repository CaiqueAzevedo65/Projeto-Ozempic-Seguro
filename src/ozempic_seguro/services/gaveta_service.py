"""
Serviço de gavetas: lógica de negócio para manipulação de gavetas.

Responsável por gerenciar estado das gavetas e histórico de operações.
"""
from typing import Optional, List, Tuple, Any

from ..repositories.gaveta_repository import GavetaRepository
from ..session import SessionManager
from ..core.logger import logger


class GavetaService:
    """
    Serviço singleton para operações de gavetas.
    
    Responsabilidades:
    - Gerenciar estado das gavetas (aberta/fechada)
    - Aplicar regras de negócio (bloqueio após abertura)
    - Consultar histórico de operações
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GavetaService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa dependências"""
        self._repository = GavetaRepository()
        self._session_manager = SessionManager.get_instance()

    @classmethod
    def get_instance(cls):
        """Retorna a instância singleton"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_estado(self, gaveta_id: int) -> bool:
        """Retorna o estado atual de uma gaveta"""
        return self._repository.get_state(gaveta_id)

    def set_estado(self, gaveta_id: int, estado: bool, usuario_tipo: str) -> Tuple[bool, str]:
        """Define o estado de uma gaveta"""
        return self._repository.set_state(gaveta_id, estado, usuario_tipo)

    def fechar_gaveta(self, gaveta_id: int, usuario_tipo: str, usuario_id: Optional[int] = None) -> Tuple[bool, str]:
        """Fecha uma gaveta (usado pelo Repositor)"""
        return self._repository.set_state(gaveta_id, False, usuario_tipo, usuario_id)

    def abrir_gaveta(self, gaveta_id: int, usuario_tipo: str, usuario_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Abre uma gaveta (usado pelo Vendedor e Administrador).
        
        Aplica regra de negócio: bloqueia sistema por 5 minutos após abertura
        por vendedor ou administrador.
        """
        # Verifica se o sistema está bloqueado
        if usuario_tipo in ['vendedor', 'administrador'] and self._session_manager.is_blocked():
            tempo_restante = self._session_manager.get_remaining_time()
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            return False, f"Sistema bloqueado por {minutos}:{segundos:02d} minutos após a abertura da gaveta."
        
        try:
            # Obtém o ID do usuário da sessão atual se não foi fornecido
            if usuario_id is None:
                usuario_id = self._session_manager.get_user_id()
                
            # Abre a gaveta e registra o histórico
            resultado = self._repository.set_state(gaveta_id, True, usuario_tipo, usuario_id)
            
            # Se for vendedor ou administrador, bloqueia o sistema por 5 minutos
            if usuario_tipo in ['vendedor', 'administrador']:
                self._session_manager.block_for_minutes(5)
                logger.info(f"Drawer {gaveta_id} opened by {usuario_tipo}, system blocked for 5 minutes")
                return True, f"Gaveta {gaveta_id} aberta com sucesso! O sistema será bloqueado por 5 minutos."
                
            return resultado[0] if isinstance(resultado, tuple) else resultado, f"Gaveta {gaveta_id} aberta com sucesso!"
        except Exception as e:
            logger.error(f"Error opening drawer {gaveta_id}: {e}")
            return False, f"Erro ao abrir a gaveta: {str(e)}"
    
    def get_historico(self, gaveta_id: int, limite: int = 10) -> List[Tuple]:
        """Obtém o histórico de alterações de uma gaveta"""
        return self._repository.get_history(gaveta_id, limite)
    
    def get_historico_paginado(self, gaveta_id: int, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """Obtém o histórico de alterações de uma gaveta com paginação"""
        return self._repository.get_history_paginated(gaveta_id, offset, limit)
    
    def get_total_historico(self, gaveta_id: int) -> int:
        """Retorna o número total de registros de histórico para uma gaveta"""
        return self._repository.count_history(gaveta_id)
    
    def get_todo_historico(self) -> List[Tuple]:
        """Retorna todo o histórico de todas as gavetas"""
        try:
            return self._repository.get_all_history()
        except Exception as e:
            logger.error(f"Error fetching all history: {e}")
            return []
    
    def get_todo_historico_paginado(self, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """Retorna o histórico de acessos paginado para todas as gavetas"""
        return self._repository.get_all_history_paginated(offset, limit)
    
    def get_total_todo_historico(self) -> int:
        """Retorna o número total de registros de histórico de todas as gavetas"""
        return self._repository.count_all_history()


# Alias para compatibilidade com código existente
GavetaStateManager = GavetaService
