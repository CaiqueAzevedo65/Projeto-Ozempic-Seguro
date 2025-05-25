import customtkinter
from tkinter import messagebox
from .components import Header, FinalizarSessaoButton
from .pages_adm.diagnostico_view import DiagnosticoFrame
from .pages_adm.parametro_sistemas_view import ParametroSistemasFrame
from .pages_adm.estado_terminal_view import EstadoTerminalFrame

class TecnicoFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do técnico"""
        # Limpa o frame atual
        for widget in self.winfo_children():
            widget.destroy()
            
        self.criar_topo()
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Técnico")

    def criar_botoes(self):
        # Frame principal para centralizar os botões
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)
        
        botoes = [
            {"texto": "Diagnóstico", "comando": self.abrir_diagnostico},
            {"texto": "Parâmetros de Sistema", "comando": self.abrir_parametros_sistema},
            {"texto": "Estado do Terminal", "comando": self.abrir_estado_terminal}
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

        
    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")
            
    def abrir_diagnostico(self):
        """Abre a tela de diagnóstico"""
        for widget in self.winfo_children():
            widget.destroy()
        DiagnosticoFrame(self, self.voltar_para_principal)
        
    def abrir_parametros_sistema(self):
        """Abre a tela de parâmetros do sistema"""
        for widget in self.winfo_children():
            widget.destroy()
        ParametroSistemasFrame(self, self.voltar_para_principal)
        
    def abrir_estado_terminal(self):
        """Abre a tela de estado do terminal"""
        for widget in self.winfo_children():
            widget.destroy()
        EstadoTerminalFrame(self, self.voltar_para_principal)
        
    def voltar_para_principal(self):
        """Volta para a tela principal do técnico"""
        self.criar_tela_principal()
