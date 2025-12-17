import customtkinter
from ..components import Header, VoltarButton
from ...session import SessionManager
from tkinter import messagebox

class ParametroSistemasFrame(customtkinter.CTkFrame):
    BG_COLOR = "#3B6A7D"
    
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        self.session_manager = SessionManager.get_instance()
        super().__init__(master, fg_color=self.BG_COLOR, *args, **kwargs)
        
        # Criar overlay para esconder construção
        self._overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.lift()
        master.update_idletasks()
        
        self.pack(fill="both", expand=True)
        
        # Criar header primeiro
        self.header = Header(self, "Parâmetro de Sistemas")
        
        # Frame principal para o conteúdo abaixo do header
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # Criar elementos restantes
        self.criar_controle_timer()
        self.criar_tabela_parametros()
        self.criar_botao_voltar()
        
        # Remover overlay após tudo estar pronto
        self.update_idletasks()
        self._overlay.destroy()

    def criar_controle_timer(self):
        """Cria o controle para ativar/desativar a função de timer de abertura de gavetas"""
        frame_controle = customtkinter.CTkFrame(
            self.main_content,
            fg_color="white",
            corner_radius=15,
            height=100
        )
        frame_controle.pack(fill="x", pady=(10, 20))
        frame_controle.pack_propagate(False)
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            frame_controle,
            text="Controle de Timer de Abertura de Gavetas",
            font=("Arial", 14, "bold"),
            text_color="#333333"
        )
        lbl_titulo.pack(side="left", padx=20, pady=10, anchor="n")
        
        # Frame para o status e botão
        frame_status = customtkinter.CTkFrame(frame_controle, fg_color="transparent")
        frame_status.pack(side="right", padx=20, pady=10, fill="y")
        
        # Status atual
        self.lbl_status = customtkinter.CTkLabel(
            frame_status,
            text="Status: " + ("Ativado" if self.session_manager.is_timer_enabled() else "Desativado"),
            font=("Arial", 12),
            text_color="#333333"
        )
        self.lbl_status.pack(pady=(0, 5))
        
        # Botão de controle
        self.btn_controle_timer = customtkinter.CTkButton(
            frame_status,
            text="",
            width=120,
            command=self.alternar_timer,
            fg_color="#4CAF50" if self.session_manager.is_timer_enabled() else "#F44336"
        )
        self.btn_controle_timer.pack()
        
        # Atualiza o texto do botão
        self.atualizar_estado_botao()
    
    def alternar_timer(self):
        """Alterna o estado da função de timer"""
        novo_estado = not self.session_manager.is_timer_enabled()
        if self.session_manager.set_timer_enabled(novo_estado):
            estado = "ativado" if novo_estado else "desativado"
            messagebox.showinfo("Sucesso", f"Timer de abertura de gavetas {estado} com sucesso!")
            
            # Se estiver ativando e houver um bloqueio ativo, mostra o tempo restante
            if novo_estado and self.session_manager.is_blocked():
                segundos = self.session_manager.get_remaining_time()
                minutos = segundos // 60
                segundos = segundos % 60
                messagebox.showinfo("Informação", 
                    f"O sistema está bloqueado por mais {minutos} minutos e {segundos} segundos.")
        else:
            messagebox.showerror("Erro", "Você não tem permissão para alterar esta configuração.")
        
        # Atualiza o estado do botão
        self.atualizar_estado_botao()
    
    def atualizar_estado_botao(self):
        """Atualiza o texto e a cor do botão de acordo com o estado do timer"""
        if self.session_manager.is_timer_enabled():
            self.btn_controle_timer.configure(
                text="Desativar Timer",
                fg_color="#4CAF50",
                hover_color="#388E3C"
            )
            self.lbl_status.configure(
                text="Status: Ativado",
                text_color="#2E7D32"
            )
        else:
            self.btn_controle_timer.configure(
                text="Ativar Timer",
                fg_color="#F44336",
                hover_color="#D32F2F"
            )
            self.lbl_status.configure(
                text="Status: Desativado",
                text_color="#C62828"
            )

    def criar_tabela_parametros(self):
        # Frame para a tabela
        self.tabela_frame = customtkinter.CTkFrame(
            self.main_content,
            fg_color="white",
            corner_radius=15,
        )
        self.tabela_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Configurar grid da tabela
        self.tabela_frame.columnconfigure(0, weight=1)
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Frame rolável para os itens
        scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tabela_frame,
            fg_color="white"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Mensagem de tabela vazia
        lbl_vazio = customtkinter.CTkLabel(
            scrollable_frame,
            text="Nenhum parâmetro encontrado.",
            text_color="#666666",
            font=("Arial", 12)
        )
        lbl_vazio.pack(pady=20)
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        cabecalho_frame.pack(fill="x", padx=10, pady=10)

        # Cabeçalhos
        cabecalhos = ["Parâmetro", "Valor", "Descrição", "Atualizado em"]
        
        for texto in cabecalhos:
            # Cria um frame para cada cabeçalho para melhor controle
            header_cell = customtkinter.CTkFrame(
                cabecalho_frame,
                fg_color="transparent"
            )
            header_cell.pack(side="left", fill="x", expand=True)
            
            lbl = customtkinter.CTkLabel(
                header_cell,
                text=texto,
                font=("Arial", 14, "bold"),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=10, pady=5)

    def criar_botao_voltar(self):
        VoltarButton(self, self.voltar_callback)