# ControlFinance (Projeto Rainbow)

Plataforma integrada de controle e inteligência financeira pessoal. O repositório centraliza o ecossistema completo da aplicação, abrangendo a API backend de alta performance, os scripts de banco de dados, a suíte de testes e os módulos de análise preditiva.

---

## Visão Geral da Arquitetura

O sistema é estruturado no padrão **Monolito Modular**, onde o backend atua como core de regras de negócio desacoplado, permitindo que cada módulo evolua de forma independente sem comprometer a integridade global do projeto.

### Estrutura Global do Repositório

```text
rainbow/
├── backend/                  # Aplicação Principal e API RESTful
│   ├── src/
│   │   ├── core/             # Conexões, configurações globais e segurança
│   │   │   ├── config.py     # Gestão de variáveis de ambiente (Pydantic Settings)
│   │   │   ├── database.py   # Engine SQLAlchemy e gerador de sessão
│   │   │   └── security.py   # Hashing e validação criptográfica de senhas (bcrypt)
│   │   ├── modules/          # Domínios de negócio isolados
│   │   │   ├── ai_insights/  # Módulo para inteligência financeira e ML
│   │   │   ├── analytics/    # Consolidação de relatórios e métricas
│   │   │   ├── auth/         # Autenticação, usuários e gestão de acessos
│   │   │   │   ├── models.py # Mapeamento ORM da tabela 'users'
│   │   │   │   ├── router.py # Endpoints HTTP (/auth)
│   │   │   │   ├── schemas.py# DTOs de validação e serialização (Pydantic)
│   │   │   │   └── service.py# Regras de negócio, busca e persistência
│   │   │   ├── budgets/      # Limites de gastos e metas financeiras
│   │   │   ├── categories/   # Categorização de despesas e receitas
│   │   │   └── transactions/ # Lançamentos de entradas, saídas e transferências
│   │   ├── shared/           # Utilitários e validações compartilhadas
│   │   └── main.py           # Ponto de entrada da aplicação FastAPI
│   ├── .env                  # Variáveis de ambiente locais (não versionado)
│   ├── pyproject.toml        # Configuração do projeto e dependências (uv)
│   └── uv.lock               # Trava de versões exatas das dependências
├── db/                       # Schemas de migração, scripts DDL e backups SQL
└── tests/                    # Suíte de testes automatizados (unitários e integração)

```

---

## Tecnologias e Stack Tecnológica

* **Linguagem**: Python 3.13+
* **Framework Backend**: FastAPI
* **ORM e Persistência**: SQLModel / SQLAlchemy sobre PostgreSQL (Supabase)
* **Validação de Contratos**: Pydantic V2 & Pydantic-Settings
* **Criptografia e Segurança**: Bcrypt
* **Gerenciador de Pacotes e Ambientes**: uv

---

## Módulos do Domínio

1. **Auth (Autenticação e Usuários)**: Gestão de perfil, controle de acesso e verificação de unicidade para dados sensíveis (E-mail, CPF, Telefone).
2. **Transactions (Transações)**: Controle de fluxo de caixa (entradas, saídas e movimentações entre contas).
3. **Categories (Categorias)**: Classificação de despesas e receitas para agrupamento financeiro.
4. **Budgets (Orçamentos)**: Definição de limites de consumo e alertas por categoria ou período.
5. **Analytics (Métricas e Relatórios)**: Consolidação de dados para renderização de gráficos e balanços.
6. **AI Insights (Inteligência Financeira)**: Módulo reservado para análise de padrões de consumo e sugestões automatizadas de economia.

---

## Configuração e Execução do Projeto

### Pré-requisitos

* Python 3.13 ou superior
* Gerenciador `uv` instalado no ambiente de desenvolvimento

### 1. Variáveis de Ambiente

Navegue até a pasta `backend` e crie o arquivo `.env` com as credenciais do banco de dados:

```bash
cd backend

```

Conteúdo do arquivo `.env`:

```env
SUPABASE_URL=postgresql://usuario:senha@host:porta/nomedobanco

```

### 2. Configuração do Workspace

Garantir que a instrução abaixo esteja presente no arquivo `backend/pyproject.toml` para que o `uv` trate o projeto como aplicação executável:

```toml
[tool.uv]
package = false

```

### 3. Sincronização de Dependências

Execute a instalação do ambiente virtual e pacotes declarados:

```bash
uv sync

```

### 4. Execução do Servidor Backend

Inicie o servidor de desenvolvimento Uvicorn:

```bash
uv run uvicorn main:app --reload

```

A API estará acessível em `http://127.0.0.1:8000`.

---

## Endpoints Implementados (Módulo Auth)

A documentação interativa Swagger UI fica disponível automaticamente em `http://127.0.0.1:8000/docs`.

| Método | Endpoint | Descrição | Status Sucesso | Tratamento de Erro |
| --- | --- | --- | --- | --- |
| **POST** | `/auth/register` | Registra um novo usuário verificando a unicidade de E-mail, CPF e Telefone. | `201 Created` | `409 Conflict` |
| **POST** | `/auth/login` | Autentica o usuário validando as credenciais cadastradas. | `200 OK` | `401 Unauthorized` |
| **GET** | `/auth/users/{user_id}` | Recupera os dados públicos do perfil por UUID. | `200 OK` | `404 Not Found` |
| **PATCH** | `/auth/users/{user_id}` | Atualiza parcialmente os dados do perfil e recarrega a data de modificação. | `200 OK` | `404 Not Found` |
| **DELETE** | `/auth/users/{user_id}` | Remove permanentemente o registro da base de dados (Hard Delete). | `204 No Content` | `404 Not Found` |

---

## Padrões de Engenharia e Segurança

* **Isolamento de Credenciais em DTOs**: Os schemas de resposta (`UserResponse`) omitem os campos `password` e `password_hash`, impedindo a exposição acidental de senhas na camada HTTP.
* **Defesa Contra Enumeração de Contas**: O fluxo de autenticação retorna mensagens de erro padronizadas (`401 Unauthorized`) tanto para falhas de e-mail inexistente quanto para senhas incorretas.
* **Gerenciamento Seguro de Conexões**: Utilização de geradores Python (`yield`) para injeção de dependência de sessões do SQLAlchemy, garantindo abertura e fechamento automático de conexões no pool.
* **Criptografia sem Legado**: Uso direto da biblioteca `bcrypt` compatível com Python 3.13+, sem dependências obsoletas de abstração de hash.