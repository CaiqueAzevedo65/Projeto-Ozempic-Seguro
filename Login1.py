import customtkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.title("Login")
        self.geometry("1000x600")
        self.configure(bg="#346172")

        # Configuração global
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        # Frame de fundo azul que cobre tudo
        self.background_frame = customtkinter.CTkFrame(self, fg_color="#346172")
        self.background_frame.pack(fill="both", expand=True)

        # Criar interface
        self.criar_topo()
        self.criar_interface_login()
        self.criar_teclado_numerico()

    def criar_topo(self):
        # Frame do topo
        top_frame = customtkinter.CTkFrame(self.background_frame, fg_color="white", corner_radius= 0, height=80)
        top_frame.pack(fill="x", side="top")

        # Título
        titulo = customtkinter.CTkLabel(top_frame, text="Login", font=("Arial", 24, "bold"), text_color="black")
        titulo.pack(side="left", padx=20)

        # Logotipo
        try:
            imagem = Image.open("logo.jpg").resize((60, 60))
            self.logo_img = ImageTk.PhotoImage(imagem)
            logo = customtkinter.CTkLabel(top_frame, image=self.logo_img, text="", bg_color="white")
            logo.pack(side="right", padx=20)
        except:
            fallback = customtkinter.CTkLabel(top_frame, text="▲", font=("Arial", 24), text_color="black", bg_color="white")
            fallback.pack(side="right", padx=20)

    def criar_interface_login(self):
        frame_login = customtkinter.CTkFrame(self.background_frame, fg_color="#2F6073")
        frame_login.place(x=40, y=100)

        customtkinter.CTkLabel(frame_login, text="Usuário", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(0, 5))
        self.usuario_entry = customtkinter.CTkEntry(frame_login, width=300, height=40)
        self.usuario_entry.pack(pady=10)

        customtkinter.CTkLabel(frame_login, text="Senha", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(20, 5))
        self.senha_entry = customtkinter.CTkEntry(frame_login, width=300, height=40, show="*")
        self.senha_entry.pack(pady=10)

        # Digital
        try:
            digital = Image.open("digital.png").resize((70, 70))
            self.digital_img = ImageTk.PhotoImage(digital)
            digital_label = customtkinter.CTkLabel(frame_login, image=self.digital_img, text="", bg_color="#2F6073")
            digital_label.pack(pady=30)
        except:
            digital_label = customtkinter.CTkLabel(frame_login, text="🔒", font=("Arial", 40), text_color="white", bg_color="#2F6073")
            digital_label.pack(pady=30)

        # Botão circular voltar
        btn_voltar = customtkinter.CTkButton(self, text="←", width=50, height=50, corner_radius=25,
                                            fg_color="white", text_color="black", command=self.voltar)
        btn_voltar.place(x=420, y=480)

    def criar_teclado_numerico(self):
        teclado_frame = customtkinter.CTkFrame(self.background_frame, fg_color="white", corner_radius=20)
        teclado_frame.place(x=520, y=100)

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

    def tecla(self, valor):
        if valor == "Apagar":
            self.senha_entry.delete(len(self.senha_entry.get()) - 1, tk.END)
        elif valor == "Cancelar":
            self.senha_entry.delete(0, tk.END)
        elif valor == "Confirmar":
            messagebox.showinfo("Confirmado", "Senha confirmada!")
        else:
            self.senha_entry.insert(tk.END, valor)

    def voltar(self):
        messagebox.showinfo("Voltar", "Você clicou em voltar")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
