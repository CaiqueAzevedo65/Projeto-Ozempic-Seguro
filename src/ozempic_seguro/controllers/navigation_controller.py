import customtkinter
from ..views.pages_iniciais.tela_toque_view import TelaToqueFrame
from ..views.pages_iniciais.tela_logo_view import TelaLogoFrame
from ..views.iniciar_sessao_view import IniciarSessaoFrame
from ..views.login_view import LoginFrame
from ..session import SessionManager


class NavigationController:
    def __init__(self, app):
        self.app = app
        self.container = app.container
        self.frames = {}
        self.current_frame = None
        self.tela_index = 0
        self.telas = [self.show_tela_toque, self.show_tela_logo]
        self.after_id = None
        self.is_running = True

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
        if self.current_frame:
            self.current_frame.pack_forget()

        if frame_name not in self.frames or not hasattr(self.frames[frame_name], 'winfo_exists') \
           or not self.frames[frame_name].winfo_exists():
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

        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
            self.current_frame = frame
            return True
        return False

    def start_alternancia(self):
        if self.after_id:
            self.app.after_cancel(self.after_id)
        self.after_id = self.app.after(2000, self.next_tela)

    def next_tela(self):
        if not self.telas:
            return
        self.tela_index = (self.tela_index + 1) % len(self.telas)
        self.telas[self.tela_index]()
        self.start_alternancia()

    def voltar_para_tela_inicial(self):
        if self.after_id:
            self.app.after_cancel(self.after_id)
        if self.current_frame:
            self.current_frame.pack_forget()
        self.show_tela_toque()
        self.start_alternancia()

    def show_tela_toque(self):
        self.show_frame('toque')

    def show_tela_logo(self):
        self.show_frame('logo')

    def show_iniciar_sessao(self):
        if self.after_id:
            self.app.after_cancel(self.after_id)
        if 'iniciar' not in self.frames or not self.frames['iniciar'].winfo_exists():
            self.frames['iniciar'] = IniciarSessaoFrame(
                self.container,
                show_login_callback=self.show_login,
                voltar_callback=self.voltar_para_tela_inicial
            )
        self.show_frame('iniciar')

    def show_login(self):
        # Limpa a sessão atual
        session_manager = SessionManager.get_instance()
        session_manager.set_current_user(None)

        # Limpa campos do login
        if 'login' in self.frames and self.frames['login'].winfo_exists():
            self.frames['login'].usuario_entry.delete(0, 'end')
            self.frames['login'].senha_entry.delete(0, 'end')
        else:
            self.frames['login'] = LoginFrame(
                self.container,
                show_iniciar_callback=self.show_iniciar_sessao
            )
        self.show_frame('login')
    
    def start_alternancia(self):
        """Inicia a alternância entre telas"""
        if self.is_running and len(self.telas) > 1:
            self.after_id = self.app.after(3000, self.alternar_tela)
    
    def alternar_tela(self):
        """Alterna entre as telas automaticamente"""
        if not self.is_running:
            return
            
        self.tela_index = (self.tela_index + 1) % len(self.telas)
        self.telas[self.tela_index]()
        
        # Agenda próxima alternância
        if self.is_running:
            self.after_id = self.app.after(3000, self.alternar_tela)
    
    def cleanup(self):
        """Limpa recursos quando a aplicação é encerrada"""
        try:
            # Parar alternância de telas
            self.is_running = False
            
            # Cancelar timer pendente
            if self.after_id:
                self.app.after_cancel(self.after_id)
                self.after_id = None
            
            # Destruir frames se existirem
            for frame_name, frame in self.frames.items():
                try:
                    if frame and hasattr(frame, 'winfo_exists') and frame.winfo_exists():
                        frame.destroy()
                except Exception as e:
                    print(f"Erro ao destruir frame {frame_name}: {e}")
            
            # Limpar dicionário de frames
            self.frames.clear()
            self.current_frame = None
            
        except Exception as e:
            print(f"Erro durante cleanup do NavigationController: {e}")
