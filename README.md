# Ozempic Seguro

Sistema de gerenciamento para controle de segurança de medicamentos, com foco especial no Ozempic.

## 🚀 Visão Geral

O Ozempic Seguro é uma aplicação desktop desenvolvida em Python com interface gráfica moderna usando CustomTkinter. O sistema foi projetado para gerenciar o controle de acesso e estoque de medicamentos, com foco na segurança e rastreabilidade do Ozempic.

## ✨ Funcionalidades Principais

- **Autenticação de Usuários**
  - Login seguro com diferentes níveis de acesso (administrador, vendedor, repositor)
  - Gerenciamento de contas de usuário
  - Controle de sessão

- **Gerenciamento de Usuários**
  - Cadastro de novos usuários
  - Edição de perfis
  - Controle de acesso baseado em funções
  - Alteração segura de senhas
  - Validação para impedir exclusão do último administrador

- **Segurança**
  - Senhas criptografadas
  - Registro de auditoria de atividades
  - Controle de acesso baseado em permissões
  - Proteção contra operações críticas não autorizadas

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.13
- **Interface Gráfica**: CustomTkinter 5.2.2
- **Banco de Dados**: SQLite3 (embutido no Python)
- **Gerenciamento de Dependências**: pip
- **Outras Bibliotecas**:
  - Pillow 10.2.0 (processamento de imagens)
  - Bcrypt (hash de senhas)

## 📦 Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

## 🚀 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro.git
   cd Projeto-Ozempic-Seguro
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # No Windows
   # ou
   source venv/bin/activate  # No Linux/Mac
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Executando o Projeto

1. **Inicie a aplicação**
   ```bash
   cd src && python -m ozempic_seguro.main
   ```

2. **Credenciais de Acesso**
   - **Admin Padrão**:
     - Usuário: `00`
     - Senha: `1234` (altere após o primeiro acesso)

## 🗃️ Estrutura do Projeto

*Nota: A partir desta versão, todo o código-fonte está em `src/ozempic_seguro/`.*

```
Projeto-Ozempic-Seguro/
├── src/
│   ├── assets/           # Recursos de imagem e ícones
│   ├── data/             # Arquivos de banco de dados
│   ├── views/            # Telas da aplicação
│   │   ├── pages_adm/    # Telas administrativas
│   │   │   ├── painel_administrador_view.py
│   │   │   └── gerenciamento_usuarios_view.py
│   │   ├── pages_iniciais/
│   │   └── ...
│   ├── auth.py          # Lógica de autenticação
│   ├── database.py       # Gerenciamento do banco de dados
│   └── main.py           # Ponto de entrada da aplicação
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔒 Política de Segurança

- Todas as senhas são armazenadas usando hash seguro (bcrypt)
- Proteção contra injeção SQL usando parâmetros preparados
- Controle de acesso baseado em funções (RBAC)
- Registro de atividades sensíveis
- Validação de entrada em todos os campos
- Proteção contra exclusão acidental de usuários críticos

## 🐛 Reportando Problemas

Encontrou um bug ou tem uma sugestão? Por favor, [abra uma issue](https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro/issues) no GitHub.

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através do email: [seu-email@exemplo.com]

---

Desenvolvido com ❤️ por Caique Azevedo

## 📌 Notas de Atualização

### [1.0.0] - 2024-05-30
- Adicionada validação para impedir exclusão do último administrador
- Corrigido fluxo de autenticação de usuários
- Melhorias no sistema de logs e auditoria
- Atualizadas dependências para as versões mais recentes
- Documentação atualizada
