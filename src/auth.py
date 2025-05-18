from src.data.database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()

    def autenticar(self, usuario, senha):
        """Autentica um usuário usando o banco de dados"""
        return self.db.autenticar_usuario(usuario, senha)