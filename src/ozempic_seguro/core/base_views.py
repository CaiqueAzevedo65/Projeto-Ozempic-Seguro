"""
Classes base abstratas para eliminar código duplicado nas views
"""
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any, Dict
import customtkinter

from ..core.logger import logger, log_exceptions, log_method_call
from ..services.service_factory import ServiceFactory
from ..config import Config


class BaseView(customtkinter.CTkFrame, ABC):
    """Classe base abstrata para todas as views"""
    
    def __init__(self, master, **kwargs):
        # Configurações padrão do tema
        default_kwargs = {
            'fg_color': Config.UI.THEME_COLOR if hasattr(Config.UI, 'THEME_COLOR') else "#3B6A7D",
            'corner_radius': 0
        }
        default_kwargs.update(kwargs)
        
        super().__init__(master, **default_kwargs)
        
        # Logging
        logger.debug(f"Initializing view: {self.__class__.__name__}")
        
        # Hook para setup customizado
        self._setup_view()
    
    @abstractmethod
    def _setup_view(self) -> None:
        """Método abstrato para configuração específica da view"""
        pass
    
    @log_method_call(include_args=False)
    def pack_full_screen(self) -> None:
        """Pack padrão para ocupar tela inteira"""
        self.pack(fill="both", expand=True)
    
    @log_method_call(include_args=False)
    def destroy_safely(self) -> None:
        """Destrói a view de forma segura com logging"""
        try:
            logger.debug(f"Destroying view: {self.__class__.__name__}")
            self.destroy()
        except Exception as e:
            logger.error(f"Error destroying view {self.__class__.__name__}: {str(e)}")


class AdminView(BaseView):
    """Classe base para views administrativas"""
    
    def __init__(self, master, voltar_callback: Optional[Callable] = None, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, **kwargs)
        
        # Serviços comuns para views administrativas
        self._user_service = None
        self._audit_service = None
    
    @property
    def user_service(self):
        """Lazy loading do UserService"""
        if self._user_service is None:
            self._user_service = ServiceFactory.get_user_service()
        return self._user_service
    
    @property 
    def audit_service(self):
        """Lazy loading do AuditService"""
        if self._audit_service is None:
            self._audit_service = ServiceFactory.get_audit_service()
        return self._audit_service
    
    @log_exceptions("Admin View - Voltar Action")
    def handle_voltar(self) -> None:
        """Handler padrão para botão voltar"""
        if self.voltar_callback:
            logger.info(f"Voltar action triggered from {self.__class__.__name__}")
            self.voltar_callback()
        else:
            logger.warning(f"No voltar_callback defined for {self.__class__.__name__}")


class UserRoleView(BaseView):
    """Classe base para views específicas de papel do usuário (vendedor, repositor, etc.)"""
    
    def __init__(self, master, finalizar_sessao_callback: Optional[Callable] = None, **kwargs):
        self.finalizar_sessao_callback = finalizar_sessao_callback
        super().__init__(master, **kwargs)
        
        # Session manager comum
        self._session_manager = None
    
    @property
    def session_manager(self):
        """Lazy loading do SessionManager"""
        if self._session_manager is None:
            self._session_manager = ServiceFactory.get_session_manager()
        return self._session_manager
    
    @log_exceptions("User Role View - Finalizar Sessao")
    def handle_finalizar_sessao(self) -> None:
        """Handler padrão para finalizar sessão"""
        if self.finalizar_sessao_callback:
            logger.info(f"Session finalization triggered from {self.__class__.__name__}")
            self.finalizar_sessao_callback()
        else:
            logger.warning(f"No finalizar_sessao_callback defined for {self.__class__.__name__}")
    
    def _setup_view(self) -> None:
        """Setup padrão para views de papel de usuário"""
        self.pack_full_screen()


class InitialScreenView(BaseView):
    """Classe base para telas iniciais (logo, toque, etc.)"""
    
    def __init__(self, master, on_click_callback: Optional[Callable] = None, **kwargs):
        self.on_click_callback = on_click_callback
        
        # Override da cor padrão para telas iniciais
        default_kwargs = {'fg_color': 'white'}
        default_kwargs.update(kwargs)
        
        super().__init__(master, **default_kwargs)
    
    @log_exceptions("Initial Screen - Click Action")
    def handle_click(self) -> None:
        """Handler padrão para clique em telas iniciais"""
        if self.on_click_callback:
            logger.info(f"Click action triggered from {self.__class__.__name__}")
            self.on_click_callback()
        else:
            logger.warning(f"No on_click_callback defined for {self.__class__.__name__}")
    
    def _setup_view(self) -> None:
        """Setup padrão para telas iniciais"""
        self.pack_full_screen()


