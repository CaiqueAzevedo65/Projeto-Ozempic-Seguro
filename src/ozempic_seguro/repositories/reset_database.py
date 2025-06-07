import os
import sqlite3
import hashlib
import secrets

def reset_database():
    """
    Remove o banco de dados existente e cria um novo com as configurações iniciais,
    incluindo um usuário administrador padrão.
    """
    # Obtém o caminho do banco de dados
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ozempic_seguro.db')
    
    # Remove o banco de dados existente, se existir
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Banco de dados antigo removido: {db_path}")
        except Exception as e:
            print(f"Erro ao remover o banco de dados existente: {e}")
            return False
    
    try:
        # Conecta ao novo banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
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
        
        # Tabela de gavetas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gavetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_gaveta TEXT NOT NULL UNIQUE,
            aberta BOOLEAN NOT NULL DEFAULT 0,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de histórico de gavetas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_gavetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gaveta_id INTEGER,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acao TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (gaveta_id) REFERENCES gavetas (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Função para criar hash da senha
        def _hash_senha(senha, salt=None):
            if salt is None:
                salt = secrets.token_hex(16)
            senha_salt = f"{senha}{salt}".encode('utf-8')
            hash_obj = hashlib.sha256(senha_salt)
            return f"{salt}${hash_obj.hexdigest()}"
        
        # Cria o usuário administrador padrão
        senha_admin = "1234"
        senha_hash = _hash_senha(senha_admin)
        
        cursor.execute(
            'INSERT INTO usuarios (username, senha_hash, nome_completo, tipo) VALUES (?, ?, ?, ?)',
            ('adm', senha_hash, 'Administrador', 'administrador')
        )
        
        # Confirma as alterações
        conn.commit()
        
        print("\nBanco de dados recriado com sucesso!")
        print("\nCredenciais de acesso:")
        print(f"Usuário: adm")
        print(f"Senha: 1234")
        print("\nPor segurança, altere a senha após o primeiro login.")
        
        return True
        
    except Exception as e:
        print(f"Erro ao recriar o banco de dados: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== RECRIAÇÃO DO BANCO DE DADOS ===\n")
    print("Este processo irá:\n")
    print("1. Remover o banco de dados existente (se houver)")
    print("2. Criar um novo banco de dados com a estrutura atualizada")
    print("3. Adicionar um usuário administrador padrão (usuário: adm, senha: 1234)\n")
    
    confirmacao = input("Deseja continuar? (s/n): ").strip().lower()
    
    if confirmacao == 's':
        if reset_database():
            print("\nOperação concluída com sucesso!")
        else:
            print("\nOcorreu um erro durante a operação.")
    else:
        print("\nOperação cancelada pelo usuário.")
