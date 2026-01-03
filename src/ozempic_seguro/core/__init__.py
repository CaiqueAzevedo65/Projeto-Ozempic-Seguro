"""
Módulo core - Componentes fundamentais do sistema.

Fornece utilitários, validadores, cache, logging e exceções customizadas.
"""
from .validators import Validators, ValidationResult
from .cache import MemoryCache, cached
from .logger import logger
from .exceptions import (
    # Base
    OzempicError,
    # Authentication
    AuthenticationError,
    InvalidCredentialsError,
    SessionExpiredError,
    AccountLockedError,
    InsufficientPermissionsError,
    # User
    UserError,
    UserNotFoundError,
    UserAlreadyExistsError,
    LastAdminError,
    InvalidUserDataError,
    # Validation
    ValidationError,
    InvalidUsernameError,
    WeakPasswordError,
    InvalidInputError,
    # Database
    DatabaseError,
    MigrationError,
    IntegrityError,
    # Drawer
    DrawerError,
    DrawerNotFoundError,
    DrawerStateError,
    # Audit
    AuditError,
    AuditLogError,
    # Configuration
    ConfigurationError,
    MissingConfigError,
    InvalidConfigError,
)

__all__ = [
    # Validators
    "Validators",
    "ValidationResult",
    # Cache
    "MemoryCache",
    "cached",
    # Logger
    "logger",
    # Exceptions - Base
    "OzempicError",
    # Exceptions - Auth
    "AuthenticationError",
    "InvalidCredentialsError",
    "SessionExpiredError",
    "AccountLockedError",
    "InsufficientPermissionsError",
    # Exceptions - User
    "UserError",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "LastAdminError",
    "InvalidUserDataError",
    # Exceptions - Validation
    "ValidationError",
    "InvalidUsernameError",
    "WeakPasswordError",
    "InvalidInputError",
    # Exceptions - Database
    "DatabaseError",
    "MigrationError",
    "IntegrityError",
    # Exceptions - Drawer
    "DrawerError",
    "DrawerNotFoundError",
    "DrawerStateError",
    # Exceptions - Audit
    "AuditError",
    "AuditLogError",
    # Exceptions - Config
    "ConfigurationError",
    "MissingConfigError",
    "InvalidConfigError",
]
