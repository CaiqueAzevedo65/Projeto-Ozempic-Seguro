"""
View base para usuários operacionais (vendedor/repositor).

Extrai código comum para reduzir duplicação.
"""
import customtkinter
from tkinter import messagebox
from .components import (
    Header,
    FinalizarSessaoButton,
    GavetaButtonGrid,
    GavetaButton,
    ModernConfirmDialog,
    ToastNotification,
)


class BaseUserFrame(customtkinter.CTkFrame):
    """
    Frame base para views de usuários operacionais.

    Subclasses devem definir:
        - TITULO: str - título exibido no header
        - TIPO_USUARIO: str - tipo de usuário para permissões
    """

    BG_COLOR = "#3B6A7D"
    TITULO: str = ""
    TIPO_USUARIO: str = ""

    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color=self.BG_COLOR, *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback

        # Criar overlay para esconder construção
        self._overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.lift()
        master.update_idletasks()

        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_grade_botoes()
        self.criar_botao_finalizar()

        # Remover overlay após tudo estar pronto
        self.update_idletasks()
        self._overlay.destroy()

    def criar_topo(self):
        Header(self, self.TITULO)

    def criar_grade_botoes(self):
        button_data = []
        # Criar 15 gavetas para testar a paginação
        for i in range(1, 16):
            gaveta_id = f"100{i}"
            button_data.append(
                {
                    "text": gaveta_id,
                    "command": lambda x=gaveta_id: self.mostrar_historico_gaveta(x),
                    "name": "gaveta_black.png",
                    "tipo_usuario": self.TIPO_USUARIO,
                }
            )

        self.grade_botoes = GavetaButtonGrid(self, button_data)

    def mostrar_historico_gaveta(self, gaveta_id):
        """Mostra o histórico de uma gaveta específica"""
        button = GavetaButton(
            self,
            text=gaveta_id,
            command=None,
            name="gaveta_black.png",
            tipo_usuario=self.TIPO_USUARIO,
        )
        button.mostrar_historico()
        # Subclasses podem sobrescrever para comportamento adicional

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        # Usar confirmação visual moderna
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
                self.after(1000, lambda: self._execute_logout())
            else:
                messagebox.showinfo("Sessão", "Sessão finalizada!")

    def _execute_logout(self):
        """Executa o logout após delay da notificação"""
        self.pack_forget()
        self.finalizar_sessao_callback()
