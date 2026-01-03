"""
Pacote de gerenciamento de sessão.

Mantém compatibilidade com imports existentes via re-export.
"""
from .session_manager import SessionManager
from .login_attempts import LoginAttemptsManager
from .timer_manager import TimerManager

__all__ = [
    "SessionManager",
    "LoginAttemptsManager",
    "TimerManager",
]
