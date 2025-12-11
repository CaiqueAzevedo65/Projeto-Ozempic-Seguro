"""
Gerenciador de sessão do sistema Ozempic Seguro.

Responsável por controlar sessões de usuário, timeouts e bloqueios.
"""
from datetime import datetime, timedelta
import threading
from typing import Optional, Dict, Any, Callable

from .config import Config
from .core.logger import logger


class SessionManager:
    """
    Gerenciador de sessão singleton thread-safe.
    
    Responsabilidades:
    - Gerenciamento de usuário logado
    - Controle de timeout de sessão
    - Controle de bloqueio por tentativas de login
    - Controle de timer do sistema
    
    Uso:
        session = SessionManager.get_instance()
        session.set_current_user(user_dict)
    """
    _instance: Optional['SessionManager'] = None
    _lock = threading.Lock()
    
    # Callback para auditoria (evita import circular)
    _audit_callback: Optional[Callable[[int, str, str, Dict], None]] = None
    
    def __new__(cls) -> 'SessionManager':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SessionManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Inicializa atributos da instância"""
        self._blocked_until: Optional[datetime] = None
        self._current_user: Optional[Dict[str, Any]] = None
        self._timer_enabled: bool = True
        self._last_activity: Optional[datetime] = None
        self._session_timeout: int = Config.Security.SESSION_TIMEOUT_MINUTES
        self._timeout_timer: Optional[threading.Timer] = None
        self._login_attempts: Dict[str, Dict] = {}
        self._max_login_attempts: int = Config.Security.MAX_LOGIN_ATTEMPTS
        self._lockout_duration: int = Config.Security.LOCKOUT_DURATION_MINUTES
    
    @classmethod
    def set_audit_callback(cls, callback: Callable[[int, str, str, Dict], None]) -> None:
        """
        Define callback para auditoria (evita import circular).
        
        Args:
            callback: Função que recebe (user_id, acao, tabela, dados)
        """
        cls._audit_callback = callback
    
    @classmethod
    def get_instance(cls):
        """Retorna a instância singleton do SessionManager"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def set_current_user(self, user):
        """Define o usuário atual da sessão"""
        self._current_user = user
        if user:
            self._last_activity = datetime.now()
            self._start_timeout_timer()
        else:
            self._stop_timeout_timer()
            self._last_activity = None
    
    def get_current_user(self):
        """Retorna o usuário atual da sessão"""
        return self._current_user
    
    def is_logged_in(self):
        """Verifica se há um usuário logado"""
        return self._current_user is not None
    
    def logout(self):
        """Faz logout do usuário atual"""
        self.set_current_user(None)
    
    def update_activity(self):
        """Atualiza o timestamp da última atividade e reinicia timer"""
        if self._current_user:
            self._last_activity = datetime.now()
            self._stop_timeout_timer()
            self._start_timeout_timer()
    
    # Alias para compatibilidade
    update_last_activity = update_activity
    
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
        # Permite admin ou técnico alterar o timer
        if not self.is_admin() and not self.is_tecnico():
            return False
            
        self._timer_enabled = enabled
        return True
    
    def is_tecnico(self):
        """Verifica se o usuário atual é técnico"""
        if self._current_user is None:
            return False
        return self._current_user.get('tipo') == 'tecnico'
    
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

    def is_session_expired(self):
        """Verifica se a sessão expirou por inatividade"""
        if not self._current_user or not self._last_activity:
            return False
        
        time_since_activity = datetime.now() - self._last_activity
        return time_since_activity.total_seconds() > (self._session_timeout * 60)
    
    def _start_timeout_timer(self):
        """Inicia o timer de timeout da sessão"""
        self._stop_timeout_timer()  # Para o timer anterior se existir
        
        if self._current_user:
            # Timer para expirar sessão após inatividade
            self._timeout_timer = threading.Timer(
                self._session_timeout * 60,  # Converte minutos para segundos
                self._expire_session
            )
            self._timeout_timer.start()
    
    def _stop_timeout_timer(self):
        """Para o timer de timeout"""
        if self._timeout_timer:
            self._timeout_timer.cancel()
            self._timeout_timer = None
    
    def _expire_session(self) -> None:
        """Expira a sessão por inatividade"""
        if self._current_user:
            user_id = self._current_user.get('id')
            
            # Log via callback (evita import circular)
            if self._audit_callback:
                try:
                    self._audit_callback(
                        user_id,
                        'SESSAO_EXPIRADA',
                        'SESSOES',
                        {'motivo': 'timeout_inatividade'}
                    )
                except Exception as e:
                    logger.error(f"Error logging session expiration: {e}")
            
            logger.info(f"Session expired for user {user_id}")
            
            # Limpa a sessão
            self._current_user = None
            self._last_activity = None
    
    def get_session_remaining_time(self):
        """Retorna tempo restante da sessão em minutos"""
        if not self._current_user or not self._last_activity:
            return 0
        
        elapsed = datetime.now() - self._last_activity
        remaining_seconds = (self._session_timeout * 60) - elapsed.total_seconds()
        return max(0, int(remaining_seconds / 60))
    
    def set_session_timeout(self, minutes):
        """Define o timeout da sessão em minutos"""
        if self.is_admin():
            self._session_timeout = minutes
            if self._current_user:
                self._start_timeout_timer()  # Reinicia timer com novo valor
            return True
        return False
    
    def record_login_attempt(self, username, success=True):
        """Registra tentativa de login para controle de força bruta"""
        now = datetime.now()
        
        if username not in self._login_attempts:
            self._login_attempts[username] = {
                'count': 0,
                'last_attempt': now,
                'locked_until': None
            }
        
        attempt_data = self._login_attempts[username]
        
        if success:
            # Reset contador em caso de sucesso
            attempt_data['count'] = 0
            attempt_data['locked_until'] = None
        else:
            # Incrementa contador de falhas
            attempt_data['count'] += 1
            attempt_data['last_attempt'] = now
            
            # Bloqueia usuário se excedeu tentativas
            if attempt_data['count'] >= self._max_login_attempts:
                attempt_data['locked_until'] = now + timedelta(minutes=self._lockout_duration)
    
    def is_user_locked(self, username):
        """Verifica se usuário está bloqueado por tentativas de login"""
        if username not in self._login_attempts:
            return False
        
        attempt_data = self._login_attempts[username]
        
        if attempt_data['locked_until'] is None:
            return False
        
        # Remove bloqueio se tempo expirou
        if datetime.now() >= attempt_data['locked_until']:
            attempt_data['locked_until'] = None
            attempt_data['count'] = 0
            return False
        
        return True
    
    def get_lockout_remaining_time(self, username):
        """Retorna tempo restante de bloqueio em minutos"""
        if username not in self._login_attempts:
            return 0
        
        attempt_data = self._login_attempts[username]
        
        if attempt_data['locked_until'] is None:
            return 0
        
        remaining = attempt_data['locked_until'] - datetime.now()
        return max(0, int(remaining.total_seconds() / 60))
    
    def get_lockout_remaining_seconds(self, username):
        """Retorna tempo restante de bloqueio em segundos para timer preciso"""
        if username not in self._login_attempts:
            return 0
        
        attempt_data = self._login_attempts[username]
        
        if attempt_data['locked_until'] is None:
            return 0
        
        remaining = attempt_data['locked_until'] - datetime.now()
        return max(0, int(remaining.total_seconds()))
    
    def get_remaining_attempts(self, username):
        """Retorna número de tentativas restantes antes do bloqueio"""
        if username not in self._login_attempts:
            return self._max_login_attempts
        
        attempt_data = self._login_attempts[username]
        used_attempts = attempt_data['count']
        remaining = self._max_login_attempts - used_attempts
        return max(0, remaining)
    
    def get_login_status_message(self, username):
        """Retorna mensagem personalizada sobre o status de login"""
        if self.is_user_locked(username):
            remaining_time = self.get_lockout_remaining_time(username)
            remaining_seconds = self.get_lockout_remaining_seconds(username)
            
            if remaining_time > 0:
                return {
                    'locked': True,
                    'message': f"Conta bloqueada por {remaining_time} minuto(s)",
                    'detailed_message': f"Muitas tentativas incorretas. Tente novamente em {remaining_time}:{remaining_seconds % 60:02d}",
                    'remaining_seconds': remaining_seconds
                }
        
        remaining_attempts = self.get_remaining_attempts(username)
        if remaining_attempts < self._max_login_attempts:
            return {
                'locked': False,
                'message': f"Atenção: {remaining_attempts} tentativa(s) restante(s)",
                'remaining_attempts': remaining_attempts
            }
        
        return {
            'locked': False,
            'message': "",
            'remaining_attempts': remaining_attempts
        }
    
    def reset_login_attempts(self, username):
        """Reseta tentativas de login de um usuário"""
        if username in self._login_attempts:
            self._login_attempts[username] = {
                'count': 0,
                'last_attempt': None,
                'locked_until': None
            }
    
    # Aliases para compatibilidade com código existente
    def increment_login_attempts(self, username):
        """Alias para record_login_attempt(success=False) - mantido para compatibilidade"""
        self.record_login_attempt(username, success=False)
    
    def is_user_blocked(self, username):
        """Alias para is_user_locked - mantido para compatibilidade"""
        return self.is_user_locked(username)
    
    is_user_blocked_by_time = is_user_blocked
    
    def cleanup(self) -> None:
        """Limpa a sessão e para timers"""
        self._stop_timeout_timer()
        
        # Log via callback se houver usuário
        if self._current_user and self._audit_callback:
            try:
                self._audit_callback(
                    self._current_user.get('id'),
                    'SESSION_CLEANUP',
                    'SESSOES',
                    {'details': 'Sessão encerrada via cleanup'}
                )
            except Exception as e:
                logger.debug(f"Could not log cleanup: {e}")
        
        # Limpa dados da sessão
        self._current_user = None
        self._last_activity = None
        self._timeout_timer = None
        self._blocked_until = None
