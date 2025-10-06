# Ozempic Seguro

Sistema avançado de gerenciamento de gavetas para controle seguro de medicamentos com arquitetura moderna e recursos de segurança aprimorados.

## Características Principais

### Segurança
- **100% Offline**: Aplicação completamente local, sem conexões externas
- **Criptografia de Dados**: Banco de dados criptografado com Fernet
- **Autenticação Robusta**: Sistema bcrypt para hash de senhas
- **Validação Completa**: Proteção contra SQL Injection e XSS
- **Auditoria Detalhada**: Logs estruturados de todas as ações

### Arquitetura
- **Padrão MVC**: Separação clara de responsabilidades
- **Service Layer**: Camada de serviços com injeção de dependência
- **Repository Pattern**: Abstração de acesso a dados
- **Cache Inteligente**: Sistema LRU com TTL configurável
- **Singleton Thread-Safe**: Gerenciamento eficiente de recursos

### Performance
- **Cache em Memória**: Redução de acessos ao banco
- **Query Optimization**: Índices e consultas otimizadas
- **Lazy Loading**: Carregamento sob demanda
- **Connection Pooling**: Gerenciamento eficiente de conexões
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
- **Framework de Testes**: pytest 7.4.3
- **Outras Bibliotecas**:
  - Pillow 10.2.0 (processamento de imagens)
  - Bcrypt 4.1.2 (hash seguro de senhas)
  - pytest-cov 4.1.0 (cobertura de testes)
  - pytest-mock 3.12.0 (mocking para testes)

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
   python run.py
   ```

2. **Credenciais de Acesso**
   - **Admin Padrão**:
     - Usuário: `00`
     - Senha: `1234` (altere após o primeiro acesso)
   - **⚠️ Importante**: A sessão expira automaticamente após 10 minutos de inatividade

## 🗃️ Estrutura do Projeto

*Nota: A partir desta versão, todo o código-fonte está em `src/ozempic_seguro/`.*

```
Projeto-Ozempic-Seguro/
├── src/
│   └── ozempic_seguro/
│       ├── assets/           # Recursos de imagem e ícones
│       ├── controllers/      # Controladores (NavigationController)
│       ├── core/            # Componentes principais
│       ├── repositories/    # Camada de acesso a dados
│       │   ├── database.py
│       │   ├── user_repository.py
│       │   └── audit_repository.py
│       ├── services/        # Camada de serviços
│       │   ├── user_service.py
│       │   ├── audit_service.py
│       │   └── service_factory.py
│       ├── views/           # Interfaces gráficas
│       │   ├── pages_adm/   # Telas administrativas
│       │   ├── pages_iniciais/
│       │   └── components.py # Componentes UI modernos
│       ├── config.py        # Configurações centralizadas
│       ├── session.py       # Gerenciamento de sessão
│       └── main.py          # Ponto de entrada
├── tests/                   # Testes automatizados
│   ├── conftest.py         # Fixtures compartilhadas
│   ├── test_user_service.py
│   ├── test_session_manager.py
│   ├── test_user_repository.py
│   ├── test_integration.py
│   ├── test_ui_components.py
│   └── README.md           # Documentação de testes
├── .gitignore
├── pytest.ini              # Configuração de testes
├── requirements.txt
└── README.md
```

## 🔒 Política de Segurança

### **Sistema de Autenticação Avançado**
- **Hash bcrypt** com 12 rounds para senhas (migração automática de SHA256)
- **Timeout de sessão** automático após 10 minutos de inatividade
- **Proteção contra força bruta**: máximo 3 tentativas + bloqueio de 15 minutos
- **Logs de segurança detalhados** com IP, timestamp e contexto completo

### **Validação e Proteção**
- **Sanitização robusta** contra SQL injection e XSS
- **Validação rigorosa** de todos os campos de entrada
- **Escape HTML** automático em dados de usuário
- **Controle de acesso** baseado em funções (RBAC)
- **Proteção contra exclusão** do último administrador

### **Auditoria e Monitoramento**
- **Registro completo** de todas as atividades sensíveis
- **Captura automática** de IP e informações do sistema
- **Logs de violações** de segurança e tentativas suspeitas
- **Timestamps precisos** em formato ISO 8601
- **Filtros avançados** para análise de logs

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

## 🧪 Testes Automatizados

O projeto utiliza pytest como framework principal de testes, com cobertura mínima de 70%.

### Executando os Testes

```bash
# Executar todos os testes
pytest

