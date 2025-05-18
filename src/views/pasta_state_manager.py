from src.data.database import DatabaseManager

class PastaStateManager:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PastaStateManager, cls).__new__(cls)
            cls._db = DatabaseManager()
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

    def fechar_pasta(self, pasta_id, usuario_tipo):
        """Fecha uma pasta (usado pelo Repositor)"""
        return self._db.set_estado_pasta(pasta_id, False, usuario_tipo)

    def abrir_pasta(self, pasta_id, usuario_tipo):
        """Abre uma pasta (usado pelo Vendedor)"""
        return self._db.set_estado_pasta(pasta_id, True, usuario_tipo)
    
    def get_historico(self, pasta_id, limite=10):
        """Obtém o histórico de alterações de uma pasta"""
        return self._db.get_historico_pasta(pasta_id, limite)

    def get_todo_historico(self):
        """Retorna todo o histórico de todas as pastas"""
        try:
            return self._db.get_todo_historico()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []