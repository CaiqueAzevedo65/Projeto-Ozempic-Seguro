import customtkinter
from ..components import Header, VoltarButton
from data.database import DatabaseManager

class UsuariosView(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", **kwargs)
        self.voltar_callback = voltar_callback
        self.db = DatabaseManager()
        
        self.pack(fill="both", expand=True)
        self.criar_interface()
    
    def criar_interface(self):
        # Cabeçalho
        self.header = Header(self, "Gerenciamento de Usuários")
        
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
        cabecalhos = ["ID", "Usuário", "Nome Completo", "Tipo", "Status", "Data de Criação"]
        larguras = [0.1, 0.15, 0.25, 0.15, 0.1, 0.25]  # Proporções de largura
        
        for i, (texto, largura) in enumerate(zip(cabecalhos, larguras)):
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
            # Obter usuários do banco de dados
            usuarios = self.db.get_usuarios()
            
            # Adicionar itens
            for idx, (user_id, username, nome_completo, tipo, ativo, data_criacao) in enumerate(usuarios):
                self.adicionar_linha(
                    scrollable_frame,
                    user_id,
                    username,
                    nome_completo,
                    tipo,
                    ativo,
                    data_criacao,
                    idx % 2 == 0  # Alternar cor de fundo
                )
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
    
    def adicionar_linha(self, parent, user_id, username, nome_completo, tipo, ativo, data_criacao, par):
        # Formatar dados
        status = "Ativo" if ativo else "Inativo"
        data_formatada = data_criacao.split(' ')[0]  # Pega apenas a data
        
        # Frame para uma linha da tabela
        linha_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#f9f9f9" if par else "white",
            corner_radius=8
        )
        linha_frame.pack(fill="x", padx=5, pady=2)
        
        # Dados da linha
        dados = [
            str(user_id),
            username,
            nome_completo,
            tipo.capitalize(),
            status,
            data_formatada
        ]
        
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
