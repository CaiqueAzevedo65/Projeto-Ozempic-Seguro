"""
Serviço de usuários: camada de negócio isolada entre controllers e repositories.
"""
from typing import Optional, Tuple, List, Dict
import datetime

from ..repositories.user_repository import UserRepository
from ..repositories.audit_repository import AuditRepository
from ..repositories.security_logger import SecurityLogger
from ..repositories.input_validator import InputValidator
from ..config import SecurityConfig
from ..core.base_views import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()
        self.audit_repo = AuditRepository()

    def create_user(self, nome: str, username: str, senha: str, tipo: str, usuario_criador_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Cadastra um novo usuário com validações robustas e registra log de auditoria.
        """
        # Validação robusta de entrada usando método da classe base
        validation_data = {
            'username': username,
            'senha': senha,
            'nome': nome,
            'tipo': tipo
        }
        
        if not self._validate_input(validation_data):
            return False, "Dados de entrada inválidos"
        
        validation_result = InputValidator.validate_and_sanitize_user_input(
            username=username,
            password=senha,
            name=nome,
            user_type=tipo
        )
        
        if not validation_result['valid']:
            return False, "; ".join(validation_result['errors'])
        
        # Usar dados sanitizados
        sanitized_data = validation_result['sanitized_data']
        nome_sanitizado = sanitized_data['name']
        username_sanitizado = sanitized_data['username']
        tipo_sanitizado = sanitized_data['user_type']

        try:
            novo_id = self.user_repo.create_user(username_sanitizado, senha, nome_sanitizado, tipo_sanitizado)
            if not novo_id:
                return False, "Nome de usuário já está em uso"

            # Log de criação com contexto de segurança
            security_context = SecurityLogger.log_user_management(
                action='CREATE_USER',
                admin_user_id=usuario_criador_id or novo_id,
                admin_username='system',
                target_user_id=novo_id,
                target_username=username_sanitizado,
                changes={
                    'nome_completo': nome_sanitizado,
                    'tipo': tipo_sanitizado,
                    'data_criacao': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            )
            self.audit_repo.create_log(
                usuario_id=usuario_criador_id or novo_id,
                acao='CRIAR',
                tabela_afetada='USUARIOS',
                id_afetado=novo_id,
                dados_novos=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return True, "Usuário cadastrado com sucesso!"

        except Exception as e:
            return False, f"Erro ao cadastrar usuário: {str(e)}"
    
    def _validate_input(self, validation_data: Dict) -> bool:
        """Implementação da validação de entrada obrigatória da classe base"""
        required_fields = ['username', 'senha', 'nome', 'tipo']
        
        # Verificar campos obrigatórios
        for field in required_fields:
            if not validation_data.get(field):
                return False
        
        # Validar tipo de usuário
        if validation_data['tipo'] not in SecurityConfig.VALID_USER_TYPES:
            return False
            
        return True

    def authenticate(self, username: str, senha: str, endereco_ip: Optional[str] = None) -> Optional[Dict]:
        """
        Autentica usuário com validação robusta, controle de força bruta e logs detalhados.
        """
        # Validação robusta de entrada
        username_valid, username_error = InputValidator.validate_username(username)
        password_valid, password_error = InputValidator.validate_password(senha)
        
        if not username_valid:
            # Log tentativa com dados inválidos
            security_context = SecurityLogger.log_security_violation(
                violation_type='INVALID_USERNAME_FORMAT',
                details={'username': InputValidator.sanitize_string(username, 50), 'error': username_error}
            )
            self.audit_repo.create_log(
                usuario_id=None,
                acao='SECURITY_VIOLATION',
                tabela_afetada='USUARIOS',
                dados_anteriores=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return None
            
        if not password_valid:
            return None
            
        # Verificar se usuário está bloqueado por tentativas excessivas
        from ..session import SessionManager
        session_manager = SessionManager.get_instance()
        
        if session_manager.is_user_locked(username):
            remaining_time = session_manager.get_lockout_remaining_time(username)
            security_context = SecurityLogger.log_security_violation(
                violation_type='ACCOUNT_LOCKED',
                username=username,
                details={'remaining_lockout_minutes': remaining_time}
            )
            self.audit_repo.create_log(
                usuario_id=None,
                acao='LOGIN_BLOCKED',
                tabela_afetada='USUARIOS',
                dados_anteriores=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return None
            
        user = self.user_repo.authenticate_user(username, senha)
        
        if user:
            # Reset contador de tentativas em caso de sucesso
            session_manager.record_login_attempt(username, success=True)
            
            # Log de sucesso com contexto de segurança
            security_context = SecurityLogger.log_login_attempt(
                username=username,
                success=True,
                user_id=user['id']
            )
            
            self.audit_repo.create_log(
                usuario_id=user['id'],
                acao='LOGIN_SUCCESS',
                tabela_afetada='USUARIOS',
                id_afetado=user['id'],
                dados_novos=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return user
        else:
            # Registra tentativa falhada para controle de força bruta
            session_manager.record_login_attempt(username, success=False)
            
            # Log de tentativa falha com contexto de segurança
            security_context = SecurityLogger.log_login_attempt(
                username=username,
                success=False,
                failure_reason='invalid_credentials'
            )
            
            self.audit_repo.create_log(
                usuario_id=None,
                acao='LOGIN_FAILED',
                tabela_afetada='USUARIOS',
                dados_anteriores=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return None

    def logout(self, usuario_id: int, username: str, endereco_ip: Optional[str] = None) -> None:
        """Registra logout de usuário com contexto de segurança."""
        security_context = SecurityLogger.log_session_event(
            event_type='LOGOUT',
            user_id=usuario_id,
            username=username
        )
        
        self.audit_repo.create_log(
            usuario_id=usuario_id,
            acao='LOGOUT',
            tabela_afetada='USUARIOS',
            id_afetado=usuario_id,
            dados_novos=security_context,
            endereco_ip=security_context.get('ip_address', endereco_ip)
        )

    def delete_user(self, usuario_id: int) -> Tuple[bool, str]:
        """Exclui usuário e registra auditoria, impedindo remoção do único administrador."""
        if self.user_repo.is_unique_admin(usuario_id):
            return False, "Não é possível excluir o único administrador"
        sucesso = self.user_repo.delete_user(usuario_id)
        if sucesso:
            self.audit_repo.create_log(
                usuario_id=usuario_id,
                acao='EXCLUIR',
                tabela_afetada='USUARIOS',
                id_afetado=usuario_id
            )
            return True, "Usuário excluído com sucesso!"
        return False, "Falha ao excluir usuário"

    def get_all_users(self) -> List[Dict]:
        """Retorna lista de todos os usuários."""
        return self.user_repo.get_users()

    def update_password(self, usuario_id: int, nova_senha: str, admin_user_id: Optional[int] = None) -> Tuple[bool, str]:
        """Atualiza senha de usuário com validação robusta e registra auditoria."""
        # Validação robusta da nova senha
        password_valid, password_error = InputValidator.validate_password(nova_senha)
        
        if not password_valid:
            return False, f"Senha inválida: {password_error}"
            
        try:
            sucesso = self.user_repo.update_password(usuario_id, nova_senha)
            if sucesso:
                # Log com contexto de segurança
                security_context = SecurityLogger.log_user_management(
                    action='UPDATE_PASSWORD',
                    admin_user_id=admin_user_id or usuario_id,
                    admin_username='system',
                    target_user_id=usuario_id,
                    changes={'password_updated': True}
                )
                
                self.audit_repo.create_log(
                    usuario_id=admin_user_id or usuario_id,
                    acao='ATUALIZAR_SENHA',
                    tabela_afetada='USUARIOS',
                    id_afetado=usuario_id,
                    dados_novos=security_context,
                    endereco_ip=security_context.get('ip_address')
                )
                return True, "Senha atualizada com sucesso"
            return False, "Falha ao atualizar senha"
        except Exception as e:
            # Log erro de segurança
            security_context = SecurityLogger.log_security_violation(
                violation_type='PASSWORD_UPDATE_ERROR',
                user_id=admin_user_id or usuario_id,
                details={'error': str(e), 'target_user_id': usuario_id}
            )
            self.audit_repo.create_log(
                usuario_id=admin_user_id or usuario_id,
                acao='ERRO_ATUALIZAR_SENHA',
                tabela_afetada='USUARIOS',
                id_afetado=usuario_id,
                dados_anteriores=security_context,
                endereco_ip=security_context.get('ip_address')
            )
            return False, f"Erro ao atualizar senha: {str(e)}"
