"""
Gerenciador de sessão do sistema Ozempic Seguro.

.. deprecated:: 1.3.3
    Este módulo é mantido apenas para compatibilidade.
    Para novos desenvolvimentos, importe diretamente do pacote:
        from ozempic_seguro.session import SessionManager
    
    Será removido em versão futura.
"""
# Re-export do pacote session para compatibilidade
from .session.session_manager import SessionManager
from .session.login_attempts import LoginAttemptsManager
from .session.timer_manager import TimerManager

__all__ = ['SessionManager', 'LoginAttemptsManager', 'TimerManager']
