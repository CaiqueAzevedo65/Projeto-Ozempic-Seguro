from datetime import datetime, timedelta

class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._blocked_until = None
            cls._instance._current_user = None
            cls._instance._timer_enabled = True  # Timer ativado por padrão
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def set_current_user(self, user):
        """Define o usuário atual da sessão"""
        self._current_user = user
    
    def get_current_user(self):
        """Retorna o usuário atual da sessão"""
        return self._current_user
    
    def is_admin(self):
        """Verifica se o usuário atual é administrador"""
        return self._current_user and self._current_user.get('tipo') == 'administrador'
    
    def is_blocked(self):
        """Verifica se o sistema está bloqueado"""
        if not self._timer_enabled:
            return False  # Se o timer estiver desativado, nunca está bloqueado
            
        if self._blocked_until is None:
            return False
            
        # Remove o bloqueio se o tempo tiver expirado
        if datetime.now() >= self._blocked_until:
            self._blocked_until = None
            return False
            
        return True
    
    def get_remaining_time(self):
        """Retorna o tempo restante de bloqueio em segundos"""
        if not self._blocked_until or not self._timer_enabled:
            return 0
            
        remaining = (self._blocked_until - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def block_for_minutes(self, minutes=5):
        """
        Bloqueia o sistema por um número específico de minutos
        
        Args:
            minutes (int): Número de minutos para bloquear o sistema
            
        Returns:
            bool: True se o bloqueio foi aplicado, False se o usuário não tem permissão
                  ou se o timer estiver desativado
        """
        # Permite que tanto administradores quanto vendedores ativem o bloqueio
        if not (self.is_admin() or (self._current_user and self._current_user.get('tipo') == 'vendedor')) or not self._timer_enabled:
            return False
            
        self._blocked_until = datetime.now() + timedelta(minutes=minutes)
        return True
    
    def clear_block(self):
        """
        Remove o bloqueio do sistema
        
        Returns:
            bool: True se o bloqueio foi removido, False se o usuário não tem permissão
        """
        if not self.is_admin():
            return False
            
        self._blocked_until = None
        return True
    
    def set_timer_enabled(self, enabled):
        """
        Ativa ou desativa a função de timer
        
        Args:
            enabled (bool): True para ativar o timer, False para desativar
            
        Returns:
            bool: True se a alteração foi feita, False se o usuário não tem permissão
        """
        if not self.is_admin():
            return False
            
        self._timer_enabled = enabled
        return True
    
    def is_timer_enabled(self):
        """
        Verifica se a função de timer está ativada
        
        Returns:
            bool: True se o timer está ativado, False caso contrário
        """
        return self._timer_enabled
        
    def get_user_id(self):
        """
        Obtém o ID do usuário atualmente logado
        
        Returns:
            int or None: O ID do usuário ou None se não houver usuário logado
        """
        if self._current_user and 'id' in self._current_user:
            return self._current_user['id']
        return None
