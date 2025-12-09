"""
Componentes UI reutilizáveis do Ozempic Seguro.

Este pacote organiza os componentes em módulos separados por funcionalidade:
- buttons: Botões modernos e especializados
- dialogs: Diálogos e notificações
- layouts: Frames e grids responsivos
- gavetas: Componentes específicos de gavetas
- keyboard: Teclado virtual
- common: Componentes comuns (Header, ImageCache)
"""

# Importações para manter compatibilidade com código existente
from .common import Header, ImageCache, MainButton
from .buttons import ModernButton, VoltarButton, FinalizarSessaoButton
from .dialogs import ModernConfirmDialog, ToastNotification
from .layouts import ResponsiveFrame, ResponsiveButtonGrid
from .gavetas import GavetaButton, GavetaButtonGrid
from .keyboard import TecladoVirtual

__all__ = [
    # Common
    'Header',
    'ImageCache', 
    'MainButton',
    # Buttons
    'ModernButton',
    'VoltarButton',
    'FinalizarSessaoButton',
    # Dialogs
    'ModernConfirmDialog',
    'ToastNotification',
    # Layouts
    'ResponsiveFrame',
    'ResponsiveButtonGrid',
    # Gavetas
    'GavetaButton',
    'GavetaButtonGrid',
    # Keyboard
    'TecladoVirtual',
]
