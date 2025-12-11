"""
Repositório de usuários: operações CRUD e autenticação.

Implementa IUserRepository com lógica de persistência para usuários.
"""
import os
from typing import Optional, List, Dict, Any
import sqlite3

from .connection import DatabaseConnection
from .security import hash_password, verify_password
from ..core.logger import logger


class UserRepository:
    """
    Repositório para operações de usuários no banco de dados.
    
    Responsabilidades:
    - CRUD de usuários
    - Autenticação
    - Verificações de regras de negócio (único admin, etc.)
    """
    
    def __init__(self):
        self._db = DatabaseConnection.get_instance()
        self._ensure_default_users()
    
    def _ensure_default_users(self) -> None:
        """Garante que usuários padrão existam"""
        if self._db.is_new_database:
            self._create_default_admin()
            self._create_default_tecnico()
        else:
            # Verifica se existem
            self._db.execute("SELECT COUNT(*) FROM usuarios WHERE username = ?", 
                           (os.getenv('OZEMPIC_ADMIN_USERNAME', '00'),))
            if self._db.fetchone()[0] == 0:
                self._create_default_admin()
            
            self._db.execute("SELECT COUNT(*) FROM usuarios WHERE username = ?",
                           (os.getenv('OZEMPIC_TECNICO_USERNAME', '01'),))
            if self._db.fetchone()[0] == 0:
                self._create_default_tecnico()
    
    def _create_default_admin(self) -> None:
        """Cria usuário administrador padrão"""
        username = os.getenv('OZEMPIC_ADMIN_USERNAME', '00')
        senha = os.getenv('OZEMPIC_ADMIN_PASSWORD', 'admin@2025')
        senha_hash = hash_password(senha)
        
        try:
            self._db.execute(
                'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo) VALUES (?, ?, ?, ?, ?)',
                (username, senha_hash, 'ADMINISTRADOR', 'administrador', 1)
            )
            self._db.commit()
            logger.info(f"Default admin user created: {username}")
        except sqlite3.IntegrityError:
            self._db.rollback()
    
    def _create_default_tecnico(self) -> None:
        """Cria usuário técnico padrão"""
        username = os.getenv('OZEMPIC_TECNICO_USERNAME', '01')
        senha = os.getenv('OZEMPIC_TECNICO_PASSWORD', 'tecnico@2025')
        senha_hash = hash_password(senha)
        
        try:
            self._db.execute(
                'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo) VALUES (?, ?, ?, ?, ?)',
                (username, senha_hash, 'TÉCNICO', 'tecnico', 1)
            )
            self._db.commit()
            logger.info(f"Default tecnico user created: {username}")
        except sqlite3.IntegrityError:
            self._db.rollback()

    def create_user(self, username: str, senha: str, nome_completo: str, tipo: str) -> Optional[int]:
        """
        Cria um usuário e retorna seu ID.
        
        Args:
            username: Nome de usuário único
            senha: Senha em texto plano (será hasheada)
            nome_completo: Nome completo do usuário
            tipo: Tipo do usuário (administrador, vendedor, repositor, tecnico)
            
        Returns:
            ID do usuário criado ou None se falhar
        """
        senha_hash = hash_password(senha)
        try:
            self._db.execute(
                'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo) VALUES (?, ?, ?, ?)',
                (username, senha_hash, nome_completo, tipo)
            )
            self._db.commit()
            return self._db.lastrowid()
        except sqlite3.IntegrityError:
            logger.warning(f"Username already exists: {username}")
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            self._db.rollback()
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica usuário e retorna dados se bem-sucedido.
        
        Args:
            username: Nome de usuário
            password: Senha em texto plano
            
        Returns:
            Dicionário com dados do usuário ou None se falhar
        """
        self._db.execute(
            'SELECT id, username, senha_hash, nome_completo, tipo FROM usuarios WHERE username = ? AND ativo = 1',
            (username,)
        )
        row = self._db.fetchone()
        
        if row and verify_password(password, row[2]):
            return {
                'id': row[0],
                'username': row[1],
                'nome_completo': row[3],
                'tipo': row[4]
            }
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Exclui usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        # Verifica se existe
        self._db.execute('SELECT id FROM usuarios WHERE id = ?', (user_id,))
        if not self._db.fetchone():
            return False
        
        # Verifica se é único admin
        if self.is_unique_admin(user_id):
            logger.warning(f"Cannot delete last admin: {user_id}")
            return False
        
        self._db.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        self._db.commit()
        return self._db.cursor.rowcount > 0

    def update_password(self, user_id: int, new_password: str) -> bool:
        """
        Atualiza senha do usuário.
        
        Args:
            user_id: ID do usuário
            new_password: Nova senha em texto plano
            
        Returns:
            True se atualizado com sucesso
        """
        senha_hash = hash_password(new_password)
        self._db.execute(
            'UPDATE usuarios SET senha_hash = ? WHERE id = ?',
            (senha_hash, user_id)
        )
        self._db.commit()
        return self._db.cursor.rowcount > 0

    def is_unique_admin(self, user_id: int) -> bool:
        """
        Verifica se é o único administrador restante.
        
        Args:
            user_id: ID do usuário a verificar
            
        Returns:
            True se for o único admin
        """
        # Verifica se é admin
        self._db.execute('SELECT tipo FROM usuarios WHERE id = ?', (user_id,))
        row = self._db.fetchone()
        
        if not row or row[0] != 'administrador':
            return False
        
        # Conta admins
        self._db.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'administrador'")
        total = self._db.fetchone()[0]
        
        return total <= 1
    
    def get_users(self) -> List[tuple]:
        """
        Obtém lista de todos os usuários.
        
        Returns:
            Lista de tuplas com dados dos usuários
        """
        self._db.execute('''
            SELECT id, username, nome_completo, tipo, ativo, data_criacao 
            FROM usuarios
            ORDER BY data_criacao DESC
        ''')
        return self._db.fetchall()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém um usuário específico pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com dados do usuário ou None
        """
        self._db.execute(
            'SELECT id, username, nome_completo, tipo, ativo FROM usuarios WHERE id = ?',
            (user_id,)
        )
        row = self._db.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'nome_completo': row[2],
                'tipo': row[3],
                'ativo': row[4]
            }
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Obtém um usuário pelo username.
        
        Args:
            username: Nome de usuário
            
        Returns:
            Dicionário com dados do usuário ou None
        """
        self._db.execute(
            'SELECT id, username, nome_completo, tipo, ativo FROM usuarios WHERE username = ?',
            (username,)
        )
        row = self._db.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'nome_completo': row[2],
                'tipo': row[3],
                'ativo': row[4]
            }
        return None
