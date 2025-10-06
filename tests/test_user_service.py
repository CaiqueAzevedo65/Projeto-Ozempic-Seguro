"""
Testes completos para UserService.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ozempic_seguro.services.user_service import UserService


class TestUserService:
    """Testes para UserService"""
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock do DatabaseManager"""
        mock = Mock()
        mock.autenticar_usuario = Mock()
        mock.criar_usuario = Mock()
        mock.cursor = Mock()
        return mock
    
    @pytest.fixture
    def audit_service(self, mock_audit_db_manager):
        """AuditService com DatabaseManager mockado"""
        with patch('ozempic_seguro.services.audit_service.DatabaseManager') as mock_db_class:
            mock_db_class.return_value = mock_audit_db_manager
            service = AuditService()
            service.db = mock_audit_db_manager
            return service
    
    def test_audit_service_log_action(self, audit_service, mock_audit_db_manager):
        """Testa log de ação no AuditService"""
        # Arrange
        mock_user = {
            'id': 1,
            'username': 'test_user',
            'nome_completo': 'Test User',
            'tipo': 'vendedor'
        }
        
        # Act
        result = audit_service.log_action(mock_user, 'login')
        
        # Assert
        assert result is True
        mock_audit_db_manager.log_action.assert_called_once_with(
            mock_user, 'login'
        )
    
    def test_authenticate_user_success(self, user_service, mock_db_manager):
        """Testa autenticação bem-sucedida"""
        # Arrange
        mock_user = {
            'id': 1,
            'username': 'test_user',
            'nome_completo': 'Test User',
            'tipo': 'vendedor'
        }
        mock_db_manager.autenticar_usuario.return_value = mock_user
        
        # Act
        result = user_service.authenticate_user('test_user', 'password123')
        
        # Assert
        assert result == mock_user
        mock_db_manager.autenticar_usuario.assert_called_once_with('test_user', 'password123')
    
    def test_authenticate_user_failure(self, user_service, mock_db_manager):
        """Testa falha na autenticação"""
        # Arrange
        mock_db_manager.autenticar_usuario.return_value = None
        
        # Act
        result = user_service.authenticate_user('invalid_user', 'wrong_password')
        
        # Assert
        assert result is None
        mock_db_manager.autenticar_usuario.assert_called_once()
    
    def test_create_user_success(self, user_service, mock_db_manager):
        """Testa criação de usuário bem-sucedida"""
        # Arrange
        mock_db_manager.criar_usuario.return_value = True
        
        # Act
        result = user_service.create_user(
            username='new_user',
            password='Password123',
            nome_completo='New User',
            tipo='vendedor'
        )
        
        # Assert
        assert result is True
        mock_db_manager.criar_usuario.assert_called_once_with(
            'new_user', 'Password123', 'New User', 'vendedor'
        )
    
    def test_create_user_failure(self, user_service, mock_db_manager):
        """Testa falha na criação de usuário"""
        # Arrange
        mock_db_manager.criar_usuario.return_value = False
        
        # Act
        result = user_service.create_user(
            username='existing_user',
            password='Password123',
            nome_completo='Existing User',
            tipo='vendedor'
        )
        
        # Assert
        assert result is False
    
    def test_get_all_users(self, user_service, mock_db_manager):
        """Testa listagem de todos os usuários"""
        # Arrange
        mock_users = [
            (1, 'user1', 'hash1', 'User One', 'vendedor', 1),
            (2, 'user2', 'hash2', 'User Two', 'repositor', 1)
        ]
        mock_db_manager.cursor.fetchall.return_value = mock_users
        
        # Act
        result = user_service.get_all_users()
        
        # Assert
        assert len(result) == 2
        assert result[0]['username'] == 'user1'
        assert result[1]['tipo'] == 'repositor'
        mock_db_manager.cursor.execute.assert_called_with(
            'SELECT * FROM usuarios ORDER BY nome_completo'
        )
    
    def test_get_user_by_id_found(self, user_service, mock_db_manager):
        """Testa busca de usuário por ID encontrado"""
        # Arrange
        mock_user = (1, 'user1', 'hash1', 'User One', 'vendedor', 1)
        mock_db_manager.cursor.fetchone.return_value = mock_user
        
        # Act
        result = user_service.get_user_by_id(1)
        
        # Assert
        assert result is not None
        assert result['id'] == 1
        assert result['username'] == 'user1'
        mock_db_manager.cursor.execute.assert_called_with(
            'SELECT * FROM usuarios WHERE id = ?', (1,)
        )
    
    def test_get_user_by_id_not_found(self, user_service, mock_db_manager):
        """Testa busca de usuário por ID não encontrado"""
        # Arrange
        mock_db_manager.cursor.fetchone.return_value = None
        
        # Act
        result = user_service.get_user_by_id(999)
        
        # Assert
        assert result is None
    
    def test_update_user_password(self, user_service, mock_db_manager):
        """Testa atualização de senha"""
        # Arrange
        mock_db_manager.cursor.fetchone.return_value = (1, 'user1', 'old_hash', 'User', 'vendedor', 1)
        
        # Act
        with patch('ozempic_seguro.services.user_service.hash_password') as mock_hash:
            mock_hash.return_value = 'new_hash'
            result = user_service.update_user_password(1, 'NewPassword123')
        
        # Assert
        assert result is True
        mock_hash.assert_called_once_with('NewPassword123')
        mock_db_manager.cursor.execute.assert_any_call(
            'UPDATE usuarios SET senha_hash = ? WHERE id = ?',
            ('new_hash', 1)
        )
    
    def test_delete_user_success(self, user_service, mock_db_manager):
        """Testa exclusão de usuário bem-sucedida"""
        # Arrange
        # Simula que existe mais de um admin
        mock_db_manager.cursor.fetchone.side_effect = [
            (1, 'user1', 'hash', 'User', 'vendedor', 1),  # Usuário a deletar
            (2,)  # Count de admins > 1
        ]
        
        # Act
        result = user_service.delete_user(1)
        
        # Assert
        assert result is True
        mock_db_manager.cursor.execute.assert_any_call(
            'DELETE FROM usuarios WHERE id = ?', (1,)
        )
    
    def test_delete_last_admin_prevented(self, user_service, mock_db_manager):
        """Testa prevenção de exclusão do último admin"""
        # Arrange
        mock_db_manager.cursor.fetchone.side_effect = [
            (1, 'admin', 'hash', 'Admin', 'administrador', 1),  # Admin a deletar
            (1,)  # Count de admins = 1 (último admin)
        ]
        
        # Act
        result = user_service.delete_user(1)
        
        # Assert
        assert result is False  # Não deve permitir deletar
    
    def test_toggle_user_status(self, user_service, mock_db_manager):
        """Testa alternância de status do usuário"""
        # Arrange
        mock_db_manager.cursor.fetchone.return_value = (1, 'user1', 'hash', 'User', 'vendedor', 1)
        
        # Act
        result = user_service.toggle_user_status(1)
        
        # Assert
        assert result is True
        mock_db_manager.cursor.execute.assert_any_call(
            'UPDATE usuarios SET ativo = ? WHERE id = ?',
            (0, 1)  # Desativa usuário que estava ativo
        )
    
    def test_is_admin_true(self, user_service, mock_db_manager):
        """Testa verificação de admin verdadeira"""
        # Arrange
        mock_db_manager.cursor.fetchone.return_value = (1, 'admin', 'hash', 'Admin', 'administrador', 1)
        
        # Act
        result = user_service.is_admin(1)
        
        # Assert
        assert result is True
    
    def test_is_admin_false(self, user_service, mock_db_manager):
        """Testa verificação de admin falsa"""
        # Arrange
        mock_db_manager.cursor.fetchone.return_value = (1, 'user', 'hash', 'User', 'vendedor', 1)
        
        # Act
        result = user_service.is_admin(1)
        
        # Assert
        assert result is False
