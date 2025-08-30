import customtkinter
from .controllers.navigation_controller import NavigationController


class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ozempic Seguro")
        self.geometry("1000x600")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        
        # Container principal para todas as telas
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Controlador de navegação
        self.nav_controller = NavigationController(self)
        self.nav_controller.preload_frames()
        self.nav_controller.show_tela_toque()
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
            from .session import SessionManager
            session = SessionManager.get_instance()
            session.cleanup()
            
            # Destruir janela principal
            self.destroy()
            
            # Forçar encerramento se necessário
            import sys
            sys.exit(0)
            
        except Exception as e:
            print(f"Erro ao encerrar aplicação: {e}")
            # Forçar encerramento mesmo com erro
            import sys
            sys.exit(1)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()