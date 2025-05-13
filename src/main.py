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
        self.current_frame = None
        self.tela_index = 0
        self.telas = [self.show_tela_toque, self.show_tela_logo]
        self.show_tela_toque()
        self.after_id = None
        self.start_alternancia()

    def start_alternancia(self):
        self.after_id = self.after(2000, self.next_tela)  # alterna a cada 2 segundos

    def next_tela(self):
        self.tela_index = (self.tela_index + 1) % len(self.telas)
        self.telas[self.tela_index]()
        self.start_alternancia()

    def show_tela_toque(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TelaToqueFrame(self, on_click_callback=self.show_iniciar_sessao)

    def show_tela_logo(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TelaLogoFrame(self, on_click_callback=self.show_iniciar_sessao)

    def show_iniciar_sessao(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = IniciarSessaoFrame(self, show_login_callback=self.show_login)

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, show_iniciar_callback=self.show_iniciar_sessao)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 