import customtkinter
from tkinter import messagebox
from PIL import Image
import os
from .pasta_state_manager import PastaStateManager

# Lazy loading de imagens
class ImageCache:
    _logo_img = None
    _digital_img = None

    @staticmethod
    def get_logo():
        if ImageCache._logo_img is None:
            logo_path = os.path.join("src", "assets", "logo.jpg")
            imagem = Image.open(logo_path)
            ImageCache._logo_img = customtkinter.CTkImage(imagem, size=(60, 60))
        return ImageCache._logo_img

    @staticmethod
    def get_digital():
        if ImageCache._digital_img is None:
            digital_path = os.path.join("src", "assets", "digital.png")
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
        elipse_path = os.path.join("src", "assets", "elipse.png")
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

# Componente de grade de botões com imagens de pastas
class PastaButtonGrid(customtkinter.CTkFrame):
    def __init__(self, master, button_data):
        super().__init__(master, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=30, pady=(50, 150))
        
        # Configuração da grade
        rows = 2
        cols = 4
        
        # Verificar se temos dados suficientes
        if len(button_data) < rows * cols:
            raise ValueError(f"Precisa de {rows*cols} itens em button_data")
        
        # Configurar grid layout
        for i in range(rows):
            self.rowconfigure(i, weight=1, uniform="rows")
        for j in range(cols):
            self.columnconfigure(j, weight=1, uniform="cols")
        
        # Criar os botões
        self.buttons = []
        index = 0
        for i in range(rows):
            for j in range(cols):
                if index >= len(button_data):
                    break
                    
                # Frame para cada célula
                cell_frame = customtkinter.CTkFrame(self, fg_color="transparent")
                cell_frame.grid(row=i, column=j, padx=30, pady=10, sticky="nsew")
                
                # Criar o botão de pasta
                btn_data = button_data[index]
                btn = PastaButton(
                    master=cell_frame,
                    text=btn_data['text'],
                    command=btn_data['command'],
                    name=btn_data['name'],
                    tipo_usuario=btn_data['tipo_usuario']
                )
                
                self.buttons.append(btn)
                index += 1

# Componente de botão com imagem de pasta
class PastaButton:
    def __init__(self, master, text, command=None, name=None, tipo_usuario=None):
        """Componente de botão de pasta para a grade"""
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")
        
        # Obter o gerenciador de estado
        self.state_manager = PastaStateManager.get_instance()
        self.tipo_usuario = tipo_usuario  # 'repositor' ou 'vendedor'
        
        # Carregar ambas as imagens
        self.pasta_aberta = customtkinter.CTkImage(
            Image.open(os.path.join("src", "assets", "pasta.png")),
            size=(120, 120)
        )
        self.pasta_fechada = customtkinter.CTkImage(
            Image.open(os.path.join("src", "assets", "pasta_black.png")),
            size=(120, 120)
        )

        # Botão principal
        self.btn_pasta = customtkinter.CTkButton(
            self.frame,
            text="",  # Texto vazio no botão
            width=120,
            height=120,
            image=self.pasta_fechada,  # Começa com a pasta fechada
            fg_color="transparent",
            hover_color="#3B6A7D",
            command=self.manipular_estado
        )
        self.btn_pasta.pack(pady=(0, 5))

        # Label com o texto
        self.label = customtkinter.CTkLabel(
            self.frame,
            text=text,
            font=("Arial", 12),
            text_color="white"
        )
        self.label.pack()
        
        # Guardar o comando original e o ID da pasta
        self.command_original = command
        self.pasta_id = text  # Usando o texto como ID da pasta
        
        # Atualizar a imagem inicial baseada no estado atual
        self.atualizar_imagem()

    def atualizar_imagem(self):
        """Atualiza a imagem do botão baseado no estado atual"""
        estado = self.state_manager.get_estado(self.pasta_id)
        self.btn_pasta.configure(image=self.pasta_aberta if estado else self.pasta_fechada)

    def manipular_estado(self):
        """Manipula o estado da pasta baseado no tipo de usuário"""
        estado_atual = self.state_manager.get_estado(self.pasta_id)
        
        if self.tipo_usuario == 'administrador':
            # Administrador pode tanto abrir quanto fechar
            if not estado_atual:  # Se a pasta estiver fechada, abre com confirmação
                self._abrir_pasta_com_confirmacao()
            else:
                sucesso, mensagem = self.state_manager.fechar_pasta(self.pasta_id, self.tipo_usuario)
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
        
        elif self.tipo_usuario == 'vendedor':
            # Vendedor só pode abrir pastas fechadas
            if not estado_atual:
                self._abrir_pasta_com_confirmacao()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para fechar pastas")
        
        elif self.tipo_usuario == 'repositor':
            # Repositório só pode fechar pastas abertas
            if estado_atual:
                sucesso, mensagem = self.state_manager.fechar_pasta(self.pasta_id, self.tipo_usuario)
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para abrir pastas")
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido")
    
    def _abrir_pasta_com_confirmacao(self):
        """Mostra uma janela de confirmação antes de abrir a pasta"""
        # Cria uma janela de diálogo personalizada
        dialog = customtkinter.CTkToplevel()
        dialog.title("Confirmar Abertura")
        dialog.geometry("500x250")  # Aumentei a largura e altura
        dialog.resizable(False, False)  # Impede redimensionamento
        dialog.grab_set()  # Torna a janela modal
        
        # Centraliza a janela na tela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y-50}')  # Ajuste vertical
        
        # Frame principal para melhor organização
        main_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Adiciona o texto de aviso
        aviso = customtkinter.CTkLabel(
            main_frame,
            text=f"Deseja realmente abrir a pasta {self.pasta_id}?\n\n"
                 "Atenção: O sistema será bloqueado por 5 minutos após a abertura.",
            font=("Arial", 16, "bold"),  # Fonte maior
            wraplength=450,  # Largura maior para o texto
            justify="center"
        )
        aviso.pack(pady=(20, 30), padx=10, expand=True, fill="both")
        
        # Frame para os botões
        botoes_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.pack(pady=(10, 0))
        
        # Botão de confirmar
        btn_confirmar = customtkinter.CTkButton(
            botoes_frame,
            text="Confirmar",
            command=lambda: self._confirmar_abertura(dialog),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=140,
            height=40,
            font=("Arial", 14, "bold")
        )
        btn_confirmar.pack(side="left", padx=15)
        
        # Botão de cancelar
        btn_cancelar = customtkinter.CTkButton(
            botoes_frame,
            text="Cancelar",
            command=dialog.destroy,
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=140,
            height=40,
            font=("Arial", 14, "bold")
        )
        btn_cancelar.pack(side="right", padx=15)
        
        # Focar no botão de cancelar por padrão
        btn_cancelar.focus_set()
    
    def _confirmar_abertura(self, dialog):
        """Confirma a abertura da pasta e fecha o diálogo"""
        dialog.destroy()
        sucesso, mensagem = self.state_manager.abrir_pasta(self.pasta_id, self.tipo_usuario)
        messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
        if sucesso:
            self.atualizar_imagem()

    def mostrar_historico(self):
        """Mostra o histórico de alterações da pasta"""
        historico = self.state_manager.get_historico(self.pasta_id)
        
        if not historico:
            messagebox.showinfo("Histórico", "Nenhum registro de histórico para esta pasta.")
            return
        
        # Formata o histórico para exibição
        historico_formatado = []
        for acao, usuario, data in historico:
            acao_texto = "Aberta" if acao == "aberta" else "Fechada"
            historico_formatado.append(f"{data} - {acao_texto} por {usuario}")
        
        # Cria uma janela para exibir o histórico
        janela_historico = customtkinter.CTkToplevel()
        janela_historico.title(f"Histórico - Pasta {self.pasta_id}")
        janela_historico.geometry("500x300")
        
        frame = customtkinter.CTkFrame(janela_historico)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        label_titulo = customtkinter.CTkLabel(
            frame, 
            text=f"Histórico - Pasta {self.pasta_id}",
            font=("Arial", 14, "bold")
        )
        label_titulo.pack(pady=(0, 10))
        
        # Área de texto para exibir o histórico
        texto_historico = customtkinter.CTkTextbox(frame, wrap="word")
        texto_historico.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Insere os itens do histórico
        for item in historico_formatado:
            texto_historico.insert("end", item + "\n")
        
        # Desabilita a edição do texto
        texto_historico.configure(state="disabled")
        
        # Botão para fechar
        btn_fechar = customtkinter.CTkButton(
            frame,
            text="Fechar",
            command=janela_historico.destroy
        )
        btn_fechar.pack(pady=(10, 0))

# Componente de botão de voltar
class VoltarButton:
    def __init__(self, master, command):
        # Frame para agrupar o botão e o label
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.place(relx=0.5, rely=0.88, anchor="center")
        
        voltar_path = os.path.join("src", "assets", "botao_voltar.png")
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
                    fg_color="#f0f0f0" if self.maiusculas_ativado else "#ffffff",
                    text_color="#000000",
                    hover_color="#d5d5d5" if self.maiusculas_ativado else "#e0e0e0",
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
                    fg_color="#f0f0f0" if self.maiusculas_ativado else "#ffffff",
                    hover_color="#d5d5d5" if self.maiusculas_ativado else "#e0e0e0"
                )
            
            # Reconstrói o teclado para atualizar as letras
            for widget in self.winfo_children():
                widget.destroy()
            self.criar_teclado()
        else:
            # Aplica maiúsculas se estiver ativado
            tecla_inserida = tecla.upper() if self.maiusculas_ativado and tecla.isalpha() else tecla
            self.entrada_atual.insert('end', tecla_inserida)
            
            # Desativa o modo maiúsculas após inserir uma letra (comportamento comum em teclados)
            if self.maiusculas_ativado and tecla.isalpha():
                self.maiusculas_ativado = False
                if hasattr(self, 'btn_maiusculas'):
                    self.btn_maiusculas.configure(
                        fg_color="#ffffff",
                        hover_color="#e0e0e0"
                    )
            
    def definir_entrada(self, entrada):
        self.entrada_atual = entrada

# Atualizar a lista __all__ para incluir o novo componente
__all__ = [
    'Header', 'FinalizarSessaoButton', 'PastaButtonGrid', 
    'PastaButton', 'VoltarButton', 'MainButton', 'ImageCache',
    'TecladoVirtual'
]
