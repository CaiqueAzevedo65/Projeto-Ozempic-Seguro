"""
Testes para exceções customizadas do sistema.

Verifica hierarquia, mensagens e serialização das exceções.
"""
import pytest
from ozempic_seguro.core.exceptions import (
    # Base
    OzempicError,
    # Authentication
    AuthenticationError,
    InvalidCredentialsError,
    SessionExpiredError,
    AccountLockedError,
    InsufficientPermissionsError,
    # User
    UserError,
    UserNotFoundError,
    UserAlreadyExistsError,
    LastAdminError,
    InvalidUserDataError,
    # Validation
    ValidationError,
    InvalidUsernameError,
    WeakPasswordError,
    InvalidInputError,
    # Database
    DatabaseError,
    MigrationError,
    IntegrityError,
    # Drawer
    DrawerError,
    DrawerNotFoundError,
    DrawerStateError,
    # Audit
    AuditError,
    AuditLogError,
    # Configuration
    ConfigurationError,
    MissingConfigError,
    InvalidConfigError,
)


class TestExceptionHierarchy:
    """Testa hierarquia de exceções"""
    
    def test_all_exceptions_inherit_from_ozempic_error(self):
        """Todas as exceções devem herdar de OzempicError"""
        exceptions = [
            AuthenticationError,
            InvalidCredentialsError,
            SessionExpiredError,
            AccountLockedError,
            InsufficientPermissionsError,
            UserError,
            UserNotFoundError,
            UserAlreadyExistsError,
            LastAdminError,
            InvalidUserDataError,
            ValidationError,
            InvalidUsernameError,
            WeakPasswordError,
            InvalidInputError,
            DatabaseError,
            MigrationError,
            IntegrityError,
            DrawerError,
            DrawerNotFoundError,
            DrawerStateError,
            AuditError,
            AuditLogError,
            ConfigurationError,
            MissingConfigError,
            InvalidConfigError,
        ]
        
        for exc_class in exceptions:
            assert issubclass(exc_class, OzempicError), f"{exc_class.__name__} should inherit from OzempicError"
    
    def test_auth_exceptions_inherit_from_authentication_error(self):
        """Exceções de auth devem herdar de AuthenticationError"""
        auth_exceptions = [
            InvalidCredentialsError,
            SessionExpiredError,
            AccountLockedError,
        ]
        
        for exc_class in auth_exceptions:
            assert issubclass(exc_class, AuthenticationError)
    
    def test_user_exceptions_inherit_from_user_error(self):
        """Exceções de usuário devem herdar de UserError"""
        user_exceptions = [
            UserNotFoundError,
            UserAlreadyExistsError,
            LastAdminError,
            InvalidUserDataError,
        ]
        
        for exc_class in user_exceptions:
            assert issubclass(exc_class, UserError)


class TestExceptionMessages:
    """Testa mensagens e códigos das exceções"""
    
    def test_ozempic_error_default_message(self):
        """OzempicError deve ter mensagem padrão"""
        exc = OzempicError()
        assert exc.message == "Erro interno do sistema"
        assert exc.code == "OZEMPIC_ERROR"
    
    def test_invalid_credentials_error(self):
        """InvalidCredentialsError deve incluir username"""
        exc = InvalidCredentialsError(username="testuser")
        assert "testuser" in str(exc.details)
        assert exc.code == "INVALID_CREDENTIALS"
    
    def test_account_locked_error(self):
        """AccountLockedError deve incluir detalhes do bloqueio"""
        exc = AccountLockedError(
            username="testuser",
            locked_until="10 minutos",
            attempts=5
        )
        assert exc.details["username"] == "testuser"
        assert exc.details["locked_until"] == "10 minutos"
        assert exc.details["attempts"] == 5
        assert exc.code == "ACCOUNT_LOCKED"
    
    def test_user_not_found_error(self):
        """UserNotFoundError deve incluir identificador"""
        exc = UserNotFoundError(identifier=123, field="id")
        assert "123" in exc.message
        assert exc.code == "USER_NOT_FOUND"
    
    def test_user_already_exists_error(self):
        """UserAlreadyExistsError deve incluir username"""
        exc = UserAlreadyExistsError(username="existinguser")
        assert "existinguser" in exc.message
        assert exc.code == "USER_ALREADY_EXISTS"
    
    def test_last_admin_error(self):
        """LastAdminError deve ter mensagem específica"""
        exc = LastAdminError()
        assert "último administrador" in exc.message.lower()
        assert exc.code == "LAST_ADMIN_ERROR"
    
    def test_weak_password_error(self):
        """WeakPasswordError deve listar razões"""
        reasons = ["muito curta", "sem número", "sem maiúscula"]
        exc = WeakPasswordError(reasons=reasons)
        assert exc.details["reasons"] == reasons
        assert exc.code == "WEAK_PASSWORD"
    
    def test_insufficient_permissions_error(self):
        """InsufficientPermissionsError deve incluir ação e roles"""
        exc = InsufficientPermissionsError(
            action="excluir_usuario",
            required_role="administrador",
            user_role="vendedor"
        )
        assert exc.details["action"] == "excluir_usuario"
        assert exc.details["required_role"] == "administrador"
        assert exc.details["user_role"] == "vendedor"


class TestExceptionSerialization:
    """Testa serialização das exceções"""
    
    def test_to_dict_includes_all_fields(self):
        """to_dict deve incluir todos os campos"""
        exc = UserNotFoundError(identifier=123)
        result = exc.to_dict()
        
        assert "error" in result
        assert "code" in result
        assert "message" in result
        assert "details" in result
        
        assert result["error"] == "UserNotFoundError"
        assert result["code"] == "USER_NOT_FOUND"
    
    def test_str_format_with_details(self):
        """__str__ deve formatar com detalhes"""
        exc = InvalidCredentialsError(username="testuser")
        str_repr = str(exc)
        
        assert "[INVALID_CREDENTIALS]" in str_repr
        assert "testuser" in str_repr
    
    def test_str_format_without_details(self):
        """__str__ deve funcionar sem detalhes"""
        exc = OzempicError(message="Test error", code="TEST")
        str_repr = str(exc)
        
        assert "[TEST]" in str_repr
        assert "Test error" in str_repr


class TestExceptionRaising:
    """Testa que exceções podem ser levantadas e capturadas corretamente"""
    
    def test_catch_specific_exception(self):
        """Deve capturar exceção específica"""
        with pytest.raises(UserNotFoundError) as exc_info:
            raise UserNotFoundError(identifier=999)
        
        assert exc_info.value.code == "USER_NOT_FOUND"
    
    def test_catch_parent_exception(self):
        """Deve capturar exceção pai"""
        with pytest.raises(UserError):
            raise UserNotFoundError(identifier=999)
    
    def test_catch_base_exception(self):
        """Deve capturar exceção base"""
        with pytest.raises(OzempicError):
            raise InvalidCredentialsError(username="test")
    
    def test_exception_chaining(self):
        """Deve suportar encadeamento de exceções"""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise DatabaseError("Database failed") from e
        except DatabaseError as exc:
            assert exc.__cause__ is not None
            assert isinstance(exc.__cause__, ValueError)
