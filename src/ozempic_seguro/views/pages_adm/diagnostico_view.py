"""
Tela de Diagnóstico - Mostruário de gavetas conectadas.
Mostra status de até 8 gavetas (conectadas/vazias, abertas/fechadas, funcionamento).
"""
import customtkinter
from ..components import Header, VoltarButton

class DiagnosticoFrame(customtkinter.CTkFrame):
    def __init__(self, master, voltar_callback=None, *args, **kwargs):
        self.voltar_callback = voltar_callback
        super().__init__(master, fg_color="#3B6A7D", *args, **kwargs)
        self.pack(fill="both", expand=True)
        
        # Criar header primeiro
        self.header = Header(self, "Diagnóstico de Gavetas")
        
        # Frame principal para o conteúdo abaixo do header
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # Dados simulados das gavetas (para demonstração)
        self.gavetas_simuladas = [
            {"id": 1, "conectada": True, "aberta": True, "funcionando": True},
            {"id": 2, "conectada": True, "aberta": True, "funcionando": False},
            {"id": 3, "conectada": True, "aberta": False, "funcionando": True},
            {"id": 4, "conectada": True, "aberta": False, "funcionando": True},
            {"id": 5, "conectada": False, "aberta": False, "funcionando": True},
            {"id": 6, "conectada": False, "aberta": False, "funcionando": True},
            {"id": 7, "conectada": False, "aberta": False, "funcionando": True},
            {"id": 8, "conectada": False, "aberta": False, "funcionando": True},
        ]
        
        # Criar elementos restantes
        self.criar_conteudo()
        self.criar_botao_voltar()
    
    def criar_conteudo(self):
        # Frame para o conteúdo
        content_frame = customtkinter.CTkFrame(
            self.main_content,
            fg_color="white",
            corner_radius=15
        )
        content_frame.pack(fill="both", expand=True)
        
        # Título
        lbl_titulo = customtkinter.CTkLabel(
            content_frame,
            text="Status das Gavetas",
            font=("Arial", 20, "bold"),
            text_color="#333333"
        )
        lbl_titulo.pack(pady=(20, 10))
        
        # Informação do sistema
        info_frame = customtkinter.CTkFrame(
            content_frame,
            fg_color="#f0f0f0",
            corner_radius=10
        )
        info_frame.pack(pady=10, padx=20, fill="x")
        
        lbl_info = customtkinter.CTkLabel(
            info_frame,
            text="💻 Mini PC - Capacidade: 8 gavetas | Conectadas: 4 | Disponíveis: 4",
            font=("Arial", 12),
            text_color="#555555"
        )
        lbl_info.pack(pady=10)
        
        # Grid de gavetas (2x4)
        self.criar_grid_gavetas(content_frame)
        
        # Legenda
        self.criar_legenda(content_frame)
    
    def criar_grid_gavetas(self, parent):
        """Cria o grid 2x4 de gavetas"""
        grid_frame = customtkinter.CTkFrame(
            parent,
            fg_color="transparent"
        )
        grid_frame.pack(pady=20, padx=20, expand=True)
        
        # Configurar grid 2x4
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(4):
            grid_frame.columnconfigure(j, weight=1)
        
        # Criar as 8 gavetas
        for i in range(8):
            row = i // 4
            col = i % 4
            gaveta_data = self.gavetas_simuladas[i]
            
            self.criar_gaveta_widget(grid_frame, gaveta_data, row, col)
    
    def criar_gaveta_widget(self, parent, gaveta_data, row, col):
        """Cria um widget individual de gaveta"""
        # Frame da gaveta
        if gaveta_data["conectada"]:
            # Gaveta conectada - cor baseada no status
            if not gaveta_data["funcionando"]:
                bg_color = "#FFEBEE"  # Vermelho claro para mau funcionamento
                border_color = "#F44336"
            elif gaveta_data["aberta"]:
                bg_color = "#FFF3E0"  # Laranja claro para aberta
                border_color = "#FF9800"
            else:
                bg_color = "#E8F5E9"  # Verde claro para fechada e funcionando
                border_color = "#4CAF50"
        else:
            # Espaço vazio
            bg_color = "#F5F5F5"
            border_color = "#CCCCCC"
        
        # Frame da gaveta com altura mínima
        gaveta_frame = customtkinter.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=10,
            border_width=2,
            border_color=border_color,
            height=140  # Altura mínima
        )
        gaveta_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Conteúdo da gaveta
        if gaveta_data["conectada"]:
            # Número da gaveta
            lbl_numero = customtkinter.CTkLabel(
                gaveta_frame,
                text=f"Gaveta {gaveta_data['id']}",
                font=("Arial", 14, "bold"),
                text_color="#333333"
            )
            lbl_numero.pack(pady=(20, 8))
            
            # Status
            if gaveta_data["aberta"]:
                status_text = "🔓 ABERTA"
                status_color = "#FF6B35"
            else:
                status_text = "🔒 FECHADA"
                status_color = "#2E7D32"
            
            lbl_status = customtkinter.CTkLabel(
                gaveta_frame,
                text=status_text,
                font=("Arial", 12, "bold"),
                text_color=status_color
            )
            lbl_status.pack(pady=(0, 8))
            
            # Funcionamento
            if not gaveta_data["funcionando"]:
                lbl_erro = customtkinter.CTkLabel(
                    gaveta_frame,
                    text="⚠️ DEFEITO",
                    font=("Arial", 10, "bold"),
                    text_color="#D32F2F"
                )
                lbl_erro.pack(pady=(0, 20))
            else:
                lbl_ok = customtkinter.CTkLabel(
                    gaveta_frame,
                    text="✅ Funcionando",
                    font=("Arial", 10),
                    text_color="#388E3C"
                )
                lbl_ok.pack(pady=(0, 20))
        else:
            # Espaço vazio
            lbl_vazio = customtkinter.CTkLabel(
                gaveta_frame,
                text="➕",
                font=("Arial", 24),
                text_color="#999999"
            )
            lbl_vazio.pack(pady=(25, 8))
            
            lbl_texto = customtkinter.CTkLabel(
                gaveta_frame,
                text="Espaço Disponível",
                font=("Arial", 11),
                text_color="#666666"
            )
            lbl_texto.pack(pady=(0, 5))
            
            lbl_info = customtkinter.CTkLabel(
                gaveta_frame,
                text="Conecte uma gaveta",
                font=("Arial", 9),
                text_color="#999999"
            )
            lbl_info.pack(pady=(0, 20))
    
    def criar_legenda(self, parent):
        """Cria a legenda dos status"""
        legenda_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#f9f9f9",
            corner_radius=10
        )
        legenda_frame.pack(pady=(10, 20), padx=20, fill="x")
        
        lbl_titulo = customtkinter.CTkLabel(
            legenda_frame,
            text="Legenda:",
            font=("Arial", 12, "bold"),
            text_color="#333333"
        )
        lbl_titulo.pack(side="left", padx=(20, 10), pady=10)
        
        # Items da legenda
        legendas = [
            ("🟢", "Fechada/Funcionando"),
            ("🟠", "Aberta/Funcionando"),
            ("🔴", "Mau Funcionamento"),
            ("⬜", "Espaço Disponível")
        ]
        
        for cor, texto in legendas:
            item_frame = customtkinter.CTkFrame(
                legenda_frame,
                fg_color="transparent"
            )
            item_frame.pack(side="left", padx=15, pady=10)
            
            lbl_item = customtkinter.CTkLabel(
                item_frame,
                text=f"{cor} {texto}",
                font=("Arial", 11),
                text_color="#555555"
            )
            lbl_item.pack()
    
    def criar_botao_voltar(self):
        VoltarButton(self, self.voltar_callback)
