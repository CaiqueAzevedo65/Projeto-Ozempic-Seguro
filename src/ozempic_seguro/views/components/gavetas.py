"""
Componentes de gavetas: GavetaButton, GavetaButtonGrid
"""
import customtkinter
from tkinter import messagebox
from PIL import Image
import os

from ...services.drawer_service import get_drawer_service
from ...services.timer_control_service import get_timer_control_service
from ...services.auth_service import get_auth_service


# Cache global de imagens de gavetas
class _GavetaImageCache:
    _gaveta_aberta = None
    _gaveta_fechada = None
    _assets_path = None
    
    @classmethod
    def _get_assets_path(cls):
        if cls._assets_path is None:
            cls._assets_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "..", "assets"
            ))
        return cls._assets_path
    
    @classmethod
    def get_gaveta_aberta(cls):
        if cls._gaveta_aberta is None:
            cls._gaveta_aberta = customtkinter.CTkImage(
                Image.open(os.path.join(cls._get_assets_path(), "gaveta.png")),
                size=(120, 120)
            )
        return cls._gaveta_aberta
    
    @classmethod
    def get_gaveta_fechada(cls):
        if cls._gaveta_fechada is None:
            cls._gaveta_fechada = customtkinter.CTkImage(
                Image.open(os.path.join(cls._get_assets_path(), "gaveta_black.png")),
                size=(120, 120)
            )
        return cls._gaveta_fechada


