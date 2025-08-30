"""
Módulo de validação robusta de entrada para prevenir ataques e garantir integridade dos dados.
"""
import re
import html
from typing import Optional, Dict, Any, List


class InputValidator:
    """Classe para validação e sanitização de entradas"""
    
    # Padrões de validação
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{2,50}$')
    NAME_PATTERN = re.compile(r'^[a-zA-ZÀ-ÿ\s]{2,100}$')
    PASSWORD_PATTERN = re.compile(r'^.{4,128}$')
    DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    TIME_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    
    # Lista de caracteres perigosos para SQL injection
    SQL_DANGEROUS_CHARS = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
    
    # Lista de tags HTML perigosas
    DANGEROUS_HTML_TAGS = ['script', 'iframe', 'object', 'embed', 'form', 'input', 'textarea']
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """
        Sanitiza string removendo caracteres perigosos
        
        Args:
            value: String a ser sanitizada
            max_length: Comprimento máximo permitido
            
        Returns:
            String sanitizada
        """
        if not isinstance(value, str):
            value = str(value)
            
        # Remove caracteres de controle
        value = ''.join(char for char in value if ord(char) >= 32)
        
        # Escape HTML
        value = html.escape(value)
        
        # Trunca se necessário
        if len(value) > max_length:
            value = value[:max_length]
            
        return value.strip()
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """
        Valida nome de usuário
        
        Args:
            username: Nome de usuário a ser validado
            
        Returns:
            Tuple (válido, mensagem_erro)
        """
        if not username or not isinstance(username, str):
            return False, "Nome de usuário é obrigatório"
            
        username = username.strip()
        
        if len(username) < 2:
            return False, "Nome de usuário deve ter pelo menos 2 caracteres"
            
        if len(username) > 50:
            return False, "Nome de usuário não pode ter mais de 50 caracteres"
            
        if not InputValidator.USERNAME_PATTERN.match(username):
            return False, "Nome de usuário deve conter apenas letras, números e underscore"
            
        # Verifica por padrões SQL injection
        username_upper = username.upper()
        for dangerous in InputValidator.SQL_DANGEROUS_CHARS:
            if dangerous.upper() in username_upper:
                return False, "Nome de usuário contém caracteres não permitidos"
                
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Valida senha
        
        Args:
            password: Senha a ser validada
            
        Returns:
            Tuple (válido, mensagem_erro)
        """
        if not password or not isinstance(password, str):
            return False, "Senha é obrigatória"
            
        if len(password) < 4:
            return False, "Senha deve ter pelo menos 4 caracteres"
            
        if len(password) > 128:
            return False, "Senha não pode ter mais de 128 caracteres"
            
        # Verifica caracteres de controle
        if any(ord(char) < 32 for char in password):
            return False, "Senha contém caracteres inválidos"
            
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> tuple[bool, str]:
        """
        Valida nome completo
        
        Args:
            name: Nome a ser validado
            
        Returns:
            Tuple (válido, mensagem_erro)
        """
        if not name or not isinstance(name, str):
            return False, "Nome é obrigatório"
            
        name = name.strip()
        
        if len(name) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
            
        if len(name) > 100:
            return False, "Nome não pode ter mais de 100 caracteres"
            
        if not InputValidator.NAME_PATTERN.match(name):
            return False, "Nome deve conter apenas letras e espaços"
            
        return True, ""
    
    @staticmethod
    def validate_user_type(user_type: str) -> tuple[bool, str]:
        """
        Valida tipo de usuário
        
        Args:
            user_type: Tipo de usuário a ser validado
            
        Returns:
            Tuple (válido, mensagem_erro)
        """
        valid_types = ['administrador', 'vendedor', 'repositor', 'tecnico']
        
        if not user_type or not isinstance(user_type, str):
            return False, "Tipo de usuário é obrigatório"
            
        user_type = user_type.lower().strip()
        
        if user_type not in valid_types:
            return False, f"Tipo de usuário deve ser um dos: {', '.join(valid_types)}"
            
        return True, ""
    
    @staticmethod
    def validate_date(date_str: str) -> tuple[bool, str]:
        """
        Valida formato de data
        
        Args:
            date_str: String de data a ser validada (YYYY-MM-DD)
            
        Returns:
            Tuple (válido, mensagem_erro)
        """
        if not date_str or not isinstance(date_str, str):
            return False, "Data é obrigatória"
            
        if not InputValidator.DATE_PATTERN.match(date_str):
            return False, "Data deve estar no formato YYYY-MM-DD"
            
        # Validação adicional de valores
        try:
            year, month, day = map(int, date_str.split('-'))
            
            if year < 1900 or year > 2100:
                return False, "Ano deve estar entre 1900 e 2100"
                
            if month < 1 or month > 12:
                return False, "Mês deve estar entre 1 e 12"
                
            if day < 1 or day > 31:
                return False, "Dia deve estar entre 1 e 31"
                
        except ValueError:
            return False, "Data contém valores inválidos"
            
        return True, ""
    
    @staticmethod
    def sanitize_sql_input(value: str) -> str:
        """
        Sanitiza entrada para prevenir SQL injection
        
        Args:
            value: Valor a ser sanitizado
            
        Returns:
            Valor sanitizado
        """
        if not isinstance(value, str):
            value = str(value)
            
        # Remove caracteres perigosos
        for dangerous in InputValidator.SQL_DANGEROUS_CHARS:
            value = value.replace(dangerous, '')
            
        return value.strip()
    
    @staticmethod
    def validate_and_sanitize_user_input(
        username: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        user_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Valida e sanitiza entrada completa de usuário
        
        Args:
            username: Nome de usuário
            password: Senha
            name: Nome completo
            user_type: Tipo de usuário
            
        Returns:
            Dict com resultado da validação
        """
        result = {
            'valid': True,
            'errors': [],
            'sanitized_data': {}
        }
        
        # Validar username
        if username is not None:
            valid, error = InputValidator.validate_username(username)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Usuário: {error}")
            else:
                result['sanitized_data']['username'] = InputValidator.sanitize_string(username, 50)
        
        # Validar password
        if password is not None:
            valid, error = InputValidator.validate_password(password)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Senha: {error}")
            else:
                result['sanitized_data']['password'] = password  # Senha não é sanitizada, apenas validada
        
        # Validar name
        if name is not None:
            valid, error = InputValidator.validate_name(name)
            if not valid:
                result['valid'] = False
                result['errors'].append(f"Nome: {error}")
            else:
                result['sanitized_data']['name'] = InputValidator.sanitize_string(name, 100)
        
        # Validar user_type
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
        """
        Verifica se um valor é seguro para ser logado
        
        Args:
            value: Valor a ser verificado
            
        Returns:
            True se seguro para log
        """
        if not isinstance(value, str):
            return True
            
        # Não loga senhas ou dados sensíveis
        sensitive_keywords = ['password', 'senha', 'token', 'secret', 'key']
        value_lower = value.lower()
        
        for keyword in sensitive_keywords:
            if keyword in value_lower:
                return False
                
        return True
