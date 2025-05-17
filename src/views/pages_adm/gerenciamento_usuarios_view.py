# src/views/gerenciamento_usuarios_view.py
import customtkinter
from ..components import Header, VoltarButton

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
        VoltarButton(self, self.voltar_callback)