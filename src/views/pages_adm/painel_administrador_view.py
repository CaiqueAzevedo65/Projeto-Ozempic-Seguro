import customtkinter
from tkinter import messagebox
from ..components import Header, FinalizarSessaoButton
from .gerenciamento_usuarios_view import GerenciamentoUsuariosFrame
from .cadastro_usuario_view import CadastroUsuarioFrame
from .diagnostico_view import DiagnosticoFrame
from .parametro_sistemas_view import ParametroSistemasFrame
from .estado_terminal_view import EstadoTerminalFrame
from .historico_view import HistoricoView
from .admin_pastas_view import AdminPastasFrame

class PainelAdministradorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do administrador"""
        # Limpa o frame atual
        for widget in self.winfo_children():
            widget.destroy()
            
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Administrador")

    def criar_botoes(self):
        # Frame principal para centralizar os botões
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)
        
        botoes = [
            {"texto": "Gerenciar Usuários", "comando": self.gerenciar_usuarios},
            {"texto": "Gerenciar Pastas", "comando": self.gerenciar_pastas},
            {"texto": "Cadastro de Usuário", "comando": self.cadastro_usuario},
            {"texto": "Diagnóstico", "comando": self.diagnostico},
            {"texto": "Parâmetros de Sistema", "comando": self.parametro_sistemas},
            {"texto": "Estado do Terminal", "comando": self.estado_terminal},
            {"texto": "Histórico", "comando": self.mostrar_historico}
        ]
        
        # Adiciona os botões em duas colunas
        for i, btn_info in enumerate(botoes):
            row = i // 2
            col = i % 2
            btn = customtkinter.CTkButton(
                main_frame,
                text=btn_info["texto"],
                font=("Arial", 16, "bold"),
                width=250,
                height=50,
                corner_radius=15,
                fg_color="white",
                text_color="black",
                hover_color="#e0e0e0",
                command=btn_info["comando"]
            )
            btn.grid(row=row, column=col, padx=20, pady=15, sticky="nsew")

        # Configura o grid para centralizar
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(tuple(range((len(botoes) + 1) // 2)), weight=1)

    def gerenciar_pastas(self):
        """Abre a tela de gerenciamento de pastas"""
        for widget in self.winfo_children():
            widget.destroy()
        AdminPastasFrame(self, voltar_callback=self.criar_tela_principal)

    def mostrar_historico(self):
        for widget in self.winfo_children():
            widget.destroy()
        HistoricoView(self, voltar_callback=self.criar_tela_principal)

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")

    def gerenciar_usuarios(self):
        for widget in self.winfo_children():
            widget.destroy()
        GerenciamentoUsuariosFrame(self, voltar_callback=self.criar_tela_principal)

    def cadastro_usuario(self):
        for widget in self.winfo_children():
            widget.destroy()
        CadastroUsuarioFrame(self, voltar_callback=self.criar_tela_principal)

    def diagnostico(self):
        for widget in self.winfo_children():
            widget.destroy()
        DiagnosticoFrame(self, voltar_callback=self.criar_tela_principal)

    def parametro_sistemas(self):
        for widget in self.winfo_children():
            widget.destroy()
        ParametroSistemasFrame(self, voltar_callback=self.criar_tela_principal)

    def estado_terminal(self):
        for widget in self.winfo_children():
            widget.destroy()
        EstadoTerminalFrame(self, voltar_callback=self.criar_tela_principal)