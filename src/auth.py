from src.data.database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()

    def autenticar(self, usuario, senha):
        """Autentica um usuário usando o banco de dados"""
        return self.db.autenticar_usuario(usuario, senha)
        
    def cadastrar_usuario(self, nome, usuario, senha, tipo):
        """
        Cadastra um novo usuário no sistema
        
        Args:
            nome (str): Nome completo do usuário
            usuario (str): Nome de usuário para login
            senha (str): Senha do usuário
            tipo (str): Tipo de usuário (administrador, vendedor, repositor)
            
        Returns:
            tuple: (bool, str) - (sucesso, mensagem)
        """
        # Validação dos dados de entrada
        if not all([nome.strip(), usuario.strip(), senha]):
            return False, "Todos os campos são obrigatórios"
            
        if tipo not in ['administrador', 'vendedor', 'repositor', 'tecnico']:
            return False, "Tipo de usuário inválido"
            
        if len(senha) < 4:
            return False, "A senha deve ter pelo menos 4 caracteres"
            
        # Tenta cadastrar o usuário
        try:
            sucesso = self.db.criar_usuario(
                username=usuario,
                senha=senha,
                nome_completo=nome,
                tipo=tipo
            )
            
            if sucesso:
                return True, "Usuário cadastrado com sucesso!"
            else:
                return False, "Nome de usuário já está em uso"
                
        except Exception as e:
            return False, f"Erro ao cadastrar usuário: {str(e)}"