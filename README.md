# Ozempic Seguro

Sistema desktop para controle seguro de medicamentos termolábeis. Python + CustomTkinter, 100% offline.

## Quick Start

```bash
git clone https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro.git
cd Projeto-Ozempic-Seguro
python -m venv venv && .\venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env && python run.py
```

**Login**: Admin `00`/`admin@2025` | Técnico `01`/`tecnico@2025`

## Stack

| | |
|--|--|
| **Core** | Python 3.13, CustomTkinter, SQLite3, bcrypt |
| **Arquitetura** | MVC, Service Layer, Repository Pattern |
| **Testes** | pytest (1057 testes, 58% cobertura) |

## Segurança

- bcrypt 12 rounds, timeout 10 min, bloqueio após 3 falhas
- Sanitização SQL/XSS, RBAC (4 tipos de usuário)
- Auditoria completa com IP e timestamps

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure conforme necessário:

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `OZEMPIC_ENV` | Ambiente de execução (`development` ou `production`) | `production` | Não |
| `OZEMPIC_ADMIN_USERNAME` | Username do administrador padrão | `00` | Sim* |
| `OZEMPIC_ADMIN_PASSWORD` | Senha do administrador padrão | - | Sim* |
| `OZEMPIC_TECNICO_USERNAME` | Username do técnico padrão | `01` | Sim* |
| `OZEMPIC_TECNICO_PASSWORD` | Senha do técnico padrão | - | Sim* |
| `OZEMPIC_BCRYPT_ROUNDS` | Rounds do bcrypt para hashing | `12` | Não |
| `OZEMPIC_SESSION_TIMEOUT` | Timeout de sessão em minutos | `10` | Não |
| `OZEMPIC_MAX_LOGIN_ATTEMPTS` | Máximo de tentativas de login | `3` | Não |
| `OZEMPIC_LOCKOUT_DURATION` | Duração do bloqueio em minutos | `5` | Não |

> **⚠️ IMPORTANTE**: Altere as senhas padrão em produção!

## Testes

```bash
pytest                           # Todos
pytest --cov=src/ozempic_seguro  # Com cobertura
```

## Changelog

**1.3.4** (2026-01-03) - Refatoração linting, type safety, BaseUserFrame  
**1.3.3** (2025-12-18) - 1057 testes, 58% cobertura real  
**1.3.2** (2025-12-11) - Refatoração repositórios, DatabaseConnection  
**1.3.1** (2025-12-09) - Componentes UI modulares, logging estruturado  
**1.3.0** (2025-09-16) - Testes automatizados com pytest  
**1.2.0** (2025-08-30) - Migração bcrypt, proteção força bruta  
**1.1.0** (2025-06-25) - Service Layer, injeção de dependência  
**1.0.0** (2024-05-30) - Versão inicial

---

**MIT** | 📧 caiqueazevedo2005@gmail.com | [Caique Azevedo](https://github.com/CaiqueAzevedo65)