# Com relatório de cobertura HTML
pytest --cov=src/ozempic_seguro --cov-report=html

# Executar por categoria
pytest -m unit         # Testes unitários
pytest -m integration  # Testes de integração
pytest -m ui          # Testes de interface
```

### Estrutura de Testes

- **Testes Unitários**
  - `test_user_service.py`: Autenticação, CRUD, validações (17 testes)
  - `test_session_manager.py`: Sessão, timeouts, bloqueios (20 testes)
  - `test_user_repository.py`: Operações de banco (14 testes)

- **Testes de Integração**
  - Ciclo completo de usuário
  - Fluxo de segurança e bloqueios
  - ServiceFactory e injeção de dependência

- **Testes de UI**
  - Componentes modernos (ModernButton, ResponsiveGrid)
  - Teclado numérico touchscreen
  - Diálogos de confirmação e notificações

### Fixtures Disponíveis

- `temp_db`: Banco SQLite temporário para testes
- `mock_db`: Mock do DatabaseManager
- `session_manager`: Instância limpa para testes
- `mock_bcrypt`, `mock_datetime`: Mocks de dependências
- `mock_customtkinter`: Mock de componentes UI

Para mais detalhes sobre os testes, consulte `tests/README.md`.

## 📞 Suporte

Para suporte, entre em contato através do email: caiqueazevedo2005@gmail.com

---

Desenvolvido com ❤️ por Caique Azevedo

## 📌 Notas de Atualização

### [1.3.0] - 2025-09-16 - **QUALITY ASSURANCE UPDATE**
- **🧪 Testes Automatizados**: Implementação completa de testes com pytest
  - Cobertura mínima de 70% configurada e monitorada
  - 51+ testes unitários e de integração
  - Testes específicos para UI moderna
- **📚 Documentação**: Guia detalhado de testes em `tests/README.md`
- **🧰 Fixtures**: Banco temporário e mocks para testes isolados
- **🔧 CI/CD**: Configuração para integração contínua

### [1.2.0] - 2025-08-30 - **MAJOR SECURITY UPDATE**
- **🔒 Hash bcrypt**: Migração completa de SHA256+salt para bcrypt (12 rounds)
- **⏱️ Timeout de sessão**: Implementado timeout automático de 10 minutos de inatividade
- **🛡️ Proteção força bruta**: Controle de tentativas de login com bloqueio automático
- **📝 Logs avançados**: Sistema de logs de segurança com IP, timestamp e contexto
- **✅ Validação robusta**: Sanitização contra SQL injection e XSS
- **⚙️ Configurações centralizadas**: Arquivo `config.py` para gerenciamento de configurações
- **📊 Auditoria detalhada**: Logs com contexto completo de segurança
- **🔄 Compatibilidade**: Suporte a senhas legacy durante migração

### [1.1.0] - 2025-06-25
- Introduzida camada de serviços (`services/`) com `UserService` e `AuditService`.
- Removida a classe legada `AuthManager`; lógica de autenticação e auditoria centralizada nos serviços.
- Criado `service_factory.py` para prover injeção de dependência (singletons) nas views/controllers.
- Refatoradas todas as views para usar os serviços, eliminando acesso direto ao banco de dados na camada de apresentação.
- Atualizada a documentação para refletir a nova arquitetura.

### [1.0.0] - 2024-05-30
- Adicionada validação para impedir exclusão do último administrador
- Corrigido fluxo de autenticação de usuários
- Melhorias no sistema de logs e auditoria
- Atualizadas dependências para as versões mais recentes
- Documentação atualizada
