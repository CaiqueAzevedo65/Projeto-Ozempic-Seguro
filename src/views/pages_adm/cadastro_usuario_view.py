import customtkinter
import tkinter as tk
from ..components import Header, VoltarButton, TecladoVirtual
from src.auth import AuthManager

class CadastroUsuarioFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        self.auth_manager = AuthManager()
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_interface_cadastro()
        self.criar_botao_voltar()
        self.criar_teclado_virtual()
        
        # Variável para controlar qual campo está ativo
        self.campo_entrada_atual = None

    def criar_topo(self):
        Header(self, "Cadastro de Usuário")

    def criar_interface_cadastro(self):
        # Frame principal que contém o formulário
        frame_principal = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Frame para o formulário de cadastro
        frame_cadastro = customtkinter.CTkFrame(frame_principal, fg_color="#3B6A7D")
        frame_cadastro.pack(pady=20, padx=20, fill="x")
        
        # Função para definir o campo de entrada atual quando clicado
        def definir_campo_atual(entry):
            self.campo_entrada_atual = entry
            if hasattr(self, 'teclado'):
                self.teclado.definir_entrada(entry)
        
        # Campos de entrada
        campos = [
            ("Nome", "nome_entry"),
            ("Usuário", "usuario_entry"),
            ("Senha", "senha_entry")
        ]
        
        for label, attr_name in campos:
            customtkinter.CTkLabel(
                frame_cadastro, 
                text=label, 
                font=("Arial", 16, "bold"), 
                text_color="white"
            ).pack(anchor="w", pady=(10, 5), padx=20)
            
            # Configuração especial para o campo de senha
            if attr_name == "senha_entry":
                entry = customtkinter.CTkEntry(
                    frame_cadastro, 
                    width=300, 
                    height=40,
                    font=("Arial", 14),
                    show="•"  # Mostra bolinhas no lugar dos caracteres
                )
            else:
                entry = customtkinter.CTkEntry(
                    frame_cadastro, 
                    width=300, 
                    height=40,
                    font=("Arial", 14)
                )
            
            # Configura o evento de clique para definir o campo atual
            entry.bind("<Button-1>", lambda e, entry=entry: definir_campo_atual(entry))
            
            entry.pack(pady=(0, 10), padx=20)
            setattr(self, attr_name, entry)
        
        # Tipo de usuário
        customtkinter.CTkLabel(
            frame_cadastro, 
            text="Tipo de Usuário", 
            font=("Arial", 16, "bold"), 
            text_color="white"
        ).pack(anchor="w", pady=(10, 5), padx=20)
        
        self.tipo_var = customtkinter.StringVar(value="vendedor")
        tipos_usuarios = [
            ("Vendedor", "vendedor"),
            ("Repositor", "repositor"),
            ("Administrador", "administrador"),
            ("Técnico", "tecnico")
        ]
        
        for texto, valor in tipos_usuarios:
            customtkinter.CTkRadioButton(
                frame_cadastro, 
                text=texto, 
                variable=self.tipo_var, 
                value=valor, 
                text_color="white"
            ).pack(anchor="w", padx=20, pady=2)
        
        # Mensagem de status
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
        
        if not all([nome, usuario, senha]):
            self.mostrar_mensagem("Preencha todos os campos!", "erro")
            return
        
        # Chama o método de cadastro do AuthManager
        sucesso, mensagem = self.auth_manager.cadastrar_usuario(nome, usuario, senha, tipo)
        
        if sucesso:
            # Mostra mensagem de sucesso
            self.mostrar_mensagem("Usuário cadastrado com sucesso!", "sucesso")
            self.limpar_campos()
            
            # Mostra mensagem em uma janela de diálogo
            from tkinter import messagebox
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            self.mostrar_mensagem(mensagem, "erro")
    
    def mostrar_mensagem(self, mensagem, tipo):
        cores = {
            "erro": "red",
            "sucesso": "green",
            "info": "yellow"
        }
        self.mensagem_label.configure(text=mensagem, text_color=cores.get(tipo, "white"))
        self.after(5000, lambda: self.mensagem_label.configure(text=""))
    
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