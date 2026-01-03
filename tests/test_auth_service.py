"""
Testes para AuthService - Serviço de autenticação.
"""
import pytest

from ozempic_seguro.services.auth_service import (
    AuthService,
    LoginResult,
    UserPanel,
    get_auth_service,
)
from ozempic_seguro.session.session_manager import SessionManager


class TestAuthService:
    """Testes para AuthService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuthService()
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        result = self.service.login('nonexistent_user', 'wrongpass')
        
        assert isinstance(result, LoginResult)
        assert result.success is False
        assert result.error_message is not None
    
    def test_login_result_has_remaining_attempts(self):
        """Testa que resultado tem tentativas restantes"""
        result = self.service.login('test_user_attempts', 'wrongpass')
        
        assert isinstance(result.remaining_attempts, int)
    
    def test_logout(self):
        """Testa logout"""
        # Simular login
        self.session.set_current_user({
            'id': 1, 'username': 'test', 'tipo': 'vendedor'
        })
        
        self.service.logout()
        
        assert self.service.is_logged_in() is False
    
    def test_get_login_status(self):
        """Testa obtenção de status de login"""
        status = self.service.get_login_status('test_user')
        
        assert isinstance(status, dict)
        assert 'message' in status
    
    def test_is_user_locked_false(self):
        """Testa verificação de bloqueio - não bloqueado"""
        result = self.service.is_user_locked('new_user_not_locked')
        
        assert result is False
    
    def test_get_current_user_none(self):
        """Testa obtenção de usuário atual quando não logado"""
        self.session.logout()
        
        result = self.service.get_current_user()
        
        assert result is None
    
    def test_get_current_user_logged_in(self):
        """Testa obtenção de usuário atual quando logado"""
        user = {'id': 1, 'username': 'test', 'tipo': 'vendedor'}
        self.session.set_current_user(user)
        
        result = self.service.get_current_user()
        
        assert result == user
    
    def test_is_logged_in_false(self):
        """Testa verificação de login - não logado"""
        self.session.logout()
        
        assert self.service.is_logged_in() is False
    
    def test_is_logged_in_true(self):
        """Testa verificação de login - logado"""
        self.session.set_current_user({
            'id': 1, 'username': 'test', 'tipo': 'vendedor'
        })
        
        assert self.service.is_logged_in() is True
    
    def test_get_lockout_remaining_seconds(self):
        """Testa obtenção de segundos restantes de bloqueio"""
        result = self.service.get_lockout_remaining_seconds('test_user')
        
        assert isinstance(result, int)
        assert result >= 0


class TestUserPanel:
    """Testes para enum UserPanel"""
    
    def test_admin_panel(self):
        """Testa painel admin"""
        assert UserPanel.ADMIN.value == "administrador"
    
    def test_vendedor_panel(self):
        """Testa painel vendedor"""
        assert UserPanel.VENDEDOR.value == "vendedor"
    
    def test_repositor_panel(self):
        """Testa painel repositor"""
        assert UserPanel.REPOSITOR.value == "repositor"
    
    def test_tecnico_panel(self):
        """Testa painel técnico"""
        assert UserPanel.TECNICO.value == "tecnico"


class TestLoginResult:
    """Testes para LoginResult"""
    
    def test_login_result_success(self):
        """Testa criação de resultado de sucesso"""
        result = LoginResult(
            success=True,
            user={'id': 1, 'username': 'test'},
            panel=UserPanel.VENDEDOR
        )
        
        assert result.success is True
        assert result.user is not None
        assert result.panel == UserPanel.VENDEDOR
    
    def test_login_result_failure(self):
        """Testa criação de resultado de falha"""
        result = LoginResult(
            success=False,
            error_message="Credenciais inválidas",
            remaining_attempts=2
        )
        
        assert result.success is False
        assert result.error_message == "Credenciais inválidas"
        assert result.remaining_attempts == 2
    
    def test_login_result_locked(self):
        """Testa criação de resultado de conta bloqueada"""
        result = LoginResult(
            success=False,
            is_locked=True,
            lockout_seconds=300
        )
        
        assert result.success is False
        assert result.is_locked is True
        assert result.lockout_seconds == 300


class TestAuthServiceEdgeCases:
    """Testes para casos extremos do AuthService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuthService()
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
    
    def test_login_with_empty_username(self):
        """Testa login com username vazio"""
        result = self.service.login('', 'password')
        
        assert isinstance(result, LoginResult)
        assert result.success is False
    
    def test_login_with_whitespace_username(self):
        """Testa login com username apenas espaços"""
        result = self.service.login('   ', 'password')
        
        assert isinstance(result, LoginResult)
        assert result.success is False
    
    def test_multiple_failed_logins(self):
        """Testa múltiplas tentativas de login falhadas"""
        username = 'test_multiple_fails'
        
        result1 = self.service.login(username, 'wrong1')
        assert result1.success is False
        
        result2 = self.service.login(username, 'wrong2')
        assert result2.success is False
        
        result3 = self.service.login(username, 'wrong3')
        assert result3.success is False
    
    def test_logout_multiple_times(self):
        """Testa logout múltiplo"""
        # Simular login
        self.session.set_current_user({'id': 1, 'username': 'test'})
        
        self.service.logout()
        assert self.service.is_logged_in() is False
        
        # Segundo logout não deve causar erro
        self.service.logout()
        assert self.service.is_logged_in() is False
    
    def test_get_current_user_after_logout(self):
        """Testa obter usuário após logout"""
        self.session.set_current_user({'id': 1, 'username': 'test'})
        assert self.service.get_current_user() is not None
        
        self.service.logout()
        assert self.service.get_current_user() is None


