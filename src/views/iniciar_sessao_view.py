import customtkinter
from tkinter import messagebox
from PIL import Image
import os
from ..utils.image_utils import load_image_as_ctk_image
from .components import Header

class IniciarSessaoFrame(customtkinter.CTkFrame):
    def __init__(self, master, show_login_callback, *args, **kwargs):
        super().__init__(master, fg_color="#346172", *args, **kwargs)
        self.show_login_callback = show_login_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_voltar_circular()

    def criar_topo(self):
        Header(self, "Iniciar Sessão")

    def criar_botoes(self):
        main_frame = customtkinter.CTkFrame(self, fg_color="#346172")
        main_frame.pack(expand=True)
        btn_login = customtkinter.CTkButton(main_frame, text="Login", font=("Arial", 16, "bold"),
                                            width=200, height=50, corner_radius=15,
                                            fg_color="white", text_color="black",
                                            hover_color="#e0e0e0", command=self.show_login_callback)
        btn_login.grid(row=0, column=0, padx=50, pady=20)
        btn_cadastro = customtkinter.CTkButton(main_frame, text="Cadastro de Funcionário", font=("Arial", 16, "bold"),
                                            width=250, height=50, corner_radius=15,
                                            fg_color="white", text_color="black",
                                            hover_color="#e0e0e0", command=self.cadastro_funcionario)
        btn_cadastro.grid(row=0, column=1, padx=50, pady=20)

    def criar_botao_voltar_circular(self):
        # Botão circular voltar
        btn_voltar = customtkinter.CTkButton(
            self,
            text="←",
            width=50,
            height=50,
            corner_radius=25,
            fg_color="white",
            text_color="black",
            hover_color="#e0e0e0",
            command=lambda: messagebox.showinfo("Voltar", "Você clicou no botão de voltar")
        )
        btn_voltar.place(relx=0.5, rely=0.85, anchor="center")

    def cadastro_funcionario(self):
        messagebox.showinfo("Cadastro", "Você clicou em Cadastro de Funcionário") 