import customtkinter
import tkinter as tk
from ..components import Header, VoltarButton, TecladoVirtual, ModernButton, ModernConfirmDialog, ToastNotification
from ...services.service_factory import get_user_service

class CadastroUsuarioFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        self.user_service = get_user_service()
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Configuração da validação de entrada
        self.vcmd_nome = (self.register(self.validar_entrada_nome), '%P')
        self.vcmd_numerico = (self.register(self.validar_entrada_numerica), '%P')
        
        # Inicializa os temporizadores
        self.erro_timer = None
        self.mensagem_timer = None
        
        self.criar_topo()
        self.criar_interface_cadastro()
        self.criar_botao_voltar()
        self.criar_teclado_virtual()
        
        # Variável para controlar qual campo está ativo
        self.campo_entrada_atual = None

    def validar_entrada_numerica(self, valor):
        """Valida se a entrada contém apenas números e tem no máximo 8 caracteres"""
        if len(valor) > 8:  # Limite de 8 caracteres
            return False
        if valor == "":  # Permite campo vazio para poder apagar
            return True
        return valor.isdigit()
    
    def validar_entrada_nome(self, valor):
        """Valida se o nome tem no máximo 26 caracteres"""
        return len(valor) <= 26

    def criar_topo(self):
        Header(self, "Cadastro de Usuário")

    def criar_interface_cadastro(self):
        # Frame principal que contém o formulário
        frame_principal = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(side="left", fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Frame para o formulário de cadastro
        frame_cadastro = customtkinter.CTkFrame(frame_principal, fg_color="#3B6A7D")
        frame_cadastro.pack(pady=(0, 20), padx=20, fill="x")
        
        # Função para definir o campo de entrada atual quando clicado
        def definir_campo_atual(entry):
            self.campo_entrada_atual = entry
            if hasattr(self, 'teclado'):
                self.teclado.definir_entrada(entry)
        
        # Campo de Nome (aceita letras)
        customtkinter.CTkLabel(
            frame_cadastro, 
            text="Nome (máx. 26 caracteres)", 
            font=("Arial", 16, "bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(10, 5), padx=20)
        
        self.nome_entry = customtkinter.CTkEntry(
            frame_cadastro, 
            width=300, 
            height=40,
            font=("Arial", 14),
            validate="key",
            validatecommand=self.vcmd_nome
        )
        self.nome_entry.pack(pady=(0, 10), padx=20)
        self.nome_entry.bind("<Button-1>", lambda e: definir_campo_atual(self.nome_entry))
        
        # Campo de Usuário (aceita apenas números)
        customtkinter.CTkLabel(
            frame_cadastro, 
            text="Usuário (máx. 8 dígitos)", 
            font=("Arial", 16, "bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(10, 5), padx=20)
        
        self.usuario_entry = customtkinter.CTkEntry(
            frame_cadastro, 
            width=300, 
            height=40,
            font=("Arial", 14),
            validate="key",
            validatecommand=self.vcmd_numerico
        )
        self.usuario_entry.pack(pady=(0, 10), padx=20)
        self.usuario_entry.bind("<Button-1>", lambda e: definir_campo_atual(self.usuario_entry))
        
        # Campo de senha com mensagem de erro abaixo
        customtkinter.CTkLabel(
            frame_cadastro, 
            text="Senha (máx. 8 dígitos)", 
            font=("Arial", 16, "bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(10, 5), padx=20)
        
        self.senha_entry = customtkinter.CTkEntry(
            frame_cadastro, 
            width=300, 
            height=40,
            font=("Arial", 14),
            show="•",  # Mostra bolinhas no lugar dos caracteres
            validate="key",
            validatecommand=self.vcmd_numerico
        )
        self.senha_entry.pack(pady=(0, 5), padx=20)
        self.senha_entry.bind("<Button-1>", lambda e: definir_campo_atual(self.senha_entry))
        
        # Label para mensagem de erro (inicialmente vazia)
        self.lbl_erro_senha = customtkinter.CTkLabel(
            frame_cadastro,
            text="",
            text_color="red",
            font=("Arial", 12, "bold"),
            fg_color="transparent"
        )
        self.lbl_erro_senha.pack(anchor="w", padx=20, pady=(0, 5))  # Reduzido o padding vertical inferior
        
        # Tipo de usuário
        tipo_usuario_frame = customtkinter.CTkFrame(frame_cadastro, fg_color="transparent")
        tipo_usuario_frame.pack(anchor="w", fill="x", padx=20, pady=(0, 10))  # Ajustado o padding vertical
        
        customtkinter.CTkLabel(
            tipo_usuario_frame, 
            text="Tipo de Usuário", 
            font=("Arial", 16, "bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(0, 5), padx=20)
        
        self.tipo_var = customtkinter.StringVar(value="vendedor")
        tipos_usuarios = [
            ("Vendedor", "vendedor"),
            ("Repositor", "repositor"),
            ("Administrador", "administrador"),
            ("Técnico", "tecnico")
        ]
        
        for texto, valor in tipos_usuarios:
            customtkinter.CTkRadioButton(
                tipo_usuario_frame, 
                text=texto, 
                variable=self.tipo_var, 
                value=valor, 
                text_color="white"
            ).pack(anchor="w", padx=20, pady=2)
        
        # Mensagem de status (para mensagens de sucesso/informação)
        self.mensagem_label = customtkinter.CTkLabel(
            frame_cadastro, 
            text="", 
            text_color="yellow",
            font=("Arial", 12)
        )
        self.mensagem_label.pack(pady=10, padx=20)
        
        # Define o primeiro campo como ativo por padrão
        if hasattr(self, 'nome_entry'):
            definir_campo_atual(self.nome_entry)
    
    def criar_teclado_virtual(self):
        # Frame para o teclado
        frame_teclado = customtkinter.CTkFrame(self, fg_color="transparent", width=600, height=750)  # Largura e Altura fixa
        frame_teclado.pack(side="right", fill="y", padx=20, pady=20)
        frame_teclado.pack_propagate(False)  # Impede que o frame redimensione automaticamente
        
        # Título do teclado
        customtkinter.CTkLabel(
            frame_teclado,
            text=""
        ).pack(pady=(0, 10))
        
        # Cria o teclado virtual dentro de um frame com rolagem se necessário
        container = customtkinter.CTkFrame(frame_teclado, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        self.teclado = TecladoVirtual(
            container,
            entrada_atual=self.campo_entrada_atual,
            comando_salvar=self.salvar_usuario
        )
        self.teclado.pack(fill="both", expand=True, pady=10)
    
    def criar_botao_voltar(self):
        # Cria um frame para o botão de voltar no canto inferior esquerdo
        frame_voltar = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_voltar.pack(side="bottom", anchor="sw", padx=20, pady=20)
        VoltarButton(frame_voltar, self.voltar_callback)
    
    def salvar_usuario(self):
        nome = self.nome_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get()
        tipo = self.tipo_var.get()
        
        # Limpa mensagens de erro anteriores
        self.lbl_erro_senha.configure(text="")
        
        # Validação dos campos obrigatórios
        if not all([nome, usuario, senha]):
            self.mostrar_mensagem("Preencha todos os campos!", "erro")
            return
            
        # Validação do tamanho do nome
        if len(nome) > 26:
            self.mostrar_mensagem("O nome deve ter no máximo 26 caracteres!", "erro")
            return
            
        # Validação do tamanho do usuário
        if len(usuario) > 8:
            self.mostrar_mensagem("O usuário deve ter no máximo 8 dígitos!", "erro")
            return
            
        # Validação do tamanho da senha
        if len(senha) > 8:
            self.mostrar_mensagem("A senha deve ter no máximo 8 dígitos!", "erro")
            return
            
        if len(senha) < 4:
            self.mostrar_mensagem("A senha deve ter no mínimo 4 caracteres!", "erro")
            return
            
        # Validação de campos numéricos
        if not usuario.isdigit():
            self.mostrar_mensagem("O usuário deve conter apenas números!", "erro")
            return
            
        if not senha.isdigit():
            self.mostrar_mensagem("A senha deve conter apenas números!", "erro")
            return
        
        # Confirmar antes de salvar
        if not ModernConfirmDialog.ask(
            self,
            "Confirmar Cadastro",
            f"Deseja cadastrar o usuário '{nome}' do tipo '{tipo}'?",
            icon="question",
            confirm_text="Cadastrar",
            cancel_text="Cancelar"
        ):
            return
        
        # Chama o método de cadastro do AuthManager
        sucesso, mensagem = self.user_service.create_user(nome, usuario, senha, tipo)
        
        if sucesso:
            # Mostra notificação de sucesso moderna
            ToastNotification.show(self, f"Usuário '{nome}' cadastrado com sucesso!", "success")
            self.limpar_campos()
        else:
            ToastNotification.show(self, f"Erro: {mensagem}", "error")
    
    def mostrar_mensagem(self, mensagem, tipo):
        cores = {
            "erro": "red",
            "sucesso": "green",
            "info": "yellow"
        }
        
        # Cancela o temporizador anterior se existir
        if tipo == "erro":
            if self.erro_timer is not None:
                self.after_cancel(self.erro_timer)
        else:
            if self.mensagem_timer is not None:
                self.after_cancel(self.mensagem_timer)
        
        if tipo == "erro":
            # Exibe a mensagem de erro no label apropriado
            self.lbl_erro_senha.configure(text=mensagem, text_color=cores[tipo])
            # Define um novo temporizador
            self.erro_timer = self.after(5000, self.limpar_mensagem_erro)
        else:
            # Para outros tipos de mensagem (sucesso, info), usa o label normal
            self.mensagem_label.configure(text=mensagem, text_color=cores.get(tipo, "white"))
            self.mensagem_timer = self.after(5000, self.limpar_mensagem_normal)
    
    def limpar_mensagem_erro(self):
        self.lbl_erro_senha.configure(text="")
        self.erro_timer = None
    
    def limpar_mensagem_normal(self):
        self.mensagem_label.configure(text="")
        self.mensagem_timer = None
    
    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.tipo_var.set("vendedor")
        # Volta o foco para o primeiro campo
        if hasattr(self, 'nome_entry'):
            self.nome_entry.focus_set()
            self.campo_entrada_atual = self.nome_entry
            if hasattr(self, 'teclado'):
                self.teclado.definir_entrada(self.nome_entry)