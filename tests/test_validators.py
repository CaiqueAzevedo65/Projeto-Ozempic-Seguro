"""
Testes para o sistema centralizado de validação.
"""
import pytest
from ozempic_seguro.core.validators import Validators, ValidationResult, UserType


class TestValidators:
    """Testes para validadores centralizados"""
    
    def test_validate_username_valid(self):
        """Testa validação de username válido"""
        result = Validators.validate_username("user_123")
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.sanitized_value is not None
    
    def test_validate_username_too_short(self):
        """Testa username muito curto"""
        result = Validators.validate_username("u")
        assert result.is_valid is False
        assert "pelo menos 2 caracteres" in result.errors[0]
    
    def test_validate_username_too_long(self):
        """Testa username muito longo"""
        result = Validators.validate_username("a" * 51)
        assert result.is_valid is False
        assert "mais de 50 caracteres" in result.errors[0]
    
    def test_validate_username_invalid_chars(self):
        """Testa username com caracteres inválidos"""
        result = Validators.validate_username("user@123")
        assert result.is_valid is False
        assert "letras, números e underscore" in result.errors[0]
    
    def test_validate_password_strong(self):
        """Testa senha forte"""
        result = Validators.validate_password("StrongPass123")
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_password_weak(self):
        """Testa senha fraca"""
        result = Validators.validate_password("weak")
        assert result.is_valid is False
        assert "pelo menos 8 caracteres" in result.errors[0]
    
    def test_validate_password_no_uppercase(self):
        """Testa senha sem maiúscula"""
        result = Validators.validate_password("weakpass123")
        assert result.is_valid is False
        assert "letra maiúscula" in result.errors[0]
    
    def test_validate_password_no_lowercase(self):
        """Testa senha sem minúscula"""
        result = Validators.validate_password("WEAKPASS123")
        assert result.is_valid is False
        assert "letra minúscula" in result.errors[0]
    
    def test_validate_password_no_digit(self):
        """Testa senha sem número"""
        result = Validators.validate_password("WeakPassword")
        assert result.is_valid is False
        assert "um número" in result.errors[0]
    
    def test_validate_name_valid(self):
        """Testa nome válido"""
        result = Validators.validate_name("João da Silva")
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_name_single_word(self):
        """Testa nome com apenas uma palavra"""
        result = Validators.validate_name("João")
        assert result.is_valid is False
        assert "nome e sobrenome" in result.errors[0]
    
    def test_validate_name_with_special_chars(self):
        """Testa nome com caracteres especiais válidos"""
        result = Validators.validate_name("Jean-Pierre D'Alembert")
        assert result.is_valid is True
    
    def test_validate_user_type_valid(self):
        """Testa tipo de usuário válido"""
        for user_type in ["administrador", "vendedor", "repositor", "tecnico"]:
            result = Validators.validate_user_type(user_type)
            assert result.is_valid is True
            assert result.sanitized_value == user_type
    
    def test_validate_user_type_invalid(self):
        """Testa tipo de usuário inválido"""
        result = Validators.validate_user_type("gerente")
        assert result.is_valid is False
        assert "deve ser um dos" in result.errors[0]
    
    def test_validate_email_valid(self):
        """Testa email válido"""
        result = Validators.validate_email("user@example.com")
        assert result.is_valid is True
        assert result.sanitized_value == "user@example.com"
    
    def test_validate_email_invalid(self):
        """Testa email inválido"""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
            "user example@test.com"
        ]
        
        for email in invalid_emails:
            result = Validators.validate_email(email)
            assert result.is_valid is False
    
    def test_validate_phone_valid(self):
        """Testa telefone válido"""
        valid_phones = [
            "(11) 98765-4321",
            "11987654321",
            "+55 11 98765-4321"
        ]
        
        for phone in valid_phones:
            result = Validators.validate_phone(phone)
            assert result.is_valid is True
            # Verifica se foi sanitizado para apenas números
            assert result.sanitized_value.isdigit()
    
    def test_validate_date_valid(self):
        """Testa data válida"""
        result = Validators.validate_date("2024-12-25")
        assert result.is_valid is True
        assert result.sanitized_value == "2024-12-25"
    
    def test_validate_date_invalid_format(self):
        """Testa data com formato inválido"""
        invalid_dates = [
            "25/12/2024",
            "2024-13-01",  # Mês inválido
            "2024-12-32",  # Dia inválido
            "24-12-25"     # Ano com 2 dígitos
        ]
        
        for date in invalid_dates:
            result = Validators.validate_date(date)
            assert result.is_valid is False
    
    def test_sanitize_string_removes_dangerous(self):
        """Testa sanitização de strings perigosas"""
        dangerous = "<script>alert('XSS')</script>"
        sanitized = Validators.sanitize_string(dangerous)
        
        assert "<script>" not in sanitized
        assert "alert" in sanitized  # Conteúdo preservado mas escapado
        assert "&lt;script&gt;" in sanitized  # HTML escapado
    
    def test_sanitize_string_sql_injection(self):
        """Testa sanitização contra SQL injection"""
        dangerous = "'; DROP TABLE users; --"
        sanitized = Validators.sanitize_string(dangerous)
        
        assert "DROP TABLE" not in sanitized
        assert "--" not in sanitized
    
    def test_is_safe_for_logging(self):
        """Testa detecção de dados sensíveis para logs"""
        # Dados sensíveis
        assert Validators.is_safe_for_logging("password123") is False
        assert Validators.is_safe_for_logging("my_secret_token") is False
        assert Validators.is_safe_for_logging("api_key_xyz") is False
        
        # Dados seguros
        assert Validators.is_safe_for_logging("username") is True
        assert Validators.is_safe_for_logging("João Silva") is True
        assert Validators.is_safe_for_logging(123) is True
    
    def test_validate_id_valid(self):
        """Testa validação de ID válido"""
        result = Validators.validate_id(42)
        assert result.is_valid is True
        assert result.sanitized_value == 42
        
        # String que pode ser convertida
        result = Validators.validate_id("123")
        assert result.is_valid is True
        assert result.sanitized_value == 123
    
    def test_validate_id_invalid(self):
        """Testa validação de ID inválido"""
        invalid_ids = [0, -1, "abc", None, ""]
        
        for id_val in invalid_ids:
            result = Validators.validate_id(id_val)
            assert result.is_valid is False
    
    def test_validate_batch(self):
        """Testa validação em lote"""
        results = Validators.validate_batch({
            'username': ("valid_user", Validators.validate_username),
            'password': ("WeakPass123", Validators.validate_password),
            'email': ("user@test.com", Validators.validate_email)
        })
        
        assert 'username' in results
        assert 'password' in results
        assert 'email' in results
        
        assert results['username'].is_valid is True
        assert results['password'].is_valid is True
        assert results['email'].is_valid is True
    
    def test_get_all_errors(self):
        """Testa extração de todos os erros"""
        results = {
            'username': ValidationResult(is_valid=False, errors=["Username inválido"]),
            'password': ValidationResult(is_valid=False, errors=["Senha fraca", "Sem números"]),
            'email': ValidationResult(is_valid=True, errors=[])
        }
        
        errors = Validators.get_all_errors(results)
        
        assert len(errors) == 3
        assert "username: Username inválido" in errors
        assert "password: Senha fraca" in errors
        assert "password: Sem números" in errors
    
    def test_all_valid(self):
        """Testa verificação se todos são válidos"""
        # Todos válidos
        results = {
            'field1': ValidationResult(is_valid=True, errors=[]),
            'field2': ValidationResult(is_valid=True, errors=[])
        }
        assert Validators.all_valid(results) is True
        
        # Um inválido
        results['field3'] = ValidationResult(is_valid=False, errors=["Erro"])
        assert Validators.all_valid(results) is False
