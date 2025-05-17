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
            novo_estado = not estado_atual  # Inverte o estado atual
            if novo_estado:
                self.state_manager.abrir_pasta(self.pasta_id, self.tipo_usuario)
                mensagem = f"Pasta {self.pasta_id} aberta com sucesso!"
            else:
                self.state_manager.fechar_pasta(self.pasta_id, self.tipo_usuario)
                mensagem = f"Pasta {self.pasta_id} fechada com sucesso!"
            
            messagebox.showinfo("Sucesso", mensagem)
        
        elif self.tipo_usuario == 'vendedor':
            # Vendedor só pode abrir pastas fechadas
            if not estado_atual:
                self.state_manager.abrir_pasta(self.pasta_id, self.tipo_usuario)
                messagebox.showinfo("Sucesso", f"Pasta {self.pasta_id} aberta com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para fechar pastas")
                return
        
        elif self.tipo_usuario == 'repositor':
            # Repositório só pode fechar pastas abertas
            if estado_atual:
                self.state_manager.fechar_pasta(self.pasta_id, self.tipo_usuario)
                messagebox.showinfo("Sucesso", f"Pasta {self.pasta_id} fechada com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para abrir pastas")
                return
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido")
            return
        
        # Atualiza a imagem do botão
        self.atualizar_imagem()
        
        # Executa o comando original, se houver
        if hasattr(self, 'command_original') and self.command_original is not None:
            self.command_original()

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

__all__ = [
    'Header', 'FinalizarSessaoButton', 'PastaButtonGrid', 
    'PastaButton', 'VoltarButton', 'MainButton', 'ImageCache'
]


