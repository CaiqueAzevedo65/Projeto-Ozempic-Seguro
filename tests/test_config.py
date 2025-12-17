"""
Testes para módulo de configuração.
"""
import pytest

from ozempic_seguro.config import (
    Config,
    SecurityConfig,
    DatabaseConfig,
    UIConfig,
    LoggingConfig,
    AppConfig,
    EnvironmentConfig,
    validate_config,
)


class TestSecurityConfig:
    """Testes para SecurityConfig"""
    
    def test_bcrypt_rounds_minimum(self):
        """Testa que BCRYPT_ROUNDS é pelo menos 10"""
        assert SecurityConfig.BCRYPT_ROUNDS >= 10
    
    def test_session_timeout_positive(self):
        """Testa que SESSION_TIMEOUT_MINUTES é positivo"""
        assert SecurityConfig.SESSION_TIMEOUT_MINUTES > 0
    
    def test_max_login_attempts_positive(self):
        """Testa que MAX_LOGIN_ATTEMPTS é positivo"""
        assert SecurityConfig.MAX_LOGIN_ATTEMPTS > 0
    
    def test_lockout_duration_positive(self):
        """Testa que LOCKOUT_DURATION_MINUTES é positivo"""
        assert SecurityConfig.LOCKOUT_DURATION_MINUTES > 0
    
    def test_password_length_constraints(self):
        """Testa constraints de tamanho de senha"""
        assert SecurityConfig.MIN_PASSWORD_LENGTH >= 4
        assert SecurityConfig.MAX_PASSWORD_LENGTH > SecurityConfig.MIN_PASSWORD_LENGTH
    
    def test_username_length_constraints(self):
        """Testa constraints de tamanho de username"""
        assert SecurityConfig.MIN_USERNAME_LENGTH >= 2
        assert SecurityConfig.MAX_USERNAME_LENGTH > SecurityConfig.MIN_USERNAME_LENGTH
    
    def test_valid_user_types(self):
        """Testa que tipos de usuário válidos estão definidos"""
        assert 'administrador' in SecurityConfig.VALID_USER_TYPES
        assert 'vendedor' in SecurityConfig.VALID_USER_TYPES
        assert 'repositor' in SecurityConfig.VALID_USER_TYPES
        assert 'tecnico' in SecurityConfig.VALID_USER_TYPES


class TestDatabaseConfig:
    """Testes para DatabaseConfig"""
    
    def test_db_name_defined(self):
        """Testa que nome do banco está definido"""
        assert DatabaseConfig.DB_NAME is not None
        assert len(DatabaseConfig.DB_NAME) > 0
    
    def test_db_timeout_positive(self):
        """Testa que timeout é positivo"""
        assert DatabaseConfig.DB_TIMEOUT > 0
    
    def test_cache_size_positive(self):
        """Testa que cache size é positivo"""
        assert DatabaseConfig.CACHE_SIZE > 0


class TestUIConfig:
    """Testes para UIConfig"""
    
    def test_window_dimensions_positive(self):
        """Testa que dimensões da janela são positivas"""
        assert UIConfig.WINDOW_WIDTH > 0
        assert UIConfig.WINDOW_HEIGHT > 0
        assert UIConfig.WINDOW_MIN_WIDTH > 0
        assert UIConfig.WINDOW_MIN_HEIGHT > 0
    
    def test_font_sizes_positive(self):
        """Testa que tamanhos de fonte são positivos"""
        assert UIConfig.FONT_SIZE > 0
        assert UIConfig.FONT_SIZE_SMALL > 0
        assert UIConfig.FONT_SIZE_LARGE > 0
    
    def test_login_layout_defined(self):
        """Testa que layout de login está definido"""
        assert UIConfig.LOGIN_FRAME_X >= 0
        assert UIConfig.LOGIN_FRAME_Y >= 0
        assert UIConfig.LOGIN_KEYBOARD_X >= 0
        assert UIConfig.LOGIN_KEYBOARD_Y >= 0
    
    def test_colors_defined(self):
        """Testa que cores estão definidas"""
        assert UIConfig.PRIMARY_BG_COLOR is not None
        assert UIConfig.SUCCESS_COLOR is not None
        assert UIConfig.ERROR_COLOR is not None
        assert UIConfig.WARNING_COLOR is not None


class TestLoggingConfig:
    """Testes para LoggingConfig"""
    
    def test_log_level_valid(self):
        """Testa que nível de log é válido"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert LoggingConfig.LOG_LEVEL in valid_levels
    
    def test_log_format_defined(self):
        """Testa que formato de log está definido"""
        assert LoggingConfig.LOG_FORMAT is not None
        assert len(LoggingConfig.LOG_FORMAT) > 0
    
    def test_log_file_max_size_positive(self):
        """Testa que tamanho máximo de arquivo é positivo"""
        assert LoggingConfig.LOG_FILE_MAX_SIZE > 0


class TestAppConfig:
    """Testes para AppConfig"""
    
    def test_app_name_defined(self):
        """Testa que nome da aplicação está definido"""
        assert AppConfig.APP_NAME is not None
        assert len(AppConfig.APP_NAME) > 0
    
    def test_app_version_format(self):
        """Testa que versão tem formato válido"""
        version = AppConfig.APP_VERSION
        assert version is not None
        # Versão deve ter pelo menos um ponto (ex: 1.0)
        assert '.' in version or version.isdigit()
    
    def test_directories_defined(self):
        """Testa que diretórios estão definidos"""
        assert AppConfig.DATA_DIR is not None
        assert AppConfig.LOGS_DIR is not None
        assert AppConfig.BACKUP_DIR is not None


class TestConfig:
    """Testes para classe Config agregadora"""
    
    def test_config_aggregates_all(self):
        """Testa que Config agrega todas as configurações"""
        assert Config.Security is SecurityConfig
        assert Config.Database is DatabaseConfig
        assert Config.UI is UIConfig
        assert Config.Logging is LoggingConfig
        assert Config.App is AppConfig
    
    def test_get_all_configs(self):
        """Testa obtenção de todas as configurações"""
        all_configs = Config.get_all_configs()
        
        assert isinstance(all_configs, dict)
        assert 'security' in all_configs
        assert 'database' in all_configs
        assert 'ui' in all_configs
        assert 'logging' in all_configs
        assert 'app' in all_configs
    
    def test_validate_configs_success(self):
        """Testa validação de configurações"""
        result = Config.validate_configs()
        assert result is True


class TestValidateConfig:
    """Testes para função validate_config"""
    
    def test_validate_config_success(self):
        """Testa que validate_config retorna True para configs válidas"""
        result = validate_config()
        assert result is True


class TestEnvironmentConfig:
    """Testes para EnvironmentConfig"""
    
    def test_is_development_returns_bool(self):
        """Testa que is_development retorna booleano"""
        result = EnvironmentConfig.is_development()
        assert isinstance(result, bool)
    
    def test_is_production_returns_bool(self):
        """Testa que is_production retorna booleano"""
        result = EnvironmentConfig.is_production()
        assert isinstance(result, bool)
    
    def test_is_development_and_production_exclusive(self):
        """Testa que development e production são mutuamente exclusivos"""
        is_dev = EnvironmentConfig.is_development()
        is_prod = EnvironmentConfig.is_production()
        assert is_dev != is_prod
    
    def test_get_config_returns_dict(self):
        """Testa que get_config retorna dicionário"""
        config = EnvironmentConfig.get_config()
        
        assert isinstance(config, dict)
        assert 'log_level' in config
        assert 'detailed_logging' in config
        assert 'session_timeout' in config
