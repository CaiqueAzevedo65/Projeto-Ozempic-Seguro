import customtkinter
from ..components import Header, VoltarButton

class DiagnosticoFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Frame principal para o conteúdo
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        self.criar_topo()
        self.criar_tabela_diagnostico()
        self.criar_botao_voltar()

    def criar_topo(self):
        Header(self, "Diagnóstico")
        
    def criar_tabela_diagnostico(self):
        # Frame para a tabela
        self.tabela_frame = customtkinter.CTkFrame(
            self.main_content,
            fg_color="white",
            corner_radius=15,
        )
        self.tabela_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Configurar grid da tabela
        self.tabela_frame.columnconfigure(0, weight=1)
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Frame rolável para os itens
        scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tabela_frame,
            fg_color="white"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Mensagem de tabela vazia
        lbl_vazio = customtkinter.CTkLabel(
            scrollable_frame,
            text="Nenhum diagnóstico encontrado.",
            text_color="#666666",
            font=("Arial", 12)
        )
        lbl_vazio.pack(pady=20)
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        cabecalho_frame.pack(fill="x", padx=10, pady=10)

        # Cabeçalhos
        cabecalhos = ["Data/Hora", "Tipo", "Descrição", "Status"]
        
        for texto in cabecalhos:
            # Cria um frame para cada cabeçalho para melhor controle
            header_cell = customtkinter.CTkFrame(
                cabecalho_frame,
                fg_color="transparent"
            )
            header_cell.pack(side="left", fill="x", expand=True)
            
            lbl = customtkinter.CTkLabel(
                header_cell,
                text=texto,
                font=("Arial", 14, "bold"),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=10, pady=5)

    def criar_botao_voltar(self):
        VoltarButton(self, self.voltar_callback)