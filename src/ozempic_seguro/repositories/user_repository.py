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
        self.db.cursor.execute(
            'SELECT * FROM usuarios WHERE username = ? AND ativo = 1',
            (username,)
        )
        row = self.db.cursor.fetchone()
        if row and verify_password(password, row['senha_hash']):
            return dict(row)
        return None

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
        self.db.cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "administrador"')
        total = self.db.cursor.fetchone()[0]
        self.db.cursor.execute('SELECT tipo FROM usuarios WHERE id = ?', (user_id,))
        user = self.db.cursor.fetchone()
        return bool(user and user['tipo'] == 'administrador' and total == 1)

    def get_users(self) -> list[dict]:
        """Retorna todos os usuários."""
        self.db.cursor.execute(
            'SELECT id, username, nome_completo, tipo, ativo, data_criacao FROM usuarios'
        )
        return [dict(row) for row in self.db.cursor.fetchall()]
