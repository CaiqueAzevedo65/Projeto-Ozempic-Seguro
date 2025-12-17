"""
Testes para SecurityLogger - Logging de segurança.
"""
import pytest
from datetime import datetime

from ozempic_seguro.repositories.security_logger import SecurityLogger


class TestSecurityLogger:
    """Testes para SecurityLogger"""
    
    def test_get_local_ip(self):
        """Testa obtenção de IP local"""
        ip = SecurityLogger.get_local_ip()
        
        assert ip == "127.0.0.1"
    
    def test_get_system_info(self):
        """Testa obtenção de informações do sistema"""
        info = SecurityLogger.get_system_info()
        
        assert isinstance(info, dict)
        assert 'hostname' in info
        assert 'platform' in info
        assert 'system' in info
    
    def test_create_security_context(self):
        """Testa criação de contexto de segurança"""
        result = SecurityLogger.create_security_context(
            action='TEST_ACTION',
            user_id=1,
            username='testuser'
        )
        
        assert isinstance(result, dict)
        assert result['action'] == 'TEST_ACTION'
        assert result['user_id'] == 1
        assert result['username'] == 'testuser'
        assert 'timestamp' in result
        assert 'ip_address' in result
    
    def test_create_security_context_with_additional_data(self):
        """Testa criação de contexto com dados adicionais"""
        result = SecurityLogger.create_security_context(
            action='TEST_ACTION',
            additional_data={'key': 'value'}
        )
        
        assert 'additional_data' in result
        assert result['additional_data']['key'] == 'value'
    
    def test_log_login_attempt_success(self):
        """Testa log de tentativa de login bem-sucedida"""
        result = SecurityLogger.log_login_attempt(
            username='testuser',
            success=True,
            user_id=1
        )
        
        assert isinstance(result, dict)
        assert result['action'] == 'LOGIN_ATTEMPT'
        assert result['additional_data']['success'] is True
    
    def test_log_login_attempt_failure(self):
        """Testa log de tentativa de login falha"""
        result = SecurityLogger.log_login_attempt(
            username='testuser',
            success=False,
            failure_reason='Invalid password'
        )
        
        assert isinstance(result, dict)
        assert result['additional_data']['success'] is False
        assert 'failure_reason' in result['additional_data']
    
    def test_log_session_event(self):
        """Testa log de evento de sessão"""
        result = SecurityLogger.log_session_event(
            event_type='LOGIN',
            user_id=1,
            username='testuser'
        )
        
        assert isinstance(result, dict)
        assert result['action'] == 'SESSION_EVENT'
        assert result['additional_data']['event_type'] == 'LOGIN'
    
    def test_log_session_event_with_duration(self):
        """Testa log de evento de sessão com duração"""
        result = SecurityLogger.log_session_event(
            event_type='LOGOUT',
            user_id=1,
            username='testuser',
            session_duration=30
        )
        
        assert result['additional_data']['session_duration_minutes'] == 30
    
    def test_log_user_management(self):
        """Testa log de gerenciamento de usuário"""
        result = SecurityLogger.log_user_management(
            action='CREATE_USER',
            admin_user_id=1,
            admin_username='admin',
            target_user_id=2,
            target_username='newuser',
            changes={'tipo': 'vendedor'}
        )
        
        assert isinstance(result, dict)
        assert result['action'] == 'USER_MANAGEMENT'
        assert result['additional_data']['admin_action'] == 'CREATE_USER'
        assert result['additional_data']['target_user_id'] == 2
    
    def test_log_security_violation(self):
        """Testa log de violação de segurança"""
        result = SecurityLogger.log_security_violation(
            violation_type='UNAUTHORIZED_ACCESS',
            user_id=1,
            username='testuser',
            details={'resource': '/admin'}
        )
        
        assert isinstance(result, dict)
        assert result['action'] == 'SECURITY_VIOLATION'
        assert result['additional_data']['violation_type'] == 'UNAUTHORIZED_ACCESS'
        assert result['additional_data']['severity'] == 'HIGH'
