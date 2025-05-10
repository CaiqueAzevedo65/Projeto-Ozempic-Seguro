import os
from PIL import Image
import customtkinter

def load_image_as_ctk_image(image_path, size):
    """Carrega uma imagem e retorna como CTkImage."""
    try:
        image = Image.open(image_path)
        return customtkinter.CTkImage(image, size=size)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return None 