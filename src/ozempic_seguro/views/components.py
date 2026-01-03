"""
Módulo de componentes UI - Wrapper para compatibilidade.

Este módulo foi refatorado e dividido em submódulos em views/components/.
Mantido para compatibilidade com código existente.

Use preferencialmente:
    from .components import Header, ModernButton, etc.
ou:
    from .components.buttons import ModernButton
    from .components.dialogs import ToastNotification
"""

# Re-exportar todos os componentes do novo pacote
from .components import (
    # Common
    Header,
    ImageCache,
    MainButton,
    # Buttons
    ModernButton,
    VoltarButton,
    FinalizarSessaoButton,
    # Dialogs
    ModernConfirmDialog,
    ToastNotification,
    # Layouts
    ResponsiveFrame,
    ResponsiveButtonGrid,
    # Gavetas
    GavetaButton,
    GavetaButtonGrid,
    # Keyboard
    TecladoVirtual,
)

__all__ = [
    "Header",
    "ImageCache",
    "MainButton",
    "ModernButton",
    "VoltarButton",
    "FinalizarSessaoButton",
    "ModernConfirmDialog",
    "ToastNotification",
    "ResponsiveFrame",
    "ResponsiveButtonGrid",
    "GavetaButton",
    "GavetaButtonGrid",
    "TecladoVirtual",
]
