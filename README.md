# Ozempic Seguro

Sistema de gerenciamento para controle de segurança de medicamentos, com foco especial no Ozempic.

## 🚀 Visão Geral

O Ozempic Seguro é uma aplicação desktop desenvolvida em Python com interface gráfica moderna usando CustomTkinter. O sistema foi projetado para gerenciar o controle de acesso e estoque de medicamentos, com foco na segurança e rastreabilidade do Ozempic.

## ✨ Funcionalidades

- **Autenticação de Usuários**
  - Login seguro com diferentes níveis de acesso (administrador, vendedor, repositor)
  - Gerenciamento de contas de usuário
  - Controle de sessão

- **Gerenciamento de Usuários**
  - Cadastro de novos usuários
  - Edição de perfis
  - Controle de acesso baseado em funções
  - Alteração segura de senhas

- **Controle de Estoque**
  - Cadastro de medicamentos
  - Controle de lotes e validade
  - Movimentação de entrada e saída
  - Relatórios de estoque

- **Segurança**
  - Senhas criptografadas
  - Registro de atividades
  - Controle de acesso baseado em permissões

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Interface Gráfica**: CustomTkinter
- **Banco de Dados**: SQLite
- **Gerenciamento de Dependências**: pip

## 📦 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

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
   python -m src.main
   ```

2. **Credenciais de Acesso**
   - **Admin**: 
     - Usuário: admin
     - Senha: admin123 (altere após o primeiro acesso)

## 🗃️ Estrutura do Projeto

```
Projeto-Ozempic-Seguro/
├── src/
│   ├── assets/           # Recursos de imagem e ícones
│   ├── data/             # Arquivos de banco de dados
│   ├── views/            # Telas da aplicação
│   │   ├── pages_adm/    # Telas administrativas
│   │   ├── pages_iniciais/ # Telas iniciais
│   │   └── ...
│   ├── auth.py          # Lógica de autenticação
│   ├── database.py       # Gerenciamento do banco de dados
│   └── main.py           # Ponto de entrada da aplicação
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔒 Segurança

- Todas as senhas são armazenadas usando hash seguro
- Proteção contra injeção SQL
- Controle de acesso baseado em funções (RBAC)
- Registro de atividades sensíveis

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através do email: [seu-email@exemplo.com]

---

Desenvolvido com ❤️ por [Seu Nome]
