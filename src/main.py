import customtkinter
from .views.pages_iniciais.tela_toque_view import TelaToqueFrame
from .views.pages_iniciais.tela_logo_view import TelaLogoFrame
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
        
        # Dicionário para armazenar os frames
        self.frames = {}
        self.current_frame = None
        self.tela_index = 0
        
        # Lista de métodos para alternar entre telas
        self.telas = [self.show_tela_toque, self.show_tela_logo]
        
        # Carrega os frames iniciais
        self.preload_frames()
        
        # Inicia com a primeira tela
        self.show_tela_toque()
        self.after_id = None
        self.start_alternancia()

    def preload_frames(self):
        # Carrega os frames iniciais
        self.frames['toque'] = TelaToqueFrame(
            self.container, 
            on_click_callback=self.show_iniciar_sessao
        )
        self.frames['logo'] = TelaLogoFrame(
            self.container, 
            on_click_callback=self.show_iniciar_sessao
        )
        self.frames['iniciar'] = IniciarSessaoFrame(
            self.container, 
            show_login_callback=self.show_login,
            voltar_callback=self.voltar_para_tela_inicial
        )
        self.frames['login'] = LoginFrame(
            self.container, 
            show_iniciar_callback=self.show_iniciar_sessao
        )
        
        # Esconde todos os frames inicialmente
        for frame in self.frames.values():
            frame.pack_forget()

    def show_frame(self, frame_name):
        """Mostra um frame, criando-o se não existir"""
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Verifica se o frame já existe e está válido
        if frame_name not in self.frames or not hasattr(self.frames[frame_name], 'winfo_exists') or not self.frames[frame_name].winfo_exists():
            # Recria o frame se não existir ou não for válido
            if frame_name == 'toque':
                self.frames[frame_name] = TelaToqueFrame(
                    self.container, 
                    on_click_callback=self.show_iniciar_sessao
                )
            elif frame_name == 'logo':
                self.frames[frame_name] = TelaLogoFrame(
                    self.container, 
                    on_click_callback=self.show_iniciar_sessao
                )
            elif frame_name == 'iniciar':
                self.frames[frame_name] = IniciarSessaoFrame(
                    self.container,
                    show_login_callback=self.show_login,
                    voltar_callback=self.voltar_para_tela_inicial
                )
            elif frame_name == 'login':
                self.frames[frame_name] = LoginFrame(
                    self.container,
                    show_iniciar_callback=self.show_iniciar_sessao
                )
        
        # Mostra o frame
        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
            self.current_frame = frame
            return True
        return False

    def start_alternancia(self):
        """Inicia a alternância entre as telas iniciais"""
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(2000, self.next_tela)

    def next_tela(self):
        """Vai para a próxima tela na sequência"""
        if not hasattr(self, 'telas') or not self.telas:
            return
            
        self.tela_index = (self.tela_index + 1) % len(self.telas)
        if self.tela_index < len(self.telas):
            self.telas[self.tela_index]()
        self.start_alternancia()

    def voltar_para_tela_inicial(self):
        """Volta para a tela inicial"""
        if self.after_id:
            self.after_cancel(self.after_id)
        
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Mostra a tela de toque e reinicia a alternância
        self.show_tela_toque()
        self.start_alternancia()

    def show_tela_toque(self):
        """Mostra a tela de toque"""
        self.show_frame('toque')

    def show_tela_logo(self):
        """Mostra a tela do logo"""
        self.show_frame('logo')

    def show_iniciar_sessao(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        
        # Recria o frame de iniciar sessão se ele não existir mais
        if 'iniciar' not in self.frames or not self.frames['iniciar'].winfo_exists():
            self.frames['iniciar'] = IniciarSessaoFrame(
                self.container, 
                show_login_callback=self.show_login,
                voltar_callback=self.voltar_para_tela_inicial
            )
        
        self.show_frame('iniciar')

    def show_login(self):
        # Limpa a sessão atual
        from src.session_manager import SessionManager
        session_manager = SessionManager.get_instance()
        session_manager.set_current_user(None)
        
        # Mostra a tela de login e limpa os campos
        if 'login' in self.frames and self.frames['login'].winfo_exists():
            # Limpa os campos do login
            self.frames['login'].usuario_entry.delete(0, 'end')
            self.frames['login'].senha_entry.delete(0, 'end')
        else:
            # Recria o frame de login se ele não existir mais
            self.frames['login'] = LoginFrame(
                self.container, 
                show_iniciar_callback=self.show_iniciar_sessao
            )
        
        self.show_frame('login')

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 