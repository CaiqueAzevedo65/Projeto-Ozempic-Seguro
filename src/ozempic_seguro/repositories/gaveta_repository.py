"""
Repositório de gavetas: manipulação de estado e histórico.
"""
from .database import DatabaseManager

class GavetaRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def get_state(self, gaveta_id):
        """Retorna o estado atual de uma gaveta."""
        return self.db.get_estado_gaveta(gaveta_id)

    def set_state(self, gaveta_id, estado, usuario_tipo, usuario_id=None):
        """Define o estado de uma gaveta e registra no histórico."""
        return self.db.set_estado_gaveta(gaveta_id, estado, usuario_tipo, usuario_id)

    def get_history(self, gaveta_id, limit=10):
        """Retorna o histórico de uma gaveta."""
        return self.db.get_historico_gaveta(gaveta_id, limit)

    def get_history_paginated(self, gaveta_id, offset=0, limit=20):
        """Retorna o histórico de uma gaveta com paginação."""
        return self.db.get_historico_paginado(gaveta_id, offset, limit)

    def count_history(self, gaveta_id):
        """Retorna o total de registros de histórico para uma gaveta."""
        return self.db.get_total_historico(gaveta_id)

    def get_all_history(self):
        """Retorna todo o histórico de todas as gavetas."""
        return self.db.get_todo_historico()

    def get_all_history_paginated(self, offset=0, limit=20):
        """Retorna o histórico de todas as gavetas com paginação."""
        return self.db.get_todo_historico_paginado(offset, limit)

    def count_all_history(self):
        """Retorna o número total de registros de histórico de todas as gavetas."""
        return self.db.get_total_todo_historico()
