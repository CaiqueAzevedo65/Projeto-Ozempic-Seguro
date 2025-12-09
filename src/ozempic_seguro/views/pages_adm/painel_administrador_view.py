from ..base_frame import BaseFrameView
from ..components import ResponsiveButtonGrid
from .gerenciamento_usuarios_view import GerenciamentoUsuariosFrame
from .cadastro_usuario_view import CadastroUsuarioFrame
from .diagnostico_view import DiagnosticoFrame
from .historico_view import HistoricoView
from .admin_gavetas_view import AdminGavetasFrame
from .auditoria_view import AuditoriaFrame


class PainelAdministradorFrame(BaseFrameView):
    """Painel do administrador - herda de BaseFrameView"""
    
    def __init__(self, master, finalizar_sessao_callback=None, usuario_logado=None, *args, **kwargs):
        self.usuario_logado = usuario_logado
        super().__init__(master, finalizar_sessao_callback, *args, **kwargs)
        self.criar_tela_principal()

    def criar_tela_principal(self):
        """Cria a tela principal do administrador"""
        for widget in self.winfo_children():
            widget.destroy()
            
        self.criar_header("Administrador")
        self.criar_botoes()
        self.criar_botao_finalizar()

    def criar_botoes(self):
        buttons_data = [
            {"text": "👥 Gerenciar Usuários", "command": self.gerenciar_usuarios, "style": "primary"},
            {"text": "🗄️ Gerenciar Gavetas", "command": self.gerenciar_gavetas, "style": "primary"},
            {"text": "➕ Cadastro de Usuário", "command": self.cadastro_usuario, "style": "success"},
            {"text": "📋 Registro de Auditoria", "command": self.registro_auditoria, "style": "secondary"},
            {"text": "🔧 Diagnóstico", "command": self.diagnostico, "style": "warning"},
            {"text": "📊 Histórico", "command": self.mostrar_historico, "style": "secondary"}
        ]
        self.button_grid = ResponsiveButtonGrid(self, buttons_data, max_cols=3)

    def gerenciar_gavetas(self):
        self._transicao_tela(lambda: AdminGavetasFrame(self, voltar_callback=self.voltar_principal))

    def mostrar_historico(self):
        self._transicao_tela(lambda: HistoricoView(self, voltar_callback=self.voltar_principal))

    def registro_auditoria(self):
        self._transicao_tela(lambda: AuditoriaFrame(self, voltar_callback=self.voltar_principal))

    def gerenciar_usuarios(self):
        def criar():
            if hasattr(self, 'usuario_logado'):
                GerenciamentoUsuariosFrame(self, voltar_callback=self.voltar_principal, usuario_logado=self.usuario_logado)
            else:
                GerenciamentoUsuariosFrame(self, voltar_callback=self.voltar_principal, usuario_logado=None)
        self._transicao_tela(criar)

    def cadastro_usuario(self):
        self._transicao_tela(lambda: CadastroUsuarioFrame(self, voltar_callback=self.voltar_principal))

    def diagnostico(self):
        self._transicao_tela(lambda: DiagnosticoFrame(self, voltar_callback=self.voltar_principal))
    
    def voltar_principal(self):
        """Volta para a tela principal com transição"""
        self._transicao_tela(self.criar_tela_principal)
