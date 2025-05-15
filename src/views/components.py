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