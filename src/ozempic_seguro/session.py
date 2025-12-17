"""
Gerenciador de sessão do sistema Ozempic Seguro.

NOTA: Este módulo foi refatorado. A implementação agora está em session/.
Este arquivo mantém compatibilidade com imports existentes.

Para novos desenvolvimentos, importe de:
    from ozempic_seguro.session import SessionManager
"""
# Re-export do pacote session para compatibilidade
from .session.session_manager import SessionManager
from .session.login_attempts import LoginAttemptsManager
from .session.timer_manager import TimerManager

__all__ = ['SessionManager', 'LoginAttemptsManager', 'TimerManager']