class GavetaButton:
    """Componente de botão de gaveta para a grade"""
    
    def __init__(self, master, text, command=None, name=None, tipo_usuario=None):
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")
        
        self.drawer_service = get_drawer_service()
        self.timer_service = get_timer_control_service()
        self.auth_service = get_auth_service()
        self.tipo_usuario = tipo_usuario
        
        # Usar cache de imagens (muito mais rápido)
        self.gaveta_aberta = _GavetaImageCache.get_gaveta_aberta()
        self.gaveta_fechada = _GavetaImageCache.get_gaveta_fechada()

        self.btn_gaveta = customtkinter.CTkButton(
            self.frame,
            text="",
            width=120,
            height=120,
            image=self.gaveta_fechada,
            fg_color="transparent",
            hover_color="#3B6A7D",
            command=self.manipular_estado
        )
        self.btn_gaveta.pack(pady=(0, 5))

        self.label = customtkinter.CTkLabel(
            self.frame,
            text=text,
            font=("Arial", 12),
            text_color="white"
        )
        self.label.pack()
        
        self.command_original = command
        self.gaveta_id = text
        self.atualizar_imagem()

    def atualizar_imagem(self):
        """Atualiza a imagem do botão baseado no estado atual"""
        state = self.drawer_service.get_drawer_state(int(self.gaveta_id))
        esta_aberta = state.esta_aberta if state else False
        self.btn_gaveta.configure(
            image=self.gaveta_aberta if esta_aberta else self.gaveta_fechada
        )

    def manipular_estado(self):
        """Manipula o estado da gaveta baseado no tipo de usuário"""
        state = self.drawer_service.get_drawer_state(int(self.gaveta_id))
        estado_atual = state.esta_aberta if state else False
        
        current_user = self.auth_service.get_current_user()
        user_id = current_user.get('id') if current_user else None
        
        if self.tipo_usuario == 'administrador':
            if not estado_atual:
                self._abrir_gaveta_com_confirmacao()
            else:
                sucesso, mensagem = self.drawer_service.set_drawer_state(
                    int(self.gaveta_id), False, self.tipo_usuario, user_id
                )
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
        
        elif self.tipo_usuario == 'vendedor':
            if not estado_atual:
                self._abrir_gaveta_com_confirmacao()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para fechar gavetas")
        
        elif self.tipo_usuario == 'repositor':
            if estado_atual:
                sucesso, mensagem = self.drawer_service.set_drawer_state(
                    int(self.gaveta_id), False, self.tipo_usuario, user_id
                )
                messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
                if sucesso:
                    self.atualizar_imagem()
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para abrir gavetas")
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido")
    
    def _abrir_gaveta_com_confirmacao(self):
        """Mostra janela de confirmação antes de abrir a gaveta"""
        if not self.timer_service.is_timer_enabled():
            current_user = self.auth_service.get_current_user()
            user_id = current_user.get('id') if current_user else None
            sucesso, mensagem = self.drawer_service.set_drawer_state(
                int(self.gaveta_id), True, self.tipo_usuario, user_id
            )
            messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
            if sucesso:
                self.atualizar_imagem()
            return
            
        dialog = customtkinter.CTkToplevel()
        dialog.title("Confirmar Abertura")
        dialog.geometry("500x250")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (250)
        y = (dialog.winfo_screenheight() // 2) - (125)
        dialog.geometry(f'+{x}+{y}')
        
        main_frame = customtkinter.CTkFrame(dialog, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(
            main_frame,
            text="Confirmar Abertura",
            font=("Arial", 16, "bold"),
            text_color="black"
        ).pack(pady=(10, 5))
        
        if self.tipo_usuario == 'vendedor':
            mensagem = (f"Deseja realmente abrir a gaveta {self.gaveta_id}?\n\n"
                       "O sistema será bloqueado por 5 minutos após a abertura.\n"
                       "Você terá acesso somente para visualizar os dados.")
        else:
            mensagem = (f"Deseja realmente abrir a gaveta {self.gaveta_id}?\n\n"
                       "O sistema será bloqueado por 5 minutos após a abertura.")
        
        customtkinter.CTkLabel(
            main_frame,
            text=mensagem,
            font=("Arial", 12),
            text_color="black",
            wraplength=400,
            justify="center"
        ).pack(pady=10, padx=20)
        
        button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        customtkinter.CTkButton(
            button_frame,
            text="Confirmar",
            font=("Arial", 12, "bold"),
            width=120,
            command=lambda: self._on_confirmar_abertura(dialog)
        ).pack(side="left", padx=10)
        
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
        current_user = self.auth_service.get_current_user()
        user_id = current_user.get('id') if current_user else None
        
        sucesso, mensagem = self.drawer_service.set_drawer_state(
            int(self.gaveta_id), True, self.tipo_usuario, user_id
        )
        messagebox.showinfo("Sucesso" if sucesso else "Aviso", mensagem)
        if sucesso:
            self.atualizar_imagem()

    def mostrar_historico(self):
        """Mostra o histórico de alterações da gaveta com paginação"""
        self.itens_por_pagina = 20
        self.pagina_atual = 1
        
        self.janela_historico = customtkinter.CTkToplevel()
        self.janela_historico.title(f"Histórico - Gaveta {self.gaveta_id}")
        self.janela_historico.geometry("600x400")
        
        frame_principal = customtkinter.CTkFrame(self.janela_historico)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        customtkinter.CTkLabel(
            frame_principal, 
            text=f"Histórico - Gaveta {self.gaveta_id}",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))
        
        self.frame_historico = customtkinter.CTkScrollableFrame(
            frame_principal, fg_color="transparent"
        )
        self.frame_historico.pack(fill="both", expand=True)
        
        frame_controles = customtkinter.CTkFrame(frame_principal, fg_color="transparent")
        frame_controles.pack(fill="x", pady=(5, 0))
        
        self.btn_anterior = customtkinter.CTkButton(
            frame_controles, text="Anterior",
            command=self._pagina_anterior, state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=5)
        
        self.lbl_pagina = customtkinter.CTkLabel(
            frame_controles, text="Página 1", width=100
        )
        self.lbl_pagina.pack(side="left")
        
        self.btn_proximo = customtkinter.CTkButton(
            frame_controles, text="Próximo", command=self._proxima_pagina
        )
        self.btn_proximo.pack(side="left", padx=5)
        
        customtkinter.CTkButton(
            frame_controles, text="Fechar",
            command=self.janela_historico.destroy
        ).pack(side="right")
        
        self._carregar_historico()
    
    def _carregar_historico(self):
        """Carrega os itens do histórico para a página atual usando DrawerService"""
        for widget in self.frame_historico.winfo_children():
            widget.destroy()
        
        result = self.drawer_service.get_drawer_history(
            int(self.gaveta_id), page=self.pagina_atual, per_page=self.itens_por_pagina
        )
        
        total_paginas = max(1, result.total_pages)
        
        self.lbl_pagina.configure(text=f"Página {self.pagina_atual} de {total_paginas}")
        self.btn_anterior.configure(state="disabled" if self.pagina_atual == 1 else "normal")
        self.btn_proximo.configure(state="disabled" if self.pagina_atual >= total_paginas else "normal")
        
        if not result.items:
            customtkinter.CTkLabel(
                self.frame_historico,
                text="Nenhum registro de histórico para esta gaveta.",
                text_color="gray"
            ).pack(pady=10)
            return
        
        for item in result.items:
            acao_texto = item.acao_display
            
            frame_item = customtkinter.CTkFrame(
                self.frame_historico, fg_color="#f0f0f0", corner_radius=5
            )
            frame_item.pack(fill="x", pady=2, padx=2)
            
            customtkinter.CTkLabel(
                frame_item,
                text=f"{item.data_hora} - {acao_texto} por {item.usuario}",
                anchor="w", justify="left"
            ).pack(fill="x", padx=5, pady=5)
    
    def _proxima_pagina(self):
        self.pagina_atual += 1
        self._carregar_historico()
    
    def _pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self._carregar_historico()


class GavetaButtonGrid(customtkinter.CTkFrame):
    """Componente de grade de botões com imagens de gavetas"""
    
    def __init__(self, master, button_data):
        super().__init__(master, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=30, pady=20)
        
        self.button_data = button_data
        self.current_page = 0
        self.rows = 2
        self.cols = 4
        self.buttons_per_page = self.rows * self.cols
        self.total_pages = max(1, (len(self.button_data) + self.buttons_per_page - 1) // self.buttons_per_page)
        
        self.grid_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both")
        
        self.nav_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=(10, 0))
        
        for i in range(self.rows):
            self.grid_frame.rowconfigure(i, weight=1)
        for j in range(self.cols):
            self.grid_frame.columnconfigure(j, weight=1)
        
        self.criar_controles_navegacao()
        self.mostrar_pagina(0)
    
    def criar_controles_navegacao(self):
        """Cria os controles de navegação entre páginas"""
        self.btn_frame = customtkinter.CTkFrame(self.nav_frame, fg_color="transparent")
        self.btn_frame.pack(side="left", anchor="w", padx=10)
        
        self.btn_anterior = customtkinter.CTkButton(
            self.btn_frame, text="← Anterior",
            command=self.pagina_anterior, width=120, state="disabled"
        )
        self.btn_anterior.pack(side="left", padx=(0, 5))
        
        self.btn_proximo = customtkinter.CTkButton(
            self.btn_frame, text="Próxima →",
            command=self.proxima_pagina, width=120
        )
        self.btn_proximo.pack(side="left")
        
        if self.total_pages <= 1:
            self.nav_frame.pack_forget()
    
    def pagina_anterior(self):
        if self.current_page > 0:
            self.mostrar_pagina(self.current_page - 1)
            
    def proxima_pagina(self):
        if self.current_page < self.total_pages - 1:
            self.mostrar_pagina(self.current_page + 1)
            
    def mostrar_pagina(self, page_num):
        """Mostra a página especificada"""
        if page_num < 0 or page_num >= self.total_pages:
            return
            
        self.current_page = page_num
        
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        start_idx = page_num * self.buttons_per_page
        end_idx = min(start_idx + self.buttons_per_page, len(self.button_data))
        
        for i in range(self.rows):
            for j in range(self.cols):
                item_idx = start_idx + (i * self.cols) + j
                if item_idx >= end_idx:
                    break
                    
                cell_frame = customtkinter.CTkFrame(self.grid_frame, fg_color="transparent")
                cell_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                
                if item_idx < end_idx:
                    btn_data = self.button_data[item_idx]
                    GavetaButton(
                        master=cell_frame,
                        text=btn_data['text'],
                        command=btn_data['command'],
                        name=btn_data['name'],
                        tipo_usuario=btn_data['tipo_usuario']
                    )
        
        self.atualizar_controles_navegacao()
    
    def atualizar_controles_navegacao(self):
        """Atualiza o estado dos controles de navegação"""
        if hasattr(self, 'btn_anterior') and hasattr(self, 'btn_proximo'):
            self.btn_anterior.configure(
                state="normal" if self.current_page > 0 else "disabled"
            )
            self.btn_proximo.configure(
                state="normal" if self.current_page < self.total_pages - 1 else "disabled"
            )
