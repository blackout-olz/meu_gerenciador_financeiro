# ControlFinance API

Sistema de controle financeiro pessoal desenvolvido com arquitetura Monolítica Modular.

##Arquitetura de Pastas

- **`src/core/`**: Configurações globais, conexão com banco de dados e middlewares.
- **`src/modules/`**: Módulos do domínio de negócio isolados.
  - `auth/`: Autenticação e gestão de usuários.
  - `transactions/`: Lançamentos de entradas, saídas e transferências.
  - `categories/`: Gestão de categorias financeiras.
  - `budgets/`: Metas e limites de gastos.
  - `analytics/`: Relatórios e inteligência financeira.
  - `ai_insights/`: Módulo reservado para IA e Machine Learning.
- **`src/shared/`**: Utilitários, tipos e validações compartilhadas entre módulos.

## Como Executar
