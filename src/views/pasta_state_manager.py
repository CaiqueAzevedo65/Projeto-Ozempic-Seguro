from src.data.database import DatabaseManager
from src.session_manager import SessionManager

class PastaStateManager:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PastaStateManager, cls).__new__(cls)
            cls._db = DatabaseManager()
            cls._session_manager = SessionManager.get_instance()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_estado(self, pasta_id):
        """Retorna o estado atual de uma pasta"""
        return self._db.get_estado_pasta(pasta_id)

    def set_estado(self, pasta_id, estado, usuario_tipo):
        """Define o estado de uma pasta"""
        return self._db.set_estado_pasta(pasta_id, estado, usuario_tipo)

    def fechar_pasta(self, pasta_id, usuario_tipo, usuario_id=None):
        """Fecha uma pasta (usado pelo Repositor)"""
        return self._db.set_estado_pasta(pasta_id, False, usuario_tipo, usuario_id)

    def abrir_pasta(self, pasta_id, usuario_tipo, usuario_id=None):
        """Abre uma pasta (usado pelo Vendedor e Administrador)"""
        # Verifica se o sistema está bloqueado
        if usuario_tipo in ['vendedor', 'administrador'] and self._session_manager.is_blocked():
            tempo_restante = self._session_manager.get_remaining_time()
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            return False, f"Sistema bloqueado por {minutos}:{segundos:02d} minutos após a abertura da pasta."
        
        try:
            # Se não estiver bloqueado, abre a pasta e bloqueia o sistema por 5 minutos
            resultado = self._db.set_estado_pasta(pasta_id, True, usuario_tipo, usuario_id)
            if usuario_tipo in ['vendedor', 'administrador']:
                self._session_manager.block_for_minutes(5)
                return True, f"Pasta {pasta_id} aberta com sucesso! O sistema será bloqueado por 5 minutos."
            return resultado, f"Pasta {pasta_id} aberta com sucesso!"
        except Exception as e:
            return False, f"Erro ao abrir a pasta: {str(e)}"
    
    def get_historico(self, pasta_id, limite=10):
        """Obtém o histórico de alterações de uma pasta"""
        return self._db.get_historico_pasta(pasta_id, limite)
    
    def get_historico_paginado(self, pasta_id, offset=0, limit=20):
        """
        Obtém o histórico de alterações de uma pasta com paginação
        
        Args:
            pasta_id (str): ID da pasta
            offset (int): Número de registros a pular
            limit (int): Número máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (acao, usuario, data_hora)
        """
        return self._db.get_historico_paginado(pasta_id, offset, limit)
    
    def get_total_historico(self, pasta_id):
        """
        Retorna o número total de registros de histórico para uma pasta
        
        Args:
            pasta_id (str): ID da pasta
            
        Returns:
            int: Número total de registros
        """
        return self._db.get_total_historico(pasta_id)
    
    def get_todo_historico(self):
        """Retorna todo o histórico de todas as pastas"""
        try:
            return self._db.get_todo_historico()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []