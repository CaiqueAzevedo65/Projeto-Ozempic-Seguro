"""
Tela de Controle de Timer - Exclusiva para usuários técnicos.
Permite desativar temporariamente o timer enquanto o técnico está logado.
"""
import customtkinter
from ..components import Header, VoltarButton
from ...session import SessionManager
from tkinter import messagebox

class ControleTimerFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        self.session_manager = SessionManager.get_instance()
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Criar header
        self.header = Header(self, "Controle de Timer")
        
        # Frame principal para o conteúdo
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # Criar controle de timer
        self.criar_controle_timer()
        
        # Criar botão voltar
        self.criar_botao_voltar()

    def criar_controle_timer(self):
        """Cria o controle para ativar/desativar o timer"""
        # Frame central para o controle
        frame_central = customtkinter.CTkFrame(
            self.main_content,
            fg_color="white",
            corner_radius=15
        )
        frame_central.pack(expand=True, fill="both", pady=20)
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            frame_central,
            text="Controle de Timer de Sessão",
            font=("Arial", 20, "bold"),
            text_color="#333333"
        )
        lbl_titulo.pack(pady=(30, 10))
        
        # Descrição
        lbl_descricao = customtkinter.CTkLabel(
            frame_central,
            text="Quando desativado, o sistema não bloqueará automaticamente por inatividade.\nO timer será reativado automaticamente ao fazer logout.",
            font=("Arial", 12),
            text_color="#666666",
            justify="center"
        )
        lbl_descricao.pack(pady=(0, 30))
        
        # Frame para status
        frame_status = customtkinter.CTkFrame(
            frame_central,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        frame_status.pack(pady=20)
        
        # Indicador de status
        self.lbl_status = customtkinter.CTkLabel(
            frame_status,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#333333"
        )
        self.lbl_status.pack(padx=40, pady=20)
        
        # Botão de controle
        self.btn_controle = customtkinter.CTkButton(
            frame_central,
            text="",
            width=200,
            height=50,
            font=("Arial", 14, "bold"),
            command=self.alternar_timer
        )
        self.btn_controle.pack(pady=20)
        
        # Informação adicional
        lbl_info = customtkinter.CTkLabel(
            frame_central,
            text="⚠️ Esta configuração é temporária e válida apenas durante esta sessão",
            font=("Arial", 11),
            text_color="#FF6B6B"
        )
        lbl_info.pack(pady=(10, 30))
        
        # Atualizar estado inicial
        self.atualizar_estado()
    
    def alternar_timer(self):
        """Alterna o estado do timer"""
        # Verifica se o usuário é técnico
        usuario = self.session_manager.get_current_user()
        if not usuario or usuario.get('tipo') != 'tecnico':
            messagebox.showerror("Acesso Negado", "Apenas técnicos podem alterar esta configuração.")
            return
        
        # Alterna o estado
        novo_estado = not self.session_manager.is_timer_enabled()
        self.session_manager.set_timer_enabled(novo_estado)
        
        # Mensagem de confirmação
        if novo_estado:
            messagebox.showinfo("Timer Ativado", 
                "O timer de sessão foi ATIVADO.\nO sistema voltará a bloquear por inatividade.")
        else:
            messagebox.showwarning("Timer Desativado", 
                "⚠️ ATENÇÃO: Timer de sessão DESATIVADO!\n\n"
                "O sistema NÃO bloqueará por inatividade.\n"
                "Lembre-se de reativar antes de sair.")
        
        # Atualizar interface
        self.atualizar_estado()
    
    def atualizar_estado(self):
        """Atualiza a interface de acordo com o estado do timer"""
        if self.session_manager.is_timer_enabled():
            # Timer ativado
            self.lbl_status.configure(
                text="🟢 Timer ATIVADO",
                text_color="#2E7D32"
            )
            self.btn_controle.configure(
                text="Desativar Timer",
                fg_color="#F44336",
                hover_color="#D32F2F"
            )
        else:
            # Timer desativado
            self.lbl_status.configure(
                text="🔴 Timer DESATIVADO",
                text_color="#C62828"
            )
            self.btn_controle.configure(
                text="Ativar Timer",
                fg_color="#4CAF50",
                hover_color="#388E3C"
            )
    
    def criar_botao_voltar(self):
        """Cria o botão voltar"""
        VoltarButton(self, self.voltar_callback)
