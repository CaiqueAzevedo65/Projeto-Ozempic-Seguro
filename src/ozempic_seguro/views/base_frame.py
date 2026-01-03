"""
BaseFrameView - Classe base para frames com transição suave
"""
import customtkinter
from .components import Header, FinalizarSessaoButton, ModernConfirmDialog, ToastNotification


class BaseFrameView(customtkinter.CTkFrame):
    """
    Classe base para views que precisam de:
    - Transição suave entre telas internas
    - Header padrão
    - Botão de finalizar sessão
    """

    # Cor de fundo padrão - pode ser sobrescrita
    BG_COLOR = "#3B6A7D"

    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color=self.BG_COLOR, *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self._master = master

        # Criar overlay para esconder construção
        self._init_overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._init_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._init_overlay.lift()
        master.update_idletasks()

        self.pack(fill="both", expand=True)

        # Agendar remoção do overlay após inicialização completa
        self.after(1, self._hide_init_overlay)

    def _hide_init_overlay(self):
        """Remove o overlay de inicialização após a tela estar pronta"""
        if self._init_overlay:
            self.update_idletasks()
            self._init_overlay.destroy()
            self._init_overlay = None

    def _transicao_tela(self, criar_frame_func):
        """
        Executa transição suave entre telas internas.
        Usa overlay para esconder renderização de componentes.

        Args:
            criar_frame_func: Função que cria o novo frame/conteúdo
        """
        # Criar overlay para esconder renderização
        overlay = customtkinter.CTkFrame(self, fg_color=self.BG_COLOR)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.update()

        # Destruir widgets antigos (exceto overlay)
        for widget in self.winfo_children():
            if widget != overlay:
                widget.destroy()

        # Criar novo conteúdo
        criar_frame_func()

        # Forçar renderização completa
        self.update_idletasks()

        # Remover overlay
        overlay.destroy()

    def criar_header(self, titulo: str):
        """Cria header padrão com título"""
        Header(self, titulo)

    def criar_botao_finalizar(self):
        """Cria botão de finalizar sessão padrão"""
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        """Lógica padrão de finalização de sessão com confirmação"""
        if ModernConfirmDialog.ask(
            self,
            "Finalizar Sessão",
            "Tem certeza que deseja sair do sistema?",
            icon="question",
            confirm_text="Sair",
            cancel_text="Cancelar",
        ):
            ToastNotification.show(self, "Sessão finalizada com sucesso", "success")
            if self.finalizar_sessao_callback:
                self.after(1000, self._execute_logout)

    def _execute_logout(self):
        """Executa o logout após delay da notificação"""
        self.pack_forget()
        if self.finalizar_sessao_callback:
            self.finalizar_sessao_callback()
