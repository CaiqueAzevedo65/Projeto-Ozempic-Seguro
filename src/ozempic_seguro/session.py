from datetime import datetime, timedelta
import threading
from .config import Config

class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._blocked_until = None
            cls._instance._current_user = None
            cls._instance._timer_enabled = True  # Timer ativado por padrão
            cls._instance._last_activity = None
            cls._instance._session_timeout = 10  # 10 minutos padrão
            cls._instance._timeout_timer = None
            cls._instance._login_attempts = {}
            cls._instance._max_login_attempts = Config.Security.MAX_LOGIN_ATTEMPTS
            cls._instance._lockout_duration = Config.Security.LOCKOUT_DURATION_MINUTES
        return cls._instance
    
    @classmethod
    def get_instance(cls):
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
        """Atualiza o timestamp da última atividade"""
        if self._current_user:
            self._last_activity = datetime.now()
            # Reinicia o timer se estiver ativo
            if self._timeout_timer:
                self._stop_timeout_timer()
                self._start_timeout_timer()
    
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

    def update_last_activity(self):
        """Atualiza timestamp da última atividade"""
        if self._current_user:
            self._last_activity = datetime.now()
            # Reinicia o timer de timeout
            self._start_timeout_timer()
    
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
    
    def _expire_session(self):
        """Expira a sessão por inatividade"""
        if self._current_user:
            # Log da expiração da sessão
            from .services.service_factory import get_audit_service
            audit_service = get_audit_service()
            audit_service.create_log(
                usuario_id=self._current_user.get('id'),
                acao='SESSAO_EXPIRADA',
                tabela_afetada='SESSOES',
                dados_anteriores={'motivo': 'timeout_inatividade'}
            )
            
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
    
    def increment_login_attempts(self, username):
        """Incrementa tentativas de login (alias para record_login_attempt)"""
        self.record_login_attempt(username, success=False)
    
    def reset_login_attempts(self, username):
        """Reseta tentativas de login"""
        if username in self._login_attempts:
            self._login_attempts[username] = {
                'count': 0,
                'first_attempt': None,
                'locked_until': None
            }
    
    def is_user_blocked(self, username):
        """Verifica se usuário está bloqueado (alias para is_user_locked)"""
        return self.is_user_locked(username)
    
    def is_user_blocked_by_time(self, username):
        """Verifica se usuário está bloqueado por tempo"""
        if username not in self._login_attempts:
            return False
        
        attempt_data = self._login_attempts[username]
        if attempt_data['locked_until'] is None:
            return False
        
        return datetime.now() < attempt_data['locked_until']
    
    def block_user(self, username):
        """Bloqueia usuário por tempo determinado"""
        if username not in self._login_attempts:
            self._login_attempts[username] = {
                'count': 0,
                'first_attempt': None,
                'locked_until': None
            }
        
        self._login_attempts[username]['locked_until'] = datetime.now() + timedelta(minutes=self._lockout_duration)
    
    def cleanup(self):
        """Limpa a sessão e para timers"""
        # Para o timer de timeout
        self._stop_timeout_timer()
        
        # Registra logout se houver usuário
        if self._current_user:
            try:
                from .services.service_factory import get_audit_service
                audit_service = get_audit_service()
                audit_service.log_action(
                    user_id=self._current_user.get('id'),
                    action='SESSION_CLEANUP',
                    details='Sessão encerrada via cleanup'
                )
            except:
                pass
        
        # Limpa dados da sessão
        self._current_user = None
        self._last_activity = None
        self._timeout_timer = None
        self._blocked_until = None
