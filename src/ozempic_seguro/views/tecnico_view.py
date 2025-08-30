import customtkinter
from tkinter import messagebox
from .components import Header, FinalizarSessaoButton, ModernButton, ModernConfirmDialog, ToastNotification
from .pages_adm.diagnostico_view import DiagnosticoFrame
from .pages_adm.parametro_sistemas_view import ParametroSistemasFrame
from .pages_adm.estado_terminal_view import EstadoTerminalFrame

class TecnicoFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do técnico"""
        # Limpa o frame atual
        for widget in self.winfo_children():
            widget.destroy()
            
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Técnico")

    def criar_botoes(self):
        # Frame principal para centralizar os botões
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, pady=30)
        
        # Criar botões modernos com ícones
        ModernButton(
            main_frame,
            text="🔧 Diagnóstico",
            command=self.abrir_diagnostico,
            style="warning",
            width=280,
            height=60
        ).pack(pady=15)
        
        ModernButton(
            main_frame,
            text="⚙️ Parâmetros de Sistema",
            command=self.abrir_parametros_sistema,
            style="secondary",
            width=280,
            height=60
        ).pack(pady=15)
        
        ModernButton(
            main_frame,
            text="📟 Estado do Terminal",
            command=self.abrir_estado_terminal,
            style="secondary",
            width=280,
            height=60
        ).pack(pady=15)

        
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
            cancel_text="Cancelar"
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
            
    def abrir_diagnostico(self):
        """Abre a tela de diagnóstico"""
        for widget in self.winfo_children():
            widget.destroy()
        DiagnosticoFrame(self, self.voltar_para_principal)
        
    def abrir_parametros_sistema(self):
        """Abre a tela de parâmetros do sistema"""
        for widget in self.winfo_children():
            widget.destroy()
        ParametroSistemasFrame(self, self.voltar_para_principal)
        
    def abrir_estado_terminal(self):
        """Abre a tela de estado do terminal"""
        for widget in self.winfo_children():
            widget.destroy()
        EstadoTerminalFrame(self, self.voltar_para_principal)
        
    def voltar_para_principal(self):
        """Volta para a tela principal do técnico"""
        self.criar_tela_principal()
