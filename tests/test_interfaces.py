"""
Testes para interfaces de repositórios.
"""
import pytest
from abc import ABC

from ozempic_seguro.repositories.interfaces import (
    IRepository,
    IUserRepository,
    IGavetaRepository,
    IAuditRepository,
    IService,
)


class TestIRepository:
    """Testes para interface IRepository"""
    
    def test_is_abstract(self):
        """Testa que IRepository é abstrata"""
        assert issubclass(IRepository, ABC)
    
    def test_has_find_by_id(self):
        """Testa que tem método find_by_id"""
        assert hasattr(IRepository, 'find_by_id')
    
    def test_has_find_all(self):
        """Testa que tem método find_all"""
        assert hasattr(IRepository, 'find_all')
    
    def test_has_save(self):
        """Testa que tem método save"""
        assert hasattr(IRepository, 'save')
    
    def test_has_delete(self):
        """Testa que tem método delete"""
        assert hasattr(IRepository, 'delete')
    
    def test_has_exists(self):
        """Testa que tem método exists"""
        assert hasattr(IRepository, 'exists')


class TestIUserRepository:
    """Testes para interface IUserRepository"""
    
    def test_is_abstract(self):
        """Testa que IUserRepository é abstrata"""
        assert issubclass(IUserRepository, ABC)
    
    def test_extends_irepository(self):
        """Testa que estende IRepository"""
        assert issubclass(IUserRepository, IRepository)
    
    def test_has_find_by_username(self):
        """Testa que tem método find_by_username"""
        assert hasattr(IUserRepository, 'find_by_username')
    
    def test_has_find_by_type(self):
        """Testa que tem método find_by_type"""
        assert hasattr(IUserRepository, 'find_by_type')
    


class TestIGavetaRepository:
    """Testes para interface IGavetaRepository"""
    
    def test_is_abstract(self):
        """Testa que IGavetaRepository é abstrata"""
        assert issubclass(IGavetaRepository, ABC)
    
    def test_extends_irepository(self):
        """Testa que estende IRepository"""
        assert issubclass(IGavetaRepository, IRepository)
    
    def test_has_find_by_numero(self):
        """Testa que tem método find_by_numero"""
        assert hasattr(IGavetaRepository, 'find_by_numero')
    
    def test_has_find_by_status(self):
        """Testa que tem método find_by_status"""
        assert hasattr(IGavetaRepository, 'find_by_status')


class TestIAuditRepository:
    """Testes para interface IAuditRepository"""
    
    def test_is_abstract(self):
        """Testa que IAuditRepository é abstrata"""
        assert issubclass(IAuditRepository, ABC)
    
    def test_extends_irepository(self):
        """Testa que estende IRepository"""
        assert issubclass(IAuditRepository, IRepository)
    
    def test_has_find_by_user(self):
        """Testa que tem método find_by_user"""
        assert hasattr(IAuditRepository, 'find_by_user')
    
    def test_has_find_by_action(self):
        """Testa que tem método find_by_action"""
        assert hasattr(IAuditRepository, 'find_by_action')


class TestIService:
    """Testes para interface IService"""
    
    def test_is_abstract(self):
        """Testa que IService é abstrata"""
        assert issubclass(IService, ABC)
