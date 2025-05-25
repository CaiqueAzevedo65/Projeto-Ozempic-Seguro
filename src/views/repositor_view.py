import customtkinter
from tkinter import messagebox
from .components import Header, FinalizarSessaoButton, PastaButtonGrid, PastaButton

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
        button_data = []
        # Criar 15 pastas para testar a paginação
        for i in range(1, 16):
            pasta_id = f"100{i}"
            button_data.append({
                'text': pasta_id,
                'command': lambda x=pasta_id: self.mostrar_historico_pasta(x),
                'name': "pasta_black.png",
                'tipo_usuario': 'repositor'
            })
        
        self.grade_botoes = PastaButtonGrid(self, button_data)

    def mostrar_historico_pasta(self, pasta_id):
        """Mostra o histórico de uma pasta específica"""
        # Cria uma instância temporária do botão para acessar o método mostrar_historico
        # Isso é um workaround, o ideal seria refatorar para um componente separado
        temp_button = PastaButton(
            self, 
            text=pasta_id, 
            command=None, 
            name="pasta_black.png", 
            tipo_usuario='repositor'
        )
        temp_button.mostrar_historico()
        temp_button.destroy()  # Remove o botão temporário

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        if self.finalizar_sessao_callback:
            self.pack_forget()
            self.finalizar_sessao_callback()
        else:
            messagebox.showinfo("Sessão", "Sessão finalizada!")
