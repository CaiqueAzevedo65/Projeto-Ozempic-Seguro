from src.data.database import DatabaseManager
from src.session_manager import SessionManager

class GavetaStateManager:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GavetaStateManager, cls).__new__(cls)
            cls._db = DatabaseManager()
            cls._session_manager = SessionManager.get_instance()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_estado(self, gaveta_id):
        """Retorna o estado atual de uma gaveta"""
        return self._db.get_estado_gaveta(gaveta_id)

    def set_estado(self, gaveta_id, estado, usuario_tipo):
        """Define o estado de uma gaveta"""
        return self._db.set_estado_gaveta(gaveta_id, estado, usuario_tipo)

    def fechar_gaveta(self, gaveta_id, usuario_tipo, usuario_id=None):
        """Fecha uma gaveta (usado pelo Repositor)"""
        return self._db.set_estado_gaveta(gaveta_id, False, usuario_tipo, usuario_id)

    def abrir_gaveta(self, gaveta_id, usuario_tipo, usuario_id=None):
        """Abre uma gaveta (usado pelo Vendedor e Administrador)"""
        # Verifica se o sistema está bloqueado
        if usuario_tipo in ['vendedor', 'administrador'] and self._session_manager.is_blocked():
            tempo_restante = self._session_manager.get_remaining_time()
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            return False, f"Sistema bloqueado por {minutos}:{segundos:02d} minutos após a abertura da gaveta."
        
        try:
            # Obtém o ID do usuário da sessão atual se não foi fornecido
            if usuario_id is None and hasattr(self._session_manager, 'get_user_id'):
                usuario_id = self._session_manager.get_user_id()
                
            # Abre a gaveta e registra o histórico
            resultado = self._db.set_estado_gaveta(gaveta_id, True, usuario_tipo, usuario_id)
            
            # Se for vendedor ou administrador, bloqueia o sistema por 5 minutos
            if usuario_tipo in ['vendedor', 'administrador']:
                self._session_manager.block_for_minutes(5)
                return True, f"Gaveta {gaveta_id} aberta com sucesso! O sistema será bloqueado por 5 minutos."
                
            return resultado, f"Gaveta {gaveta_id} aberta com sucesso!"
        except Exception as e:
            return False, f"Erro ao abrir a gaveta: {str(e)}"
    
    def get_historico(self, gaveta_id, limite=10):
        """Obtém o histórico de alterações de uma gaveta"""
        return self._db.get_historico_gaveta(gaveta_id, limite)
    
    def get_historico_paginado(self, gaveta_id, offset=0, limit=20):
        """
        Obtém o histórico de alterações de uma gaveta com paginação
        
        Args:
            gaveta_id (str): ID da gaveta
            offset (int): Número de registros a pular
            limit (int): Número máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (acao, usuario, data_hora)
        """
        return self._db.get_historico_paginado(gaveta_id, offset, limit)
    
    def get_total_historico(self, gaveta_id):
        """
        Retorna o número total de registros de histórico para uma gaveta
        
        Args:
            gaveta_id (str): ID da gaveta
            
        Returns:
            int: Número total de registros
        """
        return self._db.get_total_historico(gaveta_id)
    
    def get_todo_historico(self):
        """Retorna todo o histórico de todas as gavetas"""
        try:
            return self._db.get_todo_historico()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []
    
    def get_todo_historico_paginado(self, offset=0, limit=20):
        """
        Retorna o histórico de acessos paginado para todas as gavetas
        
        Args:
            offset (int): Número de registros a pular
            limit (int): Número máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (data_hora, gaveta_id, acao, usuario)
        """
        return self._db.get_todo_historico_paginado(offset, limit)
    
    def get_total_todo_historico(self):
        """
        Retorna o número total de registros de histórico de todas as gavetas
        
        Returns:
            int: Número total de registros
        """
        return self._db.get_total_todo_historico()