import customtkinter
from tkinter import messagebox
from PIL import Image
import os

class PainelAdministradorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        top_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=0, height=80)
        top_frame.pack(fill="x", side="top")
        titulo = customtkinter.CTkLabel(top_frame, text="Administrador", font=("Arial", 20, "bold"), text_color="black")
        titulo.pack(side="left", padx=20, pady=20)
        # Substituir símbolo pelo logo.jpg
        try:
            from PIL import ImageTk
            logo_path = os.path.join("src", "assets", "logo.jpg")
            imagem = Image.open(logo_path).resize((60, 60))
            self.logo_img = customtkinter.CTkImage(imagem, size=(60, 60))
            logo = customtkinter.CTkLabel(top_frame, image=self.logo_img, text="", bg_color="white")
            logo.pack(side="right", padx=20)
        except Exception as e:
            logo = customtkinter.CTkLabel(top_frame, text="▲", font=("Arial", 24), text_color="black", bg_color="white")
            logo.pack(side="right", padx=20)

    def criar_botoes(self):
        botoes_frame = customtkinter.CTkFrame(self, fg_color="#3B6A7D")
        botoes_frame.pack(expand=True)
        botoes = [
            ("Gerenciar Usuários", self.gerenciar_usuarios),
            ("Cadastro de Usuário", self.cadastro_usuario),
            ("Diagnóstico", self.diagnostico),
            ("Parâmetro de Sistemas", self.parametro_sistemas),
            ("Estado Terminal", self.estado_terminal)
        ]
        # Layout 2x2 + 1
        btn1 = customtkinter.CTkButton(botoes_frame, text=botoes[0][0], width=220, height=60, font=("Arial", 16, "bold"), command=botoes[0][1])
        btn1.grid(row=0, column=0, padx=30, pady=20)
        btn2 = customtkinter.CTkButton(botoes_frame, text=botoes[1][0], width=220, height=60, font=("Arial", 16, "bold"), command=botoes[1][1])
        btn2.grid(row=0, column=1, padx=30, pady=20)
        btn3 = customtkinter.CTkButton(botoes_frame, text=botoes[2][0], width=220, height=60, font=("Arial", 16, "bold"), command=botoes[2][1])
        btn3.grid(row=1, column=0, padx=30, pady=20)
        btn4 = customtkinter.CTkButton(botoes_frame, text=botoes[3][0], width=220, height=60, font=("Arial", 16, "bold"), command=botoes[3][1])
        btn4.grid(row=1, column=1, padx=30, pady=20)
        btn5 = customtkinter.CTkButton(botoes_frame, text=botoes[4][0], width=220, height=60, font=("Arial", 16, "bold"), command=botoes[4][1])
        btn5.grid(row=2, column=0, columnspan=2, pady=20)

    def criar_botao_finalizar(self):
        btn_finalizar = customtkinter.CTkButton(self, text="✗", width=60, height=60, corner_radius=30, fg_color="white", text_color="red", font=("Arial", 28, "bold"), command=self.finalizar_sessao)
        btn_finalizar.place(relx=0.5, rely=0.88, anchor="center")
        label = customtkinter.CTkLabel(self, text="Finalizar sessão", font=("Arial", 12), text_color="white", fg_color="#3B6A7D")
        label.place(relx=0.5, rely=0.97, anchor="center")

    def finalizar_sessao(self):
        # Garante que o callback de finalizar sessão volta para a tela inicial
        if self.finalizar_sessao_callback:
            for widget in self.master.winfo_children():
                widget.destroy()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")

    def gerenciar_usuarios(self):
        messagebox.showinfo("Gerenciar Usuários", "Você clicou em Gerenciar Usuários.")

    def cadastro_usuario(self):
        messagebox.showinfo("Cadastro de Usuário", "Você clicou em Cadastro de Usuário.")

    def diagnostico(self):
        messagebox.showinfo("Diagnóstico", "Você clicou em Diagnóstico.")

    def parametro_sistemas(self):
        messagebox.showinfo("Parâmetro de Sistemas", "Você clicou em Parâmetro de Sistemas.")

    def estado_terminal(self):
        messagebox.showinfo("Estado Terminal", "Você clicou em Estado Terminal.") 