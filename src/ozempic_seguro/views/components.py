import customtkinter
from tkinter import messagebox
from PIL import Image
import os
from .gaveta_state_manager import GavetaStateManager
from ..session import SessionManager  # Importa o SessionManager do caminho correto

# Lazy loading de imagens
class ImageCache:
    _logo_img = None
    _digital_img = None

    @staticmethod
    def get_logo():
        if ImageCache._logo_img is None:
            logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.jpg"))
            imagem = Image.open(logo_path)
            ImageCache._logo_img = customtkinter.CTkImage(imagem, size=(60, 60))
        return ImageCache._logo_img

    @staticmethod
    def get_digital():
        if ImageCache._digital_img is None:
            digital_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "digital.png"))
            imagem = Image.open(digital_path)
            ImageCache._digital_img = customtkinter.CTkImage(imagem, size=(70, 70))
        return ImageCache._digital_img

# Componente de cabeçalho reutilizável
class Header(customtkinter.CTkFrame):
    def __init__(self, master, titulo, *args, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=0, height=80, *args, **kwargs)
        self.pack(fill="x", side="top")
        customtkinter.CTkLabel(self, text=titulo, font=("Arial", 24, "bold"), text_color="black").pack(side="left", padx=20, pady=20)
        logo_img = ImageCache.get_logo()
        customtkinter.CTkLabel(self, image=logo_img, text="", bg_color="white").pack(side="right", padx=20)

# Componente de botão principal reutilizável
class MainButton(customtkinter.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, font=("Arial", 16, "bold"), width=220, height=60, fg_color="white", text_color="black", hover_color="#e0e0e0", command=command, **kwargs) 

# Componente de botão de finalizar sessão
class FinalizarSessaoButton:
    def __init__(self, master, command):
        # Frame para agrupar o botão e o label
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.place(relx=0.5, rely=0.88, anchor="center")
        
        # Caminho para a imagem da elipse
        elipse_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "elipse.png"))
        size = (40, 40) # Tamanho da imagem
        
        self.elipse_img = customtkinter.CTkImage(
            Image.open(elipse_path),
            size=size
        )

        # Botão de finalizar com imagem de elipse
        self.btn_finalizar = customtkinter.CTkButton(
            self.frame,
            text="",  # Sem texto, só imagem
            width=40,
            height=40,
            image=self.elipse_img,
            fg_color="transparent",  # Ou outra cor sólida
            hover_color="#3B6A7D",
            command=command
        )
        self.btn_finalizar.pack()

        # Label "Finalizar sessão"
        self.label = customtkinter.CTkLabel(
            self.frame,
            text="Finalizar sessão",
            font=("Arial", 12),
            text_color="white",
            fg_color="transparent"
        )
        self.label.pack(pady=(5, 0))

