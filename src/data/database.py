import sqlite3
import os
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
        
        # Tabela de estados das pastas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pastas (
            id INTEGER PRIMARY KEY,
            numero_pasta TEXT NOT NULL UNIQUE,
            esta_aberta BOOLEAN DEFAULT 0,
            ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de histórico de alterações
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_pastas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pasta_id INTEGER,
            acao TEXT NOT NULL,
            usuario_tipo TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pasta_id) REFERENCES pastas (id)
        )
        ''')
        
        self.conn.commit()
    
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
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()