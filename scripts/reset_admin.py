#!/usr/bin/env python
"""
Script para resetar a senha do admin para o formato bcrypt.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ozempic_seguro.repositories.database import DatabaseManager
from ozempic_seguro.repositories.security import hash_password

def reset_admin_password():
    print("=== RESET DE SENHA DO ADMIN ===\n")
    
    db = DatabaseManager()
    
    # Gera novo hash bcrypt para senha "1234"
    new_hash = hash_password("1234")
    print(f"Novo hash gerado (bcrypt): {new_hash[:20]}...")
    
    # Atualiza senha do usuário "00"
    db.cursor.execute(
        "UPDATE usuarios SET senha_hash = ? WHERE username = ?",
        (new_hash, "00")
    )
    db.conn.commit()
    
    print("✓ Senha do admin atualizada com sucesso!")
    print("\nCredenciais:")
    print("  Usuário: 00")
    print("  Senha: 1234")
    
    # Verifica
    result = db.autenticar_usuario("00", "1234")
    if result:
        print("\n✓ Teste de login bem-sucedido!")
    else:
        print("\n✗ Erro no teste de login!")

if __name__ == "__main__":
    reset_admin_password()
