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

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()