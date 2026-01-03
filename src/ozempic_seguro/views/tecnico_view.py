import customtkinter
from .base_frame import BaseFrameView
from .components import ModernButton, ToastNotification
from .pages_adm.diagnostico_view import DiagnosticoFrame
from .pages_adm.controle_timer_view import ControleTimerFrame
from ..services.timer_control_service import get_timer_control_service


class TecnicoFrame(BaseFrameView):
    """Tela principal do técnico - herda de BaseFrameView"""

    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, finalizar_sessao_callback, *args, **kwargs)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do técnico"""
        for widget in self.winfo_children():
            widget.destroy()

        self.criar_header("Técnico")
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_botoes(self):
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, pady=30)

        ModernButton(
            main_frame,
            text="🔧 Diagnóstico",
            command=self.abrir_diagnostico,
            style="warning",
            width=280,
            height=60,
        ).pack(pady=15)

        ModernButton(
            main_frame,
            text="⏱️ Controle de Timer",
            command=self.abrir_controle_timer,
            style="secondary",
            width=280,
            height=60,
        ).pack(pady=15)

    def finalizar_sessao(self):
        """Sobrescreve para reativar timer ao sair usando TimerControlService"""
        from .components import ModernConfirmDialog

        if ModernConfirmDialog.ask(
            self,
            "Finalizar Sessão",
            "Tem certeza que deseja sair do sistema?",
            icon="question",
            confirm_text="Sair",
            cancel_text="Cancelar",
        ):
            # Reativar timer ao fazer logout do técnico usando o serviço
            timer_service = get_timer_control_service()
            if not timer_service.is_timer_enabled():
                timer_service.enable_timer()
                ToastNotification.show(self, "Timer reativado automaticamente", "info")

            ToastNotification.show(self, "Sessão finalizada com sucesso", "success")
            if self.finalizar_sessao_callback:
                self.after(1000, self._execute_logout)

    def abrir_diagnostico(self):
        """Abre a tela de diagnóstico"""
        self._transicao_tela(lambda: DiagnosticoFrame(self, self.voltar_para_principal))

    def abrir_controle_timer(self):
        """Abre a tela de controle de timer"""
        self._transicao_tela(lambda: ControleTimerFrame(self, self.voltar_para_principal))

    def voltar_para_principal(self):
        """Volta para a tela principal do técnico"""
        self._transicao_tela(self.criar_tela_principal)
