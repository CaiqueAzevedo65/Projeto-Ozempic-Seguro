import customtkinter
from .views.tela_toque_view import TelaToqueFrame
from .views.tela_logo_view import TelaLogoFrame
from .views.iniciar_sessao_view import IniciarSessaoFrame
from .views.login_view import LoginFrame

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
        
        # Cache de frames
        self.frames = {}
        self.current_frame = None
        self.tela_index = 0
        self.telas = [self.show_tela_toque, self.show_tela_logo]
        
        # Pré-carregar frames comuns
        self.preload_frames()
        
        self.show_tela_toque()
        self.after_id = None
        self.start_alternancia()

    def preload_frames(self):
        """Pré-carrega os frames mais comuns para melhor performance"""
        self.frames['toque'] = TelaToqueFrame(self.container, on_click_callback=self.show_iniciar_sessao)
        self.frames['logo'] = TelaLogoFrame(self.container, on_click_callback=self.show_iniciar_sessao)
        self.frames['iniciar'] = IniciarSessaoFrame(self.container, show_login_callback=self.show_login)
        self.frames['login'] = LoginFrame(self.container, show_iniciar_callback=self.show_iniciar_sessao)
        
        # Esconde todos os frames inicialmente
        for frame in self.frames.values():
            frame.pack_forget()

    def show_frame(self, frame_name):
        """Mostra um frame com transição suave"""
        if self.current_frame:
            self.current_frame.pack_forget()
        
        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
            self.current_frame = frame
        else:
            print(f"Frame {frame_name} não encontrado no cache")

    def start_alternancia(self):
        self.after_id = self.after(2000, self.next_tela)

    def next_tela(self):
        self.tela_index = (self.tela_index + 1) % len(self.telas)
        self.telas[self.tela_index]()
        self.start_alternancia()

    def show_tela_toque(self):
        self.show_frame('toque')

    def show_tela_logo(self):
        self.show_frame('logo')

    def show_iniciar_sessao(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.show_frame('iniciar')

    def show_login(self):
        self.show_frame('login')

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 