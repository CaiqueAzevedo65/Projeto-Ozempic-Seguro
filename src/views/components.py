import customtkinter
from PIL import Image
import os

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

# Componente de botão com imagem de pasta
class PastaButtonGrid(customtkinter.CTkFrame):
    def __init__(self, master, button_data):
        super().__init__(master, fg_color="transparent")
        # Aumentamos o pady do frame principal para empurrar o conteúdo para o centro
        self.pack(expand=True, fill="both", padx=30, pady=(50, 150))  # Aumentado pady para 100
        
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
                # Reduzimos o pady do grid para aproximar as linhas
                cell_frame.grid(row=i, column=j, padx=30, pady=10, sticky="nsew")
                
                # Criar o botão de pasta
                btn_data = button_data[index]
                btn = PastaButton(
                    master=cell_frame,
                    text=btn_data['text'],
                    command=btn_data['command']
                )
                
                self.buttons.append(btn)
                index += 1


class PastaButton:
    def __init__(self, master, text, command=None):
        """Componente de botão de pasta para a grade"""
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")
        
        # Caminho para a imagem (ajuste conforme sua estrutura de arquivos)
        pasta_path = os.path.join("src", "assets", "pasta.png")
        
        # Carregar imagem redimensionada
        self.pasta_img = customtkinter.CTkImage(
            Image.open(pasta_path),
            size=(120, 120)  # Tamanho ajustado para a grade
        )

        # Botão principal
        self.btn_pasta = customtkinter.CTkButton(
            self.frame,
            text="",  # Texto vazio no botão
            width=120,
            height=120,
            image=self.pasta_img,
            fg_color="transparent",
            hover_color="#3B6A7D",
            command=command
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