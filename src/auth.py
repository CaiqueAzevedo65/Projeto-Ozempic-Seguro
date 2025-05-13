import json
import os

class AuthManager:
    def __init__(self, usuarios_path=None):
        if usuarios_path is None:
            usuarios_path = os.path.join(os.path.dirname(__file__), 'data', 'usuarios.json')
        self.usuarios_path = usuarios_path
        self.usuarios = self._carregar_usuarios()

    def _carregar_usuarios(self):
        with open(self.usuarios_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def autenticar(self, usuario, senha):
        for user in self.usuarios:
            if user['usuario'] == usuario and user['senha'] == senha:
                return user  # Retorna o dicionário do usuário
        return None 