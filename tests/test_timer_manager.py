"""
Testes para TimerManager - Controle de timer e bloqueios do sistema.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from ozempic_seguro.session.timer_manager import TimerManager


class TestTimerManager:
    """Testes para TimerManager"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.manager = TimerManager()
        yield
    
    def test_initial_state_not_blocked(self):
        """Testa que estado inicial não está bloqueado"""
        assert self.manager.is_blocked() is False
    
    def test_block_for_minutes(self):
        """Testa bloqueio por minutos"""
        self.manager.block_for_minutes(5)
        
        assert self.manager.is_blocked() is True
    
    def test_get_remaining_time_when_blocked(self):
        """Testa obtenção de tempo restante quando bloqueado"""
        self.manager.block_for_minutes(5)
        
        remaining = self.manager.get_remaining_time()
        
        assert remaining > 0
        assert remaining <= 5 * 60  # 5 minutos em segundos
    
    def test_get_remaining_time_when_not_blocked(self):
        """Testa obtenção de tempo restante quando não bloqueado"""
        remaining = self.manager.get_remaining_time()
        
        assert remaining == 0
    
    def test_clear_block(self):
        """Testa limpeza de bloqueio"""
        self.manager.block_for_minutes(5)
        assert self.manager.is_blocked() is True
        
        self.manager.clear_block()
        
        assert self.manager.is_blocked() is False
    
    def test_timer_enabled_default(self):
        """Testa que timer está habilitado por padrão"""
        assert self.manager.is_enabled() is True
    
    def test_disable_timer(self):
        """Testa desabilitação do timer"""
        self.manager.set_enabled(False)
        
        assert self.manager.is_enabled() is False
    
    def test_enable_timer(self):
        """Testa habilitação do timer"""
        self.manager.set_enabled(False)
        self.manager.set_enabled(True)
        
        assert self.manager.is_enabled() is True
    
    @patch('ozempic_seguro.session.timer_manager.datetime')
    def test_block_expires(self, mock_datetime):
        """Testa que bloqueio expira após tempo"""
        initial_time = datetime(2025, 1, 1, 10, 0, 0)
        mock_datetime.now.return_value = initial_time
        
        self.manager.block_for_minutes(5)
        
        # Avançar tempo além do bloqueio
        future_time = initial_time + timedelta(minutes=6)
        mock_datetime.now.return_value = future_time
        
        assert self.manager.is_blocked() is False


class TestTimerManagerEdgeCases:
    """Testes de casos extremos"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        self.manager = TimerManager()
        yield
    
    def test_block_zero_minutes(self):
        """Testa bloqueio por 0 minutos"""
        self.manager.block_for_minutes(0)
        
        # Deve estar bloqueado por 0 segundos (efetivamente não bloqueado)
        assert self.manager.get_remaining_time() == 0
    
    def test_block_negative_minutes(self):
        """Testa bloqueio por minutos negativos"""
        self.manager.block_for_minutes(-5)
        
        # Não deve causar erro, deve tratar como 0
        assert self.manager.is_blocked() is False
    
    def test_multiple_blocks_override(self):
        """Testa que múltiplos bloqueios sobrescrevem"""
        self.manager.block_for_minutes(10)
        self.manager.block_for_minutes(2)
        
        remaining = self.manager.get_remaining_time()
        
        # Deve usar o último bloqueio (2 minutos)
        assert remaining <= 2 * 60
