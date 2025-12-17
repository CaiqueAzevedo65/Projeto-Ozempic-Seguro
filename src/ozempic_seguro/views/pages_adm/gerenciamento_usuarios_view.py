import tkinter
import customtkinter
from ..components import Header, VoltarButton, ModernButton, ModernConfirmDialog, ToastNotification
from ...services.user_management_service import get_user_management_service
from ...core.logger import logger

class GerenciamentoUsuariosFrame(customtkinter.CTkFrame):
    BG_COLOR = "#3B6A7D"
    
    def __init__(self, master, voltar_callback=None, usuario_logado=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        self.usuario_logado = usuario_logado  # Store the logged-in user
        super().__init__(master, fg_color=self.BG_COLOR, *args, **kwargs)
        self.management_service = get_user_management_service()
        self.usuario_selecionado = None  # Armazenará o ID do usuário selecionado
        self.usuario_selecionado_data = None  # Dados do usuário selecionado
        
        # Criar overlay para esconder construção
        self._overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.lift()
        master.update_idletasks()
        
        self.pack(fill="both", expand=True)
        
        # Variáveis para controle de estado
        self.confirmando_exclusao = False
        self.mensagem_visivel = False
        
        self.criar_topo()
        self.criar_tabela_usuarios()
        self.criar_painel_direito()
        self.criar_botao_voltar()
        
        # Remover overlay após tudo estar pronto
        self.update_idletasks()
        self._overlay.destroy()
        
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
        self.tabela_frame.rowconfigure(1, weight=1)  # Linha para o conteúdo rolável
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Frame para o conteúdo rolável
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tabela_frame,
            fg_color="white"
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scrollable_frame.columnconfigure(0, weight=1)
        
        # Carregar dados iniciais
        self.carregar_dados()
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#e0e0e0",
            corner_radius=8,
            border_width=1,
            border_color="#cccccc"
        )
        cabecalho_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Configurar grid dos cabeçalhos
        for i in range(3):  # 3 colunas
            cabecalho_frame.columnconfigure(i, weight=1)

        # Cabeçalhos atualizados
        cabecalhos = ["Usuário", "Nome Completo", "Tipo"]
        
        for col, texto in enumerate(cabecalhos):
            lbl = customtkinter.CTkLabel(
                cabecalho_frame,
                text=texto,
                font=("Arial", 13, "bold"),
                text_color="#333333",
                anchor="w"
            )
            lbl.grid(row=0, column=col, padx=15, pady=8, sticky="ew")
    
    def carregar_dados(self):
        # Limpar frame existente
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            # Obter usuários usando o serviço de gerenciamento
            usuarios = self.management_service.get_all_users()
            
            # Adicionar itens
            for idx, user in enumerate(usuarios):
                # Frame para uma linha da tabela
                linha_frame = customtkinter.CTkFrame(
                    self.scrollable_frame,
                    fg_color="#f0f0f0" if idx % 2 == 0 else "#f8f8f8",
                    corner_radius=8,
                    height=50,
                    border_width=1,
                    border_color="#e0e0e0"
                )
                linha_frame.grid(row=idx, column=0, sticky="nsew", pady=2, padx=5)
                linha_frame.grid_propagate(False)
                
                # Armazenar dados do usuário para uso no clique (usando UserData)
                linha_frame.dados_usuario = (user.id, user.username, user.nome_completo, user.tipo, user.ativo, user.data_criacao)
                
                # Frame para o conteúdo da linha que preenche todo o espaço
                conteudo_frame = customtkinter.CTkFrame(
                    linha_frame,
                    fg_color="transparent"
                )
                conteudo_frame.pack(fill="both", expand=True, padx=10, pady=8)
                
                # Configurar grid do conteúdo
                for i in range(3):
                    conteudo_frame.columnconfigure(i, weight=1)
                
                # Dados a serem exibidos (usando propriedades do UserData)
                dados = [
                    user.username,
                    user.nome_completo,
                    user.tipo_display
                ]
                
                # Adicionar os dados como labels dentro do frame
                for col, texto in enumerate(dados):
                    # Frame para cada célula que preenche o espaço disponível
                    cell_frame = customtkinter.CTkFrame(
                        conteudo_frame,
                        fg_color="transparent"
                    )
                    cell_frame.grid(row=0, column=col, sticky="nsew", padx=5)
                    cell_frame.columnconfigure(0, weight=1)
                    
                    # Definir estilo da fonte
                    font_style = ("Arial", 12, "bold") if col == 0 else ("Arial", 12)
                    
                    lbl = customtkinter.CTkLabel(
                        cell_frame,
                        text=str(texto),
                        font=font_style,
                        text_color="#333333",
                        anchor="w"
                    )
                    lbl.pack(side="left", fill="x", expand=True, anchor="w")
                    
                    # Configurar para que a célula ocupe todo o espaço horizontal
                    cell_frame.grid_propagate(False)
                
                # Função para lidar com eventos de clique
                def make_click_handler(dados):
                    return lambda e: self.exibir_detalhes_usuario(*dados)
                
                # Criar handler de clique
                click_handler = make_click_handler(linha_frame.dados_usuario)
                
                # Adicionar evento de clique apenas uma vez no frame principal
                linha_frame.bind("<Button-1>", click_handler)
                
                # Função para propagar o clique para os elementos filhos
                def propagate_click(widget, handler):
                    widget.bind("<Button-1>", handler)
                    for child in widget.winfo_children():
                        if isinstance(child, (customtkinter.CTkFrame, customtkinter.CTkLabel)):
                            propagate_click(child, handler)
                
                # Aplicar propagação de clique para os elementos internos
                propagate_click(conteudo_frame, click_handler)
                
                # Remover efeitos de cursor apenas
                for widget in [linha_frame, conteudo_frame] + conteudo_frame.winfo_children():
                    try:
                        if hasattr(widget, 'configure'):
                            widget.configure(cursor="")
                    except Exception:
                        continue
                
        except Exception as e:
            logger.error(f"Erro ao carregar usuários: {e}")
    
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
        self.tipo_usuario_selecionado = tipo  # Armazenar o tipo do usuário selecionado
        
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
        
        # Formatar data de criação
        try:
            if data_criacao and isinstance(data_criacao, str):
                data_formatada = data_criacao.split(' ')[0] if ' ' in data_criacao else data_criacao
            else:
                data_formatada = "N/A"
        except (ValueError, AttributeError, IndexError):
            data_formatada = "N/A"
        
        # Informações do usuário
        campos = [
            ("Usuário:", username),
            ("Nome Completo:", nome_completo),
            ("Tipo:", tipo.capitalize()),
            ("Status:", "Ativo" if ativo else "Inativo"),
            ("Data de Criação:", data_formatada)
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
        
        # Limpar botões existentes
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()
        
        # Configurar grid para os botões (2 colunas)
        self.frame_botoes.columnconfigure(0, weight=1)
        self.frame_botoes.columnconfigure(1, weight=1)
        
        # Verificar se é um usuário técnico
        is_tecnico = tipo.lower() == 'tecnico'
        
        # Botão Alterar Senha - desabilitado para técnicos
        btn_alterar_senha = ModernButton(
            self.frame_botoes,
            text="🔑 Alterar Senha",
            command=self.abrir_janela_alterar_senha if not is_tecnico else self.mostrar_aviso_tecnico,
            style="success" if not is_tecnico else "secondary",
            height=50
        )
        btn_alterar_senha.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        
        # Botão Excluir Usuário - desabilitado para técnicos
        btn_excluir = ModernButton(
            self.frame_botoes,
            text="🗑️ Excluir Usuário",
            command=self.confirmar_exclusao if not is_tecnico else self.mostrar_aviso_tecnico,
            style="danger" if not is_tecnico else "secondary",
            height=50
        )
        btn_excluir.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        
        # Se for técnico, mostrar aviso
        if is_tecnico:
            aviso_frame = customtkinter.CTkFrame(
                self.frame_detalhes,
                fg_color="#FFF3CD",
                corner_radius=8
            )
            aviso_frame.grid(row=len(campos)+2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
            
            lbl_aviso = customtkinter.CTkLabel(
                aviso_frame,
                text="⚠️ Usuários técnicos não podem ser modificados ou excluídos",
                font=("Arial", 11, "bold"),
                text_color="#856404",
                wraplength=300
            )
            lbl_aviso.pack(padx=10, pady=10)
        
        # Esconder instrução
        self.lbl_instrucao.grid_forget()
    
    def abrir_janela_alterar_senha(self):
        if not self.usuario_selecionado:
            return
            
        # Criar janela de diálogo
        self.dialog = customtkinter.CTkToplevel(self)
        self.dialog.title("Alterar Senha")
        self.dialog.geometry("700x400")  # Largura: 700px, Altura: 400px
        self.dialog.grab_set()  # Torna a janela modal
        
        # Centralizar a janela
        window_width = 700
        window_height = 400
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Frame principal
        main_frame = customtkinter.CTkFrame(self.dialog, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame para os campos de senha (lado esquerdo)
        campos_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            campos_frame,
            text="Alterar Senha",
            font=("Arial", 16, "bold")
        )
        lbl_titulo.pack(pady=(0, 20))
        
        # Campo Nova Senha
        lbl_nova_senha = customtkinter.CTkLabel(campos_frame, text="Nova Senha:", anchor="w")
        lbl_nova_senha.pack(fill="x", pady=(0, 5))
        
        self.entry_nova_senha = customtkinter.CTkEntry(campos_frame, show="•", width=300)
        self.entry_nova_senha.pack(fill="x", pady=(0, 10))
        self.entry_nova_senha.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.entry_nova_senha))
        
        # Campo Confirmar Senha
        lbl_confirmar_senha = customtkinter.CTkLabel(campos_frame, text="Confirmar Senha:", anchor="w")
        lbl_confirmar_senha.pack(fill="x", pady=(10, 5))
        
        self.entry_confirmar_senha = customtkinter.CTkEntry(campos_frame, show="•", width=300)
        self.entry_confirmar_senha.pack(fill="x", pady=(0, 10))
        self.entry_confirmar_senha.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.entry_confirmar_senha))
        
        # Rótulo para mensagens de erro/sucesso
        self.lbl_mensagem = customtkinter.CTkLabel(
            campos_frame,
            text="",
            text_color="red",
            wraplength=300,
            justify="left"
        )
        self.lbl_mensagem.pack(fill="x", pady=(10, 0))
        
        # Frame para botões
        botoes_frame = customtkinter.CTkFrame(campos_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(20, 0))
        
        # Botão Salvar
        btn_salvar = ModernButton(
            botoes_frame,
            text="💾 Salvar",
            command=self.salvar_nova_senha,
            style="success",
            height=40
        )
        btn_salvar.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Botão Cancelar
        btn_cancelar = ModernButton(
            botoes_frame,
            text="❌ Cancelar",
            command=self.dialog.destroy,
            style="secondary",
            height=40
        )
        btn_cancelar.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Frame para o teclado (lado direito)
        teclado_frame = customtkinter.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        teclado_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # Título do teclado
        customtkinter.CTkLabel(
            teclado_frame,
            text="Teclado Numérico",
            font=("Arial", 14, "bold"),
            text_color="black"
        ).pack(pady=(10, 5))
        
        # Teclado numérico
        botoes = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["", "0", "⌫"]
        ]
        
        for i, linha in enumerate(botoes):
            frame_linha = customtkinter.CTkFrame(teclado_frame, fg_color="transparent")
            frame_linha.pack(fill="x", pady=2)
            
            # Configurar 3 colunas iguais
            for col in range(3):
                frame_linha.columnconfigure(col, weight=1, uniform="botao")
            
            for j, texto in enumerate(linha):
                if texto:
                    btn = ModernButton(
                        frame_linha, 
                        text=texto, 
                        command=lambda t=texto: self.tecla_pressionada(t),
                        style="primary",
                        height=50,
                        font=("Arial", 16)
                    )
                    btn.grid(row=0, column=j, padx=3, pady=3, sticky="nsew")
        
        # Definir campo ativo inicial
        self.campo_ativo = self.entry_nova_senha
        self.entry_nova_senha.focus_set()
    
    def definir_campo_ativo(self, campo):
        """Define qual campo está ativo para receber entrada do teclado"""
        self.campo_ativo = campo
    
    def tecla_pressionada(self, valor):
        """Manipula o pressionamento das teclas do teclado numérico"""
        if valor == "⌫":  # Backspace
            current_text = self.campo_ativo.get()
            self.campo_ativo.delete(0, tkinter.END)
            self.campo_ativo.insert(0, current_text[:-1])
        else:
            self.campo_ativo.insert(tkinter.END, valor)
    
    def salvar_nova_senha(self):
        """Salva nova senha usando UserManagementService"""
        nova_senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        
        # Usar o serviço para alterar senha (validação inclusa)
        result = self.management_service.change_password(
            self.usuario_selecionado, nova_senha, confirmar_senha
        )
        
        if result.success:
            self.lbl_mensagem.configure(text=f"✅ {result.message}", text_color="#28a745")
        # Obter dados do usuário para confirmação
        user = self.management_service.get_user_by_id(self.usuario_selecionado)
        if not user:
            ToastNotification.show(self, "Usuário não encontrado", "error")
            return
        
        # Confirmação moderna antes de excluir
        if not ModernConfirmDialog.ask(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o usuário '{user.nome_completo}' (ID: {user.username})?\n\nEsta ação não pode ser desfeita.",
            icon="warning",
            confirm_text="Excluir",
            cancel_text="Cancelar"
        ):
            return
        
        # Obter ID do usuário logado para evitar auto-exclusão
        current_user_id = self.usuario_logado.get('id') if self.usuario_logado else None
        
        # Usar o serviço para excluir
        result = self.management_service.delete_user(self.usuario_selecionado, current_user_id)
        
        # Reiniciar estado de exclusão
        self.reiniciar_estado_exclusao()
        
        if result.success:
            self.carregar_dados()
            self.limpar_painel_detalhes()
            ToastNotification.show(self, result.message, "success")
        else:
            ToastNotification.show(self, result.message, "error")
    
    def mostrar_aviso_tecnico(self):
        """Mostra aviso de que usuários técnicos não podem ser modificados"""
        from tkinter import messagebox
        messagebox.showwarning(
            "Ação Não Permitida",
            "Usuários do tipo técnico não podem ser modificados ou excluídos.\n\n"
            "Esta é uma medida de segurança do sistema."
        )
    
    def limpar_painel_detalhes(self):
        # Esconder frames de detalhes e botões
        self.frame_detalhes.grid_forget()
        self.frame_botoes.grid_forget()
        
        # Mostrar instrução novamente
        self.lbl_instrucao.grid(row=0, column=0, pady=50, padx=20, sticky="n")
        
        # Limpar usuário selecionado
        self.usuario_selecionado = None
        self.tipo_usuario_selecionado = None
    
    def mostrar_mensagem_erro(self, mensagem):
        """
        Exibe uma mensagem de erro em uma janela de diálogo personalizada.
        
        Args:
            mensagem (str): Mensagem de erro a ser exibida
        """
        # Cria uma janela de diálogo personalizada
        janela_erro = customtkinter.CTkToplevel(self)
        janela_erro.title("Aviso")
        janela_erro.geometry("500x200")
        janela_erro.grab_set()  # Torna a janela modal
        
        # Centraliza a janela na tela
        largura_janela = 500
        altura_janela = 200
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_erro.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
        
        # Frame principal
        frame_principal = customtkinter.CTkFrame(janela_erro, fg_color="#f8d7da", corner_radius=10)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Ícone de aviso
        icone_aviso = customtkinter.CTkLabel(
            frame_principal, 
            text="⚠️", 
            font=("Arial", 24)
        )
        icone_aviso.pack(pady=(20, 10))
        
        # Mensagem de erro
        lbl_mensagem = customtkinter.CTkLabel(
            frame_principal,
            text=mensagem,
            text_color="#721c24",
            font=("Arial", 12),
            wraplength=400,
            justify="center"
        )
        lbl_mensagem.pack(padx=20, pady=10)
        
        # Botão OK
        btn_ok = ModernButton(
            frame_principal,
            text="OK",
            command=janela_erro.destroy,
            style="danger",
            width=100,
            height=35
        )
        btn_ok.pack(pady=(10, 20))
        
        # Configura o que acontece quando a janela é fechada
        janela_erro.protocol("WM_DELETE_WINDOW", janela_erro.destroy)
        
        # Espera até que a janela seja fechada
        self.wait_window(janela_erro)
    
    def mostrar_mensagem_sucesso(self, mensagem):
        """
        Exibe uma mensagem de sucesso em uma janela de diálogo personalizada.
        
        Args:
            mensagem (str): Mensagem de sucesso a ser exibida
        """
        # Cria uma janela de diálogo personalizada
        janela_sucesso = customtkinter.CTkToplevel(self)
        janela_sucesso.title("Sucesso")
        janela_sucesso.geometry("500x200")
        janela_sucesso.grab_set()  # Torna a janela modal
        
        # Centraliza a janela na tela
        largura_janela = 500
        altura_janela = 200
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_sucesso.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
        
        # Frame principal
        frame_principal = customtkinter.CTkFrame(janela_sucesso, fg_color="#dff0d8", corner_radius=10)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Ícone de sucesso
        icone_sucesso = customtkinter.CTkLabel(
            frame_principal, 
            text="✔️", 
            font=("Arial", 24)
        )
        icone_sucesso.pack(pady=(20, 10))
        
        # Mensagem de sucesso
        lbl_mensagem = customtkinter.CTkLabel(
            frame_principal,
            text=mensagem,
            text_color="#3c763d",
            font=("Arial", 12),
            wraplength=400,
            justify="center"
        )
        lbl_mensagem.pack(padx=20, pady=10)
        
        # Botão OK
        btn_ok = ModernButton(
            frame_principal,
            text="OK",
            command=janela_sucesso.destroy,
            style="success",
            width=100,
            height=35
        )
        btn_ok.pack(pady=(10, 20))
        
        # Configura o que acontece quando a janela é fechada
        janela_sucesso.protocol("WM_DELETE_WINDOW", janela_sucesso.destroy)
        
        # Espera até que a janela seja fechada
        self.wait_window(janela_sucesso)
    
    def criar_botao_voltar(self):
        # Botão voltar (adicionado por último para ficar por cima)
        self.voltar_btn = VoltarButton(
            self, 
            command=self.voltar_callback
        )