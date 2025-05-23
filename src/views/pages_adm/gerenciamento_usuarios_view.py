import customtkinter
from ..components import Header, VoltarButton
from ...data.database import DatabaseManager

class GerenciamentoUsuariosFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.db = DatabaseManager()
        self.usuario_selecionado = None  # Armazenará o ID do usuário selecionado
        self.pack(fill="both", expand=True)
        
        # Variáveis para controle de estado
        self.confirmando_exclusao = False
        self.mensagem_visivel = False
        
        self.criar_topo()
        self.criar_tabela_usuarios()
        self.criar_painel_direito()
        self.criar_botao_voltar()
        
    def criar_topo(self):
        # Cabeçalho
        self.header = Header(self, "Gerenciamento de Usuários")
        
        # Frame principal para o conteúdo
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=(20, 100))

        # Frame para a tabela e área vazia
        self.content_frame = customtkinter.CTkFrame(self.main_content, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        
        # Configurar grid para dividir o espaço
        self.content_frame.columnconfigure(0, weight=1)  # Coluna da tabela
        self.content_frame.columnconfigure(1, weight=1)  # Coluna do painel direito
        self.content_frame.rowconfigure(0, weight=1)     # Única linha

    def criar_tabela_usuarios(self):
        # Frame para a tabela
        self.tabela_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15,
        )
        self.tabela_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        # Configurar grid da tabela
        self.tabela_frame.columnconfigure(0, weight=1)
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Linhas da tabela
        self.carregar_dados()
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        cabecalho_frame.pack(fill="x", padx=10, pady=10)

        # Cabeçalhos atualizados
        cabecalhos = ["Usuário", "Nome Completo", "Tipo"]
        
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
        tipo_formatado = tipo.capitalize()
        
        # Frame para uma linha da tabela
        linha_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#f9f9f9" if par else "white",
            corner_radius=8
        )
        linha_frame.pack(fill="x", padx=5, pady=2)
        
        # Armazenar dados do usuário para uso no clique
        linha_frame.dados_usuario = (user_id, username, nome_completo, tipo, ativo, data_criacao)
        
        # Tornar a linha clicável
        linha_frame.bind("<Button-1>", lambda e, dados=linha_frame.dados_usuario: self.exibir_detalhes_usuario(*dados))
        
        # Apenas os dados necessários
        dados = [
            username,
            nome_completo,
            tipo_formatado
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
            
            # Tornar os labels da linha clicáveis também
            lbl.bind("<Button-1>", lambda e, dados=linha_frame.dados_usuario: self.exibir_detalhes_usuario(*dados))
    
    def criar_painel_direito(self):
        # Frame para o painel direito
        self.painel_direito = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15,
        )
        self.painel_direito.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        # Configurar grid do painel direito
        self.painel_direito.columnconfigure(0, weight=1)
        
        # Label de instrução inicial
        self.lbl_instrucao = customtkinter.CTkLabel(
            self.painel_direito,
            text="Selecione um usuário para visualizar e editar",
            font=("Arial", 14, "bold"),
            text_color="#666666",
            wraplength=300
        )
        self.lbl_instrucao.grid(row=0, column=0, pady=50, padx=20, sticky="n")
        
        # Frame para os detalhes do usuário (inicialmente oculto)
        self.frame_detalhes = customtkinter.CTkFrame(
            self.painel_direito,
            fg_color="white"
        )
        
        # Frame para os botões de ação
        self.frame_botoes = customtkinter.CTkFrame(
            self.painel_direito,
            fg_color="white"
        )
        
        # Frame para mensagens (inicialmente vazio)
        self.frame_mensagem = customtkinter.CTkFrame(
            self.painel_direito,
            fg_color="white"
        )
    
    def exibir_detalhes_usuario(self, user_id, username, nome_completo, tipo, ativo, data_criacao):
        self.usuario_selecionado = user_id
        
        # Limpar frame de detalhes
        for widget in self.frame_detalhes.winfo_children():
            widget.destroy()
            
        # Configurar frame de detalhes
        self.frame_detalhes.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            self.frame_detalhes,
            text="Detalhes do Usuário",
            font=("Arial", 16, "bold"),
            text_color="#333333"
        )
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")
        
        # Informações do usuário
        campos = [
            ("Usuário:", username),
            ("Nome Completo:", nome_completo),
            ("Tipo:", tipo.capitalize()),
            ("Status:", "Ativo" if ativo else "Inativo"),
            ("Data de Criação:", data_criacao.split(' ')[0])
        ]
        
        for idx, (label, valor) in enumerate(campos):
            frame = customtkinter.CTkFrame(self.frame_detalhes, fg_color="transparent")
            frame.grid(row=idx+1, column=0, columnspan=2, padx=10, pady=2, sticky="nsew")
            
            lbl = customtkinter.CTkLabel(
                frame,
                text=label,
                font=("Arial", 12, "bold"),
                anchor="w"
            )
            lbl.pack(side="left")
            
            lbl_valor = customtkinter.CTkLabel(
                frame,
                text=valor,
                font=("Arial", 12),
                text_color="#333333"
            )
            lbl_valor.pack(side="left")
        
        # Configurar frame de botões
        self.frame_botoes.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="nsew")
        
        # Botão Alterar Senha
        btn_alterar_senha = customtkinter.CTkButton(
            self.frame_botoes,
            text="Alterar Senha",
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.abrir_janela_alterar_senha
        )
        btn_alterar_senha.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        
        # Botão Excluir Usuário
        btn_excluir = customtkinter.CTkButton(
            self.frame_botoes,
            text="Excluir Usuário",
            fg_color="#f44336",
            hover_color="#d32f2f",
            command=self.confirmar_exclusao
        )
        btn_excluir.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        
        # Esconder instrução
        self.lbl_instrucao.grid_forget()
    
    def abrir_janela_alterar_senha(self):
        if not self.usuario_selecionado:
            return
            
        # Criar janela de diálogo
        self.dialog = customtkinter.CTkToplevel(self)
        self.dialog.title("Alterar Senha")
        self.dialog.geometry("400x350")  # Aumentei a altura para acomodar a mensagem
        self.dialog.grab_set()  # Torna a janela modal
        
        # Centralizar a janela
        window_width = 400
        window_height = 350
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Frame principal
        frame = customtkinter.CTkFrame(self.dialog, fg_color="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.columnconfigure(0, weight=1)  # Configura a coluna para expandir
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            frame,
            text="Alterar Senha",
            font=("Arial", 16, "bold")
        )
        lbl_titulo.grid(row=0, column=0, pady=(0, 20), sticky="n")
        
        # Frame para campos de senha
        campos_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        campos_frame.grid(row=1, column=0, sticky="nsew")
        
        # Campo Nova Senha
        lbl_nova_senha = customtkinter.CTkLabel(campos_frame, text="Nova Senha:", anchor="w")
        lbl_nova_senha.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.entry_nova_senha = customtkinter.CTkEntry(campos_frame, show="•", width=300)
        self.entry_nova_senha.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        
        # Campo Confirmar Senha
        lbl_confirmar_senha = customtkinter.CTkLabel(campos_frame, text="Confirmar Senha:", anchor="w")
        lbl_confirmar_senha.grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        self.entry_confirmar_senha = customtkinter.CTkEntry(campos_frame, show="•", width=300)
        self.entry_confirmar_senha.grid(row=3, column=0, pady=(0, 10), sticky="ew")
        
        # Rótulo para mensagens de erro/sucesso
        self.lbl_mensagem = customtkinter.CTkLabel(
            campos_frame,
            text="",
            text_color="red",
            wraplength=300,
            justify="left"
        )
        self.lbl_mensagem.grid(row=4, column=0, pady=(5, 10), sticky="w")
        
        # Frame para botões
        botoes_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        botoes_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        
        # Botão Salvar
        btn_salvar = customtkinter.CTkButton(
            botoes_frame,
            text="Salvar",
            command=lambda: self.salvar_nova_senha()
        )
        btn_salvar.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Botão Cancelar
        btn_cancelar = customtkinter.CTkButton(
            botoes_frame,
            text="Cancelar",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=self.dialog.destroy
        )
        btn_cancelar.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Configurar o grid para expandir corretamente
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Focar no primeiro campo
        self.entry_nova_senha.focus_set()
    
    def salvar_nova_senha(self):
        nova_senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        
        # Limpar mensagem anterior
        self.lbl_mensagem.configure(text="", text_color="red")
        
        if not nova_senha or not confirmar_senha:
            self.lbl_mensagem.configure(text="Por favor, preencha todos os campos.")
            return False
            
        if nova_senha != confirmar_senha:
            self.lbl_mensagem.configure(text="As senhas não coincidem.")
            return False
            
        if len(nova_senha) < 4:
            self.lbl_mensagem.configure(text="A senha deve ter pelo menos 4 caracteres.")
            return False
            
        try:
            # Atualiza a senha no banco de dados
            sucesso = self.db.atualizar_senha(self.usuario_selecionado, nova_senha)
            
            if sucesso:
                self.lbl_mensagem.configure(
                    text="Senha alterada com sucesso!", 
                    text_color="green"
                )
                # Fechar a janela após 1.5 segundos
                self.dialog.after(1500, self.dialog.destroy)
                return True
            else:
                self.lbl_mensagem.configure(text="Erro ao alterar a senha. Tente novamente.")
                return False
        except Exception as e:
            self.lbl_mensagem.configure(text=f"Erro ao alterar senha: {str(e)}")
            return False
    
    def confirmar_exclusao(self):
        if not self.usuario_selecionado:
            return
            
        if not self.confirmando_exclusao:
            # Primeiro clique - Mostrar confirmação
            self.confirmando_exclusao = True
            
            # Limpar frame de mensagem
            for widget in self.frame_mensagem.winfo_children():
                widget.destroy()
                
            # Configurar frame de mensagem
            self.frame_mensagem.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
            
            # Mensagem de confirmação
            lbl_confirmacao = customtkinter.CTkLabel(
                self.frame_mensagem,
                text="Tem certeza que deseja excluir este usuário?\nEsta ação não pode ser desfeita.",
                text_color="#333333",
                font=("Arial", 12),
                justify="left"
            )
            lbl_confirmacao.pack(side="left", padx=(0, 10))
            
            # Botão Confirmar
            btn_confirmar = customtkinter.CTkButton(
                self.frame_mensagem,
                text="Confirmar",
                fg_color="#dc3545",
                hover_color="#c82333",
                command=self.excluir_usuario,
                width=100
            )
            btn_confirmar.pack(side="left", padx=(0, 5))
            
            # Botão Cancelar
            btn_cancelar = customtkinter.CTkButton(
                self.frame_mensagem,
                text="Cancelar",
                fg_color="#6c757d",
                hover_color="#5a6268",
                command=self.cancelar_exclusao,
                width=100
            )
            btn_cancelar.pack(side="left")
            
            # Desabilitar botão de excluir
            for widget in self.frame_botoes.winfo_children():
                if widget.cget("text") == "Excluir Usuário":
                    widget.configure(state="disabled")
    
    def cancelar_exclusao(self):
        """Cancela a confirmação de exclusão"""
        self.confirmando_exclusao = False
        self.frame_mensagem.grid_forget()
        
        # Reativar botão de excluir
        for widget in self.frame_botoes.winfo_children():
            if widget.cget("text") == "Excluir Usuário":
                widget.configure(state="normal")
    
    def excluir_usuario(self):
        """Exclui o usuário selecionado"""
        if not self.usuario_selecionado:
            return
            
        try:
            # Verifica se é o único administrador
            if self.db.eh_unico_administrador(self.usuario_selecionado):
                self.mostrar_mensagem_erro(
                    "Não é possível excluir o único administrador do sistema.\n"
                    "Promova outro usuário a administrador antes de remover este."
                )
                self.cancelar_exclusao()
                return
                
            # Chama o método do banco de dados para excluir o usuário
            sucesso = self.db.excluir_usuario(self.usuario_selecionado)
            
            # Limpar frame de mensagem
            for widget in self.frame_mensagem.winfo_children():
                widget.destroy()
                
            if sucesso:
                # Mostrar mensagem de sucesso
                lbl_sucesso = customtkinter.CTkLabel(
                    self.frame_mensagem,
                    text="Usuário excluído com sucesso!",
                    text_color="#28a745",
                    font=("Arial", 12, "bold")
                )
                lbl_sucesso.pack(pady=5)
                
                # Atualizar a tabela de usuários após 1.5 segundos
                self.after(1500, self.atualizar_apos_exclusao)
            else:
                # Mostrar mensagem de erro
                lbl_erro = customtkinter.CTkLabel(
                    self.frame_mensagem,
                    text="Não foi possível excluir o usuário.",
                    text_color="#dc3545",
                    font=("Arial", 12, "bold")
                )
                lbl_erro.pack(pady=5)
                
                # Reativar botão de excluir após 2 segundos
                self.after(2000, self.reiniciar_estado_exclusao)
                
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            self.mostrar_mensagem_erro(f"Erro ao excluir usuário: {str(e)}")
    
    def atualizar_apos_exclusao(self):
        """Atualiza a interface após a exclusão bem-sucedida"""
        self.confirmando_exclusao = False
        self.frame_mensagem.grid_forget()
        
        # Atualizar a tabela
        self.carregar_dados()
        
        # Limpar painel de detalhes
        self.limpar_painel_detalhes()
        
        # Mostrar instrução novamente
        self.lbl_instrucao.grid(row=0, column=0, pady=50, padx=20, sticky="n")
    
    def reiniciar_estado_exclusao(self):
        """Reinicia o estado dos botões após uma tentativa de exclusão"""
        self.confirmando_exclusao = False
        self.frame_mensagem.grid_forget()
        
        # Reativar botão de excluir
        for widget in self.frame_botoes.winfo_children():
            if widget.cget("text") == "Excluir Usuário":
                widget.configure(state="normal")
    
    def limpar_painel_detalhes(self):
        # Esconder frames de detalhes e botões
        self.frame_detalhes.grid_forget()
        self.frame_botoes.grid_forget()
        
        # Mostrar instrução novamente
        self.lbl_instrucao.grid(row=0, column=0, pady=50, padx=20, sticky="n")
        
        # Limpar usuário selecionado
        self.usuario_selecionado = None
    
    def mostrar_mensagem_erro(self, mensagem):
        # Implemente a exibição de mensagem de erro conforme sua aplicação
        print(f"ERRO: {mensagem}")
        
    def mostrar_mensagem_sucesso(self, mensagem):
        # Implemente a exibição de mensagem de sucesso conforme sua aplicação
        print(f"SUCESSO: {mensagem}")
    
    def criar_botao_voltar(self):
        # Botão voltar (adicionado por último para ficar por cima)
        self.voltar_btn = VoltarButton(
            self, 
            command=self.voltar_callback
        )