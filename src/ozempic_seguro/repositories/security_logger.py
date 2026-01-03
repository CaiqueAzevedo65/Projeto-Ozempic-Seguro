"""
Módulo para logs de segurança avançados com contexto local.
Sistema completamente offline - sem conexões de rede.
"""
import platform
import datetime
import socket
from typing import Optional, Dict, Any


class SecurityLogger:
    """Classe para logs de segurança com informações detalhadas"""

    @staticmethod
    def get_local_ip() -> str:
        """Retorna IP local para aplicação offline"""
        # Aplicação completamente offline - sempre localhost
        return "127.0.0.1"

    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Captura informações do sistema local"""
        import os

        return {
            "hostname": os.environ.get("COMPUTERNAME", "LOCAL"),
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    @staticmethod
    def create_security_context(
        action: str,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Cria contexto completo de segurança para logs

        Args:
            action: Ação sendo executada
            user_id: ID do usuário
            username: Nome do usuário
            additional_data: Dados adicionais específicos da ação

        Returns:
            Dict com contexto completo de segurança
        """
        context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "ip_address": SecurityLogger.get_local_ip(),
            "hostname": socket.gethostname(),
            "system": platform.system(),
            "user_agent": f"OzempicSeguro/{platform.system()}",
        }

        if user_id:
            context["user_id"] = user_id
        if username:
            context["username"] = username
        if additional_data:
            context["additional_data"] = additional_data

        return context

    @staticmethod
    def log_login_attempt(
        username: str,
        success: bool,
        user_id: Optional[int] = None,
        failure_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Log específico para tentativas de login"""
        additional_data = {"success": success, "attempt_time": datetime.datetime.now().isoformat()}

        if not success and failure_reason:
            additional_data["failure_reason"] = failure_reason

        return SecurityLogger.create_security_context(
            action="LOGIN_ATTEMPT",
            user_id=user_id,
            username=username,
            additional_data=additional_data,
        )

    @staticmethod
    def log_session_event(
        event_type: str, user_id: int, username: str, session_duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """Log específico para eventos de sessão"""
        additional_data = {
            "event_type": event_type,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        if session_duration:
            additional_data["session_duration_minutes"] = session_duration

        return SecurityLogger.create_security_context(
            action="SESSION_EVENT",
            user_id=user_id,
            username=username,
            additional_data=additional_data,
        )

    @staticmethod
    def log_user_management(
        action: str,
        admin_user_id: int,
        admin_username: str,
        target_user_id: Optional[int] = None,
        target_username: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Log específico para gerenciamento de usuários"""
        additional_data = {"admin_action": action, "timestamp": datetime.datetime.now().isoformat()}

        if target_user_id:
            additional_data["target_user_id"] = target_user_id
        if target_username:
            additional_data["target_username"] = target_username
        if changes:
            additional_data["changes"] = changes

        return SecurityLogger.create_security_context(
            action="USER_MANAGEMENT",
            user_id=admin_user_id,
            username=admin_username,
            additional_data=additional_data,
        )

    @staticmethod
    def log_security_violation(
        violation_type: str,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Log específico para violações de segurança"""
        additional_data = {
            "violation_type": violation_type,
            "severity": "HIGH",
            "timestamp": datetime.datetime.now().isoformat(),
        }

        if details:
            additional_data["details"] = details

        return SecurityLogger.create_security_context(
            action="SECURITY_VIOLATION",
            user_id=user_id,
            username=username,
            additional_data=additional_data,
        )
