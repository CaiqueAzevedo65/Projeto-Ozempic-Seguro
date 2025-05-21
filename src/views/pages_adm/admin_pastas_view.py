import customtkinter
from ..components import Header, VoltarButton, PastaButtonGrid, PastaButton

class AdminPastasFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.voltar_callback = voltar_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_grade_botoes()
        self.criar_botao_voltar()

    def criar_topo(self):
        """Cria o cabeçalho da tela"""
        Header(self, "Administrador - Gerenciar Pastas")

    def criar_grade_botoes(self):
        """Cria a grade de botões das pastas"""
        button_data = []
        for i in range(1, 9):  # 8 pastas (1001 a 1008)
            pasta_id = f"100{i}"
            button_data.append({
                'text': pasta_id,
                'command': lambda x=pasta_id: self.mostrar_historico_pasta(x),
                'name': "pasta_black.png",
                'tipo_usuario': 'administrador'  # Permite abrir e fechar
            })
        
        self.grade_botoes = PastaButtonGrid(self, button_data)

    def mostrar_historico_pasta(self, pasta_id):
        """Mostra o histórico de uma pasta específica"""
        temp_button = PastaButton(
            self, 
            text=pasta_id, 
            command=None, 
            name="pasta_black.png", 
            tipo_usuario='administrador'
        )
        temp_button.mostrar_historico()

    def criar_botao_voltar(self):
        """Cria o botão de voltar usando o componente VoltarButton"""
        self.voltar_btn = VoltarButton(
            self,
            command=self.voltar_ao_painel
        )

    def voltar_ao_painel(self):
        """Volta para o painel principal do administrador"""
        if self.voltar_callback:
            self.pack_forget()
            self.voltar_callback()
