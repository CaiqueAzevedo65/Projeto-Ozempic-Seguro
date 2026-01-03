"""
Componente de teclado virtual: TecladoVirtual
"""
import customtkinter


class TecladoVirtual(customtkinter.CTkFrame):
    """Teclado virtual para entrada de dados"""

    LAYOUT = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ç"],
        ["z", "x", "c", "v", "b", "n", "m"],
        ["MAIÚSCULAS", "LIMPAR", "ESPAÇO"],
    ]

    def __init__(self, master, entrada_atual=None, comando_salvar=None, **kwargs):
        super().__init__(master, fg_color="#f0f0f0", corner_radius=10, **kwargs)
        self.entrada_atual = entrada_atual
        self.comando_salvar = comando_salvar
        self.maiusculas_ativado = False
        self.btn_maiusculas = None
        self.criar_teclado()

    def criar_teclado(self):
        """Cria o layout do teclado"""
        for i, linha in enumerate(self.LAYOUT):
            self.grid_rowconfigure(i, weight=1)

            if i == len(self.LAYOUT) - 2:  # Penúltima linha
                self._criar_linha_com_acoes(i, linha)
            elif i == len(self.LAYOUT) - 1:  # Última linha
                self._criar_linha_funcoes(i)
            else:
                self._criar_linha_normal(i, linha)

    def _criar_linha_normal(self, row, linha):
        """Cria uma linha normal de teclas"""
        for j in range(10):
            self.grid_columnconfigure(j, weight=1)

        for j, tecla in enumerate(linha):
            tecla_exibida = tecla.upper() if self.maiusculas_ativado and tecla.isalpha() else tecla

            btn = customtkinter.CTkButton(
                self,
                text=tecla_exibida,
                height=40,
                font=("Arial", 12, "bold"),
                fg_color="#ffffff",
                text_color="#000000",
                hover_color="#e0e0e0",
                corner_radius=5,
                command=lambda t=tecla: self.tecla_pressionada(t),
            )
            btn.grid(row=row, column=j, padx=2, pady=2, sticky="nsew")

    def _criar_linha_com_acoes(self, row, linha):
        """Cria a penúltima linha com botões de ação"""
        for j in range(10):
            self.grid_columnconfigure(j, weight=1)

        # Letras
        for j, tecla in enumerate(linha):
            btn = customtkinter.CTkButton(
                self,
                text=tecla.upper() if self.maiusculas_ativado else tecla,
                height=40,
                font=("Arial", 12, "bold"),
                fg_color="#ffffff",
                text_color="#000000",
                hover_color="#e0e0e0",
                corner_radius=5,
                command=lambda t=tecla: self.tecla_pressionada(t),
            )
            btn.grid(row=row, column=j, padx=2, pady=2, sticky="nsew")

        # Botão SALVAR
        btn_salvar = customtkinter.CTkButton(
            self,
            text="SALVAR",
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#2ecc71",
            text_color="white",
            hover_color="#27ae60",
            corner_radius=5,
            command=lambda: self.tecla_pressionada("SALVAR"),
        )
        btn_salvar.grid(row=row, column=7, columnspan=2, padx=2, pady=2, sticky="nsew")

        # Botão Apagar
        btn_apagar = customtkinter.CTkButton(
            self,
            text="⌫",
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#e74c3c",
            text_color="white",
            hover_color="#c0392b",
            corner_radius=5,
            command=lambda: self.tecla_pressionada("⌫"),
        )
        btn_apagar.grid(row=row, column=9, padx=2, pady=2, sticky="nsew")

    def _criar_linha_funcoes(self, row):
        """Cria a última linha com botões de função"""
        for j in range(10):
            self.grid_columnconfigure(j, weight=1)

        # MAIÚSCULAS
        self.btn_maiusculas = customtkinter.CTkButton(
            self,
            text="MAIÚSCULAS",
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#3498db" if self.maiusculas_ativado else "#ffffff",
            text_color="#ffffff" if self.maiusculas_ativado else "#000000",
            hover_color="#2980b9" if self.maiusculas_ativado else "#e0e0e0",
            corner_radius=5,
            command=lambda: self.tecla_pressionada("MAIÚSCULAS"),
        )
        self.btn_maiusculas.grid(row=row, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")

        # LIMPAR
        customtkinter.CTkButton(
            self,
            text="LIMPAR",
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#ffffff",
            text_color="#000000",
            hover_color="#e0e0e0",
            corner_radius=5,
            command=lambda: self.tecla_pressionada("LIMPAR"),
        ).grid(row=row, column=2, columnspan=2, padx=2, pady=2, sticky="nsew")

        # ESPAÇO
        customtkinter.CTkButton(
            self,
            text="______",
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#ffffff",
            text_color="#000000",
            hover_color="#e0e0e0",
            corner_radius=5,
            command=lambda: self.tecla_pressionada(" "),
        ).grid(row=row, column=4, columnspan=6, padx=2, pady=2, sticky="nsew")

    def tecla_pressionada(self, tecla):
        """Processa a tecla pressionada"""
        if not self.entrada_atual:
            return

        if tecla == "⌫":
            texto_atual = self.entrada_atual.get()
            self.entrada_atual.delete(0, "end")
            self.entrada_atual.insert(0, texto_atual[:-1])
        elif tecla == "LIMPAR":
            self.entrada_atual.delete(0, "end")
        elif tecla == "SALVAR" and self.comando_salvar:
            self.comando_salvar()
        elif tecla == "MAIÚSCULAS":
            self.maiusculas_ativado = not self.maiusculas_ativado

            if self.btn_maiusculas:
                self.btn_maiusculas.configure(
                    fg_color="#3498db" if self.maiusculas_ativado else "#ffffff",
                    text_color="#ffffff" if self.maiusculas_ativado else "#000000",
                    hover_color="#2980b9" if self.maiusculas_ativado else "#e0e0e0",
                )

            # Reconstrói o teclado
            for widget in self.winfo_children():
                widget.destroy()
            self.criar_teclado()
        else:
            tecla_inserida = tecla.upper() if self.maiusculas_ativado and tecla.isalpha() else tecla
            self.entrada_atual.insert("end", tecla_inserida)

    def definir_entrada(self, entrada):
        """Define o campo de entrada ativo"""
        self.entrada_atual = entrada
