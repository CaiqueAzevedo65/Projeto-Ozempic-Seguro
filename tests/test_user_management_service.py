"""
Testes para UserManagementService - Serviço de gerenciamento de usuários.
"""
import pytest

from ozempic_seguro.services.user_management_service import (
    UserManagementService,
    UserData,
    OperationResult,
    get_user_management_service,
)


class TestUserData:
    """Testes para UserData"""
    
    def test_is_tecnico_true(self):
        """Testa identificação de técnico"""
        user = UserData(1, "123", "Test", "tecnico", True, "2025-01-01")
        assert user.is_tecnico is True
    
    def test_is_tecnico_false(self):
        """Testa identificação de não-técnico"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.is_tecnico is False
    
    def test_is_admin_true(self):
        """Testa identificação de admin"""
        user = UserData(1, "123", "Test", "administrador", True, "2025-01-01")
        assert user.is_admin is True
    
    def test_is_admin_false(self):
        """Testa identificação de não-admin"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.is_admin is False
    
    def test_can_be_modified_tecnico(self):
        """Testa que técnico não pode ser modificado"""
        user = UserData(1, "123", "Test", "tecnico", True, "2025-01-01")
        assert user.can_be_modified is False
    
    def test_can_be_modified_vendedor(self):
        """Testa que vendedor pode ser modificado"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.can_be_modified is True
    
    def test_can_be_deleted_tecnico(self):
        """Testa que técnico não pode ser excluído"""
        user = UserData(1, "123", "Test", "tecnico", True, "2025-01-01")
        assert user.can_be_deleted is False
    
    def test_can_be_deleted_vendedor(self):
        """Testa que vendedor pode ser excluído"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.can_be_deleted is True
    
    def test_tipo_display(self):
        """Testa formatação do tipo"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.tipo_display == "Vendedor"
    
    def test_status_display_ativo(self):
        """Testa formatação do status ativo"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01")
        assert user.status_display == "Ativo"
    
    def test_status_display_inativo(self):
        """Testa formatação do status inativo"""
        user = UserData(1, "123", "Test", "vendedor", False, "2025-01-01")
        assert user.status_display == "Inativo"
    
    def test_data_criacao_display(self):
        """Testa formatação da data"""
        user = UserData(1, "123", "Test", "vendedor", True, "2025-01-01 10:00:00")
        assert user.data_criacao_display == "2025-01-01"


class TestUserManagementService:
    """Testes para UserManagementService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = UserManagementService()
        yield
    
    def test_get_all_users(self):
        """Testa obtenção de todos os usuários"""
        users = self.service.get_all_users()
        
        assert isinstance(users, list)
        if users:
            assert isinstance(users[0], UserData)
    
    def test_get_user_by_id_existing(self):
        """Testa obtenção de usuário existente"""
        users = self.service.get_all_users()
        if users:
            user = self.service.get_user_by_id(users[0].id)
            assert user is not None
            assert isinstance(user, UserData)
    
    def test_get_user_by_id_nonexistent(self):
        """Testa obtenção de usuário inexistente"""
        user = self.service.get_user_by_id(99999)
        assert user is None
    
    def test_change_password_empty(self):
        """Testa alteração com senha vazia"""
        result = self.service.change_password(1, "", "")
        
        assert result.success is False
        assert len(result.errors) > 0
    
    def test_change_password_mismatch(self):
        """Testa alteração com senhas diferentes"""
        result = self.service.change_password(1, "1234", "5678")
        
        assert result.success is False
        assert "coincidem" in result.message.lower()
    
    def test_change_password_nonexistent_user(self):
        """Testa alteração para usuário inexistente"""
        result = self.service.change_password(99999, "1234", "1234")
        
        assert result.success is False
    
    def test_delete_user_self(self):
        """Testa exclusão de si mesmo"""
        result = self.service.delete_user(1, current_user_id=1)
        
        assert result.success is False
        assert "própria" in result.message.lower()
    
    def test_delete_user_nonexistent(self):
        """Testa exclusão de usuário inexistente"""
        result = self.service.delete_user(99999)
        
        assert result.success is False
        assert "encontrado" in result.message.lower()
    
    def test_can_modify_user_nonexistent(self):
        """Testa verificação de modificação para usuário inexistente"""
        can_modify, reason = self.service.can_modify_user(99999)
        
        assert can_modify is False
        assert "encontrado" in reason.lower()
    
    def test_can_delete_user_self(self):
        """Testa verificação de exclusão de si mesmo"""
        can_delete, reason = self.service.can_delete_user(1, current_user_id=1)
        
        assert can_delete is False
        assert "própria" in reason.lower()
    
    def test_can_delete_user_nonexistent(self):
        """Testa verificação de exclusão de usuário inexistente"""
        can_delete, reason = self.service.can_delete_user(99999)
        
        assert can_delete is False
        assert "encontrado" in reason.lower()


class TestOperationResult:
    """Testes para OperationResult"""
    
    def test_success_result(self):
        """Testa criação de resultado de sucesso"""
        result = OperationResult(success=True, message="Operação realizada")
        
        assert result.success is True
        assert result.message == "Operação realizada"
        assert result.errors == []
    
    def test_failure_result(self):
        """Testa criação de resultado de falha"""
        result = OperationResult(
            success=False,
            message="Erro",
            errors=["Erro 1", "Erro 2"]
        )
        
        assert result.success is False
        assert len(result.errors) == 2


class TestGetUserManagementService:
    """Testes para função get_user_management_service"""
    
    def test_returns_service(self):
        """Testa que retorna UserManagementService"""
        service = get_user_management_service()
        
        assert isinstance(service, UserManagementService)
