import customtkinter
from tkinter import messagebox
from .components import Header, VoltarButton

class IniciarSessaoFrame(customtkinter.CTkFrame):
    def __init__(self, master, show_login_callback, voltar_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#346172", *args, **kwargs)
        self.show_login_callback = show_login_callback
        self.voltar_callback = voltar_callback
        # Não fazer pack aqui - NavigationController gerencia
        self.criar_topo()
        self.criar_botao_login()
        self.criar_botao_voltar()

    def criar_topo(self):
        Header(self, "Iniciar Sessão")

    def criar_botao_login(self):
        main_frame = customtkinter.CTkFrame(self, fg_color="#346172")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_login = customtkinter.CTkButton(
            main_frame, 
            text="Iniciar Sessão", 
            font=("Arial", 16, "bold"),
            width=300, 
            height=60, 
            corner_radius=15,
            fg_color="white", 
            text_color="black",
            hover_color="#e0e0e0", 
            command=self.show_login_callback
        )
        btn_login.pack(pady=20)

    def criar_botao_voltar(self):
        VoltarButton(self, self.voltar_callback)

    def cadastro_funcionario(self):
        messagebox.showinfo("Cadastro", "Você clicou em Cadastro de Funcionário")