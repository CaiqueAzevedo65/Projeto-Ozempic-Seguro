import customtkinter
from PIL import Image
import os

class TelaToqueFrame(customtkinter.CTkFrame):
    def __init__(self, master, on_click_callback, *args, **kwargs):
        super().__init__(master, fg_color="white", *args, **kwargs)
        self.pack(fill="both", expand=True)
        self.label = customtkinter.CTkLabel(self, text="TOQUE NA TELA PARA COMEÇAR", font=("Arial", 32, "bold"), text_color="black")
        self.label.pack(pady=40)
        # Mostra a imagem do dedo
        img_path = os.path.join("src", "assets", "dedo.png")  # ajuste o nome se necessário
        self.img = customtkinter.CTkImage(Image.open(img_path), size=(300, 300))
        self.img_label = customtkinter.CTkLabel(self, image=self.img, text="")
        self.img_label.pack(pady=20)
        self.bind("<Button-1>", lambda e: on_click_callback())
        self.label.bind("<Button-1>", lambda e: on_click_callback())
        self.img_label.bind("<Button-1>", lambda e: on_click_callback()) 