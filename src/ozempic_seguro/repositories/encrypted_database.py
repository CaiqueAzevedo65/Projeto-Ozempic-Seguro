"""
Gerenciador de banco de dados com criptografia.
Implementa criptografia de dados sensíveis usando Fernet (symmetric encryption).
"""
import sqlite3
import os
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import json


class EncryptedDatabaseManager:
    """
    Gerenciador de banco de dados com criptografia de campos sensíveis.
    Usa Fernet para criptografia simétrica.
    """
    
    _instance = None
    _encryption_key: Optional[bytes] = None
    _cipher: Optional[Fernet] = None
    
    # Campos que devem ser criptografados
    ENCRYPTED_FIELDS = {
        'usuarios': ['password_hash', 'nome_completo'],
        'audit_logs': ['details'],
        'gavetas': ['conteudo']
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_encryption()
        return cls._instance
    
    def _initialize_encryption(self):
        """Inicializa sistema de criptografia"""
        # Gera ou carrega chave de criptografia
        key_file = self._get_key_path()
        
        if os.path.exists(key_file):
            # Carrega chave existente
            with open(key_file, 'rb') as f:
                self._encryption_key = f.read()
        else:
            # Gera nova chave
            self._encryption_key = self._generate_encryption_key()
            # Salva chave de forma segura
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(self._encryption_key)
            # Define permissões restritas (apenas owner)
            if os.name != 'nt':  # Unix/Linux
                os.chmod(key_file, 0o600)
        
        self._cipher = Fernet(self._encryption_key)
    
    def _generate_encryption_key(self) -> bytes:
        """Gera chave de criptografia baseada em senha mestra"""
        # Em produção, isso deveria vir de um HSM ou key vault
        # Por ora, usa uma senha mestra derivada do sistema
        import uuid
        import hashlib
        
        # Combina informações únicas do sistema
        system_id = f"{os.environ.get('COMPUTERNAME', '')}{uuid.getnode()}"
        password = hashlib.sha256(system_id.encode()).digest()
        
        # Deriva chave usando PBKDF2
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'ozempic_seguro_salt_2024',  # Salt fixo para consistência
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _get_key_path(self) -> str:
        """Retorna caminho seguro para armazenar chave"""
        # Armazena em diretório protegido do usuário
        if os.name == 'nt':  # Windows
            base_dir = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        else:  # Unix/Linux
            base_dir = os.path.expanduser('~/.local/share')
        
        return os.path.join(base_dir, 'ozempic_seguro', '.encryption.key')
    
    def _get_db_path(self) -> str:
        """Retorna o caminho do banco de dados"""
        base_dir = Path(__file__).parent.parent
        db_dir = base_dir / "data"
        db_dir.mkdir(exist_ok=True)
        return str(db_dir / "ozempic_seguro.db")
    
    def encrypt_value(self, value: str) -> str:
        """Criptografa um valor"""
        if not value:
            return value
        
        encrypted = self._cipher.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_value(self, encrypted_value: str) -> str:
        """Descriptografa um valor"""
        if not encrypted_value:
            return encrypted_value
        
        try:
            encrypted = base64.b64decode(encrypted_value.encode())
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            # Se falhar, retorna o valor original (pode ser não criptografado)
            return encrypted_value
    
    def encrypt_row(self, table: str, row: Dict[str, Any]) -> Dict[str, Any]:
        """Criptografa campos sensíveis de uma linha"""
        if table not in self.ENCRYPTED_FIELDS:
            return row
        
        encrypted_row = row.copy()
        for field in self.ENCRYPTED_FIELDS[table]:
            if field in encrypted_row and encrypted_row[field]:
                encrypted_row[field] = self.encrypt_value(str(encrypted_row[field]))
        
        return encrypted_row
    
    def decrypt_row(self, table: str, row: Dict[str, Any]) -> Dict[str, Any]:
        """Descriptografa campos sensíveis de uma linha"""
        if table not in self.ENCRYPTED_FIELDS or not row:
            return row
        
        decrypted_row = row.copy()
        for field in self.ENCRYPTED_FIELDS[table]:
            if field in decrypted_row and decrypted_row[field]:
                decrypted_row[field] = self.decrypt_value(str(decrypted_row[field]))
        
        return decrypted_row
    
    def execute_query(self, query: str, params: Tuple = ()) -> bool:
        """
        Executa query com criptografia automática de dados sensíveis.
        
        Args:
            query: SQL query
            params: Parâmetros da query
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Detecta tabela da query
            table = self._extract_table_from_query(query)
            
            # Se é INSERT ou UPDATE, criptografa parâmetros sensíveis
            if table and ('INSERT' in query.upper() or 'UPDATE' in query.upper()):
                params = self._encrypt_params(table, query, params)
            
            with sqlite3.connect(self._get_db_path()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return False
    
    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Busca um registro com descriptografia automática.
        
        Args:
            query: SQL query
            params: Parâmetros da query
            
        Returns:
            Dicionário com o registro ou None
        """
        try:
            table = self._extract_table_from_query(query)
            
            with sqlite3.connect(self._get_db_path()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                
                if row:
                    result = dict(row)
                    if table:
                        result = self.decrypt_row(table, result)
                    return result
                    
                return None
                
        except Exception as e:
            print(f"Erro ao buscar registro: {e}")
            return None
    
    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """
        Busca múltiplos registros com descriptografia automática.
        
        Args:
            query: SQL query
            params: Parâmetros da query
            
        Returns:
            Lista de dicionários com os registros
        """
        try:
            table = self._extract_table_from_query(query)
            
            with sqlite3.connect(self._get_db_path()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    result = dict(row)
                    if table:
                        result = self.decrypt_row(table, result)
                    results.append(result)
                
                return results
                
        except Exception as e:
            print(f"Erro ao buscar registros: {e}")
            return []
    
    def _extract_table_from_query(self, query: str) -> Optional[str]:
        """Extrai nome da tabela de uma query SQL"""
        query_upper = query.upper()
        
        # Padrões para identificar tabela
        patterns = [
            ('FROM', 'WHERE'),
            ('FROM', 'ORDER'),
            ('FROM', 'GROUP'),
            ('FROM', 'LIMIT'),
            ('FROM', ';'),
            ('INTO', '('),
            ('UPDATE', 'SET'),
        ]
        
        for start, end in patterns:
            if start in query_upper:
                start_idx = query_upper.index(start) + len(start)
                end_idx = len(query)
                
                if end in query_upper[start_idx:]:
                    end_idx = query_upper.index(end, start_idx)
                
                table_part = query[start_idx:end_idx].strip()
                # Remove aspas e espaços
                table_name = table_part.split()[0].strip('`"\'')
                
                if table_name.lower() in self.ENCRYPTED_FIELDS:
                    return table_name.lower()
        
        return None
    
    def _encrypt_params(self, table: str, query: str, params: Tuple) -> Tuple:
        """Criptografa parâmetros sensíveis baseado na tabela e query"""
        if table not in self.ENCRYPTED_FIELDS or not params:
            return params
        
        # Identifica campos na query
        encrypted_params = list(params)
        fields_to_encrypt = self.ENCRYPTED_FIELDS[table]
        
        # Tenta identificar posição dos campos sensíveis
        for field in fields_to_encrypt:
            if field in query.lower():
                # Encontra posição aproximada do campo nos parâmetros
                # Esta é uma heurística simples, pode precisar de refinamento
                for i, param in enumerate(encrypted_params):
                    if param and isinstance(param, str):
                        # Criptografa se parece ser um campo sensível
                        if field == 'password_hash' or (field == 'nome_completo' and i > 0):
                            encrypted_params[i] = self.encrypt_value(param)
        
        return tuple(encrypted_params)
    
    def create_tables(self):
        """Cria tabelas do banco com suporte a criptografia"""
        # Usa as mesmas tabelas do DatabaseManager original
        # mas com consciência de que alguns campos serão criptografados
        
        queries = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS gavetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                status TEXT DEFAULT 'disponivel',
                conteudo TEXT,
                usuario_id INTEGER,
                data_abertura TIMESTAMP,
                data_fechamento TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios (id)
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_gavetas_status ON gavetas(status);
            """
        ]
        
        for query in queries:
            self.execute_query(query)
