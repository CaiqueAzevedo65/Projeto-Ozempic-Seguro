import customtkinter
from tkinter import messagebox
from .components import Header, FinalizarSessaoButton, GavetaButtonGrid, GavetaButton, ModernConfirmDialog, ToastNotification

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
        # Criar 15 gavetas para testar a paginação
        for i in range(1, 16):
            gaveta_id = f"100{i}"
            button_data.append({
                'text': gaveta_id,
                'command': lambda x=gaveta_id: self.mostrar_historico_gaveta(x),
                'name': "gaveta_black.png",
                'tipo_usuario': 'repositor'  # Permite abrir e fechar
            })
        
        self.grade_botoes = GavetaButtonGrid(self, button_data)

    def mostrar_historico_gaveta(self, gaveta_id):
        """Mostra o histórico de uma gaveta específica"""
        # Cria uma instância temporária do botão para acessar o método mostrar_historico
        # Isso é um workaround, o ideal seria refatorar para um componente separado
        temp_button = GavetaButton(
            self, 
            text=gaveta_id, 
            command=None, 
            name="gaveta_black.png", 
            tipo_usuario='repositor'
        )
        temp_button.mostrar_historico()
        temp_button.destroy()  # Remove o botão temporário

    def criar_botao_finalizar(self):
        FinalizarSessaoButton(self, self.finalizar_sessao)

    def finalizar_sessao(self):
        # Usar confirmação visual moderna
        if ModernConfirmDialog.ask(
            self, 
            "Finalizar Sessão", 
            "Tem certeza que deseja sair do sistema?",
            icon="question",
            confirm_text="Sair",
            cancel_text="Cancelar"
        ):
            ToastNotification.show(self, "Sessão finalizada com sucesso", "success")
            if self.finalizar_sessao_callback:
                self.after(1000, lambda: self._execute_logout())
            else:
                messagebox.showinfo("Sessão", "Sessão finalizada!")
    
    def _execute_logout(self):
        """Executa o logout após delay da notificação"""
        self.pack_forget()
        self.finalizar_sessao_callback()
