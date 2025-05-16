# src/views/gerenciamento_usuarios_view.py
import customtkinter
from .components import Header, FinalizarSessaoButton

class GerenciamentoUsuariosFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_botao_voltar()

    def criar_topo(self):
        Header(self, "Gerenciamento de Usuários")

    def criar_botao_voltar(self):
        # Você pode usar o FinalizarSessaoButton, mas com texto "Voltar"
        # Ou criar um botão simples, como abaixo:
        btn_voltar = customtkinter.CTkButton(
            self,
            text="Voltar",
            font=("Arial", 16, "bold"),
            width=120,
            height=40,
            fg_color="white",
            text_color="black",
            hover_color="#e0e0e0",
            command=self.voltar
        )
        btn_voltar.place(relx=0.5, rely=0.9, anchor="center")  # Centralizado na parte de baixo

    def voltar(self):
        if self.voltar_callback:
            self.pack_forget()
            self.voltar_callback()