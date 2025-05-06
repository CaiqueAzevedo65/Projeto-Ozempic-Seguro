import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.title("Iniciar Sessão")
        self.geometry("1000x600")
        self.configure(bg="#346172")

        # Configuração global
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        # Frame principal de fundo
        self.background_frame = customtkinter.CTkFrame(self, fg_color="#346172")
        self.background_frame.pack(fill="both", expand=True)

        # Criar interface
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_voltar_circular()

    def criar_topo(self):
        # Frame do topo
        top_frame = customtkinter.CTkFrame(self.background_frame, fg_color="white", corner_radius= 0, height=80)
        top_frame.pack(fill="x", side="top")

        # Título
        titulo = customtkinter.CTkLabel(top_frame, text="Iniciar Sessão", font=("Arial", 24, "bold"), text_color="black")
        titulo.pack(side="left", padx=20, pady=20)

        # Logotipo
        try:
            imagem = Image.open("logo.jpg").resize((60, 60))
            self.logo_img = ImageTk.PhotoImage(imagem)  # guardar referência
            logo = customtkinter.CTkLabel(top_frame, image=self.logo_img, text="", bg_color="white")
            logo.pack(side="right", padx=20)
        except FileNotFoundError:
            logo_fallback = customtkinter.CTkLabel(top_frame, text="▲", font=("Arial", 24), text_color="black", bg_color="white")
            logo_fallback.pack(side="right", padx=20)

    def criar_botoes(self):
        main_frame = customtkinter.CTkFrame(self.background_frame, fg_color="#346172")
        main_frame.pack(expand=True)

        # Botão Login
        btn_login = customtkinter.CTkButton(main_frame, text="Login", font=("Arial", 16, "bold"),
                                            width=200, height=50, corner_radius=15,
                                            fg_color="white", text_color="black",
                                            hover_color="#e0e0e0", command=self.login)
        btn_login.grid(row=0, column=0, padx=50, pady=20)

        # Botão Cadastro
        btn_cadastro = customtkinter.CTkButton(main_frame, text="Cadastro de Funcionário", font=("Arial", 16, "bold"),
                                            width=250, height=50, corner_radius=15,
                                            fg_color="white", text_color="black",
                                            hover_color="#e0e0e0", command=self.cadastro_funcionario)
        btn_cadastro.grid(row=0, column=1, padx=50, pady=20)

    def criar_botao_voltar_circular(self):
        canvas = customtkinter.CTkCanvas(self.background_frame, width=60, height=60, bg="#346172", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.85, anchor="center")

        # Círculo branco
        circle = canvas.create_oval(5, 5, 55, 55, fill="white", outline="white")

        # Seta preta no meio
        text = canvas.create_text(30, 30, text="←", font=("Arial", 20, "bold"), fill="black")

        # Evento de clique
        def on_click(event):
            self.voltar()

        canvas.tag_bind(circle, "<Button-1>", on_click)
        canvas.tag_bind(text, "<Button-1>", on_click)

        # Hover: muda a cor do círculo
        def on_enter(event):
            canvas.itemconfig(circle, fill="#e0e0e0", outline="#e0e0e0")

        def on_leave(event):
            canvas.itemconfig(circle, fill="white", outline="white")

        canvas.tag_bind(circle, "<Enter>", on_enter)
        canvas.tag_bind(text, "<Enter>", on_enter)
        canvas.tag_bind(circle, "<Leave>", on_leave)
        canvas.tag_bind(text, "<Leave>", on_leave)


    # Funções dos botões
    def login(self):
        messagebox.showinfo("Login", "Você clicou em Login")

    def cadastro_funcionario(self):
        messagebox.showinfo("Cadastro", "Você clicou em Cadastro de Funcionário")

    def voltar(self):
        messagebox.showinfo("Voltar", "Você clicou no botão de voltar")


if __name__ == "__main__":
    app = App()
    app.mainloop()
