"""
View do repositor - permite abrir e fechar gavetas.
"""
from .base_user_view import BaseUserFrame
from .components import GavetaButton


class RepositorFrame(BaseUserFrame):
    """Frame para usuários do tipo repositor."""

    TITULO = "Repositor"
    TIPO_USUARIO = "repositor"

    def mostrar_historico_gaveta(self, gaveta_id):
        """Mostra o histórico de uma gaveta específica"""
        button = GavetaButton(
            self,
            text=gaveta_id,
            command=None,
            name="gaveta_black.png",
            tipo_usuario=self.TIPO_USUARIO,
        )
        button.mostrar_historico()
        button.destroy()
