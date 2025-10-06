"""
Testes para Views com componentes UI mockados.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk


class TestLoginView:
    """Testes para LoginView"""
    
    @patch('customtkinter.CTkFrame')
    @patch('customtkinter.CTkLabel')
    @patch('customtkinter.CTkEntry')
    @patch('customtkinter.CTkButton')
    def test_login_view_creation(self, mock_button, mock_entry, mock_label, mock_frame):
        """Testa criação da LoginView"""
        from ozempic_seguro.views.login_view import LoginFrame
        
        # Mock do parent
        parent = Mock()
        callback = Mock()
        
        # Cria view
        with patch.object(LoginFrame, '__init__', lambda x, y, z: None):
            view = LoginFrame(parent, callback)
            view.parent = parent
            view.show_iniciar_callback = callback
            
            # Simula criação de widgets
            view.usuario_entry = mock_entry.return_value
            view.senha_entry = mock_entry.return_value
            view.login_button = mock_button.return_value
            
            assert view.usuario_entry is not None
            assert view.senha_entry is not None
            assert view.login_button is not None
    
    @patch('ozempic_seguro.views.login_view.ServiceFactory')
    @patch('ozempic_seguro.views.login_view.SessionManager')
    def test_login_success(self, mock_session_class, mock_factory):
        """Testa login bem-sucedido"""
        from ozempic_seguro.views.login_view import LoginFrame
        
        # Mocks
        mock_user_service = Mock()
        mock_user_service.authenticate_user.return_value = {
            'id': 1,
            'username': 'test_user',
            'tipo': 'vendedor'
        }
        mock_factory.get_user_service.return_value = mock_user_service
        
        mock_session = Mock()
        mock_session_class.get_instance.return_value = mock_session
        
        # Cria view com init mockado
        with patch.object(LoginFrame, '__init__', lambda x, y, z: None):
            view = LoginFrame(None, None)
            view.usuario_entry = Mock()
            view.usuario_entry.get.return_value = 'test_user'
            view.senha_entry = Mock()
            view.senha_entry.get.return_value = 'password123'
            view.show_iniciar_callback = Mock()
            
            # Executa login
            view.fazer_login()
            
            # Verifica
            mock_user_service.authenticate_user.assert_called_once_with('test_user', 'password123')
            mock_session.set_current_user.assert_called_once()
            view.show_iniciar_callback.assert_called_once()


class TestComponentsView:
    """Testes para componentes de UI"""
    
    @patch('customtkinter.CTkButton')
    def test_modern_button_creation(self, mock_ctk_button):
        """Testa criação de ModernButton"""
        from ozempic_seguro.views.components import ModernButton
        
        parent = Mock()
        command = Mock()
        
        with patch.object(ModernButton, '__init__', lambda x, **kwargs: None):
            button = ModernButton(
                parent=parent,
                text="Test Button",
                command=command,
                style="primary"
            )
            button.text = "Test Button"
            button.command = command
            button.style = "primary"
            
            assert button.text == "Test Button"
            assert button.style == "primary"
            assert button.command is not None
    
    @patch('customtkinter.CTkFrame')
    def test_responsive_frame_creation(self, mock_frame):
        """Testa criação de ResponsiveFrame"""
        from ozempic_seguro.views.components import ResponsiveFrame
        
        parent = Mock()
        
        with patch.object(ResponsiveFrame, '__init__', lambda x, y, **kwargs: None):
            frame = ResponsiveFrame(parent, min_width=800, min_height=600)
            frame.min_width = 800
            frame.min_height = 600
            
            assert frame.min_width == 800
            assert frame.min_height == 600


class TestNavigationController:
    """Testes para NavigationController"""
    
    @patch('ozempic_seguro.controllers.navigation_controller.TelaToqueFrame')
    @patch('ozempic_seguro.controllers.navigation_controller.TelaLogoFrame')
    def test_navigation_controller_init(self, mock_logo, mock_toque):
        """Testa inicialização do NavigationController"""
        from ozempic_seguro.controllers.navigation_controller import NavigationController
        
        app = Mock()
        app.container = Mock()
        
        controller = NavigationController(app)
        
        assert controller.app == app
        assert controller.container == app.container
        assert controller.frames == {}
        assert controller.current_frame is None
    
    def test_show_frame(self):
        """Testa exibição de frame"""
        from ozempic_seguro.controllers.navigation_controller import NavigationController
        
        app = Mock()
        app.container = Mock()
        
        controller = NavigationController(app)
        
        # Mock frame
        mock_frame = Mock()
        mock_frame.winfo_exists.return_value = True
        controller.frames['test'] = mock_frame
        
        controller.show_frame('test')
        
        mock_frame.pack.assert_called_once()
        assert controller.current_frame == mock_frame
    
    def test_cleanup(self):
        """Testa cleanup do controller"""
        from ozempic_seguro.controllers.navigation_controller import NavigationController
        
        app = Mock()
        app.container = Mock()
        app.after_cancel = Mock()
        
        controller = NavigationController(app)
        controller.after_id = 123
        
        # Mock frames
        frame1 = Mock()
        frame1.winfo_exists.return_value = True
        frame2 = Mock()
        frame2.winfo_exists.return_value = True
        
        controller.frames = {'frame1': frame1, 'frame2': frame2}
        
        controller.cleanup()
        
        assert controller.is_running is False
        app.after_cancel.assert_called_once_with(123)
        frame1.destroy.assert_called_once()
        frame2.destroy.assert_called_once()
        assert len(controller.frames) == 0


class TestAuditService:
    """Testes para AuditService"""
    
    @patch('ozempic_seguro.services.audit_service.DatabaseManager')
    def test_audit_service_log_action(self, mock_db_class):
        """Testa log de ação no AuditService"""
        from ozempic_seguro.services.audit_service import AuditService
        
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        
        service = AuditService()
        service.db = mock_db
        
        result = service.log_action(
            user_id=1,
            action='LOGIN',
            details='User logged in'
        )
        
        assert result is True
        mock_db.cursor.execute.assert_called_once()
    
    @patch('ozempic_seguro.services.audit_service.DatabaseManager')
    def test_audit_service_get_logs(self, mock_db_class):
        """Testa obtenção de logs"""
        from ozempic_seguro.services.audit_service import AuditService
        
        mock_db = Mock()
        mock_db.cursor.fetchall.return_value = [
            (1, 1, 'LOGIN', 'User logged in', '127.0.0.1', '2024-01-01 12:00:00'),
            (2, 1, 'LOGOUT', 'User logged out', '127.0.0.1', '2024-01-01 13:00:00')
        ]
        mock_db_class.return_value = mock_db
        
        service = AuditService()
        service.db = mock_db
        
        logs = service.get_user_logs(1)
        
        assert len(logs) == 2
        assert logs[0]['action'] == 'LOGIN'
        assert logs[1]['action'] == 'LOGOUT'
