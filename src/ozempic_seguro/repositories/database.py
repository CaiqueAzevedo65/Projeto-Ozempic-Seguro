"""
DatabaseManager - Wrapper de compatibilidade (DEPRECATED).

.. deprecated:: 1.3.2
    Este módulo é mantido apenas para compatibilidade com código legado.
    Para novos desenvolvimentos, use diretamente:
    - DatabaseConnection para conexão
    - UserRepository para operações de usuários
    - AuditRepository para operações de auditoria
    - GavetaRepository para operações de gavetas
"""
import sqlite3
import os
import json
import warnings
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

from ..core.logger import logger
from ..config import Config


def _deprecation_warning(method_name: str, alternative: str) -> None:
    """Emite aviso de deprecação para métodos legados"""
    warnings.warn(
        f"DatabaseManager.{method_name}() está deprecated. "
        f"Use {alternative} em vez disso.",
        DeprecationWarning,
        stacklevel=3
    )


class DatabaseManager:
    """
    Wrapper de compatibilidade para código legado (DEPRECATED).
    
    .. deprecated:: 1.3.2
        Esta classe será removida em versões futuras.
        Use os repositórios específicos:
        - DatabaseConnection para conexão
        - UserRepository para operações de usuários
        - AuditRepository para operações de auditoria
        - GavetaRepository para operações de gavetas
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa conexão via DatabaseConnection"""
        from .connection import DatabaseConnection
        self._db = DatabaseConnection.get_instance()
        self.conn = self._db.conn
        self.cursor = self._db.cursor

    def criar_usuario(self, username, senha, nome_completo, tipo):
        """
        Cria um novo usuário com bcrypt.
        
        .. deprecated:: 1.3.2
            Use UserRepository.create_user() em vez disso.
        """
        _deprecation_warning('criar_usuario', 'UserRepository.create_user()')
        from ..repositories.security import hash_password
        senha_hash = hash_password(senha)
        try:
            self.cursor.execute(
                'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo) VALUES (?, ?, ?, ?)',
                (username, senha_hash, nome_completo, tipo)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def autenticar_usuario(self, username, senha):
        """Autentica um usuário com bcrypt"""
        from ..repositories.security import verify_password
        self.cursor.execute(
            'SELECT id, username, senha_hash, nome_completo, tipo FROM usuarios WHERE username = ? AND ativo = 1',
            (username,)
        )
        usuario = self.cursor.fetchone()
        
        if usuario and verify_password(senha, usuario[2]):
            return {
                'id': usuario[0],
                'username': usuario[1],
                'nome_completo': usuario[3],
                'tipo': usuario[4]
            }
        return None
    
    def _migrar_usuarios_se_necessario(self):
        """Garante que os usuários padrão existam no banco de dados"""
        try:
            # Criar usuário administrador padrão se não existir
            self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = '00'")
            if self.cursor.fetchone()[0] == 0:
                self._criar_usuario_admin_padrao()
            
            # Criar usuário técnico padrão se não existir
            self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = '01'")
            if self.cursor.fetchone()[0] == 0:
                self._criar_usuario_tecnico_padrao()
                
        except Exception as e:
            logger.error(f"Erro ao verificar usuários padrão: {e}")
    
    def get_estado_gaveta(self, numero_gaveta):
        """Obtém o estado atual de uma gaveta"""
        self.cursor.execute(
            'SELECT esta_aberta FROM gavetas WHERE numero_gaveta = ?',
            (numero_gaveta,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else False
    
    def set_estado_gaveta(self, numero_gaveta, estado, usuario_tipo, usuario_id=None):
        """Define o estado de uma gaveta e registra no histórico"""
        try:
            # Verifica se a gaveta já existe
            self.cursor.execute(
                'SELECT id, esta_aberta FROM gavetas WHERE numero_gaveta = ?',
                (numero_gaveta,)
            )
            gaveta = self.cursor.fetchone()
            
            # Se a gaveta não existe, insere um novo registro
            if not gaveta:
                self.cursor.execute(
                    'INSERT INTO gavetas (numero_gaveta, esta_aberta) VALUES (?, ?)',
                    (numero_gaveta, estado)
                )
                gaveta_id = self.cursor.lastrowid
                acao = 'aberta' if estado else 'fechada'
            else:
                gaveta_id = gaveta[0]
                estado_anterior = bool(gaveta[1])
                acao = 'aberta' if estado and not estado_anterior else 'fechada' if not estado and estado_anterior else None
                
                # Atualiza apenas se o estado for diferente
                if acao:
                    self.cursor.execute(
                        'UPDATE gavetas SET esta_aberta = ?, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?',
                        (estado, gaveta_id)
                    )
            
            # Registra no histórico se houve mudança de estado
            if acao and usuario_id:
                self.cursor.execute(
                    'INSERT INTO historico_gavetas (gaveta_id, acao, usuario_id) VALUES (?, ?, ?)',
                    (gaveta_id, acao, usuario_id)
                )
            elif acao:  # Se não houver usuário, registra sem o ID do usuário
                self.cursor.execute(
                    'INSERT INTO historico_gavetas (gaveta_id, acao) VALUES (?, ?)',
                    (gaveta_id, acao)
                )
            
            self.conn.commit()
            return True, f"Gaveta {numero_gaveta} {acao} com sucesso!"
        except Exception as e:
            self.conn.rollback()
            return False, f"Erro ao atualizar o estado da gaveta: {str(e)}"
    
    def get_historico_gaveta(self, numero_gaveta, limite=10):
        """Obtém o histórico de uma gaveta"""
        self.cursor.execute('''
            SELECT h.acao, u.username, strftime('%d/%m/%Y %H:%M:%S', h.data_hora, 'localtime')
            FROM historico_gavetas h
            JOIN usuarios u ON h.usuario_id = u.id
            WHERE h.gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
            ORDER BY h.data_hora DESC
            LIMIT ?
        ''', (numero_gaveta, limite))
        return self.cursor.fetchall()
    
    def get_historico_paginado(self, numero_gaveta, offset=0, limit=20):
        """Obtém o histórico de uma gaveta com paginação"""
        self.cursor.execute('''
            SELECT h.acao, u.username, strftime('%d/%m/%Y %H:%M:%S', h.data_hora, 'localtime')
            FROM historico_gavetas h
            JOIN usuarios u ON h.usuario_id = u.id
            WHERE h.gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
            ORDER BY h.data_hora DESC
            LIMIT ? OFFSET ?
        ''', (numero_gaveta, limit, offset))
        return self.cursor.fetchall()
    
    def get_total_historico(self, numero_gaveta):
        """Retorna o número total de registros de histórico para uma gaveta"""
        self.cursor.execute('''
            SELECT COUNT(*) 
            FROM historico_gavetas 
            WHERE gaveta_id = (SELECT id FROM gavetas WHERE numero_gaveta = ?)
        ''', (numero_gaveta,))
        return self.cursor.fetchone()[0]
    
    def get_todo_historico(self):
        """Retorna todo o histórico de todas as gavetas"""
        self.cursor.execute('''
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
        return self.cursor.fetchall()
    
    def get_todo_historico_paginado(self, offset=0, limit=20):
        """
        Retorna o histórico de todas as gavetas com paginação
        
        Args:
            offset (int): Número de registros a pular
            limit (int): Número máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (data_hora, numero_gaveta, acao, usuario)
        """
        self.cursor.execute('''
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
        
        return self.cursor.fetchall()
    
    def get_total_todo_historico(self):
        """
        Retorna o número total de registros de histórico de todas as gavetas
        
        Returns:
            int: Número total de registros
        """
        self.cursor.execute('SELECT COUNT(*) FROM historico_gavetas')
        return self.cursor.fetchone()[0]
    
    def get_usuarios(self):
        """Obtém a lista de todos os usuários"""
        self.cursor.execute('''
            SELECT id, username, nome_completo, tipo, ativo, data_criacao 
            FROM usuarios
            ORDER BY data_criacao DESC
        ''')
        return self.cursor.fetchall()

    def excluir_usuario(self, usuario_id):
        """
        Exclui um usuário do banco de dados.
        
        Args:
            usuario_id (int): ID do usuário a ser excluído
            
        Returns:
            bool: True se o usuário foi excluído com sucesso, False caso contrário
        """
        try:
            # Primeiro, verifica se existe um usuário com o ID fornecido
            self.cursor.execute('SELECT id FROM usuarios WHERE id = ?', (usuario_id,))
            if not self.cursor.fetchone():
                return False
                
            # Verifica se o usuário é o único administrador
            if self.eh_unico_administrador(usuario_id):
                return False  # Não permite excluir o único administrador
            
            # Exclui o usuário
            self.cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Erro ao excluir usuário: {e}")
            return False

    def eh_unico_administrador(self, usuario_id):
        """
        Verifica se o usuário é o único administrador no sistema.
        
        Args:
            usuario_id (int): ID do usuário a ser verificado
            
        Returns:
            bool: True se for o único administrador, False caso contrário
        """
        try:
            # Primeiro, verifica se o usuário é administrador
            self.cursor.execute('SELECT tipo FROM usuarios WHERE id = ?', (usuario_id,))
            resultado = self.cursor.fetchone()
            
            if not resultado or resultado[0] != 'administrador':
                return False  # Se não for admin, não precisa bloquear a exclusão
                
            # Conta quantos administradores existem
            self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'administrador'")
            total_admins = self.cursor.fetchone()[0]
            
            return total_admins <= 1
            
        except Exception as e:
            logger.error(f"Erro ao verificar se é único administrador: {e}")
            return True  # Em caso de erro, previne a exclusão por segurança

    def atualizar_senha(self, usuario_id, nova_senha):
        """
        Atualiza a senha de um usuário.
        
        Args:
            usuario_id (int): ID do usuário
            nova_senha (str): Nova senha em texto plano
            
        Returns:
            bool: True se a senha foi atualizada com sucesso, False caso contrário
        """
        from ..repositories.security import hash_password
        
        try:
            # Primeiro, obter o nome de usuário para o log
            self.cursor.execute('SELECT username FROM usuarios WHERE id = ?', (usuario_id,))
            resultado = self.cursor.fetchone()
            
            if not resultado:
                return False
                
            username = resultado[0]
            senha_hash = hash_password(nova_senha)
            
            # Registrar a alteração de senha na auditoria
            self.registrar_auditoria(
                usuario_id=usuario_id,
                acao='ALTERAR_SENHA',
                tabela_afetada='USUARIOS',
                id_afetado=usuario_id,
                dados_anteriores={'usuario': username, 'acao': 'senha_alterada'},
                dados_novos={'usuario': username, 'hora_alteracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            )
            
            # Atualizar a senha no banco de dados
            self.cursor.execute(
                'UPDATE usuarios SET senha_hash = ? WHERE id = ?',
                (senha_hash, usuario_id)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
            
        except Exception as e:
            # Registrar erro na auditoria
            self.registrar_auditoria(
                usuario_id=usuario_id,
                acao='ERRO_ALTERAR_SENHA',
                tabela_afetada='USUARIOS',
                id_afetado=usuario_id,
                dados_anteriores={'erro': str(e), 'hora_erro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            )
            logger.error(f"Erro ao atualizar senha: {e}")
            return False

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def _criar_usuario_admin_padrao(self):
        """Cria um usuário administrador padrão com bcrypt"""
        import os
        from ..repositories.security import hash_password
        
        # Dados do administrador padrão (usa variáveis de ambiente ou valores padrão)
        username = os.getenv('OZEMPIC_ADMIN_USERNAME', '00')
        senha = os.getenv('OZEMPIC_ADMIN_PASSWORD', 'admin@2025')
        nome_completo = "ADMINISTRADOR"
        
        # Gera hash bcrypt
        senha_hash = hash_password(senha)
        
        try:
            # Insere o usuário administrador
            self.cursor.execute('''
            INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
            VALUES (?, ?, ?, 'administrador', 1)
            ''', (username, senha_hash, nome_completo))
            
            self.conn.commit()
            logger.info(f"Usuário administrador padrão criado: {username}")
            
        except sqlite3.IntegrityError:
            # Se o usuário já existir, não faz nada
            self.conn.rollback()
            logger.debug("Usuário administrador padrão já existe.")
    
    def _criar_usuario_tecnico_padrao(self):
        """Cria um usuário técnico padrão com bcrypt"""
        import os
        from ..repositories.security import hash_password
        
        # Dados do técnico padrão (usa variáveis de ambiente ou valores padrão)
        username = os.getenv('OZEMPIC_TECNICO_USERNAME', '01')
        senha = os.getenv('OZEMPIC_TECNICO_PASSWORD', 'tecnico@2025')
        nome_completo = "TÉCNICO"
        
        # Gera hash bcrypt
        senha_hash = hash_password(senha)
        
        try:
            # Insere o usuário técnico
            self.cursor.execute('''
            INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
            VALUES (?, ?, ?, 'tecnico', 1)
            ''', (username, senha_hash, nome_completo))
            
            self.conn.commit()
            logger.info(f"Usuário técnico padrão criado: {username}")
            
        except sqlite3.IntegrityError:
            # Se o usuário já existir, não faz nada
            self.conn.rollback()
            logger.debug("Usuário técnico padrão já existe.")
    
    def registrar_auditoria(self, usuario_id, acao, tabela_afetada, id_afetado=None, 
                          dados_anteriores=None, dados_novos=None, endereco_ip=None):
        """Registra uma ação na tabela de auditoria
        
        Args:
            usuario_id (int): ID do usuário que realizou a ação
            acao (str): Ação realizada (ex: 'LOGIN', 'LOGOUT', 'CRIAR', 'ATUALIZAR', 'EXCLUIR')
            tabela_afetada (str): Nome da tabela afetada
            id_afetado (int, optional): ID do registro afetado
            dados_anteriores (dict, optional): Dados antes da alteração
            dados_novos (dict, optional): Dados após a alteração
            endereco_ip (str, optional): Endereço IP do usuário
            
        Returns:
            int: ID do registro de auditoria criado
        """
        try:
            # Converter dicionários para strings JSON
            dados_anteriores_json = json.dumps(dados_anteriores, ensure_ascii=False) if dados_anteriores else None
            dados_novos_json = json.dumps(dados_novos, ensure_ascii=False) if dados_novos else None
            
            self.cursor.execute('''
                INSERT INTO auditoria 
                (usuario_id, acao, tabela_afetada, id_afetado, dados_anteriores, dados_novos, endereco_ip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id, acao, tabela_afetada, id_afetado, dados_anteriores_json, dados_novos_json, endereco_ip))
            
            self.conn.commit()
            return self.cursor.lastrowid
            
        except Exception as e:
            logger.error(f"Erro ao registrar auditoria: {e}")
            self.conn.rollback()
            return None
    
    def buscar_logs_auditoria(self, offset=0, limit=50, filtro_usuario=None, filtro_acao=None, filtro_tabela=None, 
                             data_inicio=None, data_fim=None):
        """
        Busca registros de auditoria com filtros opcionais
        
        Args:
            offset (int): Número de registros para pular (paginação)
            limit (int): Número máximo de registros a retornar
            filtro_usuario (int, optional): ID do usuário para filtrar
            filtro_acao (str, optional): Ação para filtrar
            filtro_tabela (str, optional): Tabela para filtrar
            data_inicio (str, optional): Data de início no formato 'YYYY-MM-DD'
            data_fim (str, optional): Data de fim no formato 'YYYY-MM-DD'
            
        Returns:
            list: Lista de dicionários com os registros de auditoria
        """
        try:
            query = '''
                SELECT 
                    a.id,
                    a.acao,
                    a.tabela_afetada,
                    a.id_afetado,
                    a.dados_anteriores,
                    a.dados_novos,
                    a.data_hora,
                    u.username as usuario
                FROM auditoria a
                LEFT JOIN usuarios u ON a.usuario_id = u.id
                WHERE 1=1
            '''
            
            params = []
            
            # Aplicar filtros
            if filtro_usuario is not None:
                query += ' AND a.usuario_id = ?'
                params.append(filtro_usuario)
                
            if filtro_acao:
                query += ' AND a.acao = ?'
                params.append(filtro_acao)
                
            if filtro_tabela:
                query += ' AND a.tabela_afetada = ?'
                params.append(filtro_tabela)
                
            if data_inicio:
                query += ' AND DATE(a.data_hora) >= ?'
                params.append(data_inicio)
                
            if data_fim:
                query += ' AND DATE(a.data_hora) <= ?'
                params.append(data_fim)
            
            # Ordenar por data mais recente primeiro
            query += ' ORDER BY a.data_hora DESC'
            
            # Adicionar paginação
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            self.cursor.execute(query, params)
            colunas = [desc[0] for desc in self.cursor.description]
            
            # Converter para lista de dicionários
            resultados = []
            for row in self.cursor.fetchall():
                resultado = dict(zip(colunas, row))
                # Converter strings JSON de volta para dicionários
                if resultado.get('dados_anteriores'):
                    resultado['dados_anteriores'] = json.loads(resultado['dados_anteriores'])
                if resultado.get('dados_novos'):
                    resultado['dados_novos'] = json.loads(resultado['dados_novos'])
                
                # Formatar data para exibição
                if resultado.get('data_hora'):
                    data_obj = datetime.strptime(resultado['data_hora'], '%Y-%m-%d %H:%M:%S')
                    resultado['data_formatada'] = data_obj.strftime('%d/%m/%Y %H:%M:%S')
                
                resultados.append(resultado)
                
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao buscar logs de auditoria: {e}")
            return []
    
    def contar_logs_auditoria(self, filtro_usuario=None, filtro_acao=None, filtro_tabela=None, 
                             data_inicio=None, data_fim=None):
        """
        Conta o número total de registros de auditoria que correspondem aos filtros
        
        Args:
            filtro_usuario (int, optional): ID do usuário para filtrar
            filtro_acao (str, optional): Ação para filtrar
            filtro_tabela (str, optional): Tabela para filtrar
            data_inicio (str, optional): Data de início no formato 'YYYY-MM-DD'
            data_fim (str, optional): Data de fim no formato 'YYYY-MM-DD'
            
        Returns:
            int: Número total de registros que correspondem aos filtros
        """
        try:
            query = 'SELECT COUNT(*) FROM auditoria a WHERE 1=1'
            params = []
            
            # Aplicar filtros (mesmos filtros da busca)
            if filtro_usuario is not None:
                query += ' AND a.usuario_id = ?'
                params.append(filtro_usuario)
                
            if filtro_acao:
                query += ' AND a.acao = ?'
                params.append(filtro_acao)
                
            if filtro_tabela:
                query += ' AND a.tabela_afetada = ?'
                params.append(filtro_tabela)
                
            if data_inicio:
                query += ' AND DATE(a.data_hora) >= ?'
                params.append(data_inicio)
                
            if data_fim:
                query += ' AND DATE(a.data_hora) <= ?'
                params.append(data_fim)
            
            self.cursor.execute(query, params)
            return self.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Erro ao contar logs de auditoria: {e}")
            return 0

    # =========================================================================
    # Aliases em inglês para padronização de nomenclatura
    # Mantidos para compatibilidade com código existente em português
    # =========================================================================
    
    # User methods
    create_user = criar_usuario
    authenticate_user = autenticar_usuario
    update_password = atualizar_senha
    delete_user = excluir_usuario
    get_users = get_usuarios
    is_unique_admin = eh_unico_administrador
    
    # Drawer (gaveta) methods
    get_drawer_state = get_estado_gaveta
    set_drawer_state = set_estado_gaveta
    get_drawer_history = get_historico_gaveta
    get_drawer_history_paginated = get_historico_paginado
    get_total_drawer_history = get_total_historico
    get_all_history = get_todo_historico
    get_all_history_paginated = get_todo_historico_paginado
    get_total_all_history = get_total_todo_historico
    
    # Audit methods
    create_audit_log = registrar_auditoria
    search_audit_logs = buscar_logs_auditoria
    count_audit_logs = contar_logs_auditoria