class BaseService(ABC):
    """Classe base abstrata para todos os serviços"""
    
    def __init__(self):
        self._database_manager = None
        self._logger = logger
        
        # Log da criação do serviço
        self._logger.info(f"Service created: {self.__class__.__name__}")
    
    @property
    def database_manager(self):
        """Lazy loading do DatabaseManager"""
        if self._database_manager is None:
            self._database_manager = ServiceFactory.get_database_manager()
        return self._database_manager
    
    @abstractmethod
    def _validate_input(self, *args, **kwargs) -> bool:
        """Método abstrato para validação de entrada"""
        pass
    
    @log_exceptions("Service Operation")
    def execute_with_logging(self, operation_name: str, operation_func: Callable, *args, **kwargs) -> Any:
        """
        Executa uma operação com logging automático
        
        Args:
            operation_name: Nome da operação para logging
            operation_func: Função a ser executada
            *args, **kwargs: Argumentos para a função
        
        Returns:
            Resultado da operação
        """
        self._logger.info(f"Starting operation: {operation_name} in {self.__class__.__name__}")
        
        try:
            result = operation_func(*args, **kwargs)
            self._logger.info(f"Operation completed successfully: {operation_name}")
            return result
        except Exception as e:
            self._logger.error(f"Operation failed: {operation_name} - {str(e)}")
            raise


class BaseRepository(ABC):
    """Classe base abstrata para todos os repositórios"""
    
    def __init__(self):
        self._database_manager = None
        self._logger = logger
        
        # Log da criação do repositório
        self._logger.debug(f"Repository created: {self.__class__.__name__}")
    
    @property
    def database_manager(self):
        """Lazy loading do DatabaseManager"""
        if self._database_manager is None:
            from ..repositories.database import DatabaseManager
            self._database_manager = DatabaseManager()
        return self._database_manager
    
    @abstractmethod
    def _validate_data(self, data: Dict[str, Any]) -> bool:
        """Método abstrato para validação de dados"""
        pass
    
    @log_exceptions("Repository Operation")
    def execute_query_with_logging(self, query_name: str, query_func: Callable, *args, **kwargs) -> Any:
        """
        Executa uma query com logging automático
        
        Args:
            query_name: Nome da query para logging
            query_func: Função de query a ser executada
            *args, **kwargs: Argumentos para a função
        
        Returns:
            Resultado da query
        """
        self._logger.debug(f"Executing query: {query_name} in {self.__class__.__name__}")
        
        try:
            result = query_func(*args, **kwargs)
            self._logger.debug(f"Query executed successfully: {query_name}")
            return result
        except Exception as e:
            self._logger.error(f"Query failed: {query_name} - {str(e)}")
            raise


class ConfigurableComponent(ABC):
    """Classe base para componentes configuráveis"""
    
    def __init__(self, config_section: str = None):
        self.config_section = config_section
        self._config = Config
        self._logger = logger
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração de forma segura
        
        Args:
            key: Chave da configuração
            default: Valor padrão se não encontrar
        
        Returns:
            Valor da configuração ou padrão
        """
        try:
            if self.config_section:
                section = getattr(self._config, self.config_section, None)
                if section:
                    return getattr(section, key, default)
            return default
        except Exception as e:
            self._logger.warning(f"Failed to get config value {key}: {str(e)}")
            return default
    
    def apply_theme_config(self, widget: customtkinter.CTkBaseClass) -> None:
        """Aplica configurações de tema a um widget"""
        try:
            # Aplicar configurações de tema se disponíveis
            theme_mode = self.get_config_value('THEME_MODE', 'dark')
            theme_color = self.get_config_value('THEME_COLOR', 'blue')
            
            if hasattr(widget, 'configure'):
                widget.configure(
                    fg_color=self.get_config_value('THEME_COLOR', '#3B6A7D')
                )
        except Exception as e:
            self._logger.debug(f"Could not apply theme config: {str(e)}")


# Mixin para funcionalidades comuns
class ValidatedMixin:
    """Mixin para adicionar funcionalidades de validação"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_validator = None
    
    @property
    def input_validator(self):
        """Lazy loading do InputValidator"""
        if self._input_validator is None:
            self._input_validator = ServiceFactory.get_input_validator()
        return self._input_validator
    
    def validate_user_input(self, input_data: Dict[str, Any]) -> bool:
        """Valida entrada do usuário usando o InputValidator"""
        try:
            return self.input_validator.validate_all_fields(input_data)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False


class AuditedMixin:
    """Mixin para adicionar funcionalidades de auditoria"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._security_logger = None
    
    @property
    def security_logger(self):
        """Lazy loading do SecurityLogger"""
        if self._security_logger is None:
            self._security_logger = ServiceFactory.get_security_logger()
        return self._security_logger
    
    def log_user_action(self, action: str, context: Dict[str, Any] = None) -> None:
        """Registra ação do usuário para auditoria"""
        try:
            self.security_logger.log_user_action(action, context or {})
        except Exception as e:
            logger.error(f"Failed to log user action: {str(e)}")
