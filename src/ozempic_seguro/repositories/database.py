import sqlite3
import os
import hashlib
import secrets
import json
from datetime import datetime

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize_database()
        return cls._instance
    
    def _get_db_path(self):
        """Retorna o caminho para o arquivo do banco de dados"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'ozempic_seguro.db')
    
    def _initialize_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        db_exists = os.path.exists(self._get_db_path())
        
        self.conn = sqlite3.connect(self._get_db_path())
        self.cursor = self.conn.cursor()
        
        # Tabela de usuários
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('administrador', 'vendedor', 'repositor', 'tecnico')),
            ativo BOOLEAN DEFAULT 1,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Se o banco de dados não existia, cria o usuário administrador padrão
        if not db_exists:
            self._criar_usuario_admin_padrao()
        
        # Tabelas existentes (mantidas)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS gavetas (
            id INTEGER PRIMARY KEY,
            numero_gaveta TEXT NOT NULL UNIQUE,
            esta_aberta BOOLEAN DEFAULT 0,
            ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_gavetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gaveta_id INTEGER,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gaveta_id) REFERENCES gavetas (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de auditoria
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            tabela_afetada TEXT NOT NULL,
            id_afetado INTEGER,
            dados_anteriores TEXT,
            dados_novos TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            endereco_ip TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        self.conn.commit()
        self._migrar_usuarios_se_necessario()

    def _hash_senha(self, senha, salt=None):
        """Gera um hash seguro da senha"""
        if salt is None:
            salt = secrets.token_hex(16)
        senha_salt = f"{senha}{salt}".encode('utf-8')
        hash_obj = hashlib.sha256(senha_salt)
        return f"{salt}${hash_obj.hexdigest()}"

    def verificar_senha(self, senha, senha_hash):
        """Verifica se a senha está correta"""
        try:
            salt, _ = senha_hash.split('$')
            return senha_hash == self._hash_senha(senha, salt)
        except:
            return False

    def criar_usuario(self, username, senha, nome_completo, tipo):
        """Cria um novo usuário"""
        senha_hash = self._hash_senha(senha)
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
        """Autentica um usuário"""
        self.cursor.execute(
            'SELECT id, username, senha_hash, nome_completo, tipo FROM usuarios WHERE username = ? AND ativo = 1',
            (username,)
        )
        usuario = self.cursor.fetchone()
        
        if usuario and self.verificar_senha(senha, usuario[2]):
            return {
                'id': usuario[0],
                'username': usuario[1],
                'nome_completo': usuario[3],
                'tipo': usuario[4]
            }
        return None
    
    def _migrar_usuarios_se_necessario(self):
        """Migra usuários do arquivo JSON para o banco de dados, se necessário"""
        try:
            # Verifica se já existem usuários no banco
            self.cursor.execute('SELECT COUNT(*) FROM usuarios')
            if self.cursor.fetchone()[0] > 0:
                return  # Já existem usuários, não precisa migrar
                
            # Lê os usuários do arquivo JSON
            usuarios_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'usuarios.json')
            with open(usuarios_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
                
            # Insere cada usuário no banco
            for user in usuarios:
                self.criar_usuario(
                    username=user['usuario'],
                    senha=user['senha'],  # Senha será hasheada no método criar_usuario
                    nome_completo=user['usuario'].capitalize(),  # Nome padrão baseado no username
                    tipo=user['tipo']
                )
            
        except Exception as e:
            print(f"Erro ao migrar usuários: {e}")
    
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
            print(f"Erro ao excluir usuário: {e}")
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
            print(f"Erro ao verificar se é único administrador: {e}")
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
        try:
            # Primeiro, obter o nome de usuário para o log
            self.cursor.execute('SELECT username FROM usuarios WHERE id = ?', (usuario_id,))
            resultado = self.cursor.fetchone()
            
            if not resultado:
                return False
                
            username = resultado[0]
            senha_hash = self._hash_senha(nova_senha)
            
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
            print(f"Erro ao atualizar senha: {e}")
            return False

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()

    def _criar_usuario_admin_padrao(self):
        """Cria um usuário administrador padrão"""
        from hashlib import sha256
        import secrets
        
        # Dados do administrador padrão
        username = "00"
        senha = "1234"
        nome_completo = "ADM"
        
        # Gera um salt aleatório
        salt = secrets.token_hex(8)
        # Cria o hash da senha
        senha_hash = sha256(f"{senha}{salt}".encode('utf-8')).hexdigest()
        
        try:
            # Insere o usuário administrador
            self.cursor.execute('''
            INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
            VALUES (?, ?, ?, 'administrador', 1)
            ''', (username, f"{salt}${senha_hash}", nome_completo))
            
            self.conn.commit()
            print("Usuário administrador padrão criado com sucesso!")
            print(f"Usuário: {username}")
            print(f"Senha: {senha}")
            
        except sqlite3.IntegrityError:
            # Se o usuário já existir, não faz nada
            self.conn.rollback()
            print("Usuário administrador padrão já existe.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao criar usuário administrador padrão: {e}")

    def registrar_auditoria(self, usuario_id, acao, tabela_afetada, id_afetado=None, dados_anteriores=None, dados_novos=None, endereco_ip=None):
        """
        Registra uma ação na tabela de auditoria
        
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
            print(f"Erro ao registrar auditoria: {e}")
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
            print(f"Erro ao buscar logs de auditoria: {e}")
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
            print(f"Erro ao contar logs de auditoria: {e}")
            return 0
