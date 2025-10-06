"""
Testes completos para SessionManager.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from ozempic_seguro.session import SessionManager


class TestSessionManager:
    """Testes para SessionManager"""
    
    @pytest.fixture
    def session_manager(self):
        """Cria instância limpa do SessionManager"""
        # Reset singleton
        SessionManager._instance = None
        session = SessionManager.get_instance()
        yield session
        # Cleanup
        if hasattr(session, '_timeout_timer') and session._timeout_timer:
            session._timeout_timer.cancel()
        SessionManager._instance = None
    
    def test_singleton_pattern(self):
        """Testa padrão singleton"""
        SessionManager._instance = None
        session1 = SessionManager.get_instance()
        session2 = SessionManager.get_instance()
        assert session1 is session2
        SessionManager._instance = None
    
    def test_set_and_get_current_user(self, session_manager):
        """Testa definir e obter usuário atual"""
        user = {'id': 1, 'username': 'test_user', 'tipo': 'vendedor'}
        
        session_manager.set_current_user(user)
        
        assert session_manager.get_current_user() == user
        assert session_manager.is_logged_in() is True
    
    def test_logout(self, session_manager):
        """Testa logout"""
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        
        session_manager.logout()
        
        assert session_manager.get_current_user() is None
        assert session_manager.is_logged_in() is False
    
    def test_update_activity(self, session_manager):
        """Testa atualização de atividade"""
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        
        initial_activity = session_manager._last_activity
        
        # Simula passagem de tempo
        import time
        time.sleep(0.1)
        
        session_manager.update_activity()
        
        assert session_manager._last_activity > initial_activity
    
    @patch('ozempic_seguro.session.datetime')
    def test_is_session_expired_true(self, mock_datetime, session_manager):
        """Testa sessão expirada"""
        now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        session_manager._last_activity = now - timedelta(minutes=11)
        
        assert session_manager.is_session_expired() is True
    
    @patch('ozempic_seguro.session.datetime')
    def test_is_session_expired_false(self, mock_datetime, session_manager):
        """Testa sessão não expirada"""
        now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        session_manager._last_activity = now - timedelta(minutes=5)
        
        assert session_manager.is_session_expired() is False
    
    def test_increment_login_attempts(self, session_manager):
        """Testa incremento de tentativas de login"""
        username = 'test_user'
        
        session_manager.increment_login_attempts(username)
        session_manager.increment_login_attempts(username)
        
        assert session_manager._login_attempts[username] == 2
    
    def test_reset_login_attempts(self, session_manager):
        """Testa reset de tentativas de login"""
        username = 'test_user'
        session_manager._login_attempts[username] = 3
        
        session_manager.reset_login_attempts(username)
        
        assert session_manager._login_attempts.get(username, 0) == 0
    
    def test_is_user_blocked_by_attempts(self, session_manager):
        """Testa bloqueio por tentativas"""
        username = 'test_user'
        
        # Simula 5 tentativas
        for _ in range(5):
            session_manager.increment_login_attempts(username)
        
        assert session_manager.is_user_blocked(username) is True
    
    def test_is_user_not_blocked(self, session_manager):
        """Testa usuário não bloqueado"""
        username = 'test_user'
        session_manager._login_attempts[username] = 2
        
        assert session_manager.is_user_blocked(username) is False
    
    @patch('ozempic_seguro.session.datetime')
    def test_block_user(self, mock_datetime, session_manager):
        """Testa bloqueio de usuário"""
        now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        username = 'test_user'
        session_manager.block_user(username)
        
        expected_until = now + timedelta(minutes=15)
        assert session_manager._blocked_until[username] == expected_until
    
    @patch('ozempic_seguro.session.datetime')
    def test_is_user_blocked_by_time_true(self, mock_datetime, session_manager):
        """Testa usuário bloqueado por tempo"""
        now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        username = 'test_user'
        session_manager._blocked_until[username] = now + timedelta(minutes=5)
        
        assert session_manager.is_user_blocked_by_time(username) is True
    
    @patch('ozempic_seguro.session.datetime')
    def test_is_user_blocked_by_time_false(self, mock_datetime, session_manager):
        """Testa usuário não bloqueado por tempo"""
        now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = now
        
        username = 'test_user'
        session_manager._blocked_until[username] = now - timedelta(minutes=1)
        
        assert session_manager.is_user_blocked_by_time(username) is False
    
    @patch('ozempic_seguro.session.get_audit_service')
    def test_start_timeout_timer(self, mock_get_audit, session_manager):
        """Testa início do timer de timeout"""
        mock_audit = Mock()
        mock_get_audit.return_value = mock_audit
        
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        
        session_manager._start_timeout_timer()
        
        assert session_manager._timeout_timer is not None
    
    @patch('ozempic_seguro.session.get_audit_service')
    def test_stop_timeout_timer(self, mock_get_audit, session_manager):
        """Testa parada do timer de timeout"""
        mock_audit = Mock()
        mock_get_audit.return_value = mock_audit
        
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        session_manager._start_timeout_timer()
        
        session_manager._stop_timeout_timer()
        
        assert session_manager._timeout_timer is None
    
    @patch('ozempic_seguro.session.get_audit_service')
    def test_cleanup(self, mock_get_audit, session_manager):
        """Testa cleanup completo"""
        mock_audit = Mock()
        mock_get_audit.return_value = mock_audit
        
        user = {'id': 1, 'username': 'test_user'}
        session_manager.set_current_user(user)
        
        session_manager.cleanup()
        
        assert session_manager._current_user is None
        assert session_manager._timeout_timer is None
        mock_audit.log_action.assert_called_once()