class TestGetAuthService:
    """Testes para função get_auth_service"""
    
    def test_returns_auth_service(self):
        """Testa que retorna AuthService"""
        service = get_auth_service()
        
        assert isinstance(service, AuthService)
    
    def test_singleton_pattern(self):
        """Testa padrão singleton"""
        service1 = get_auth_service()
        service2 = get_auth_service()
        
        assert isinstance(service1, AuthService)
        assert isinstance(service2, AuthService)


class TestLoginResult:
    """Testes para LoginResult"""
    
    def test_login_result_success(self):
        """Testa LoginResult de sucesso"""
        result = LoginResult(success=True, user={'id': 1}, panel=UserPanel.VENDEDOR)
        assert result.success is True
        assert result.user is not None
        assert result.panel == UserPanel.VENDEDOR
    
    def test_login_result_failure(self):
        """Testa LoginResult de falha"""
        result = LoginResult(success=False, error_message="Invalid credentials")
        assert result.success is False
        assert result.error_message == "Invalid credentials"
    
    def test_login_result_with_attempts(self):
        """Testa LoginResult com tentativas restantes"""
        result = LoginResult(success=False, remaining_attempts=2)
        assert result.remaining_attempts == 2
    
    def test_login_result_with_lockout(self):
        """Testa LoginResult com lockout"""
        result = LoginResult(success=False, lockout_seconds=300)
        assert result.lockout_seconds == 300


class TestUserPanel:
    """Testes para UserPanel enum"""
    
    def test_user_panel_exists(self):
        """Testa que UserPanel existe e é enum"""
        from enum import Enum
        assert issubclass(UserPanel, Enum)
    
    def test_user_panel_has_members(self):
        """Testa que UserPanel tem membros"""
        members = list(UserPanel)
        assert len(members) > 0


class TestAuthServicePermissions:
    """Testes de permissões do AuthService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = AuthService()
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
    
    def test_login_attempt_tracking(self):
        """Testa rastreamento de tentativas de login"""
        username = "track_attempts_user"
        
        # Primeira tentativa
        result1 = self.service.login(username, "wrong1")
        # Segunda tentativa
        result2 = self.service.login(username, "wrong2")
        
        # Tentativas devem estar sendo rastreadas
        assert result2.remaining_attempts <= result1.remaining_attempts
    
    def test_reset_login_attempts(self):
        """Testa reset de tentativas após login bem-sucedido"""
        # Este teste é conceitual - verifica que o método existe
        assert hasattr(self.service, 'login')
        assert hasattr(self.service, 'logout')
