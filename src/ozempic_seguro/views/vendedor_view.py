import customtkinter
from tkinter import messagebox
from .components import Header, FinalizarSessaoButton, GavetaButtonGrid, GavetaButton

class VendedorFrame(customtkinter.CTkFrame):
    def __init__(self, master, finalizar_sessao_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.finalizar_sessao_callback = finalizar_sessao_callback
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_grade_botoes()
        self.criar_botao_finalizar()

    def criar_topo(self):
        Header(self, "Vendedor")

    def criar_grade_botoes(self):
        button_data = []
        # Criar 15 gavetas para testar a paginação
        for i in range(1, 16):
            gaveta_id = f"100{i}"
            button_data.append({
                'text': gaveta_id,
                'command': lambda x=gaveta_id: self.mostrar_historico_gaveta(x),
                'name': "gaveta_black.png",
                'tipo_usuario': 'vendedor'  # Permite apenas abrir
            })
        
        self.grade_botoes = GavetaButtonGrid(self, button_data)

    def mostrar_historico_gaveta(self, gaveta_id):
        """Mostra o histórico de uma gaveta específica"""
        # Cria uma instância temporária do botão para acessar o método mostrar_historico
        temp_button = GavetaButton(
            self, 
            text=gaveta_id, 
            command=None, 
            name="gaveta_black.png", 
            tipo_usuario='vendedor'
        )
        temp_button.mostrar_historico()

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")