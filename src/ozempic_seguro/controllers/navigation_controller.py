import customtkinter
from ..views.pages_iniciais.tela_toque_view import TelaToqueFrame
from ..views.pages_iniciais.tela_logo_view import TelaLogoFrame
from ..views.iniciar_sessao_view import IniciarSessaoFrame
from ..views.login_view import LoginFrame
from ..session.session_manager import SessionManager
from ..core.logger import logger


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
        self._transitioning = False

        # Overlay para transições suaves
        self._transition_overlay = customtkinter.CTkFrame(self.container, fg_color="#3B6A7D")

    def preload_frames(self):
        """Pré-carrega os frames iniciais de forma invisível"""
        # Criar frames e renderizar fora da tela visível
        self.frames["toque"] = TelaToqueFrame(
            self.container, on_click_callback=self.show_iniciar_sessao
        )
        self._prerender_frame(self.frames["toque"])

        self.frames["logo"] = TelaLogoFrame(
            self.container, on_click_callback=self.show_iniciar_sessao
        )
        self._prerender_frame(self.frames["logo"])

        self.frames["iniciar"] = IniciarSessaoFrame(
            self.container,
            show_login_callback=self.show_login,
            voltar_callback=self.voltar_para_tela_inicial,
        )
        self._prerender_frame(self.frames["iniciar"])

        self.frames["login"] = LoginFrame(
            self.container, show_iniciar_callback=self.show_iniciar_sessao
        )
        self._prerender_frame(self.frames["login"])

    def _prerender_frame(self, frame):
        """Pré-renderiza um frame de forma invisível"""
        # Posicionar fora da tela para renderizar sem mostrar
        frame.place(x=-9999, y=-9999)
        self.app.update_idletasks()
        frame.place_forget()

    def show_frame(self, frame_name, animate=True):
        """Mostra um frame específico com transição suave"""
        if self._transitioning:
            return False

        # Verificar se precisa criar o frame
        needs_creation = (
            frame_name not in self.frames
            or not hasattr(self.frames[frame_name], "winfo_exists")
            or not self.frames[frame_name].winfo_exists()
        )

        if needs_creation:
            self._create_frame(frame_name)

        frame = self.frames.get(frame_name)
        if not frame:
            return False

        # Se é o mesmo frame, não fazer nada
        if self.current_frame == frame:
            return True

        self._transitioning = True
        old_frame = self.current_frame

        # 1. Mostrar overlay cobrindo tudo
        self._transition_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._transition_overlay.lift()
        self.app.update_idletasks()

        # 2. Esconder frame antigo
        if old_frame:
            old_frame.place_forget()
            old_frame.pack_forget()

        # 3. Posicionar novo frame
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.app.update_idletasks()

        # 4. Trazer novo frame para frente e esconder overlay
        frame.lift()
        self._transition_overlay.place_forget()

        self.current_frame = frame
        self._transitioning = False
        return True

    def _create_frame(self, frame_name):
        """Cria um frame específico"""
        if frame_name == "toque":
            self.frames[frame_name] = TelaToqueFrame(
                self.container, on_click_callback=self.show_iniciar_sessao
            )
        elif frame_name == "logo":
            self.frames[frame_name] = TelaLogoFrame(
                self.container, on_click_callback=self.show_iniciar_sessao
            )
        elif frame_name == "iniciar":
            self.frames[frame_name] = IniciarSessaoFrame(
                self.container,
                show_login_callback=self.show_login,
                voltar_callback=self.voltar_para_tela_inicial,
            )
        elif frame_name == "login":
            self.frames[frame_name] = LoginFrame(
                self.container, show_iniciar_callback=self.show_iniciar_sessao
            )

        self.app.update_idletasks()

    def voltar_para_tela_inicial(self):
        if self.after_id:
            self.app.after_cancel(self.after_id)
        if self.current_frame:
            self.current_frame.pack_forget()
        self.show_tela_toque()
        self.start_alternancia()

    def show_tela_toque(self):
        self.show_frame("toque")

    def show_tela_logo(self):
        self.show_frame("logo")

    def show_iniciar_sessao(self):
        if self.after_id:
            self.app.after_cancel(self.after_id)
        if "iniciar" not in self.frames or not self.frames["iniciar"].winfo_exists():
            self.frames["iniciar"] = IniciarSessaoFrame(
                self.container,
                show_login_callback=self.show_login,
                voltar_callback=self.voltar_para_tela_inicial,
            )
        self.show_frame("iniciar")

    def show_login(self):
        # Limpa a sessão atual
        session_manager = SessionManager.get_instance()
        session_manager.set_current_user(None)

        # Limpa campos do login
        if "login" in self.frames and self.frames["login"].winfo_exists():
            self.frames["login"].usuario_entry.delete(0, "end")
            self.frames["login"].senha_entry.delete(0, "end")
        else:
            self.frames["login"] = LoginFrame(
                self.container, show_iniciar_callback=self.show_iniciar_sessao
            )
        self.show_frame("login")

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
                    if frame and hasattr(frame, "winfo_exists") and frame.winfo_exists():
                        frame.destroy()
                except Exception as e:
                    logger.warning(f"Erro ao destruir frame {frame_name}: {e}")

            # Limpar dicionário de frames
            self.frames.clear()
            self.current_frame = None

        except Exception as e:
            logger.error(f"Erro durante cleanup do NavigationController: {e}")
