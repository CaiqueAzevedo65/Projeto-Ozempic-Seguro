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
        self.conn = sqlite3.connect(self._get_db_path())
        self.cursor = self.conn.cursor()
        
        # Tabela de usuários
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('administrador', 'vendedor', 'repositor')),
            ativo BOOLEAN DEFAULT 1,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabelas existentes (mantidas)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pastas (
            id INTEGER PRIMARY KEY,
            numero_pasta TEXT NOT NULL UNIQUE,
            esta_aberta BOOLEAN DEFAULT 0,
            ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_pastas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pasta_id INTEGER,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pasta_id) REFERENCES pastas (id),
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
    
    def get_estado_pasta(self, numero_pasta):
        """Obtém o estado atual de uma pasta"""
        self.cursor.execute(
            'SELECT esta_aberta FROM pastas WHERE numero_pasta = ?',
            (numero_pasta,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else False
    
    def set_estado_pasta(self, numero_pasta, estado, usuario_tipo):
        """Define o estado de uma pasta e registra no histórico"""
        # Verifica se a pasta já existe
        self.cursor.execute(
            'SELECT id, esta_aberta FROM pastas WHERE numero_pasta = ?',
            (numero_pasta,)
        )
        pasta = self.cursor.fetchone()
        
        # Se a pasta não existe, insere um novo registro
        if not pasta:
            self.cursor.execute(
                'INSERT INTO pastas (numero_pasta, esta_aberta) VALUES (?, ?)',
                (numero_pasta, estado)
            )
            pasta_id = self.cursor.lastrowid
            acao = 'aberta' if estado else 'fechada'
        else:
            pasta_id = pasta[0]
            estado_anterior = bool(pasta[1])
            acao = 'aberta' if estado and not estado_anterior else 'fechada' if not estado and estado_anterior else None
            
            # Atualiza apenas se o estado for diferente
            if acao:
                self.cursor.execute(
                    'UPDATE pastas SET esta_aberta = ?, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?',
                    (estado, pasta_id)
                )
        
        # Registra no histórico se houve mudança de estado
        if acao:
            self.cursor.execute(
                'INSERT INTO historico_pastas (pasta_id, acao, usuario_tipo) VALUES (?, ?, ?)',
                (pasta_id, acao, usuario_tipo)
            )
        
        self.conn.commit()
        return estado
    
    def get_historico_pasta(self, numero_pasta, limite=10):
        """Obtém o histórico de alterações de uma pasta"""
        self.cursor.execute('''
            SELECT h.acao, h.usuario_tipo, h.data_hora 
            FROM historico_pastas h
            JOIN pastas p ON h.pasta_id = p.id
            WHERE p.numero_pasta = ?
            ORDER BY h.data_hora DESC
            LIMIT ?
        ''', (numero_pasta, limite))
        
        return self.cursor.fetchall()
    
    def get_todo_historico(self):
        """Obtém o histórico completo de todas as pastas"""
        self.cursor.execute('''
            SELECT h.data_hora, p.numero_pasta, h.acao, h.usuario_tipo 
            FROM historico_pastas h
            JOIN pastas p ON h.pasta_id = p.id
            ORDER BY h.data_hora DESC
        ''')
        
        return self.cursor.fetchall()
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()





