"""
Testes estendidos para DatabaseConnection - Cobertura adicional.
"""
import pytest

from ozempic_seguro.repositories.connection import DatabaseConnection


class TestDatabaseConnectionExtended:
    """Testes estendidos para DatabaseConnection"""
    
    def test_singleton_pattern(self):
        """Testa que DatabaseConnection é singleton"""
        conn1 = DatabaseConnection.get_instance()
        conn2 = DatabaseConnection.get_instance()
        
        assert conn1 is conn2
    
    def test_execute_select(self):
        """Testa execução de SELECT"""
        conn = DatabaseConnection.get_instance()
        
        conn.execute("SELECT 1 as test")
        result = conn.fetchone()
        
        assert result is not None
    
    def test_execute_with_params(self):
        """Testa execução com parâmetros"""
        conn = DatabaseConnection.get_instance()
        
        conn.execute("SELECT ? as test", (42,))
        result = conn.fetchone()
        
        assert result is not None
    
    def test_fetchall(self):
        """Testa fetchall"""
        conn = DatabaseConnection.get_instance()
        
        conn.execute("SELECT 1 as test UNION SELECT 2")
        results = conn.fetchall()
        
        assert isinstance(results, list)
        assert len(results) >= 1
    
    def test_commit(self):
        """Testa commit"""
        conn = DatabaseConnection.get_instance()
        
        # Não deve lançar exceção
        conn.commit()
    
    def test_rollback(self):
        """Testa rollback"""
        conn = DatabaseConnection.get_instance()
        
        # Não deve lançar exceção
        conn.rollback()
    
    def test_conn_property(self):
        """Testa propriedade conn"""
        conn = DatabaseConnection.get_instance()
        
        assert conn.conn is not None
    
    def test_cursor_property(self):
        """Testa propriedade cursor"""
        conn = DatabaseConnection.get_instance()
        
        assert conn.cursor is not None
    
    def test_is_new_database_property(self):
        """Testa propriedade is_new_database"""
        conn = DatabaseConnection.get_instance()
        
        assert isinstance(conn.is_new_database, bool)
    
    def test_context_manager(self):
        """Testa uso como context manager"""
        with DatabaseConnection.get_instance() as conn:
            conn.execute("SELECT 1")
            result = conn.fetchone()
            assert result is not None
    
    def test_lastrowid(self):
        """Testa lastrowid"""
        conn = DatabaseConnection.get_instance()
        
        # Executar um insert para ter lastrowid
        conn.execute("SELECT 1")
        
        # lastrowid pode ser 0 ou None se não houve insert
        rowid = conn.lastrowid()
        assert rowid is None or isinstance(rowid, int)
