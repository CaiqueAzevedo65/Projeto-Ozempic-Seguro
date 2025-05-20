import sqlite3
import os

def run_migration():
    """Adiciona o tipo 'tecnico' à restrição CHECK da coluna 'tipo' na tabela 'usuarios'"""
    # Obtém o caminho do banco de dados
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ozempic_seguro.db')
    
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Cria uma nova tabela temporária com a restrição atualizada
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('administrador', 'vendedor', 'repositor', 'tecnico')),
            ativo BOOLEAN DEFAULT 1,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 2. Copia os dados da tabela antiga para a nova
        cursor.execute('''
        INSERT INTO usuarios_new 
        SELECT * FROM usuarios
        ''')
        
        # 3. Remove a tabela antiga
        cursor.execute('DROP TABLE usuarios')
        
        # 4. Renomeia a nova tabela para o nome original
        cursor.execute('ALTER TABLE usuarios_new RENAME TO usuarios')
        
        # 5. Recria índices e triggers, se houver
        # (Adicione aqui a recriação de índices ou triggers, se necessário)
        
        # 6. Salva as alterações
        conn.commit()
        print("Migração concluída com sucesso! O tipo 'tecnico' foi adicionado aos tipos de usuário permitidos.")
        
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_migration()
