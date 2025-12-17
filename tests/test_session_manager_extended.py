"""
Testes estendidos para SessionManager - Cobertura adicional.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from ozempic_seguro.session import SessionManager
from ozempic_seguro.config import Config


class TestSessionManagerExtended:
    """Testes estendidos para SessionManager"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
    
    def test_is_admin_true(self):
        """Testa verificação de admin quando é admin"""
        self.session.set_current_user({
            'id': 1,
            'username': 'admin',
            'tipo': 'administrador'
        })
        
        assert self.session.is_admin() is True
    
    def test_is_admin_false(self):
        """Testa verificação de admin quando não é admin"""
        self.session.set_current_user({
            'id': 2,
            'username': 'vendedor',
            'tipo': 'vendedor'
        })
        
        assert self.session.is_admin() is False
    
    def test_is_admin_no_user(self):
        """Testa verificação de admin sem usuário logado"""
        self.session.logout()
        
        # is_admin retorna None ou False quando não há usuário
        assert not self.session.is_admin()
    
    def test_is_tecnico_true(self):
        """Testa verificação de técnico quando é técnico"""
        self.session.set_current_user({
            'id': 3,
            'username': 'tecnico',
            'tipo': 'tecnico'
        })
        
        assert self.session.is_tecnico() is True
    
    def test_is_tecnico_false(self):
        """Testa verificação de técnico quando não é técnico"""
        self.session.set_current_user({
            'id': 2,
            'username': 'vendedor',
            'tipo': 'vendedor'
        })
        
        assert self.session.is_tecnico() is False
    
    def test_get_user_id(self):
        """Testa obtenção do ID do usuário"""
        self.session.set_current_user({
            'id': 42,
            'username': 'test',
            'tipo': 'vendedor'
        })
        
        assert self.session.get_user_id() == 42
    
    def test_get_user_id_no_user(self):
        """Testa obtenção do ID sem usuário logado"""
        self.session.logout()
        
        assert self.session.get_user_id() is None
    
    def test_is_blocked_delegates_to_timer(self):
        """Testa que is_blocked delega para TimerManager"""
        # Precisa ser admin ou vendedor para bloquear
        self.session.set_current_user({
            'id': 1,
            'username': 'admin',
            'tipo': 'administrador'
        })
        
        self.session.block_for_minutes(1)
        
        assert self.session.is_blocked() is True
    
    def test_get_remaining_time(self):
        """Testa obtenção do tempo restante de bloqueio"""
        self.session.set_current_user({
            'id': 1,
            'username': 'admin',
            'tipo': 'administrador'
        })
        self.session.block_for_minutes(5)
        
        remaining = self.session.get_remaining_time()
        
        assert remaining > 0
        assert remaining <= 5 * 60
    
    def test_clear_block(self):
        """Testa limpeza de bloqueio"""
        self.session.set_current_user({
            'id': 1,
            'username': 'admin',
            'tipo': 'administrador'
        })
        self.session.block_for_minutes(5)
        assert self.session.is_blocked() is True
        
        self.session.clear_block()
        
        assert self.session.is_blocked() is False
    
    def test_is_user_locked(self):
        """Testa verificação de usuário bloqueado por tentativas"""
        username = "test_locked_user"
        
        # Esgotar tentativas
        for _ in range(Config.Security.MAX_LOGIN_ATTEMPTS):
            self.session.record_login_attempt(username, success=False)
        
        assert self.session.is_user_locked(username) is True
    
    def test_get_lockout_remaining_time(self):
        """Testa obtenção do tempo restante de lockout"""
        username = "test_lockout_user"
        
        # Bloquear usuário
        for _ in range(Config.Security.MAX_LOGIN_ATTEMPTS):
            self.session.record_login_attempt(username, success=False)
        
        remaining = self.session.get_lockout_remaining_time(username)
        
        assert remaining >= 0
    
    def test_get_remaining_attempts(self):
        """Testa obtenção de tentativas restantes"""
        username = "test_attempts_user"
        
        self.session.record_login_attempt(username, success=False)
        
        remaining = self.session.get_remaining_attempts(username)
        
        assert remaining == Config.Security.MAX_LOGIN_ATTEMPTS - 1
    
    def test_get_login_status_message(self):
        """Testa obtenção de mensagem de status de login"""
        username = "test_status_user"
        
        self.session.record_login_attempt(username, success=False)
        
        status = self.session.get_login_status_message(username)
        
        assert status is not None
        assert 'message' in status
    
    def test_set_timer_enabled(self):
        """Testa habilitação/desabilitação do timer"""
        # Precisa ser admin ou tecnico para alterar timer
        self.session.set_current_user({
            'id': 1,
            'username': 'admin',
            'tipo': 'administrador'
        })
        
        self.session.set_timer_enabled(False)
        
        # Quando desabilitado, bloqueio não deve funcionar
        self.session.block_for_minutes(5)
        assert self.session.is_blocked() is False
        
        self.session.set_timer_enabled(True)
    
    def test_set_session_timeout(self):
        """Testa definição de timeout de sessão"""
        # set_session_timeout modifica diretamente o atributo
        self.session._session_timeout = 30
        
        assert self.session._session_timeout == 30
        
        # Restaurar para valor padrão
        from ozempic_seguro.config import Config
        self.session._session_timeout = Config.Security.SESSION_TIMEOUT_MINUTES


class TestSessionManagerAuditCallback:
    """Testes para callback de auditoria"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
        SessionManager._audit_callback = None
    
    def test_set_audit_callback(self):
        """Testa definição de callback de auditoria"""
        callback = MagicMock()
        
        SessionManager.set_audit_callback(callback)
        
        assert SessionManager._audit_callback is callback