# Componente de grade de botões com imagens de gavetas
class GavetaButtonGrid(customtkinter.CTkFrame):
    def __init__(self, master, button_data):
        super().__init__(master, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Armazenar os dados dos botões
        self.button_data = button_data
        self.current_page = 0
        
        # Configurações da grade
        self.rows = 2
        self.cols = 4
        self.buttons_per_page = self.rows * self.cols
        
        # Calcular número total de páginas
        self.total_pages = max(1, (len(self.button_data) + self.buttons_per_page - 1) // self.buttons_per_page)
        
        # Frame para a grade de botões
        self.grid_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both")
        
        # Frame para a navegação
        self.nav_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=(10, 0))
        
        # Configurar grid layout
        for i in range(self.rows):
            self.grid_frame.rowconfigure(i, weight=1)
        for j in range(self.cols):
            self.grid_frame.columnconfigure(j, weight=1)
        
        # Criar controles de navegação
        self.criar_controles_navegacao()
        
        # Exibir a primeira página
        self.mostrar_pagina(0)
    
    def criar_controles_navegacao(self):
        """Cria os controles de navegação entre páginas"""
        # Frame para agrupar os botões de navegação
        self.btn_frame = customtkinter.CTkFrame(self.nav_frame, fg_color="transparent")
        self.btn_frame.pack(side="left", anchor="w", padx=10)  # Alinha à esquerda
        
        # Botão página anterior
        self.btn_anterior = customtkinter.CTkButton(
            self.btn_frame,
            text="← Anterior",
            command=self.pagina_anterior,
            width=120,
            state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=(0, 5))  # Espaço apenas à direita
        
        # Botão próxima página
        self.btn_proximo = customtkinter.CTkButton(
            self.btn_frame,
            text="Próxima →",
            command=self.proxima_pagina,
            width=120
        )
        self.btn_proximo.pack(side="left")  # Sem espaço extra
        
        # Esconder controles de navegação se houver apenas uma página
        if self.total_pages <= 1:
            self.nav_frame.pack_forget()
    
    def pagina_anterior(self):
        """Vai para a página anterior"""
        if self.current_page > 0:
            self.mostrar_pagina(self.current_page - 1)
            
    def proxima_pagina(self):
        """Vai para a próxima página"""
        if self.current_page < self.total_pages - 1:
            self.mostrar_pagina(self.current_page + 1)
            
    def mostrar_pagina(self, page_num):
        """Mostra a página especificada"""
        # Validar número da página
        if page_num < 0 or page_num >= self.total_pages:
            return
            
        self.current_page = page_num
        
        # Limpar a grade atual
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # Calcular índices dos itens a serem exibidos
        start_idx = page_num * self.buttons_per_page
        end_idx = min(start_idx + self.buttons_per_page, len(self.button_data))
        
        # Criar os botões da página atual
        for i in range(self.rows):
            for j in range(self.cols):
                item_idx = start_idx + (i * self.cols) + j
                if item_idx >= end_idx:
                    break
                    
                # Criar frame para a célula
                cell_frame = customtkinter.CTkFrame(
                    self.grid_frame,
                    fg_color="transparent"
                )
                cell_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                
                if item_idx < end_idx:
                    # Criar o botão de gaveta
                    btn_data = self.button_data[item_idx]
                    btn = GavetaButton(
                        master=cell_frame,
                        text=btn_data['text'],
                        command=btn_data['command'],
                        name=btn_data['name'],
                        tipo_usuario=btn_data['tipo_usuario']
                    )
        
        # Atualizar controles de navegação
        self.atualizar_controles_navegacao()
    
    def atualizar_controles_navegacao(self):
        """Atualiza o estado dos controles de navegação"""
        if hasattr(self, 'btn_anterior') and hasattr(self, 'btn_proximo'):
            self.btn_anterior.configure(state="normal" if self.current_page > 0 else "disabled")
            self.btn_proximo.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")

# Componente de botão com imagem de gaveta
class GavetaButton:
    def __init__(self, master, text, command=None, name=None, tipo_usuario=None):
        """Componente de botão de gaveta para a grade"""
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")
        
        # Obter o gerenciador de estado
        self.state_manager = GavetaStateManager.get_instance()
        self.tipo_usuario = tipo_usuario  # 'repositor' ou 'vendedor'
        
        # Carregar ambas as imagens
        self.gaveta_aberta = customtkinter.CTkImage(
            Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "gaveta.png"))),
            size=(120, 120)
        )
        self.gaveta_fechada = customtkinter.CTkImage(
            Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "gaveta_black.png"))),
            size=(120, 120)
        )

        # Botão principal
        self.btn_gaveta = customtkinter.CTkButton(
            self.frame,
            text="",  # Texto vazio no botão
            width=120,
            height=120,
            image=self.gaveta_fechada,  # Começa com a gaveta fechada
            fg_color="transparent",
            hover_color="#3B6A7D",
            command=self.manipular_estado
        )
        self.btn_gaveta.pack(pady=(0, 5))

        # Label com o texto
        self.label = customtkinter.CTkLabel(
            self.frame,
            text=text,
            font=("Arial", 12),
            text_color="white"
        )
        self.label.pack()
        
        # Guardar o comando original e o ID da gaveta
        self.command_original = command
        self.gaveta_id = text  # Usando o texto como ID da gaveta
        
        # Atualizar a imagem inicial baseada no estado atual
        self.atualizar_imagem()

    def atualizar_imagem(self):
        """Atualiza a imagem do botão baseado no estado atual"""
        estado = self.state_manager.get_estado(self.gaveta_id)
        self.btn_gaveta.configure(image=self.gaveta_aberta if estado else self.gaveta_fechada)

    def manipular_estado(self):
        """Manipula o estado da gaveta baseado no tipo de usuário"""
        estado_atual = self.state_manager.get_estado(self.gaveta_id)
        
        # Obtém o ID do usuário atual, se disponível
        session_manager = SessionManager.get_instance()
        current_user = session_manager.get_current_user()
        user_id = current_user.get('id') if current_user else None
        
        if self.tipo_usuario == 'administrador':
            # Administrador pode tanto abrir quanto fechar
            if not estado_atual:  # Se a gaveta estiver fechada, abre com confirmação
                self._abrir_gaveta_com_confirmacao()
            else:
                sucesso, mensagem = self.state_manager.fechar_gaveta(
                    self.gaveta_id, 
                    self.tipo_usuario,
                    user_id
                )
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
        
        elif self.tipo_usuario == 'vendedor':
            # Vendedor só pode abrir gavetas fechadas
            if not estado_atual:
                self._abrir_gaveta_com_confirmacao()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para fechar gavetas")
        
        elif self.tipo_usuario == 'repositor':
            # Repositório só pode fechar gavetas abertas
            if estado_atual:
                sucesso, mensagem = self.state_manager.fechar_gaveta(
                    self.gaveta_id, 
                    self.tipo_usuario,
                    user_id
                )
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para abrir gavetas")
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido")
    
    def _abrir_gaveta_com_confirmacao(self):
        """Mostra uma janela de confirmação antes de abrir a gaveta, se o timer estiver ativado"""
        # Verifica se o timer está ativado
        session_manager = SessionManager.get_instance()
        if not session_manager.is_timer_enabled():
            # Se o timer estiver desativado, abre a gaveta diretamente sem mostrar a janela de confirmação
            current_user = session_manager.get_current_user()
            user_id = current_user.get('id') if current_user else None
            sucesso, mensagem = self.state_manager.abrir_gaveta(self.gaveta_id, self.tipo_usuario, user_id)
            messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
            if sucesso:
                self.atualizar_imagem()
            return
            
        # Se o timer estiver ativado, mostra a janela de confirmação
        dialog = customtkinter.CTkToplevel()
        dialog.title("Confirmar Abertura")
        dialog.geometry("500x250")  # Aumentei a largura e altura
        dialog.resizable(False, False)  # Impede redimensionamento
        dialog.grab_set()  # Torna a janela modal
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Frame principal
        main_frame = customtkinter.CTkFrame(dialog, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        customtkinter.CTkLabel(
            main_frame,
            text="Confirmar Abertura",
            font=("Arial", 16, "bold"),
            text_color="black"
        ).pack(pady=(10, 5))
        
        # Mensagem
        if self.tipo_usuario == 'vendedor':
            mensagem = f"Deseja realmente abrir a gaveta {self.gaveta_id}?\n\n" \
                       "O sistema será bloqueado por 5 minutos após a abertura.\n" \
                       "Você terá acesso somente para visualizar os dados."
        else:
            mensagem = f"Deseja realmente abrir a gaveta {self.gaveta_id}?\n\n" \
                       "O sistema será bloqueado por 5 minutos após a abertura."
        
        customtkinter.CTkLabel(
            main_frame,
            text=mensagem,
            font=("Arial", 12),
            text_color="black",
            wraplength=400,
            justify="center"
        ).pack(pady=10, padx=20)
        
        # Frame para os botões
        button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Botão de confirmar
        customtkinter.CTkButton(
            button_frame,
            text="Confirmar",
            font=("Arial", 12, "bold"),
            width=120,
            command=lambda: self._on_confirmar_abertura(dialog)
        ).pack(side="left", padx=10)
        
        # Botão de cancelar
        customtkinter.CTkButton(
            button_frame,
            text="Cancelar",
            font=("Arial", 12),
            fg_color="#6c757d",
            hover_color="#5a6268",
            width=120,
            command=dialog.destroy
        ).pack(side="right", padx=10)
        
        dialog.transient(self.frame.winfo_toplevel())
        dialog.wait_window(dialog)

    def _on_confirmar_abertura(self, dialog):
        """Confirma a abertura da gaveta"""
        dialog.destroy()
        # Obtém o ID do usuário atual, se disponível
        session_manager = SessionManager.get_instance()
        current_user = session_manager.get_current_user()
        user_id = current_user.get('id') if current_user else None
        
        sucesso, mensagem = self.state_manager.abrir_gaveta(
            self.gaveta_id, 
            self.tipo_usuario,
            user_id
        )
        messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
        if sucesso:
            self.atualizar_imagem()

    def mostrar_historico(self):
        """Mostra o histórico de alterações da gaveta com paginação"""
        # Configuração da paginação
        self.itens_por_pagina = 20
        self.pagina_atual = 1
        
        # Criar janela
        self.janela_historico = customtkinter.CTkToplevel()
        self.janela_historico.title(f"Histórico - Gaveta {self.gaveta_id}")
        self.janela_historico.geometry("600x400")
        
        # Frame principal
        frame_principal = customtkinter.CTkFrame(self.janela_historico)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        label_titulo = customtkinter.CTkLabel(
            frame_principal, 
            text=f"Histórico - Gaveta {self.gaveta_id}",
            font=("Arial", 14, "bold")
        )
        label_titulo.pack(pady=(0, 10))
        
        # Frame para os controles de paginação (superior)
        frame_controles_cima = customtkinter.CTkFrame(frame_principal, fg_color="transparent")
        frame_controles_cima.pack(fill="x", pady=(0, 5))
        
        # Frame para a lista de histórico
        self.frame_historico = customtkinter.CTkScrollableFrame(
            frame_principal,
            fg_color="transparent"
        )
        self.frame_historico.pack(fill="both", expand=True)
        
        # Frame para os controles de paginação (inferior)
        frame_controles_baixo = customtkinter.CTkFrame(frame_principal, fg_color="transparent")
        frame_controles_baixo.pack(fill="x", pady=(5, 0))
        
        # Botões de navegação
        self.btn_anterior = customtkinter.CTkButton(
            frame_controles_baixo,
            text="Anterior",
            command=self._pagina_anterior,
            state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=5)
        
        self.lbl_pagina = customtkinter.CTkLabel(
            frame_controles_baixo,
            text="Página 1",
            width=100
        )
        self.lbl_pagina.pack(side="left")
        
        self.btn_proximo = customtkinter.CTkButton(
            frame_controles_baixo,
            text="Próximo",
            command=self._proxima_pagina
        )
        self.btn_proximo.pack(side="left", padx=5)
        
        # Botão de fechar
        btn_fechar = customtkinter.CTkButton(
            frame_controles_baixo,
            text="Fechar",
            command=self.janela_historico.destroy
        )
        btn_fechar.pack(side="right")
        
        # Carregar a primeira página
        self._carregar_historico()
    
    def _carregar_historico(self):
        """Carrega os itens do histórico para a página atual"""
        # Limpa o frame de histórico
        for widget in self.frame_historico.winfo_children():
            widget.destroy()
        
        # Obtém o histórico paginado
        offset = (self.pagina_atual - 1) * self.itens_por_pagina
        historico = self.state_manager.get_historico_paginado(
            self.gaveta_id, 
            offset=offset, 
            limit=self.itens_por_pagina
        )
        
        # Obtém o total de itens para controle de paginação
        total_itens = self.state_manager.get_total_historico(self.gaveta_id)
        total_paginas = (total_itens + self.itens_por_pagina - 1) // self.itens_por_pagina
        
        # Atualiza controles de paginação
        self.lbl_pagina.configure(text=f"Página {self.pagina_atual} de {total_paginas}")
        self.btn_anterior.configure(state="disabled" if self.pagina_atual == 1 else "normal")
        self.btn_proximo.configure(state="disabled" if self.pagina_atual >= total_paginas else "normal")
        
        # Adiciona os itens ao frame
        if not historico:
            lbl_vazio = customtkinter.CTkLabel(
                self.frame_historico,
                text="Nenhum registro de histórico para esta gaveta.",
                text_color="gray"
            )
            lbl_vazio.pack(pady=10)
            return
        
        for acao, usuario, data in historico:
            acao_texto = "Aberta" if acao == "aberta" else "Fechada"
            
            frame_item = customtkinter.CTkFrame(
                self.frame_historico,
                fg_color="#f0f0f0",
                corner_radius=5
            )
            frame_item.pack(fill="x", pady=2, padx=2)
            
            lbl_item = customtkinter.CTkLabel(
                frame_item,
                text=f"{data} - {acao_texto} por {usuario}",
                anchor="w",
                justify="left"
            )
            lbl_item.pack(fill="x", padx=5, pady=5)
    
    def _proxima_pagina(self):
        """Vai para a próxima página do histórico"""
        self.pagina_atual += 1
        self._carregar_historico()
    
    def _pagina_anterior(self):
        """Volta para a página anterior do histórico"""
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self._carregar_historico()

# Componente de botão de voltar
class VoltarButton:
    def __init__(self, master, command):
        # Frame para agrupar o botão e o label
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.place(relx=0.5, rely=0.88, anchor="center")
        
        voltar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "botao_voltar.png"))
        size = (40, 40) # Tamanho da imagem
        
        self.elipse_img = customtkinter.CTkImage(
            Image.open(voltar_path),
            size=size
        )

        self.btn_voltar = customtkinter.CTkButton(
            self.frame,
            text="",  # Sem texto, só imagem
            width=40,
            height=40,
            image=self.elipse_img,
            fg_color="transparent",  # Ou outra cor sólida
            hover_color="#3B6A7D",
            command=command
        )
        self.btn_voltar.pack()

