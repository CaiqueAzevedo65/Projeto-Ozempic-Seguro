"""
Repositório de auditoria: registros de ações do sistema.

Implementa IAuditRepository com lógica de persistência para logs de auditoria.
"""
import json
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

from .connection import DatabaseConnection
from .interfaces import IAuditRepository
from ..core.logger import logger


class AuditRepository(IAuditRepository):
    """
    Repositório para operações de auditoria no banco de dados.

    Responsabilidades:
    - Registrar logs de auditoria
    - Buscar e filtrar logs
    - Contagem de registros
    """

    def __init__(self):
        self._db = DatabaseConnection.get_instance()

    def create_log(
        self,
        usuario_id: Optional[int] = None,
        acao: Optional[str] = None,
        tabela_afetada: Optional[str] = None,
        id_afetado: Optional[int] = None,
        dados_anteriores: Optional[Dict] = None,
        dados_novos: Optional[Dict] = None,
        endereco_ip: Optional[str] = None,
    ) -> Optional[int]:
        """
        Registra um log de auditoria e retorna o ID do registro.

        Args:
            usuario_id: ID do usuário que realizou a ação
            acao: Tipo de ação (LOGIN, LOGOUT, CRIAR, ATUALIZAR, EXCLUIR, etc.)
            tabela_afetada: Nome da tabela afetada
            id_afetado: ID do registro afetado
            dados_anteriores: Dados antes da alteração
            dados_novos: Dados após a alteração
            endereco_ip: Endereço IP do usuário

        Returns:
            ID do registro criado ou None se falhar
        """
        try:
            prev_json = (
                json.dumps(dados_anteriores, ensure_ascii=False) if dados_anteriores else None
            )
            new_json = json.dumps(dados_novos, ensure_ascii=False) if dados_novos else None

            self._db.execute(
                """
                INSERT INTO auditoria
                (usuario_id, acao, tabela_afetada, id_afetado, dados_anteriores, dados_novos, endereco_ip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (usuario_id, acao, tabela_afetada, id_afetado, prev_json, new_json, endereco_ip),
            )

            self._db.commit()
            return self._db.lastrowid()

        except sqlite3.Error as e:
            logger.error(f"Database error creating audit log: {e}")
            self._db.rollback()
            return None

    def get_logs(
        self,
        offset: int = 0,
        limit: int = 50,
        filtro_usuario: Optional[int] = None,
        filtro_acao: Optional[str] = None,
        filtro_tabela: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retorna logs de auditoria com filtros e paginação.

        Args:
            offset: Número de registros a pular
            limit: Número máximo de registros
            filtro_usuario: Filtrar por ID do usuário
            filtro_acao: Filtrar por tipo de ação
            filtro_tabela: Filtrar por tabela afetada
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)

        Returns:
            Lista de dicionários com os logs
        """
        try:
            query = """
                SELECT
                    a.id, a.acao, a.tabela_afetada, a.id_afetado,
                    a.dados_anteriores, a.dados_novos, a.data_hora,
                    u.username as usuario
                FROM auditoria a
                LEFT JOIN usuarios u ON a.usuario_id = u.id
                WHERE 1=1
            """
            params: List[Any] = []

            if filtro_usuario is not None:
                query += " AND a.usuario_id = ?"
                params.append(filtro_usuario)
            if filtro_acao:
                query += " AND a.acao = ?"
                params.append(filtro_acao)
            if filtro_tabela:
                query += " AND a.tabela_afetada = ?"
                params.append(filtro_tabela)
            if data_inicio:
                query += " AND DATE(a.data_hora) >= ?"
                params.append(data_inicio)
            if data_fim:
                query += " AND DATE(a.data_hora) <= ?"
                params.append(data_fim)

            query += " ORDER BY a.data_hora DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            self._db.execute(query, tuple(params))
            columns = [desc[0] for desc in self._db.cursor.description]

            results = []
            for row in self._db.fetchall():
                result = dict(zip(columns, row))

                # Parse JSON fields
                if result.get("dados_anteriores"):
                    result["dados_anteriores"] = json.loads(result["dados_anteriores"])
                if result.get("dados_novos"):
                    result["dados_novos"] = json.loads(result["dados_novos"])

                # Format date
                if result.get("data_hora"):
                    try:
                        dt = datetime.strptime(result["data_hora"], "%Y-%m-%d %H:%M:%S")
                        result["data_formatada"] = dt.strftime("%d/%m/%Y %H:%M:%S")
                    except ValueError:
                        result["data_formatada"] = result["data_hora"]

                results.append(result)

            return results

        except sqlite3.Error as e:
            logger.error(f"Database error fetching audit logs: {e}")
            return []

    def count_logs(
        self,
        filtro_usuario: Optional[int] = None,
        filtro_acao: Optional[str] = None,
        filtro_tabela: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
    ) -> int:
        """
        Retorna o total de logs que correspondem aos filtros.

        Args:
            filtro_usuario: Filtrar por ID do usuário
            filtro_acao: Filtrar por tipo de ação
            filtro_tabela: Filtrar por tabela afetada
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)

        Returns:
            Número total de registros
        """
        try:
            query = "SELECT COUNT(*) FROM auditoria a WHERE 1=1"
            params: List[Any] = []

            if filtro_usuario is not None:
                query += " AND a.usuario_id = ?"
                params.append(filtro_usuario)
            if filtro_acao:
                query += " AND a.acao = ?"
                params.append(filtro_acao)
            if filtro_tabela:
                query += " AND a.tabela_afetada = ?"
                params.append(filtro_tabela)
            if data_inicio:
                query += " AND DATE(a.data_hora) >= ?"
                params.append(data_inicio)
            if data_fim:
                query += " AND DATE(a.data_hora) <= ?"
                params.append(data_fim)

            self._db.execute(query, tuple(params))
            return self._db.fetchone()[0]

        except sqlite3.Error as e:
            logger.error(f"Database error counting audit logs: {e}")
            return 0

    # Métodos da interface IRepository
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Implementação de IRepository.find_by_id"""
        self._db.execute("SELECT * FROM auditoria WHERE id = ?", (entity_id,))
        row = self._db.fetchone()
        if row:
            return {"id": row[0], "usuario_id": row[1], "acao": row[2], "data_hora": row[3]}
        return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Implementação de IRepository.find_all"""
        return self.get_logs(limit=1000)

    def save(self, entity: Dict[str, Any]) -> bool:
        """Implementação de IRepository.save"""
        result = self.create_log(
            usuario_id=entity.get("usuario_id"),
            acao=entity.get("acao"),
            tabela_afetada=entity.get("tabela_afetada"),
            dados_anteriores=entity.get("dados_anteriores"),
        )
        return result is not None

    def delete(self, entity_id: int) -> bool:
        """Implementação de IRepository.delete - Logs não devem ser deletados"""
        return False

    def exists(self, entity_id: int) -> bool:
        """Implementação de IRepository.exists"""
        return self.find_by_id(entity_id) is not None

    # Métodos da interface IAuditRepository
    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> bool:
        """Implementação de IAuditRepository.log_action"""
        result = self.create_log(
            usuario_id=user_id,
            acao=action,
            dados_anteriores={"details": details} if details else None,
            endereco_ip=ip_address,
        )
        return result is not None

    def find_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Implementação de IAuditRepository.find_by_user"""
        return self.get_logs(filtro_usuario=user_id)

    def find_by_action(self, action: str) -> List[Dict[str, Any]]:
        """Implementação de IAuditRepository.find_by_action"""
        return self.get_logs(filtro_acao=action)

    def find_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Implementação de IAuditRepository.find_by_date_range"""
        return self.get_logs(data_inicio=start_date, data_fim=end_date)
