# Ozempic Seguro

Sistema de gerenciamento de gavetas para controle seguro de medicamentos termolábeis.

O Ozempic Seguro é uma aplicação desktop desenvolvida em Python com interface gráfica moderna usando CustomTkinter. O sistema foi projetado para gerenciar o controle de acesso e estoque de medicamentos, com foco na segurança e rastreabilidade, controlando o tempo em que cada medicamento pode ser removido do refrigerador.

## Características

| Categoria | Recursos |
|-----------|----------|
| **Segurança** | 100% offline, bcrypt (12 rounds), proteção SQL/XSS, auditoria completa |
| **Arquitetura** | MVC, Service Layer, Repository Pattern, Cache LRU |
| **Usuários** | 4 tipos (admin, vendedor, repositor, técnico), RBAC, bloqueio por tentativas |

## Tecnologias

- **Python 3.13** + CustomTkinter 5.2.2
- **SQLite3** + bcrypt + Pillow
- **pytest** (cobertura mínima 70%)

## Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

## Instalação

```bash
git clone https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro.git
cd Projeto-Ozempic-Seguro
python -m venv venv && .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # Configure as credenciais
python run.py
```

## Executando o Projeto

**Credenciais padrão** (configure em `.env`):
- Admin: `00` / `admin@2025`
- Técnico: `01` / `tecnico@2025`

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

### [1.3.2] - 2025-12-11
- **Arquitetura**: Refatoração completa da camada de persistência
  - Nova classe `DatabaseConnection` para gerenciamento de conexão
  - Repositórios (`UserRepository`, `AuditRepository`, `GavetaRepository`) com implementação direta
  - `DatabaseManager` marcado como deprecated (wrapper de compatibilidade)
- **Segurança**: Senhas via variáveis de ambiente (`.env.example`)
- **Código**: 
  - Correção de `UIConfig` duplicada
  - Unificação de validadores (`core/validators.py`)
  - Correção de import circular em `SessionManager` (callback pattern)
  - Type hints consistentes nos módulos principais
  - `__all__` adicionado aos pacotes (`repositories`, `services`, `core`)
- **Limpeza**: Remoção de código morto (`flet_app/`), reorganização do README

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
