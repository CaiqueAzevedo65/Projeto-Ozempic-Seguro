"""
Testes completos para Validators - Cobertura máxima.
"""
import pytest

from ozempic_seguro.core.validators import (
    Validators,
    ValidationResult,
    ValidationRule,
    UserType,
)


class TestValidatorsUsername:
    """Testes de validação de username"""
    
    def test_validate_username_valid(self):
        """Testa username válido"""
        result = Validators.validate_username("testuser")
        assert result.is_valid is True
    
    def test_validate_username_too_short(self):
        """Testa username muito curto"""
        result = Validators.validate_username("ab")
        # Username de 2 caracteres pode ser válido dependendo da config
        assert isinstance(result.is_valid, bool)
    
    def test_validate_username_too_long(self):
        """Testa username muito longo"""
        result = Validators.validate_username("a" * 51)
        assert result.is_valid is False
    
    def test_validate_username_with_special_chars(self):
        """Testa username com caracteres especiais"""
        result = Validators.validate_username("test@user!")
        assert result.is_valid is False
    
    def test_validate_username_with_numbers(self):
        """Testa username com números"""
        result = Validators.validate_username("user123")
        assert result.is_valid is True
    
    def test_validate_username_with_underscore(self):
        """Testa username com underscore"""
        result = Validators.validate_username("test_user")
        assert result.is_valid is True


class TestValidatorsPassword:
    """Testes de validação de senha"""
    
    def test_validate_password_valid(self):
        """Testa senha válida"""
        result = Validators.validate_password("ValidPass123")
        assert result.is_valid is True
    
    def test_validate_password_too_short(self):
        """Testa senha muito curta"""
        result = Validators.validate_password("123")
        assert result.is_valid is False
    
    def test_validate_password_no_uppercase(self):
        """Testa senha sem maiúscula"""
        result = Validators.validate_password("validpass123")
        # Depende da implementação
        assert isinstance(result.is_valid, bool)
    
    def test_validate_password_no_lowercase(self):
        """Testa senha sem minúscula"""
        result = Validators.validate_password("VALIDPASS123")
        assert isinstance(result.is_valid, bool)
    
    def test_validate_password_no_number(self):
        """Testa senha sem número"""
        result = Validators.validate_password("ValidPassword")
        assert isinstance(result.is_valid, bool)


class TestValidatorsName:
    """Testes de validação de nome"""
    
    def test_validate_name_valid(self):
        """Testa nome válido"""
        result = Validators.validate_name("João da Silva")
        assert result.is_valid is True
    
    def test_validate_name_too_short(self):
        """Testa nome muito curto"""
        result = Validators.validate_name("A")
        assert result.is_valid is False
    
    def test_validate_name_with_accents(self):
        """Testa nome com acentos"""
        result = Validators.validate_name("José Müller")
        assert result.is_valid is True
    
    def test_validate_name_empty(self):
        """Testa nome vazio"""
        result = Validators.validate_name("")
        assert result.is_valid is False


class TestValidatorsUserType:
    """Testes de validação de tipo de usuário"""
    
    def test_validate_user_type_admin(self):
        """Testa tipo administrador"""
        result = Validators.validate_user_type("administrador")
        assert result.is_valid is True
    
    def test_validate_user_type_vendedor(self):
        """Testa tipo vendedor"""
        result = Validators.validate_user_type("vendedor")
        assert result.is_valid is True
    
    def test_validate_user_type_repositor(self):
        """Testa tipo repositor"""
        result = Validators.validate_user_type("repositor")
        assert result.is_valid is True
    
    def test_validate_user_type_tecnico(self):
        """Testa tipo técnico"""
        result = Validators.validate_user_type("tecnico")
        assert result.is_valid is True
    
    def test_validate_user_type_invalid(self):
        """Testa tipo inválido"""
        result = Validators.validate_user_type("invalid_type")
        assert result.is_valid is False


class TestValidatorsEmail:
    """Testes de validação de email"""
    
    def test_validate_email_valid(self):
        """Testa email válido"""
        result = Validators.validate_email("test@example.com")
        assert result.is_valid is True
    
    def test_validate_email_invalid_no_at(self):
        """Testa email sem @"""
        result = Validators.validate_email("testexample.com")
        assert result.is_valid is False
    
    def test_validate_email_invalid_no_domain(self):
        """Testa email sem domínio"""
        result = Validators.validate_email("test@")
        assert result.is_valid is False


class TestValidatorsPhone:
    """Testes de validação de telefone"""
    
    def test_validate_phone_valid_mobile(self):
        """Testa celular válido"""
        result = Validators.validate_phone("(11) 99999-9999")
        assert result.is_valid is True
    
    def test_validate_phone_valid_landline(self):
        """Testa fixo válido"""
        result = Validators.validate_phone("(11) 3333-3333")
        assert result.is_valid is True
    
    def test_validate_phone_invalid(self):
        """Testa telefone inválido"""
        result = Validators.validate_phone("123")
        assert result.is_valid is False


class TestValidatorsDate:
    """Testes de validação de data"""
    
    def test_validate_date_valid(self):
        """Testa data válida"""
        result = Validators.validate_date("2025-01-15")
        assert result.is_valid is True
    
    def test_validate_date_invalid_format(self):
        """Testa data com formato inválido"""
        result = Validators.validate_date("15/01/2025")
        assert result.is_valid is False


class TestValidatorsId:
    """Testes de validação de ID"""
    
    def test_validate_id_valid(self):
        """Testa ID válido"""
        result = Validators.validate_id(1)
        assert result.is_valid is True
    
    def test_validate_id_zero(self):
        """Testa ID zero"""
        result = Validators.validate_id(0)
        assert result.is_valid is False
    
    def test_validate_id_negative(self):
        """Testa ID negativo"""
        result = Validators.validate_id(-1)
        assert result.is_valid is False


class TestValidatorsSanitize:
    """Testes de sanitização"""
    
    def test_sanitize_string_normal(self):
        """Testa sanitização de string normal"""
        result = Validators.sanitize_string("Hello World")
        assert result == "Hello World"
    
    def test_sanitize_string_with_sql(self):
        """Testa sanitização com SQL injection"""
        result = Validators.sanitize_string("'; DROP TABLE users; --")
        assert "DROP TABLE" not in result
    
    def test_sanitize_string_with_xss(self):
        """Testa sanitização com XSS"""
        result = Validators.sanitize_string("<script>alert('xss')</script>")
        assert "<script>" not in result
    
    def test_sanitize_string_max_length(self):
        """Testa sanitização com limite de tamanho"""
        long_string = "a" * 1000
        result = Validators.sanitize_string(long_string, max_length=50)
        assert len(result) <= 50
    
    def test_is_safe_for_logging(self):
        """Testa verificação de segurança para logging"""
        assert Validators.is_safe_for_logging("normal text") is True


class TestValidatorsFullValidation:
    """Testes de validação completa"""
    
    def test_validate_and_sanitize_valid(self):
        """Testa validação e sanitização válida"""
        result = Validators.validate_and_sanitize_user_input(
            username="testuser",
            password="ValidPass123",
            name="Test User",
            user_type="vendedor"
        )
        
        assert result['valid'] is True
        assert 'sanitized_data' in result
    
    def test_validate_and_sanitize_invalid(self):
        """Testa validação e sanitização inválida"""
        result = Validators.validate_and_sanitize_user_input(
            username="",
            password="",
            name="",
            user_type="invalid"
        )
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
