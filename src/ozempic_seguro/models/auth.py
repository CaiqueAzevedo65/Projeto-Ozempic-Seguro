from ..repositories.database import DatabaseManager
import datetime

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.usuario_logado = None

    def autenticar(self, usuario, senha, endereco_ip=None):
        """Autentica um usuário usando o banco de dados"""
        resultado = self.db.autenticar_usuario(usuario, senha)
        
        if resultado:
            self.usuario_logado = resultado
            # Registrar login bem-sucedido
            self.db.registrar_auditoria(
                usuario_id=resultado['id'],
                acao='LOGIN',
                tabela_afetada='USUARIOS',
                id_afetado=resultado['id'],
                dados_novos={'usuario': usuario, 'hora_login': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                endereco_ip=endereco_ip
            )
        else:
            # Tentativa de login falha
            self.db.registrar_auditoria(
                usuario_id=None,
                acao='TENTATIVA_LOGIN',
                tabela_afetada='USUARIOS',
                dados_anteriores={'usuario': usuario, 'hora_tentativa': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                endereco_ip=endereco_ip
            )
            
        return resultado
        
    def logout(self, usuario_id, endereco_ip=None):
        """Registra o logout do usuário"""
        if usuario_id:
            self.db.registrar_auditoria(
                usuario_id=usuario_id,
                acao='LOGOUT',
                tabela_afetada='USUARIOS',
                id_afetado=usuario_id,
                endereco_ip=endereco_ip
            )
        self.usuario_logado = None
        
    def cadastrar_usuario(self, nome, usuario, senha, tipo, usuario_criador_id=None):
        """
        Cadastra um novo usuário no sistema
        
        Args:
            nome (str): Nome completo do usuário
            usuario (str): Nome de usuário para login
            senha (str): Senha do usuário
            tipo (str): Tipo de usuário (administrador, vendedor, repositor)
            usuario_criador_id (int, optional): ID do usuário que está criando este usuário
            
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
                # Obter o ID do usuário recém-criado
                self.db.cursor.execute('SELECT id FROM usuarios WHERE username = ?', (usuario,))
                novo_usuario_id = self.db.cursor.fetchone()[0]
                
                # Registrar a criação do usuário
                self.db.registrar_auditoria(
                    usuario_id=usuario_criador_id if usuario_criador_id else novo_usuario_id,
                    acao='CRIAR',
                    tabela_afetada='USUARIOS',
                    id_afetado=novo_usuario_id,
                    dados_novos={
                        'username': usuario,
                        'nome_completo': nome,
                        'tipo': tipo,
                        'data_criacao': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
                
                return True, "Usuário cadastrado com sucesso!"
            else:
                return False, "Nome de usuário já está em uso"
                
        except Exception as e:
            # Registrar erro na criação do usuário
            self.db.registrar_auditoria(
                usuario_id=usuario_criador_id,
                acao='ERRO_CRIACAO_USUARIO',
                tabela_afetada='USUARIOS',
                dados_anteriores={
                    'username': usuario,
                    'erro': str(e),
                    'hora_erro': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            )
            return False, f"Erro ao cadastrar usuário: {str(e)}"