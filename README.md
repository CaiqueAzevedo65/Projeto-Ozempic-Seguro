# Ozempic Seguro

Sistema de gerenciamento de gavetas para controle seguro de medicamentos.

## Características

| Categoria | Recursos |
|-----------|----------|
| **Segurança** | 100% offline, bcrypt (12 rounds), proteção SQL/XSS, auditoria completa |
| **Arquitetura** | MVC, Service Layer, Repository Pattern, Cache LRU |
| **Usuários** | 4 tipos (admin, vendedor, repositor, técnico), RBAC, bloqueio por tentativas |
O Ozempic Seguro é uma aplicação desktop desenvolvida em Python com interface gráfica moderna usando CustomTkinter. O sistema foi projetado para gerenciar o controle de acesso e estoque de medicamentos, com foco na segurança e rastreabilidade de remédios termolábeis, controlando o tempo em que cada medicameto pode ser removido do refrigerador.

## Tecnologias

- **Python 3.13** + CustomTkinter 5.2.2
- **SQLite3** + bcrypt + Pillow
- **pytest** (cobertura mínima 70%)

## Instalação

```bash
git clone https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro.git
cd Projeto-Ozempic-Seguro
python -m venv venv && .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```
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

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Executando o Projeto

**Credenciais padrão:**
- Admin: `00` / `1234`
- Técnico: `01` / `1234`

> ⚠️ Sessão expira após 10 min de inatividade. Bloqueio após 3 tentativas falhas (5 min).

## Estrutura

```
src/ozempic_seguro/
├── controllers/      # NavigationController
├── core/            # Cache, Logger, Validators
├── repositories/    # DatabaseManager, UserRepository
├── services/        # UserService, AuditService, ServiceFactory
├── views/
│   ├── components/  # Componentes UI modulares
│   ├── pages_adm/   # Telas administrativas
│   └── pages_iniciais/
├── config.py        # Configurações centralizadas
├── session.py       # Gerenciamento de sessão
└── main.py
```

## Testes

```bash
pytest                                    # Todos os testes
pytest --cov=src/ozempic_seguro          # Com cobertura
pytest -m unit|integration|ui            # Por categoria
```

## Segurança

- **Autenticação**: bcrypt 12 rounds, timeout 10 min, bloqueio 5 min após 3 falhas
- **Validação**: Sanitização SQL/XSS, escape HTML, RBAC
- **Auditoria**: Logs com IP, timestamp ISO 8601, contexto completo

## Contribuição

1. Fork → 2. Branch (`feature/...`) → 3. Commit → 4. PR

## Contato

📧 caiqueazevedo2005@gmail.com

---

**Licença MIT** | Desenvolvido por Caique Azevedo

## Changelog
Para suporte, entre em contato através do email: [caiqueazevedo2005@gmail.com](caiqueazevedo2005@gmail.com)

### [1.3.1] - 2025-12-09
- Refatoração de componentes UI em módulos (`views/components/`)
- Substituição de `print()` por logging estruturado
- Remoção de código legado e duplicado
- Unificação de validadores (`InputValidator` → `Validators`)
- Correção de hash SHA256 legado → bcrypt em `reset_database.py`

### [1.3.0] - 2025-09-16
- Testes automatizados com pytest (70%+ cobertura)
- Fixtures e mocks para testes isolados

### [1.2.0] - 2025-08-30
- Migração bcrypt, timeout de sessão, proteção força bruta
- Logs de segurança, validação robusta, configurações centralizadas

### [1.1.0] - 2025-06-25
- Service Layer com injeção de dependência
- Remoção de `AuthManager` legado

### [1.0.0] - 2024-05-30
- Versão inicial com autenticação e auditoria
