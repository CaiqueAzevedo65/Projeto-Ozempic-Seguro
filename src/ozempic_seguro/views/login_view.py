import customtkinter
import tkinter as tk
from tkinter import messagebox
from .pages_adm.painel_administrador_view import PainelAdministradorFrame
from .components import Header, ImageCache, VoltarButton, ModernButton, ToastNotification
from ..services.service_factory import get_user_service
from ..session import SessionManager
from .repositor_view import RepositorFrame
from .vendedor_view import VendedorFrame
from .tecnico_view import TecnicoFrame

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, show_iniciar_callback, *args, **kwargs):
        super().__init__(master, fg_color="#346172", *args, **kwargs)
        self.show_iniciar_callback = show_iniciar_callback
        self.user_service = get_user_service()
        self.session_manager = SessionManager.get_instance()
        self.timer_job = None
        self.pack(fill="both", expand=True)
        self.criar_topo()
        self.criar_interface_login()
        self.criar_teclado_numerico()
        self.criar_botao_voltar()

    def criar_topo(self):
        Header(self, "Login")

    def criar_interface_login(self):
        frame_login = customtkinter.CTkFrame(self, fg_color="#346172")
        frame_login.place(x=40, y=100)
        
        # Campo de usuário
        customtkinter.CTkLabel(frame_login, text="Usuário", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(0, 5))
        self.usuario_entry = customtkinter.CTkEntry(frame_login, width=300, height=40)
        self.usuario_entry.pack(pady=10)
        self.usuario_entry.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.usuario_entry))
        
        # Campo de senha
        customtkinter.CTkLabel(frame_login, text="Senha", font=("Arial", 16, "bold"), text_color="white").pack(anchor="w", pady=(20, 5))
        self.senha_entry = customtkinter.CTkEntry(frame_login, width=300, height=40, show="*")
        self.senha_entry.pack(pady=10)
        self.senha_entry.bind("<Button-1>", lambda e: self.definir_campo_ativo(self.senha_entry))
        
        # Label de status/avisos
        self.status_label = customtkinter.CTkLabel(
            frame_login, 
            text="Digite suas credenciais para acessar o sistema", 
            font=("Arial", 12), 
            text_color="#90EE90",
            wraplength=280
        )
        self.status_label.pack(pady=(10, 0))
        
        # Campo ativo por padrão
        self.campo_ativo = self.usuario_entry
        
        # Bind para atualizar status quando usuário digita
        self.usuario_entry.bind("<KeyRelease>", self.atualizar_status_login)
        
        # Define o foco no campo de usuário
        self.after(100, lambda: self.usuario_entry.focus_set())

    def criar_botao_voltar(self):
        VoltarButton(self, self.show_iniciar_callback)

    def criar_teclado_numerico(self):
        teclado_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=20)
        teclado_frame.place(x=500, y=100)
        botoes = [
            ["1", "2", "3"],
            ["4", "5", "6"], 
            ["7", "8", "9"],
            ["", "0", ""]
        ]
        
        # Criar botões numéricos
        for i, linha in enumerate(botoes):
            for j, texto in enumerate(linha):
                if texto:
                    btn = ModernButton(
                        teclado_frame, 
                        text=texto, 
                        command=lambda t=texto: self.tecla(t),
                        style="secondary",
                        width=90,
                        height=50,
                        font=("Arial", 16, "bold")
                    )
                    btn.grid(row=i, column=j, padx=8, pady=8)
        
        # Botões de ação na parte inferior
        action_frame = customtkinter.CTkFrame(teclado_frame, fg_color="transparent")
        action_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        ModernButton(
            action_frame,
            text="🗑️ Apagar",
            command=lambda: self.tecla("Apagar"),
            style="warning",
            width=120,
            height=45
        ).pack(side="left", padx=5)
        
        ModernButton(
            action_frame,
            text="❌ Cancelar", 
            command=lambda: self.tecla("Cancelar"),
            style="danger",
            width=120,
            height=45
        ).pack(side="left", padx=5)
        
        ModernButton(
            action_frame,
            text="✅ Confirmar",
            command=lambda: self.tecla("Confirmar"),
            style="success",
            width=120,
            height=45
        ).pack(side="left", padx=5)

    def verificar_login(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get()
        
        # Verifica se usuário está bloqueado
        if self.session_manager.is_user_locked(usuario):
            status = self.session_manager.get_login_status_message(usuario)
            messagebox.showerror("Conta Bloqueada", status['detailed_message'])
            self.iniciar_timer_bloqueio(usuario)
            return
        
        # Tenta autenticar
        user = self.user_service.authenticate(usuario, senha)
        if user:
            # Sucesso - Reset tentativas e prossegue
            self.session_manager.record_login_attempt(usuario, success=True)
            self.session_manager.set_current_user(user)
            
            if user.get('tipo') == 'administrador':
                self.abrir_painel_administrador()
            elif user.get('tipo') == 'repositor':
                self.abrir_painel_repositor()
            elif user.get('tipo') == 'vendedor':
                self.abrir_painel_vendedor()
            elif user.get('tipo') == 'tecnico':
                self.abrir_painel_tecnico()
            else:
                messagebox.showinfo("Sucesso", f"Login realizado como {user.get('tipo','usuário')}!") 
        else:
            # Falha - Registra tentativa e mostra aviso personalizado
            self.session_manager.record_login_attempt(usuario, success=False)
            status = self.session_manager.get_login_status_message(usuario)
            
            if status['locked']:
                messagebox.showerror("Conta Bloqueada", status['detailed_message'])
                self.iniciar_timer_bloqueio(usuario)
            else:
                messagebox.showerror("Login Inválido", status['detailed_message'])
            
            # Atualiza status visual
            self.atualizar_status_login()

    def abrir_painel_tecnico(self):
        """Abre o painel do técnico"""
        self.pack_forget()
        TecnicoFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def abrir_painel_vendedor(self):
        self.pack_forget()
        VendedorFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def abrir_painel_repositor(self):
        self.pack_forget()
        RepositorFrame(self.master, finalizar_sessao_callback=self.show_iniciar_callback)

    def abrir_painel_administrador(self):
        self.pack_forget()
        # Get the current user from SessionManager and pass it to PainelAdministradorFrame
        session_manager = SessionManager.get_instance()
        usuario_logado = session_manager.get_current_user()
        PainelAdministradorFrame(
            self.master, 
            finalizar_sessao_callback=self.show_iniciar_callback,
            usuario_logado=usuario_logado
        )

    def definir_campo_ativo(self, campo):
        """Define qual campo está ativo para receber entrada do teclado"""
        self.campo_ativo = campo

    def tecla(self, valor):
        if valor == "Apagar":
            if self.campo_ativo == self.usuario_entry:
                self.usuario_entry.delete(len(self.usuario_entry.get()) - 1, tk.END)
            else:
                self.senha_entry.delete(len(self.senha_entry.get()) - 1, tk.END)
        elif valor == "Cancelar":
            if self.campo_ativo == self.usuario_entry:
                self.usuario_entry.delete(0, tk.END)
            else:
                self.senha_entry.delete(0, tk.END)
        elif valor == "Confirmar":
            self.verificar_login()
        else:
            # Incrementa entrada no campo ativo
            if self.campo_ativo == self.usuario_entry:
                self.usuario_entry.insert(tk.END, valor)
            else:
                self.senha_entry.insert(tk.END, valor)

    def atualizar_status_login(self, event=None):
        """Atualiza o status de login baseado no usuário digitado"""
        usuario = self.usuario_entry.get().strip()
        
        if not usuario:
            self.status_label.configure(
                text="Digite suas credenciais para acessar o sistema",
                text_color="#90EE90"
            )
            return
        
        status = self.session_manager.get_login_status_message(usuario)
        
        if status['locked']:
            self.status_label.configure(
                text=status['message'],
                text_color="#FF6B6B"
            )
            self.iniciar_timer_bloqueio(usuario)
        elif status['remaining_attempts'] < 3:
            self.status_label.configure(
                text=status['message'],
                text_color="#FFA500"
            )
        else:
            self.status_label.configure(
                text=status['message'],
                text_color="#90EE90"
            )

    def iniciar_timer_bloqueio(self, usuario):
        """Inicia timer visual para conta bloqueada"""
        if self.timer_job:
            self.after_cancel(self.timer_job)
        
        self.atualizar_timer_bloqueio(usuario)

    def atualizar_timer_bloqueio(self, usuario):
        """Atualiza o timer de bloqueio em tempo real"""
        remaining_seconds = self.session_manager.get_lockout_remaining_seconds(usuario)
        
        if remaining_seconds <= 0:
            # Bloqueio expirou
            self.status_label.configure(
                text="Bloqueio expirado. Você pode tentar fazer login novamente",
                text_color="#90EE90"
            )
            self.timer_job = None
            return
        
        # Formatar tempo restante
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        
        self.status_label.configure(
            text=f" Conta bloqueada - Restam {minutes}:{seconds:02d}",
            text_color="#FF6B6B"
        )
        
        # Agenda próxima atualização
        self.timer_job = self.after(1000, lambda: self.atualizar_timer_bloqueio(usuario))