import customtkinter
from tkinter import messagebox
from ..components import Header, FinalizarSessaoButton, ResponsiveButtonGrid, ModernButton, ModernConfirmDialog, ToastNotification
from .gerenciamento_usuarios_view import GerenciamentoUsuariosFrame
from .cadastro_usuario_view import CadastroUsuarioFrame
from .diagnostico_view import DiagnosticoFrame
from .parametro_sistemas_view import ParametroSistemasFrame
from .historico_view import HistoricoView
from .admin_gavetas_view import AdminGavetasFrame
from .auditoria_view import AuditoriaFrame

class PainelAdministradorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, usuario_logado=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.usuario_logado = usuario_logado  # Store the logged-in user
        self.pack(fill="both", expand=True)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do administrador"""
        # Limpa o frame atual
        for widget in self.winfo_children():
            widget.destroy()
            
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Administrador")

    def criar_botoes(self):
        # Dados dos botões com estilos e ícones
        buttons_data = [
            {"text": "👥 Gerenciar Usuários", "command": self.gerenciar_usuarios, "style": "primary"},
            {"text": "🗄️ Gerenciar Gavetas", "command": self.gerenciar_gavetas, "style": "primary"},
            {"text": "➕ Cadastro de Usuário", "command": self.cadastro_usuario, "style": "success"},
            {"text": "📋 Registro de Auditoria", "command": self.registro_auditoria, "style": "secondary"},
            {"text": "🔧 Diagnóstico", "command": self.diagnostico, "style": "warning"},
            {"text": "📊 Histórico", "command": self.mostrar_historico, "style": "secondary"}
        ]
        
        # Usar grid responsivo
        self.button_grid = ResponsiveButtonGrid(self, buttons_data, max_cols=3)

    def gerenciar_gavetas(self):
        """Abre a tela de gerenciamento de gavetas"""
        for widget in self.winfo_children():
            widget.destroy()
        AdminGavetasFrame(self, voltar_callback=self.criar_tela_principal)

    def mostrar_historico(self):
        for widget in self.winfo_children():
            widget.destroy()
        HistoricoView(self, voltar_callback=self.criar_tela_principal)

    def registro_auditoria(self):
        """Abre a tela de registro de auditoria"""
        for widget in self.winfo_children():
            widget.destroy()
        AuditoriaFrame(self, voltar_callback=self.criar_tela_principal)

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

    def gerenciar_usuarios(self):
        for widget in self.winfo_children():
            widget.destroy()
        # Pass the logged-in user to the GerenciamentoUsuariosFrame
        if hasattr(self, 'usuario_logado'):
            GerenciamentoUsuariosFrame(self, voltar_callback=self.criar_tela_principal, usuario_logado=self.usuario_logado)
        else:
            # If for some reason usuario_logado is not set, pass None
            GerenciamentoUsuariosFrame(self, voltar_callback=self.criar_tela_principal, usuario_logado=None)

    def cadastro_usuario(self):
        for widget in self.winfo_children():
            widget.destroy()
        CadastroUsuarioFrame(self, voltar_callback=self.criar_tela_principal)

    def diagnostico(self):
        for widget in self.winfo_children():
            widget.destroy()
        DiagnosticoFrame(self, voltar_callback=self.criar_tela_principal)
