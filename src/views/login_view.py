import customtkinter
import tkinter as tk
from tkinter import messagebox
from .pages_adm.painel_administrador_view import PainelAdministradorFrame
from .components import Header, ImageCache, VoltarButton
from ..auth import AuthManager
from src.session_manager import SessionManager
from .repositor_view import RepositorFrame
from .vendedor_view import VendedorFrame

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, show_iniciar_callback, *args, **kwargs):
        super().__init__(master, fg_color="#346172", *args, **kwargs)
        self.show_iniciar_callback = show_iniciar_callback
        self.auth_manager = AuthManager()
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_interface_login()
        self.criar_teclado_numerico()
        self.criar_botao_voltar()

    def criar_topo(self):
        Header(self, "Login")

    def criar_interface_login(self):
        frame_login = customtkinter.CTkFrame(self, fg_color="#346172")
        frame_login.place(x=40, y=100)
        
        # Campo de usuário
        customtkinter.CTkLabel(frame_login, text="Usuário", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(0, 5))
        self.usuario_entry = customtkinter.CTkEntry(frame_login, width=300, height=40)
        self.usuario_entry.pack(pady=10)
        self.usuario_entry.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.usuario_entry))
        
        # Campo de senha
        customtkinter.CTkLabel(frame_login, text="Senha", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(20, 5))
        self.senha_entry = customtkinter.CTkEntry(frame_login, width=300, height=40, show="*")
        self.senha_entry.pack(pady=10)
        self.senha_entry.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.senha_entry))
        
        # Campo ativo por padrão
        self.campo_ativo = self.usuario_entry
        
        try:
            digital_img = ImageCache.get_digital()
            digital_label = customtkinter.CTkLabel(frame_login, image=digital_img, text="", bg_color="#2F6073")
            digital_label.pack(pady=30)
        except:
            digital_label = customtkinter.CTkLabel(frame_login, text="🔒", font=("Arial", 40), text_color="white", bg_color="#2F6073")
            digital_label.pack(pady=30)

    def criar_botao_voltar(self):
        VoltarButton(self, self.show_iniciar_callback)

    def criar_teclado_numerico(self):
        teclado_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=20)
        teclado_frame.place(x=500, y=100)
        botoes = [
            ["1", "2", "3", "Confirmar"],
            ["4", "5", "6", "Apagar"],
            ["7", "8", "9", "Cancelar"],
            ["", "0", "", ""]
        ]
        for i, linha in enumerate(botoes):
            for j, texto in enumerate(linha):
                if texto:
                    btn = customtkinter.CTkButton(teclado_frame, text=texto, width=100, height=60,
                                                font=("Arial", 18, "bold"), fg_color="#D9D9D9",
                                                text_color="black", hover_color="#c0c0c0",
                                                command=lambda t=texto: self.tecla(t))
                    btn.grid(row=i, column=j, padx=10, pady=10)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        user = self.auth_manager.autenticar(usuario, senha)
        if user:
            # Define o usuário atual no SessionManager
            session_manager = SessionManager.get_instance()
            session_manager.set_current_user(user)
            
            if user.get('tipo') == 'administrador':
                self.abrir_painel_administrador()
            elif user.get('tipo') == 'repositor':
                self.abrir_painel_repositor()
            elif user.get('tipo') == 'vendedor':
                self.abrir_painel_vendedor()
            else:
                messagebox.showinfo("Sucesso", f"Login realizado como {user.get('tipo','usuário')}!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_painel_vendedor(self):
        self.pack_forget()
        VendedorFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def abrir_painel_repositor(self):
        self.pack_forget()
        RepositorFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def abrir_painel_administrador(self):
        self.pack_forget()
        PainelAdministradorFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def definir_campo_ativo(self, campo):
        """Define qual campo está ativo para receber entrada do teclado"""
        self.campo_ativo = campo

    def tecla(self, valor):
        if valor == "Apagar":
            if self.campo_ativo == self.usuario_entry:
                self.usuario_entry.delete(len(self.usuario_entry.get()) - 1, tk.END)
            else:
                self.senha_entry.delete(len(self.senha_entry.get()) - 1, tk.END)
        elif valor == "Cancelar":
            if self.campo_ativo == self.usuario_entry:
                self.usuario_entry.delete(0, tk.END)
            else:
                self.senha_entry.delete(0, tk.END)
        elif valor == "Confirmar":
            self.verificar_login()
        else:
            self.campo_ativo.insert(tk.END, valor) 