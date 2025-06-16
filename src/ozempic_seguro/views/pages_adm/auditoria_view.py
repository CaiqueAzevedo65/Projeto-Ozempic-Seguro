import customtkinter
from tkinter import ttk
from datetime import datetime, timedelta
from ...repositories.database import DatabaseManager
from ..components import Header

class AuditoriaFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.db = DatabaseManager()
        self.pack(fill="both", expand=True)
        
        # Variáveis para filtros
        self.filtro_acao = customtkinter.StringVar(value="Todas")
        self.filtro_data_inicio = customtkinter.StringVar()
        self.filtro_data_fim = customtkinter.StringVar()
        
        # Definir data padrão (últimos 7 dias)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=7)
        self.filtro_data_inicio.set(data_inicio.strftime("%Y-%m-%d"))
        self.filtro_data_fim.set(data_fim.strftime("%Y-%m-%d"))
        
        self.criar_topo()
        self.criar_filtros()
        self.criar_tabela()
        self.carregar_dados()
        self.criar_botao_voltar()
    
    def criar_topo(self):
        """Cria o cabeçalho da página"""
        # Frame para o cabeçalho
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)
        
        # Título
        self.titulo = customtkinter.CTkLabel(
            self.header_frame,
            text="Registro de Auditoria",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.titulo.pack(side="left")
        
        # Botão de atualizar
        self.btn_atualizar = customtkinter.CTkButton(
            self.header_frame,
            text="Atualizar",
            command=self.carregar_dados,
            width=120,
            height=35,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.btn_atualizar.pack(side="right", padx=10)
    
    def criar_filtros(self):
        """Cria os controles de filtro"""
        # Frame para os filtros
        self.filtros_frame = customtkinter.CTkFrame(self, fg_color="#2c4d5c")
        self.filtros_frame.pack(fill="x", padx=20, pady=(0, 10), ipady=10)
        
        # Filtro por ação
        customtkinter.CTkLabel(
            self.filtros_frame,
            text="Ação:",
            text_color="white",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Apenas ações relacionadas a usuários
        self.cmb_acao = customtkinter.CTkComboBox(
            self.filtros_frame,
            values=["Todas", "LOGIN", "LOGOUT", "CRIAR", "ATUALIZAR", "EXCLUIR"],
            variable=self.filtro_acao,
            width=150,
            state="readonly"
        )
        self.cmb_acao.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Filtro por data de início
        customtkinter.CTkLabel(
            self.filtros_frame,
            text="Data Início:",
            text_color="white",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        self.entry_data_inicio = customtkinter.CTkEntry(
            self.filtros_frame,
            textvariable=self.filtro_data_inicio,
            width=120
        )
        self.entry_data_inicio.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Filtro por data de fim
        customtkinter.CTkLabel(
            self.filtros_frame,
            text="Data Fim:",
            text_color="white",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=4, padx=10, pady=5, sticky="w")
        
        self.entry_data_fim = customtkinter.CTkEntry(
            self.filtros_frame,
            textvariable=self.filtro_data_fim,
            width=120
        )
        self.entry_data_fim.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        # Botão de aplicar filtros
        self.btn_aplicar = customtkinter.CTkButton(
            self.filtros_frame,
            text="Aplicar Filtros",
            command=self.aplicar_filtros,
            width=120,
            height=30,
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        self.btn_aplicar.grid(row=0, column=6, padx=10, pady=5, sticky="e")
    
    def criar_tabela(self):
        """Cria a tabela para exibir os registros de auditoria"""
        # Frame para a tabela
        self.tabela_frame = customtkinter.CTkFrame(self, fg_color="white")
        self.tabela_frame.pack(fill="both", expand=True, padx=20, pady=(0, 100))
        
        # Criar Treeview com barra de rolagem
        self.tree_scroll = ttk.Scrollbar(self.tabela_frame)
        self.tree_scroll.pack(side="right", fill="y")
        
        # Definir estilo para a árvore
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#ffffff",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ffffff",
                        font=('Arial', 10))
        
        style.configure("Treeview.Heading", 
                        font=('Arial', 10, 'bold'))
        
        # Criar a árvore
        self.tree = ttk.Treeview(
            self.tabela_frame,
            yscrollcommand=self.tree_scroll.set,
            selectmode="extended",
            height=20
        )
        
        # Configurar a barra de rolagem
        self.tree_scroll.config(command=self.tree.yview)
        
        # Definir colunas
        self.tree['columns'] = ("data", "usuario", "acao", "tabela", "id_afetado", "detalhes")
        
        # Formatar colunas
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("data", anchor="w", width=150)
        self.tree.column("usuario", anchor="w", width=120)
        self.tree.column("acao", anchor="w", width=100)
        self.tree.column("tabela", anchor="w", width=100)
        self.tree.column("id_afetado", anchor="center", width=80)
        self.tree.column("detalhes", anchor="w", width=300)
        
        # Cabeçalhos
        self.tree.heading("data", text="Data/Hora", anchor="w")
        self.tree.heading("usuario", text="Usuário", anchor="w")
        self.tree.heading("acao", text="Ação", anchor="w")
        self.tree.heading("tabela", text="Tabela", anchor="w")
        self.tree.heading("id_afetado", text="ID Afetado", anchor="center")
        self.tree.heading("detalhes", text="Detalhes", anchor="w")
        
        # Adicionar a árvore ao frame
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Adicionar evento de clique duplo para ver detalhes
        self.tree.bind("<Double-1>", self.mostrar_detalhes)
    
    def carregar_dados(self, aplicar_filtros=False):
        """Carrega os dados da tabela de auditoria"""
        # Limpar a árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obter os filtros
        filtro_acao = None if self.filtro_acao.get() == "Todas" else self.filtro_acao.get()
        data_inicio = self.filtro_data_inicio.get()
        data_fim = self.filtro_data_fim.get()
        
        try:
            # Obter os registros de auditoria filtrados
            registros = self.db.buscar_logs_auditoria(
                filtro_acao=filtro_acao,
                filtro_tabela="USUARIOS",
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            # Preencher a tabela com os registros
            for registro in registros:
                # Extrair dados do registro
                data = registro.get('data_formatada', '')
                usuario = registro.get('usuario', 'Sistema')
                acao = registro.get('acao', '')
                tabela = registro.get('tabela_afetada', '')
                id_afetado = registro.get('id_afetado', '')
                
                # Formatar detalhes
                detalhes = ""
                dados_novos = registro.get('dados_novos', {})
                if isinstance(dados_novos, dict):
                    detalhes = ", ".join([f"{k}: {v}" for k, v in dados_novos.items()])
                
                # Inserir na árvore
                self.tree.insert(
                    "", "end",
                    values=(data, usuario, acao, tabela, id_afetado, detalhes),
                    tags=('linha',)
                )
                
                # Configurar tags para cores alternadas
                self.tree.tag_configure('linha', background='white')
                self.tree.tag_configure('linha_alternada', background='#f0f0f0')
                
                # Alternar cores das linhas
                for i, item in enumerate(self.tree.get_children()):
                    tag = 'linha_alternada' if i % 2 == 0 else 'linha'
                    self.tree.item(item, tags=(tag,))
                    
        except Exception as e:
            print(f"Erro ao carregar dados de auditoria: {e}")
    
    def formatar_detalhes_resumido(self, registro):
        """Formata os detalhes do registro para exibição resumida"""
        acao = registro.get('acao', '').lower()
        
        if acao == 'login':
            return "Login realizado com sucesso"
        elif acao == 'logout':
            return "Logout realizado"
        elif acao == 'criar':
            return "Novo usuário criado"
        elif acao == 'atualizar':
            return "Dados do usuário atualizados"
        elif acao == 'excluir':
            return "Usuário removido"
            
        return ""
    
    def aplicar_filtros(self):
        """Aplica os filtros selecionados"""
        self.carregar_dados(aplicar_filtros=True)
    
    def mostrar_detalhes(self, event):
        """Mostra os detalhes completos do registro selecionado"""
        item = self.tree.selection()[0]
        valores = self.tree.item(item, 'values')
        
        # Criar janela de detalhes
        janela = customtkinter.CTkToplevel(self)
        janela.title("Detalhes do Registro")
        janela.geometry("600x400")
        janela.grab_set()
        
        # Frame para os detalhes
        frame_detalhes = customtkinter.CTkFrame(janela, fg_color="white")
        frame_detalhes.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Exibir os detalhes
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"Data/Hora: {valores[0]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"Usuário: {valores[1]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"Ação: {valores[2]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"Tabela: {valores[3]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"ID Afetado: {valores[4]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        customtkinter.CTkLabel(
            frame_detalhes,
            text=f"Detalhes: {valores[5]}",
            font=("Arial", 12),
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
        # Botão para fechar
        btn_fechar = customtkinter.CTkButton(
            janela,
            text="Fechar",
            command=janela.destroy,
            width=100,
            height=35,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        btn_fechar.pack(pady=10)
    
    def criar_botao_voltar(self):
        """Cria o botão de voltar"""
        from ..components import VoltarButton
        VoltarButton(self, self.voltar_callback)
