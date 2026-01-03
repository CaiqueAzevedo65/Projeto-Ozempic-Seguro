import customtkinter
from ..components import Header, VoltarButton
from ...services.gaveta_service import GavetaService, DrawerHistoryItem, PaginatedResult
from ...core.logger import logger

class HistoricoView(customtkinter.CTkFrame):
    BG_COLOR = "#3B6A7D"
    
    def __init__(self, master, voltar_callback=None, tipo_usuario="administrador", **kwargs):
        super().__init__(master, fg_color=self.BG_COLOR, **kwargs)
        self.voltar_callback = voltar_callback
        self.tipo_usuario = tipo_usuario
        self._gaveta_service = GavetaService.get_instance()
        self.current_page = 1
        self.items_per_page = 20
        
        # Criar overlay para esconder construção
        self._overlay = customtkinter.CTkFrame(master, fg_color=self.BG_COLOR)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.lift()
        master.update_idletasks()
        
        self.pack(fill="both", expand=True)
        self.criar_interface()
        
        # Remover overlay após tudo estar pronto
        self.update_idletasks()
        self._overlay.destroy()
    
    def criar_interface(self):
        # Cabeçalho
        self.header = Header(self, "Histórico de Ações nas Gavetas")
        
        # Frame para o conteúdo
        self.content_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # Frame branco para a tabela
        self.tabela_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15
        )
        self.tabela_frame.pack(fill="both", expand=True, pady=10)
        
        # Cabeçalhos da tabela
        self.criar_cabecalhos()
        
        # Frame para os controles de paginação
        self.paginacao_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.paginacao_frame.pack(fill="x", pady=(10, 0))
        
        # Botões de navegação
        self.btn_anterior = customtkinter.CTkButton(
            self.paginacao_frame,
            text="Anterior",
            command=self.pagina_anterior,
            width=100,
            state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=5)
        
        self.lbl_pagina = customtkinter.CTkLabel(
            self.paginacao_frame,
            text="Página 1"
        )
        self.lbl_pagina.pack(side="left", padx=5)
        
        self.btn_proximo = customtkinter.CTkButton(
            self.paginacao_frame,
            text="Próximo",
            command=self.proxima_pagina,
            width=100
        )
        self.btn_proximo.pack(side="left", padx=5)
        
        # Linhas da tabela
        self.carregar_dados()

        # Botão voltar (adicionado por último para ficar por cima)
        self.voltar_btn = VoltarButton(
            self, 
            command=self.voltar
        )
    
    def criar_cabecalhos(self):
        # Frame para os cabeçalhos
        cabecalho_frame = customtkinter.CTkFrame(
            self.tabela_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        cabecalho_frame.pack(fill="x", padx=10, pady=10)

        # Cabeçalhos
        cabecalhos = ["Data/Hora", "Gaveta", "Ação", "Usuário"]
        larguras = [0.3, 0.2, 0.25, 0.25]  # Proporções de largura
        
        for i, (texto, largura) in enumerate(zip(cabecalhos, larguras)):
            # Cria um frame para cada cabeçalho para melhor controle
            header_cell = customtkinter.CTkFrame(
                cabecalho_frame,
                fg_color="transparent"
            )
            header_cell.pack(side="left", fill="x", expand=True)
            
            # Configura o padding apenas para o cabeçalho "Gaveta"
            padx_left = 65 if texto == "Gaveta" else 0
            
            lbl = customtkinter.CTkLabel(
                header_cell,
                text=texto,
                font=("Arial", 14, "bold"),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=(padx_left, 0), pady=5)
            
            # Define o peso da coluna
            cabecalho_frame.columnconfigure(i, weight=int(largura * 100))
    
    def carregar_dados(self):
        # Limpa a tabela atual
        for widget in self.tabela_frame.winfo_children():
            if widget != self.tabela_frame.winfo_children()[0]:  # Mantém o cabeçalho
                widget.destroy()
        
        # Frame rolável para os itens
        scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tabela_frame,
            fg_color="white"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        try:
            # Calcula o offset com base na página atual
            offset = (self.current_page - 1) * self.items_per_page
            
            # Obtém os dados paginados usando GavetaService
            history_raw = self._gaveta_service.get_all_history_paginated(offset, self.items_per_page)
            total = self._gaveta_service.count_all_history()
            
            # Atualiza controles de paginação
            self.atualizar_controles_paginacao(total)
            
            # Adicionar itens
            for idx, h in enumerate(history_raw):
                self.adicionar_linha(
                    scrollable_frame,
                    h[0],  # data_hora
                    h[1],  # gaveta_id
                    h[2],  # acao
                    h[3],  # usuario
                    idx % 2 == 0  # Alternar cor de fundo
                )
        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
    
    def atualizar_controles_paginacao(self, total_itens):
        # Calcula o total de páginas
        total_paginas = (total_itens + self.items_per_page - 1) // self.items_per_page
        total_paginas = max(1, total_paginas)  # Garante pelo menos 1 página
        
        # Atualiza o texto da página
        self.lbl_pagina.configure(text=f"Página {self.current_page} de {total_paginas}")
        
        # Mostra ou esconde os controles de paginação com base no número de páginas
        if total_paginas <= 1:
            # Esconde os controles de paginação se houver apenas uma página
            self.btn_anterior.pack_forget()
            self.lbl_pagina.pack_forget()
            self.btn_proximo.pack_forget()
        else:
            # Mostra os controles e atualiza os estados dos botões
            self.btn_anterior.pack(side="left", padx=5)
            self.lbl_pagina.pack(side="left", padx=5)
            self.btn_proximo.pack(side="left", padx=5)
            
            # Atualiza estados dos botões
            self.btn_anterior.configure(state="normal" if self.current_page > 1 else "disabled")
            self.btn_proximo.configure(
                state="normal" if self.current_page < total_paginas else "disabled"
            )
    
    def proxima_pagina(self):
        self.current_page += 1
        self.carregar_dados()
    
    def pagina_anterior(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.carregar_dados()
    
    def adicionar_linha(self, parent, data_hora, gaveta_id, acao, usuario, par):
        # Frame para uma linha da tabela
        linha_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#f9f9f9" if par else "white",
            corner_radius=8
        )
        linha_frame.pack(fill="x", padx=5, pady=2)
        
        # Dados da linha
        dados = [data_hora, gaveta_id, acao, usuario]
        
        for texto in dados:
            lbl = customtkinter.CTkLabel(
                linha_frame,
                text=str(texto),
                font=("Arial", 12),
                text_color="black",
                anchor="w"
            )
            lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)
    
    def voltar(self):
        """Volta para a tela anterior"""
        if self.voltar_callback:
            self.voltar_callback()