"""
Testes para DatabaseManager e DatabaseConnection.

Testa a camada de persistência usando banco SQLite.
"""
import pytest
import tempfile
import os
import shutil
import sqlite3
from unittest.mock import patch, Mock, MagicMock


class TestDatabaseManager:
    """Testes para o DatabaseManager usando banco SQLite direto"""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset do singleton antes e depois de cada teste"""
        from ozempic_seguro.repositories.database import DatabaseManager
        from ozempic_seguro.repositories.connection import DatabaseConnection
        
        # Limpa antes
        for cls in [DatabaseManager, DatabaseConnection]:
            if hasattr(cls, '_instance'):
                if cls._instance and hasattr(cls._instance, 'conn'):
                    try:
                        cls._instance.conn.close()
                    except:
                        pass
                cls._instance = None
        
        yield
        
        # Limpa depois
        for cls in [DatabaseManager, DatabaseConnection]:
            if hasattr(cls, '_instance'):
                if cls._instance and hasattr(cls._instance, 'conn'):
                    try:
                        cls._instance.conn.close()
                    except:
                        pass
                cls._instance = None

    def test_singleton_pattern(self):
        """Testa se DatabaseManager é singleton"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        DatabaseManager._instance = None
        db1 = DatabaseManager()
        db2 = DatabaseManager()
        assert db1 is db2

    def test_create_tables(self):
        """Testa criação de tabelas no banco através da inicialização"""
        from ozempic_seguro.repositories.connection import DatabaseConnection
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch.object(DatabaseConnection, '_get_db_path', return_value=db_path):
                try:
                    db = DatabaseConnection.get_instance()
                    
                    # Verificar se tabelas foram criadas
                    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = db.cursor.fetchall()
                    table_names = [t[0] for t in tables]
                    
                    assert 'usuarios' in table_names
                    assert 'gavetas' in table_names
                    assert 'historico_gavetas' in table_names
                finally:
                    if hasattr(db, '_conn'):
                        db._conn.close()
                    DatabaseConnection._instance = None

    def test_execute_query_success(self):
        """Testa execução de query com sucesso"""
        from ozempic_seguro.repositories.database import DatabaseManager
        from ozempic_seguro.repositories.connection import DatabaseConnection
        from ozempic_seguro.repositories.user_repository import UserRepository
        
        # Reset singletons
        DatabaseManager._instance = None
        DatabaseConnection._instance = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch.object(DatabaseConnection, '_get_db_path', return_value=db_path):
                try:
                    db = DatabaseManager()
                    user_repo = UserRepository()
                    
                    # Inserir usuário de teste usando UserRepository
                    result = user_repo.create_user(
                        username='test_user',
                        senha='senha123',
                        nome_completo='Test User',
                        tipo='vendedor'
                    )
                    
                    # create_user retorna o ID do usuário ou None
                    assert result is not None
                    
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None
                    DatabaseConnection._instance = None

    def test_fetch_one(self):
        """Testa busca de um registro"""
        from ozempic_seguro.repositories.database import DatabaseManager
        from ozempic_seguro.repositories.connection import DatabaseConnection
        from ozempic_seguro.repositories.user_repository import UserRepository
        
        DatabaseManager._instance = None
        DatabaseConnection._instance = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch.object(DatabaseConnection, '_get_db_path', return_value=db_path):
                try:
                    db = DatabaseManager()
                    user_repo = UserRepository()
                    
                    # Inserir usuário usando UserRepository
                    user_repo.create_user(
                        username='test_user',
                        senha='senha123',
                        nome_completo='Test User',
                        tipo='vendedor'
                    )
                    
                    # Buscar usuário usando cursor
                    db.cursor.execute("SELECT * FROM usuarios WHERE username = ?", ('test_user',))
                    user = db.cursor.fetchone()
                    
                    assert user is not None
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None
                    DatabaseConnection._instance = None

    def test_fetch_all(self):
        """Testa busca de múltiplos registros"""
        from ozempic_seguro.repositories.database import DatabaseManager
        from ozempic_seguro.repositories.connection import DatabaseConnection
        from ozempic_seguro.repositories.user_repository import UserRepository
        
        DatabaseManager._instance = None
        DatabaseConnection._instance = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch.object(DatabaseConnection, '_get_db_path', return_value=db_path):
                try:
                    db = DatabaseManager()
                    user_repo = UserRepository()
                    
                    # Inserir múltiplos usuários usando UserRepository
                    users_data = [
                        ('user1', 'senha1', 'User One', 'vendedor'),
                        ('user2', 'senha2', 'User Two', 'repositor'),
                        ('user3', 'senha3', 'User Three', 'administrador')
                    ]
                    
                    for username, senha, nome, tipo in users_data:
                        user_repo.create_user(username, senha, nome, tipo)
                    
                    # Buscar todos os usuários
                    db.cursor.execute("SELECT * FROM usuarios")
                    users = db.cursor.fetchall()
                    
                    # Como pode ter o usuário admin padrão, verifica se tem pelo menos 3
                    assert len(users) >= 3
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None
                    DatabaseConnection._instance = None

    def test_transaction_rollback(self):
        """Testa rollback de transação em caso de erro"""
        from ozempic_seguro.repositories.database import DatabaseManager
        from ozempic_seguro.repositories.connection import DatabaseConnection
        from ozempic_seguro.repositories.user_repository import UserRepository
        
        DatabaseManager._instance = None
        DatabaseConnection._instance = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch.object(DatabaseConnection, '_get_db_path', return_value=db_path):
                try:
                    db = DatabaseManager()
                    user_repo = UserRepository()
                    
                    # Criar usuário único usando UserRepository
                    result1 = user_repo.create_user('unique_user', 'senha1', 'User', 'vendedor')
                    # create_user retorna o ID do usuário ou None
                    assert result1 is not None
                    
                    # Segunda inserção deve falhar (username único) - retorna None
                    result2 = user_repo.create_user('unique_user', 'senha2', 'User2', 'vendedor')
                    assert result2 is None
                    
                    # Verificar que só existe um usuário com esse username
                    db.cursor.execute("SELECT * FROM usuarios WHERE username = ?", ('unique_user',))
                    users = db.cursor.fetchall()
                    assert len(users) == 1
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None
                    DatabaseConnection._instance = None
