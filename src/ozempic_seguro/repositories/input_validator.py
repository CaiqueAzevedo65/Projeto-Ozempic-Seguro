"""
Módulo de validação robusta de entrada para prevenir ataques e garantir integridade dos dados.

Este módulo delega para core.validators para evitar duplicação de código.
Mantido para compatibilidade com código existente.
"""
from typing import Optional, Dict, Any, Tuple

from ..core.validators import Validators


class InputValidator:
    """
    Classe para validação e sanitização de entradas.
    Delega para core.validators para implementação centralizada.
    """
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Sanitiza string removendo caracteres perigosos"""
        return Validators.sanitize_string(value, max_length)
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Valida nome de usuário"""
        result = Validators.validate_username(username)
        if result.is_valid:
            return True, ""
        return False, result.errors[0] if result.errors else "Usuário inválido"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Valida senha (validação básica para compatibilidade).
        Usa regras simplificadas: 4-128 caracteres.
        """
        if not password or not isinstance(password, str):
            return False, "Senha é obrigatória"
        if len(password) < 4:
            return False, "Senha deve ter pelo menos 4 caracteres"
        if len(password) > 128:
            return False, "Senha não pode ter mais de 128 caracteres"
        if any(ord(char) < 32 for char in password):
            return False, "Senha contém caracteres inválidos"
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Valida nome completo (sem exigir sobrenome para compatibilidade)"""
        if not name or not isinstance(name, str):
            return False, "Nome é obrigatório"
        name = name.strip()
        if len(name) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
        if len(name) > 100:
            return False, "Nome não pode ter mais de 100 caracteres"
        # Permite apenas letras, espaços e acentos
        import re
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]{2,100}$', name):
            return False, "Nome deve conter apenas letras e espaços"
        return True, ""
    
    @staticmethod
    def validate_user_type(user_type: str) -> Tuple[bool, str]:
        """Valida tipo de usuário"""
        result = Validators.validate_user_type(user_type)
        if result.is_valid:
            return True, ""
        return False, result.errors[0] if result.errors else "Tipo inválido"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Valida formato de data (YYYY-MM-DD)"""
        result = Validators.validate_date(date_str)
        if result.is_valid:
            return True, ""
        return False, result.errors[0] if result.errors else "Data inválida"
    
    @staticmethod
    def sanitize_sql_input(value: str) -> str:
        """Sanitiza entrada para prevenir SQL injection"""
        return Validators.sanitize_string(value)
    
    @staticmethod
    def validate_and_sanitize_user_input(
        username: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        user_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Valida e sanitiza entrada completa de usuário"""
        result = {
            'valid': True,
            'errors': [],
            'sanitized_data': {}
        }
        
        if username is not None:
            valid, error = InputValidator.validate_username(username)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Usuário: {error}")
            else:
                result['sanitized_data']['username'] = InputValidator.sanitize_string(username, 50)
        
        if password is not None:
            valid, error = InputValidator.validate_password(password)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Senha: {error}")
            else:
                result['sanitized_data']['password'] = password
        
        if name is not None:
            valid, error = InputValidator.validate_name(name)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Nome: {error}")
            else:
                result['sanitized_data']['name'] = InputValidator.sanitize_string(name, 100)
        
        if user_type is not None:
            valid, error = InputValidator.validate_user_type(user_type)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Tipo: {error}")
            else:
                result['sanitized_data']['user_type'] = user_type.lower().strip()
        
        return result
    
    @staticmethod
    def is_safe_for_logging(value: str) -> bool:
        """Verifica se um valor é seguro para ser logado"""
        return Validators.is_safe_for_logging(value)
