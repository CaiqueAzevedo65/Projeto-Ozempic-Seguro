import customtkinter
from tkinter import messagebox
from ..components import Header, MainButton, FinalizarSessaoButton
from .gerenciamento_usuarios_view import GerenciamentoUsuariosFrame

class PainelAdministradorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Administrador")

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
        btn1 = MainButton(botoes_frame, text=botoes[0][0], command=botoes[0][1])
        btn1.grid(row=0, column=0, padx=30, pady=20)
        btn2 = MainButton(botoes_frame, text=botoes[1][0], command=botoes[1][1])
        btn2.grid(row=0, column=1, padx=30, pady=20)
        btn3 = MainButton(botoes_frame, text=botoes[2][0], command=botoes[2][1])
        btn3.grid(row=1, column=0, padx=30, pady=20)
        btn4 = MainButton(botoes_frame, text=botoes[3][0], command=botoes[3][1])
        btn4.grid(row=1, column=1, padx=30, pady=20)
        btn5 = MainButton(botoes_frame, text=botoes[4][0], command=botoes[4][1])
        btn5.grid(row=2, column=0, columnspan=2, pady=20)

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()  # Apenas esconde o frame atual ao invés de destruí-lo
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")

    def gerenciar_usuarios(self):
        # Remove todos os widgets atuais da tela
        for widget in self.master.winfo_children():
            widget.destroy()
        # Cria e exibe a tela de gerenciamento de usuários
        GerenciamentoUsuariosFrame(self.master, voltar_callback=self.voltar_para_painel)

    def voltar_para_painel(self):
        # Volta para o painel do administrador
        # Remove todos os widgets atuais da tela
        for widget in self.master.winfo_children():
            widget.destroy()
        # Recria o painel do administrador
        PainelAdministradorFrame(self.master, finalizar_sessao_callback=self.finalizar_sessao_callback)

    def cadastro_usuario(self):
        messagebox.showinfo("Cadastro de Usuário", "Você clicou em Cadastro de Usuário.")

    def diagnostico(self):
        messagebox.showinfo("Diagnóstico", "Você clicou em Diagnóstico.")

    def parametro_sistemas(self):
        messagebox.showinfo("Parâmetro de Sistemas", "Você clicou em Parâmetro de Sistemas.")

    def estado_terminal(self):
        messagebox.showinfo("Estado Terminal", "Você clicou em Estado Terminal.") 