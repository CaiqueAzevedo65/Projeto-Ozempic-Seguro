import customtkinter
from .components import Header, VoltarButton, PastaButtonGrid
from src.views.pasta_state_manager import PastaStateManager

class HistoricoView(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, tipo_usuario="administrador", **kwargs):
        super().__init__(master, fg_color="#3B6A7D", **kwargs)
        self.voltar_callback = voltar_callback
        self.tipo_usuario = tipo_usuario
        self.state_manager = PastaStateManager.get_instance()
        
        self.pack(fill="both", expand=True)
        self.criar_interface()
    
    def criar_interface(self):
        # Cabeçalho
        self.header = Header(self, "Histórico de Pastas")
        
        # Botão voltar
        self.voltar_btn = VoltarButton(
            self, 
            command=self.voltar
        )
        
        # Frame para o conteúdo
        self.content_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = customtkinter.CTkLabel(
            self.content_frame,
            text="Histórico de Ações nas Pastas",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Área de rolagem para o histórico
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            corner_radius=10
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Carregar o histórico
        self.carregar_historico()
    
    def carregar_historico(self):
        """Carrega o histórico de todas as pastas"""
        # Limpa o frame de rolagem
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Obtém o histórico de todas as pastas
        historico = self.state_manager.get_todo_historico()
        
        if not historico:
            # Se não houver histórico, mostra mensagem
            sem_historico = customtkinter.CTkLabel(
                self.scrollable_frame,
                text="Nenhum registro de histórico encontrado.",
                font=("Arial", 14)
            )
            sem_historico.pack(pady=20)
            return
        
        # Cabeçalho da tabela
        cabecalho_frame = customtkinter.CTkFrame(
            self.scrollable_frame,
            fg_color="#2C4A57",
            corner_radius=5
        )
        cabecalho_frame.pack(fill="x", pady=(0, 5), padx=5)
        
        # Colunas do cabeçalho
        customtkinter.CTkLabel(
            cabecalho_frame,
            text="Data/Hora",
            font=("Arial", 12, "bold"),
            width=150
        ).pack(side="left", padx=5, pady=5)
        
        customtkinter.CTkLabel(
            cabecalho_frame,
            text="Pasta",
            font=("Arial", 12, "bold"),
            width=100
        ).pack(side="left", padx=5, pady=5)
        
        customtkinter.CTkLabel(
            cabecalho_frame,
            text="Ação",
            font=("Arial", 12, "bold"),
            width=100
        ).pack(side="left", padx=5, pady=5)
        
        customtkinter.CTkLabel(
            cabecalho_frame,
            text="Usuário",
            font=("Arial", 12, "bold"),
            width=150
        ).pack(side="left", padx=5, pady=5)
        
        # Adiciona cada item do histórico
        for acao, pasta_id, usuario, data in historico:
            item_frame = customtkinter.CTkFrame(
                self.scrollable_frame,
                fg_color="#3A5A6B",
                corner_radius=5
            )
            item_frame.pack(fill="x", pady=2, padx=5)
            
            # Formata os dados
            acao_text = "Aberta" if acao == "aberta" else "Fechada"
            
            # Adiciona as colunas
            customtkinter.CTkLabel(
                item_frame,
                text=data,
                width=150
            ).pack(side="left", padx=5, pady=5)
            
            customtkinter.CTkLabel(
                item_frame,
                text=pasta_id,
                width=100
            ).pack(side="left", padx=5, pady=5)
            
            customtkinter.CTkLabel(
                item_frame,
                text=acao_text,
                width=100
            ).pack(side="left", padx=5, pady=5)
            
            customtkinter.CTkLabel(
                item_frame,
                text=usuario,
                width=150
            ).pack(side="left", padx=5, pady=5)
    
    def voltar(self):
        """Volta para a tela anterior"""
        if self.voltar_callback:
            self.voltar_callback()