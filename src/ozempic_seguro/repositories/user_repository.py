"""
Repositório de usuários: operações CRUD e autenticação.
"""
from .database import DatabaseManager
from .security import hash_password, verify_password

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def create_user(self, username: str, senha: str, nome_completo: str, tipo: str) -> int|None:
        """Cria um usuário e retorna seu ID."""
        senha_hash = hash_password(senha)
        try:
            self.db.cursor.execute(
                'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo) VALUES (?, ?, ?, ?)',
                (username, senha_hash, nome_completo, tipo)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception:
            return None

    def authenticate_user(self, username: str, password: str) -> dict|None:
        """Autentica usuário e retorna dados se bem-sucedido."""
        # Usa o método do DatabaseManager que já funciona corretamente
        return self.db.autenticar_usuario(username, password)

    def delete_user(self, user_id: int) -> bool:
        """Exclui usuário por ID."""
        self.db.cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0

    def update_password(self, user_id: int, new_password: str) -> bool:
        """Atualiza senha do usuário."""
        senha_hash = hash_password(new_password)
        self.db.cursor.execute(
            'UPDATE usuarios SET senha_hash = ? WHERE id = ?',
            (senha_hash, user_id)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0

    def is_unique_admin(self, user_id: int) -> bool:
        """Verifica se é o único administrador restante."""
        return self.db.eh_unico_administrador(user_id)
    
    def get_users(self):
        """Obtém lista de todos os usuários."""
        return self.db.get_usuarios()
    
    def get_user_by_id(self, user_id: int) -> dict|None:
        """Obtém um usuário específico pelo ID."""
        self.db.cursor.execute(
            'SELECT id, username, nome_completo, tipo, ativo FROM usuarios WHERE id = ?',
            (user_id,)
        )
        row = self.db.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'nome_completo': row[2],
                'tipo': row[3],
                'ativo': row[4]
            }
        return None
