import customtkinter
from ..components import Header, VoltarButton
from ..pasta_state_manager import PastaStateManager

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
        self.header = Header(self, "Histórico de Ações nas Pastas")
        
        # Frame para o conteúdo
        self.content_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # Frame branco para a tabela
        self.tabela_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15
        )
        self.tabela_frame.pack(fill="both", expand=True, pady=10)
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Linhas da tabela
        self.carregar_dados()

        # Botão voltar (adicionado por último para ficar por cima)
        self.voltar_btn = VoltarButton(
            self, 
            command=self.voltar
        )
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        cabecalho_frame.pack(fill="x", padx=10, pady=10)

        # Cabeçalhos
        cabecalhos = ["Data/Hora", "Pasta", "Ação", "Usuário"]
        larguras = [0.3, 0.2, 0.25, 0.25]  # Proporções de largura
        
        for i, (texto, largura) in enumerate(zip(cabecalhos, larguras)):
            # Cria um frame para cada cabeçalho para melhor controle
            header_cell = customtkinter.CTkFrame(
                cabecalho_frame,
                fg_color="transparent"
            )
            header_cell.pack(side="left", fill="x", expand=True)
            
            # Configura o padding apenas para o cabeçalho "Pasta"
            padx_left = 65 if texto == "Pasta" else 0
            
            lbl = customtkinter.CTkLabel(
                header_cell,
                text=texto,
                font=("Arial", 14, "bold"),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=(padx_left, 0), pady=5)
            
            # Define o peso da coluna
            cabecalho_frame.columnconfigure(i, weight=int(largura * 100))
    
    def carregar_dados(self):
        # Frame rolável para os itens
        scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tabela_frame,
            fg_color="white"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        try:
            # Obter histórico do gerenciador de estado
            historico = self.state_manager.get_todo_historico()
            
            # Adicionar itens
            for idx, (data_hora, pasta_id, acao, usuario) in enumerate(historico):
                self.adicionar_linha(
                    scrollable_frame,
                    data_hora,
                    pasta_id,
                    acao,
                    usuario,
                    idx % 2 == 0  # Alternar cor de fundo
                )
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
    
    def adicionar_linha(self, parent, data_hora, pasta_id, acao, usuario, par):
        # Frame para uma linha da tabela
        linha_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#f9f9f9" if par else "white",
            corner_radius=8
        )
        linha_frame.pack(fill="x", padx=5, pady=2)
        
        # Dados da linha
        dados = [data_hora, pasta_id, acao, usuario]
        
        for texto in dados:
            lbl = customtkinter.CTkLabel(
                linha_frame,
                text=str(texto),
                font=("Arial", 12),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)
    
    def voltar(self):
        """Volta para a tela anterior"""
        if self.voltar_callback:
            self.voltar_callback()