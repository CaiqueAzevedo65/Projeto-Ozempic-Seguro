"""
View do vendedor - permite apenas abrir gavetas.
"""
from .base_user_view import BaseUserFrame


class VendedorFrame(BaseUserFrame):
    """Frame para usuários do tipo vendedor."""

    TITULO = "Vendedor"
    TIPO_USUARIO = "vendedor"
