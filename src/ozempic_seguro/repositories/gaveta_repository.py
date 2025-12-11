"""
Repositório de gavetas: manipulação de estado e histórico.

Implementa IGavetaRepository com lógica de persistência para gavetas.
"""
from typing import Optional, List, Tuple, Any

from .connection import DatabaseConnection
from ..core.logger import logger


class GavetaRepository:
    """
    Repositório para operações de gavetas no banco de dados.
    
    Responsabilidades:
    - Gerenciar estado das gavetas (aberta/fechada)
    - Registrar histórico de operações
    - Consultar histórico com paginação
    """
    
    def __init__(self):
        self._db = DatabaseConnection.get_instance()

    def get_state(self, numero_gaveta: int) -> bool:
        """
        Retorna o estado atual de uma gaveta.
        
        Args:
            numero_gaveta: Número da gaveta
            
        Returns:
            True se aberta, False se fechada
        """
        self._db.execute(
            'SELECT esta_aberta FROM gavetas WHERE numero_gaveta = ?',
            (numero_gaveta,)
        )
        result = self._db.fetchone()
        return bool(result[0]) if result else False

    def set_state(
        self, 
        numero_gaveta: int, 
        estado: bool, 
        usuario_tipo: str, 
        usuario_id: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Define o estado de uma gaveta e registra no histórico.
        
        Args:
            numero_gaveta: Número da gaveta
            estado: True para abrir, False para fechar
            usuario_tipo: Tipo do usuário que realizou a ação
            usuario_id: ID do usuário (opcional)
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Verifica se a gaveta existe
            self._db.execute(
                'SELECT id, esta_aberta FROM gavetas WHERE numero_gaveta = ?',
                (numero_gaveta,)
            )
            gaveta = self._db.fetchone()
            
            if not gaveta:
                # Cria nova gaveta
                self._db.execute(
                    'INSERT INTO gavetas (numero_gaveta, esta_aberta) VALUES (?, ?)',
                    (numero_gaveta, estado)
                )
                gaveta_id = self._db.lastrowid()
                acao = 'aberta' if estado else 'fechada'
            else:
                gaveta_id = gaveta[0]
                estado_anterior = bool(gaveta[1])
                
                # Determina ação
                if estado and not estado_anterior:
                    acao = 'aberta'
                elif not estado and estado_anterior:
                    acao = 'fechada'
                else:
                    acao = None
                
                # Atualiza se mudou
                if acao:
                    self._db.execute(
                        'UPDATE gavetas SET esta_aberta = ?, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?',
                        (estado, gaveta_id)
                    )
            
            # Registra histórico
            if acao and usuario_id:
                self._db.execute(
                    'INSERT INTO historico_gavetas (gaveta_id, acao, usuario_id) VALUES (?, ?, ?)',
                    (gaveta_id, acao, usuario_id)
                )
            elif acao:
                self._db.execute(
                    'INSERT INTO historico_gavetas (gaveta_id, acao) VALUES (?, ?)',
                    (gaveta_id, acao)
                )
            
            self._db.commit()
            return True, f"Gaveta {numero_gaveta} {acao or 'sem alteração'}"
            
        except Exception as e:
            logger.error(f"Error setting drawer state: {e}")
            self._db.rollback()
            return False, f"Erro ao atualizar gaveta: {str(e)}"

    def get_history(self, numero_gaveta: int, limit: int = 10) -> List[Tuple]:
        """
        Retorna o histórico de uma gaveta.
        
        Args:
            numero_gaveta: Número da gaveta
            limit: Número máximo de registros
            
        Returns:
            Lista de tuplas (acao, username, data_hora)
        """
        self._db.execute('''
            SELECT h.acao, u.username, strftime('%d/%m/%Y %H:%M:%S', h.data_hora, 'localtime')
            FROM historico_gavetas h
            JOIN usuarios u ON h.usuario_id = u.id
            WHERE h.gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
            ORDER BY h.data_hora DESC
            LIMIT ?
        ''', (numero_gaveta, limit))
        return self._db.fetchall()

    def get_history_paginated(self, numero_gaveta: int, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """
        Retorna o histórico de uma gaveta com paginação.
        
        Args:
            numero_gaveta: Número da gaveta
            offset: Registros a pular
            limit: Número máximo de registros
            
        Returns:
            Lista de tuplas (acao, username, data_hora)
        """
        self._db.execute('''
            SELECT h.acao, u.username, strftime('%d/%m/%Y %H:%M:%S', h.data_hora, 'localtime')
            FROM historico_gavetas h
            JOIN usuarios u ON h.usuario_id = u.id
            WHERE h.gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
            ORDER BY h.data_hora DESC
            LIMIT ? OFFSET ?
        ''', (numero_gaveta, limit, offset))
        return self._db.fetchall()

    def count_history(self, numero_gaveta: int) -> int:
        """
        Retorna o total de registros de histórico para uma gaveta.
        
        Args:
            numero_gaveta: Número da gaveta
            
        Returns:
            Número total de registros
        """
        self._db.execute('''
            SELECT COUNT(*) 
            FROM historico_gavetas 
            WHERE gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
        ''', (numero_gaveta,))
        return self._db.fetchone()[0]

    def get_all_history(self) -> List[Tuple]:
        """
        Retorna todo o histórico de todas as gavetas.
        
        Returns:
            Lista de tuplas (data_hora, numero_gaveta, acao, usuario)
        """
        self._db.execute('''
            SELECT 
                strftime('%d/%m/%Y %H:%M:%S', h.data_hora, 'localtime') as data_hora,
                p.numero_gaveta,
                h.acao,
                u.username as usuario
            FROM historico_gavetas h
            JOIN gavetas p ON h.gaveta_id = p.id
            JOIN usuarios u ON h.usuario_id = u.id
            ORDER BY h.data_hora DESC
        ''')
        return self._db.fetchall()

    def get_all_history_paginated(self, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """
        Retorna o histórico de todas as gavetas com paginação.
        
        Args:
            offset: Registros a pular
            limit: Número máximo de registros
            
        Returns:
            Lista de tuplas (data_hora, numero_gaveta, acao, usuario)
        """
        self._db.execute('''
            SELECT 
                strftime('%d/%m/%Y %H:%M:%S', h.data_hora) as data_hora, 
                p.numero_gaveta, 
                h.acao, 
                COALESCE(u.nome_completo, u.username, 'Sistema') as usuario
            FROM historico_gavetas h
            JOIN gavetas p ON h.gaveta_id = p.id
            LEFT JOIN usuarios u ON h.usuario_id = u.id
            ORDER BY h.data_hora DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        return self._db.fetchall()

    def count_all_history(self) -> int:
        """
        Retorna o número total de registros de histórico de todas as gavetas.
        
        Returns:
            Número total de registros
        """
        self._db.execute('SELECT COUNT(*) FROM historico_gavetas')
        return self._db.fetchone()[0]
