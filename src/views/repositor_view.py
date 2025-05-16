import customtkinter
from tkinter import messagebox
from PIL import Image
import os
from .components import Header, FinalizarSessaoButton, PastaButtonGrid

class RepositorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_grade_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Repositor")

    def criar_grade_botoes(self):
        # Dados dos botões da grade 4x2
        button_data = [
            {'text': "1001", 'command': lambda: print("Pasta 1001")},
            {'text': "1002", 'command': lambda: print("Pasta 1002")},
            {'text': "1003", 'command': lambda: print("Pasta 1003")},
            {'text': "1004", 'command': lambda: print("Pasta 1004")},
            {'text': "1005", 'command': lambda: print("Pasta 1005")},
            {'text': "1006", 'command': lambda: print("Pasta 1006")},
            {'text': "1007", 'command': lambda: print("Pasta 1007")},
            {'text': "1008", 'command': lambda: print("Pasta 1008")}
        ]
        
        # Criar a grade de botões
        self.grade_botoes = PastaButtonGrid(self, button_data)

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")
