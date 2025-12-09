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
        # Importa aqui para evitar problemas de importação circular
        from ozempic_seguro.repositories.database import DatabaseManager
        
        # Limpa antes
        if hasattr(DatabaseManager, '_instance'):
            if DatabaseManager._instance and hasattr(DatabaseManager._instance, 'conn'):
                try:
                    DatabaseManager._instance.conn.close()
                except:
                    pass
            DatabaseManager._instance = None
        
        yield
        
        # Limpa depois
        if hasattr(DatabaseManager, '_instance'):
            if DatabaseManager._instance and hasattr(DatabaseManager._instance, 'conn'):
                try:
                    DatabaseManager._instance.conn.close()
                except:
                    pass
            DatabaseManager._instance = None

    def test_singleton_pattern(self):
        """Testa se DatabaseManager é singleton"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        DatabaseManager._instance = None
        db1 = DatabaseManager()
        db2 = DatabaseManager()
        assert db1 is db2

    def test_create_tables(self):
        """Testa criação de tabelas no banco através da inicialização"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch('ozempic_seguro.repositories.database.DatabaseManager._get_db_path') as mock_path:
                mock_path.return_value = db_path
                
                try:
                    # A inicialização já cria as tabelas via migrations
                    db = DatabaseManager()
                    
                    # Verificar se tabelas foram criadas
                    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = db.cursor.fetchall()
                    table_names = [t[0] for t in tables]
                    
                    assert 'usuarios' in table_names
                    assert 'gavetas' in table_names
                    assert 'historico_gavetas' in table_names
                finally:
                    # Fechar conexão para evitar lock no Windows
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None

    def test_execute_query_success(self):
        """Testa execução de query com sucesso"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        # Reset singleton para evitar conflitos
        DatabaseManager._instance = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch('ozempic_seguro.repositories.database.DatabaseManager._get_db_path') as mock_path:
                mock_path.return_value = db_path
                
                try:
                    db = DatabaseManager()
                    
                    # Inserir usuário de teste usando método existente
                    result = db.criar_usuario(
                        username='test_user',
                        senha='senha123',
                        nome_completo='Test User',
                        tipo='vendedor'
                    )
                    
                    assert result is True
                    
                finally:
                    # Fechar conexão para evitar lock
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None

    def test_fetch_one(self):
        """Testa busca de um registro"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch('ozempic_seguro.repositories.database.DatabaseManager._get_db_path') as mock_path:
                mock_path.return_value = db_path
                
                try:
                    db = DatabaseManager()
                    
                    # Inserir usuário
                    db.criar_usuario(
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

    def test_fetch_all(self):
        """Testa busca de múltiplos registros"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch('ozempic_seguro.repositories.database.DatabaseManager._get_db_path') as mock_path:
                mock_path.return_value = db_path
                
                try:
                    db = DatabaseManager()
                    
                    # Inserir múltiplos usuários
                    users_data = [
                        ('user1', 'senha1', 'User One', 'vendedor'),
                        ('user2', 'senha2', 'User Two', 'repositor'),
                        ('user3', 'senha3', 'User Three', 'administrador')
                    ]
                    
                    for username, senha, nome, tipo in users_data:
                        db.criar_usuario(username, senha, nome, tipo)
                    
                    # Buscar todos os usuários
                    db.cursor.execute("SELECT * FROM usuarios")
                    users = db.cursor.fetchall()
                    
                    # Como pode ter o usuário admin padrão, verifica se tem pelo menos 3
                    assert len(users) >= 3
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None

    def test_transaction_rollback(self):
        """Testa rollback de transação em caso de erro"""
        from ozempic_seguro.repositories.database import DatabaseManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, 'test.db')
            
            with patch('ozempic_seguro.repositories.database.DatabaseManager._get_db_path') as mock_path:
                mock_path.return_value = db_path
                
                try:
                    db = DatabaseManager()
                    
                    # Criar usuário único
                    result1 = db.criar_usuario('unique_user', 'senha1', 'User', 'vendedor')
                    assert result1 is True
                    
                    # Segunda inserção deve falhar (username único)
                    result2 = db.criar_usuario('unique_user', 'senha2', 'User2', 'vendedor')
                    assert result2 is False
                    
                    # Verificar que só existe um usuário com esse username
                    db.cursor.execute("SELECT * FROM usuarios WHERE username = ?", ('unique_user',))
                    users = db.cursor.fetchall()
                    assert len(users) == 1
                finally:
                    if hasattr(db, 'conn'):
                        db.conn.close()
                    DatabaseManager._instance = None
