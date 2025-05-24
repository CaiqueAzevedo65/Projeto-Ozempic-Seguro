import time
from datetime import datetime, timedelta

class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._blocked_until = None
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def is_blocked(self):
        """Verifica se o sistema está bloqueado"""
        if self._blocked_until is None:
            return False
        return datetime.now() < self._blocked_until
    
    def get_remaining_time(self):
        """Retorna o tempo restante de bloqueio em segundos"""
        if not self._blocked_until:
            return 0
        remaining = (self._blocked_until - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def block_for_minutes(self, minutes=5):
        """Bloqueia o sistema por um número específico de minutos"""
        self._blocked_until = datetime.now() + timedelta(minutes=minutes)
    
    def clear_block(self):
        """Remove o bloqueio do sistema"""
        self._blocked_until = None
