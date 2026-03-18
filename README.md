# Sistema de Doação

## Sumário

Este projeto implementa um Sistema de Doação abrangente, desenvolvido em Python utilizando SQLAlchemy para interação com banco de dados. O sistema gerencia o ciclo completo de doações, desde o cadastro de usuários (doadores, beneficiários, ONGs), itens e categorias, até o rastreamento de doações, pedidos de auxílio, distribuição de itens e gestão de vagas de voluntariado. O objetivo principal é facilitar a organização e a transparência no processo de doação, conectando quem deseja doar com quem precisa de ajuda.

- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configuração e Instalação](#configuração-e-instalação)
- [Povoamento de Dados de Teste](#povoamento-de-dados-de-teste)
- [Como Executar](#como-executar)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Funcionalidades

O sistema oferece as seguintes funcionalidades:

*   **Gestão de Usuários**: Cadastro e gerenciamento de usuários, incluindo Pessoas Físicas e Pessoas Jurídicas (ONGs).
*   **Gestão de Beneficiários**: Registro e acompanhamento de beneficiários que recebem as doações.
*   **Categorias e Itens**: Definição de categorias de itens (e.g., Alimentos, Vestuário, Higiene) e cadastro detalhado dos itens disponíveis para doação.
*   **Doações**: Registro de doações realizadas, com a especificação dos itens doados e suas quantidades.
*   **Pedidos de Auxílio**: Beneficiários podem registrar pedidos de auxílio, especificando suas necessidades.
*   **Distribuição de Itens**: Gerenciamento da distribuição de itens em resposta aos pedidos de auxílio.
*   **Voluntariado**: Criação e gestão de vagas de voluntariado, permitindo que usuários se inscrevam para ajudar.
*   **Rastreamento**: Acompanhamento do status e localização dos itens doados ao longo do processo.

## Estrutura do Projeto

O projeto segue uma estrutura modular, organizada da seguinte forma:

```
Sistema_doacao-main/
├── README.md
├── itens_teste.py
├── main.py
├── requirements.txt
└── src/
    ├── config/
    │   ├── __init__.py
    │   └── db_config.py
    ├── database/
    │   ├── __init__.py
    │   ├── database.py
    │   └── tables.py
    ├── domain/
    │   ├── __init__.py
    │   ├── beneficiarios.py
    │   ├── distribuicoes.py
    │   ├── distribuicoesItens.py
    │   ├── doacoes.py
    │   ├── doacoesItem.py
    │   ├── inscricoes.py
    │   ├── itens.py
    │   ├── itensCategoria.py
    │   ├── pedidosAuxilio.py
    │   ├── pessoasFisica.py
    │   ├── pessoasJuridica.py
    │   ├── rastreios.py
    │   ├── usuarios.py
    │   └── vagasVoluntariado.py
    └── repositories/
        ├── __init__.py
        ├── repository.py
        ├── repository_beneficiarios.py
        ├── ... (outros repositórios para cada entidade)
```

*   `main.py`: Ponto de entrada principal da aplicação.
*   `itens_teste.py`: Script para povoamento do banco de dados com dados de teste.
*   `src/config/db_config.py`: Configurações de conexão com o banco de dados.
*   `src/database/`: Contém a lógica de conexão (`database.py`) e a definição das tabelas (`tables.py`) usando SQLAlchemy.
*   `src/domain/`: Define as classes de domínio (modelos) para cada entidade do sistema (e.g., `Usuario`, `Item`, `Doacao`).
*   `src/repositories/`: Contém as classes de repositório que implementam a lógica de persistência de dados para cada entidade, interagindo com o banco de dados.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **SQLAlchemy**: ORM (Object-Relational Mapper) para interação com o banco de dados.
*   **SQLite**: Banco de dados padrão para desenvolvimento e testes (configurável para outros SGBDs como PostgreSQL).

## Configuração e Instalação

Para configurar e executar o projeto localmente, siga os passos abaixo:

1.  **Clone o repositório** (se aplicável, ou descompacte o arquivo fornecido).

2.  **Navegue até o diretório do projeto**:
    ```bash
    cd Sistema_doacao-main
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
    *Certifique-se de ter `pip` e `python3` instalados e configurados em seu ambiente.*

4.  **Configuração do Banco de Dados**:
    O projeto está configurado para usar SQLite por padrão. O arquivo `src/config/db_config.py` define a `DATABASE_URL`.
    Para usar SQLite, a configuração já está definida como:
    ```python
    DATABASE_URL = 'sqlite:///sistema_doacao.db'
    ```
    Se desejar usar outro banco de dados (e.g., PostgreSQL), você precisará alterar esta linha para a URL de conexão apropriada e instalar o driver correspondente (e.g., `psycopg2-binary` para PostgreSQL).

## Povoamento de Dados de Teste

Para popular o banco de dados com dados de exemplo e testar as funcionalidades, execute o script `itens_teste.py`:

1.  **Garanta que as tabelas foram criadas**: O script `itens_teste.py` irá criar as tabelas se elas não existirem. No entanto, você pode garantir a criação executando `main.py` uma vez, que chama `tb.criar_tabelas(db)`.

2.  **Execute o script de povoamento**:
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    python3 itens_teste.py
    ```
    Este script irá inserir dados de teste para usuários, itens, doações, pedidos de auxílio, distribuições, vagas de voluntariado e rastreios.

## Como Executar

Após a configuração e o povoamento (opcional), você pode executar a aplicação principal:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 main.py
```

*Nota: O `main.py` atual contém apenas a criação das tabelas e a inicialização dos repositórios, além de algumas instâncias de teste. Para uma aplicação completa, seria necessário adicionar a lógica de interface (CLI, Web, etc.) e a interação com os repositórios.* 