class TecladoVirtual(customtkinter.CTkFrame):
    def __init__(self, master, entrada_atual=None, comando_salvar=None, **kwargs):
        super().__init__(master, fg_color="#f0f0f0", corner_radius=10, **kwargs)
        self.entrada_atual = entrada_atual
        self.comando_salvar = comando_salvar
        self.maiusculas_ativado = False  # Estado inicial: minúsculas
        self.criar_teclado()
        
    def criar_teclado(self):
        # Layout do teclado
        self.linhas = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],  # Letras normais
            ['MAIÚSCULAS', 'LIMPAR', 'ESPAÇO']  # Última linha
        ]
        
        # Configuração do grid
        for i, linha in enumerate(self.linhas):
            self.grid_rowconfigure(i, weight=1)
            
            # Configuração para a penúltima linha (onde adicionaremos SALVAR e ⌫)
            if i == len(self.linhas) - 2:  # Penúltima linha
                # Primeiro, adiciona as letras normais
                for j, tecla in enumerate(linha):
                    btn = customtkinter.CTkButton(
                        self,
                        text=tecla.upper() if self.maiusculas_ativado and tecla.isalpha() else tecla,
                        height=40,
                        font=("Arial", 12, "bold"),
                        fg_color="#ffffff",
                        text_color="#000000",
                        hover_color="#e0e0e0",
                        corner_radius=5,
                        command=lambda t=tecla: self.tecla_pressionada(t)
                    )
                    btn.grid(
                        row=i,
                        column=j,
                        padx=2,
                        pady=2,
                        sticky="nsew"
                    )
                
                # Adiciona o botão SALVAR (colunas 7 e 8)
                btn_salvar = customtkinter.CTkButton(
                    self,
                    text="SALVAR",
                    height=40,
                    font=("Arial", 12, "bold"),
                    fg_color="#2ecc71",
                    text_color="white",
                    hover_color="#27ae60",
                    corner_radius=5,
                    command=lambda: self.tecla_pressionada('SALVAR')
                )
                btn_salvar.grid(
                    row=i,
                    column=7,
                    columnspan=2,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )
                
                # Adiciona o botão ⌫ (coluna 9)
                btn_apagar = customtkinter.CTkButton(
                    self,
                    text="⌫",
                    height=40,
                    font=("Arial", 12, "bold"),
                    fg_color="#e74c3c",
                    text_color="white",
                    hover_color="#c0392b",
                    corner_radius=5,
                    command=lambda: self.tecla_pressionada('⌫')
                )
                btn_apagar.grid(
                    row=i,
                    column=9,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )
                
                # Configura as colunas para a penúltima linha
                for j in range(10):
                    self.grid_columnconfigure(j, weight=1)
            
            # Configuração para a última linha (botões de função)
            elif i == len(self.linhas) - 1:
                # Configura 10 colunas no total
                for j in range(10):
                    self.grid_columnconfigure(j, weight=1)
                
                # Botão MAIÚSCULAS (colunas 0-1)
                btn_maiusculas = customtkinter.CTkButton(
                    self,
                    text="MAIÚSCULAS",
                    height=40,
                    font=("Arial", 12, "bold"),
                    fg_color="#3498db" if self.maiusculas_ativado else "#ffffff",
                    text_color="#ffffff" if self.maiusculas_ativado else "#000000",
                    hover_color="#2980b9" if self.maiusculas_ativado else "#e0e0e0",
                    corner_radius=5,
                    command=lambda: self.tecla_pressionada('MAIÚSCULAS')
                )
                btn_maiusculas.grid(
                    row=i,
                    column=0,
                    columnspan=2,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )
                self.btn_maiusculas = btn_maiusculas
                
                # Botão LIMPAR (colunas 2-3)
                btn_limpar = customtkinter.CTkButton(
                    self,
                    text="LIMPAR",
                    height=40,
                    font=("Arial", 12, "bold"),
                    fg_color="#ffffff",
                    text_color="#000000",
                    hover_color="#e0e0e0",
                    corner_radius=5,
                    command=lambda: self.tecla_pressionada('LIMPAR')
                )
                btn_limpar.grid(
                    row=i,
                    column=2,
                    columnspan=2,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )
                
                # Botão ESPAÇO (colunas 4-9)
                btn_espaco = customtkinter.CTkButton(
                    self,
                    text="______",
                    height=40,
                    font=("Arial", 12, "bold"),
                    fg_color="#ffffff",
                    text_color="#000000",
                    hover_color="#e0e0e0",
                    corner_radius=5,
                    command=lambda: self.tecla_pressionada(' ')
                )
                btn_espaco.grid(
                    row=i,
                    column=4,
                    columnspan=6,  # Ocupa 6 colunas (4 a 9)
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )
            
            # Configuração para as linhas superiores (teclas normais)
            else:
                # Configura 10 colunas (uma para cada tecla)
                for j in range(10):
                    self.grid_columnconfigure(j, weight=1)
                
                for j, tecla in enumerate(linha):
                    # Aplica maiúsculas se estiver ativado
                    tecla_exibida = tecla.upper() if self.maiusculas_ativado and tecla not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] else tecla
                    
                    btn = customtkinter.CTkButton(
                        self,
                        text=tecla_exibida,
                        height=40,
                        font=("Arial", 12, "bold"),
                        fg_color="#ffffff",
                        text_color="#000000",
                        hover_color="#e0e0e0",
                        corner_radius=5,
                        command=lambda t=tecla: self.tecla_pressionada(t)
                    )
                    
                    btn.grid(
                        row=i,
                        column=j,
                        padx=2,
                        pady=2,
                        sticky="nsew"
                    )
    
    def tecla_pressionada(self, tecla):
        if not self.entrada_atual:
            return
            
        if tecla == '⌫':
            texto_atual = self.entrada_atual.get()
            self.entrada_atual.delete(0, 'end')
            self.entrada_atual.insert(0, texto_atual[:-1])
        elif tecla == 'LIMPAR':
            self.entrada_atual.delete(0, 'end')
        elif tecla == 'SALVAR' and self.comando_salvar:
            self.comando_salvar()
        elif tecla == 'MAIÚSCULAS':
            # Alterna entre maiúsculas e minúsculas
            self.maiusculas_ativado = not self.maiusculas_ativado
            
            # Atualiza a aparência do botão de maiúsculas
            if hasattr(self, 'btn_maiusculas'):
                self.btn_maiusculas.configure(
                    fg_color="#3498db" if self.maiusculas_ativado else "#ffffff",
                    text_color="#ffffff" if self.maiusculas_ativado else "#000000",
                    hover_color="#2980b9" if self.maiusculas_ativado else "#e0e0e0"
                )
            
            # Reconstrói o teclado para atualizar as letras
            for widget in self.winfo_children():
                widget.destroy()
            self.criar_teclado()
        else:
            # Aplica maiúsculas se estiver ativado
            tecla_inserida = tecla.upper() if self.maiusculas_ativado and tecla.isalpha() else tecla
            self.entrada_atual.insert('end', tecla_inserida)
            
    def definir_entrada(self, entrada):
        self.entrada_atual = entrada

# Atualizar a lista __all__ para incluir o novo componente
__all__ = [
    'Header', 'FinalizarSessaoButton', 'GavetaButtonGrid', 
    'GavetaButton', 'VoltarButton', 'MainButton', 'ImageCache',
    'TecladoVirtual'
]