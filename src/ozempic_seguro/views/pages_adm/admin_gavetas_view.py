import customtkinter
from ..components import (
    Header,
    VoltarButton,
    GavetaButtonGrid,
    GavetaButton,
    ToastNotification,
)


class AdminGavetasFrame(customtkinter.CTkFrame):
    BG_COLOR = "#3B6A7D"

    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        super().__init__(master, fg_color=self.BG_COLOR, *args, **kwargs)
        self.voltar_callback = voltar_callback

        # Criar overlay para esconder construção
        self._overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.lift()
        master.update_idletasks()

        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_grade_botoes()
        self.criar_botao_voltar()

        # Remover overlay após tudo estar pronto
        self.update_idletasks()
        self._overlay.destroy()

    def criar_topo(self):
        """Cria o cabeçalho da tela"""
        Header(self, "Administrador - Gerenciar Gavetas")

    def criar_grade_botoes(self):
        """Cria a grade de botões das gavetas"""
        button_data = []
        # Criar 15 gavetas para testar a paginação
        for i in range(1, 16):
            gaveta_id = f"100{i}"
            button_data.append(
                {
                    "text": gaveta_id,
                    "command": lambda x=gaveta_id: self.mostrar_historico_gaveta(x),
                    "name": "gaveta_black.png",
                    "tipo_usuario": "administrador",  # Permite abrir e fechar
                }
            )

        self.grade_botoes = GavetaButtonGrid(self, button_data)

    def mostrar_historico_gaveta(self, gaveta_id):
        """Mostra o histórico de uma gaveta específica"""
        ToastNotification.show(self, f"Carregando histórico da gaveta {gaveta_id}...", "info")
        temp_button = GavetaButton(
            self,
            text=gaveta_id,
            command=None,
            name="gaveta_black.png",
            tipo_usuario="administrador",
        )
        temp_button.mostrar_historico()

    def criar_botao_voltar(self):
        """Cria o botão de voltar usando o componente VoltarButton"""
        self.voltar_btn = VoltarButton(self, command=self.voltar_ao_painel)

    def voltar_ao_painel(self):
        """Volta para o painel principal do administrador"""
        if self.voltar_callback:
            self.pack_forget()
            self.voltar_callback()
