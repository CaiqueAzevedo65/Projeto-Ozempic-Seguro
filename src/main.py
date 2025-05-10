import customtkinter
from views.login_view import LoginFrame
from views.iniciar_sessao_view import IniciarSessaoFrame

class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ozempic Seguro")
        self.geometry("1000x600")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.current_frame = None
        self.show_iniciar_sessao()

    def show_iniciar_sessao(self):
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