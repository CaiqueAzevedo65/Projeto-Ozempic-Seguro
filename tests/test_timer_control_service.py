"""
Testes para TimerControlService - Serviço de controle de timer.
"""
import pytest

from ozempic_seguro.services.timer_control_service import (
    TimerControlService,
    TimerStatus,
    get_timer_control_service,
)
from ozempic_seguro.session import SessionManager


class TestTimerStatus:
    """Testes para TimerStatus"""
    
    def test_remaining_display_not_blocked(self):
        """Testa display quando não bloqueado"""
        status = TimerStatus(enabled=True, blocked=False, remaining_seconds=0, remaining_minutes=0)
        assert status.remaining_display == "Não bloqueado"
    
    def test_remaining_display_blocked(self):
        """Testa display quando bloqueado"""
        status = TimerStatus(enabled=True, blocked=True, remaining_seconds=125, remaining_minutes=2)
        assert "2:05" in status.remaining_display
    
    def test_status_display_disabled(self):
        """Testa status display desabilitado"""
        status = TimerStatus(enabled=False, blocked=False, remaining_seconds=0, remaining_minutes=0)
        assert "desabilitado" in status.status_display.lower()
    
    def test_status_display_enabled(self):
        """Testa status display habilitado"""
        status = TimerStatus(enabled=True, blocked=False, remaining_seconds=0, remaining_minutes=0)
        assert "habilitado" in status.status_display.lower()
    
    def test_status_display_blocked(self):
        """Testa status display bloqueado"""
        status = TimerStatus(enabled=True, blocked=True, remaining_seconds=60, remaining_minutes=1)
        assert "bloqueado" in status.status_display.lower()


class TestTimerControlService:
    """Testes para TimerControlService"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.service = TimerControlService()
        self.session = SessionManager.get_instance()
        self.session.cleanup()
        yield
        self.session.cleanup()
    
    def test_get_status(self):
        """Testa obtenção de status"""
        status = self.service.get_status()
        
        assert isinstance(status, TimerStatus)
        assert isinstance(status.enabled, bool)
        assert isinstance(status.blocked, bool)
    
    def test_enable_timer(self):
        """Testa habilitação do timer"""
        success, msg = self.service.enable_timer()
        
        assert success is True
        assert self.service.is_timer_enabled() is True
    
    def test_disable_timer(self):
        """Testa desabilitação do timer"""
        # Configurar usuário admin para ter permissão
        self.session.set_current_user({'id': 1, 'username': 'admin', 'tipo': 'administrador'})
        self.service.enable_timer()
        success, msg = self.service.disable_timer()
        
        assert success is True
    
    def test_toggle_timer(self):
        """Testa alternância do timer"""
        initial = self.service.is_timer_enabled()
        success, msg, new_state = self.service.toggle_timer()
        
        assert success is True
        assert new_state != initial
    
    def test_block_system(self):
        """Testa bloqueio do sistema"""
        # Configurar usuário admin para ter permissão
        self.session.set_current_user({'id': 1, 'username': 'admin', 'tipo': 'administrador'})
        self.service.enable_timer()
        success, msg = self.service.block_system(1)
        
        assert success is True
    
    def test_block_system_invalid_time(self):
        """Testa bloqueio com tempo inválido"""
        success, msg = self.service.block_system(0)
        
        assert success is False
    
    def test_unblock_system(self):
        """Testa desbloqueio do sistema"""
        self.service.enable_timer()
        self.service.block_system(1)
        success, msg = self.service.unblock_system()
        
        assert success is True
        assert self.service.is_blocked() is False
    
    def test_get_remaining_time(self):
        """Testa obtenção de tempo restante"""
        remaining = self.service.get_remaining_time()
        
        assert isinstance(remaining, int)
        assert remaining >= 0


class TestGetTimerControlService:
    """Testes para função get_timer_control_service"""
    
    def test_returns_service(self):
        """Testa que retorna TimerControlService"""
        service = get_timer_control_service()
        
        assert isinstance(service, TimerControlService)
