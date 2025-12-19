# Ozempic Seguro

Sistema desktop para controle seguro de medicamentos termolábeis. Python + CustomTkinter, 100% offline.

## Quick Start

```bash
git clone https://github.com/CaiqueAzevedo65/Projeto-Ozempic-Seguro.git
cd Projeto-Ozempic-Seguro
python -m venv venv && .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env && python run.py
```

**Login**: Admin `00`/`admin@2025` | Técnico `01`/`tecnico@2025`

## Stack

| | |
|--|--|
| **Core** | Python 3.13, CustomTkinter, SQLite3, bcrypt |
| **Arquitetura** | MVC, Service Layer, Repository Pattern |
| **Testes** | pytest (1101 testes, 85% cobertura) |

## Segurança

- bcrypt 12 rounds, timeout 10 min, bloqueio após 3 falhas
- Sanitização SQL/XSS, RBAC (4 tipos de usuário)
- Auditoria completa com IP e timestamps

## Testes

```bash
pytest                           # Todos
pytest --cov=src/ozempic_seguro  # Com cobertura
```

## Changelog

**1.3.3** (2025-12-18) - 1101 testes, 85% cobertura  
**1.3.2** (2025-12-11) - Refatoração repositórios, DatabaseConnection  
**1.3.1** (2025-12-09) - Componentes UI modulares, logging estruturado  
**1.3.0** (2025-09-16) - Testes automatizados com pytest  
**1.2.0** (2025-08-30) - Migração bcrypt, proteção força bruta  
**1.1.0** (2025-06-25) - Service Layer, injeção de dependência  
**1.0.0** (2024-05-30) - Versão inicial

---

**MIT** | 📧 caiqueazevedo2005@gmail.com | [Caique Azevedo](https://github.com/CaiqueAzevedo65)
