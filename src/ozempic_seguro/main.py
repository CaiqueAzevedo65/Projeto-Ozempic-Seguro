"""
Módulo principal da aplicação Ozempic Seguro.

Inicializa a interface gráfica e configura os componentes do sistema.
"""
import customtkinter
from .controllers.navigation_controller import NavigationController
from .core.logger import logger


def _preload_images() -> None:
    """Pré-carrega imagens para acelerar a renderização das telas"""
    from .views.components.common import ImageCache
    from .views.components.gavetas import _GavetaImageCache
    
    # Pré-carregar imagens do header
    ImageCache.get_logo()
    ImageCache.get_digital()
    
    # Pré-carregar imagens das gavetas
    _GavetaImageCache.get_gaveta_aberta()
    _GavetaImageCache.get_gaveta_fechada()


def _setup_audit_callback() -> None:
    """Configura callback de auditoria para SessionManager (evita import circular)"""
    from .session.session_manager import SessionManager
    from .services.audit_service import AuditService
    
    audit_service = AuditService()
    
    def audit_callback(user_id: int, acao: str, tabela: str, dados: dict) -> None:
        audit_service.create_log(
            usuario_id=user_id,
            acao=acao,
            tabela_afetada=tabela,
            dados_anteriores=dados
        )
    
    SessionManager.set_audit_callback(audit_callback)


class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        from .config import UIConfig, AppConfig
        
        # Esconder janela durante inicialização
        self.withdraw()
        
        # Pré-carregar imagens para acelerar renderização
        _preload_images()
        
        # Configura callback de auditoria primeiro
        _setup_audit_callback()
        
        self.title(AppConfig.APP_NAME)
        self.geometry(f"{UIConfig.WINDOW_WIDTH}x{UIConfig.WINDOW_HEIGHT}")
        self.minsize(UIConfig.WINDOW_MIN_WIDTH, UIConfig.WINDOW_MIN_HEIGHT)
        customtkinter.set_appearance_mode(UIConfig.THEME_MODE)
        customtkinter.set_default_color_theme(UIConfig.THEME_COLOR)
        
        # Container principal para todas as telas
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Controlador de navegação - inicialização direta
        self.nav_controller = NavigationController(self)
        self.nav_controller.preload_frames()
        self.nav_controller.show_tela_toque()
        
        # Forçar renderização completa antes de mostrar
        self.update_idletasks()
        self.update()
        
        # Mostrar janela após tudo estar pronto
        self.deiconify()
        
        self.nav_controller.start_alternancia()
        
        # Configurar encerramento adequado da aplicação
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Encerra a aplicação de forma adequada, limpando todos os recursos"""
        try:
            # Parar navegação controller se existir
            if hasattr(self, 'nav_controller') and self.nav_controller:
                self.nav_controller.cleanup()
            
            # Limpar session manager
            from .session.session_manager import SessionManager
            session = SessionManager.get_instance()
            session.cleanup()
            
            # Destruir janela principal
            self.destroy()
            
            # Forçar encerramento se necessário
            import sys
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Erro ao encerrar aplicação: {e}")
            # Forçar encerramento mesmo com erro
            import sys
            sys.exit(1)

def main():
    """Função principal para iniciar a aplicação"""
    try:
        app = MainApp()
        app.mainloop()
    except KeyboardInterrupt:
        # Encerramento via Ctrl+C ou fechamento abrupto
        pass
    except Exception as e:
        logger.error(f"Erro fatal na aplicação: {e}")

if __name__ == "__main__":
    main()