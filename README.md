# Pipeline ETL — Tabela FIPE

Pipeline ETL completo em Python que extrai dados reais de veículos
da API FIPE, transforma e carrega em banco de dados PostgreSQL para análise.

---

## Stack

- Python 3.11+
- Pandas
- Requests
- Regex
- Docker + Docker Compose
- PostgreSQL 15
- Apache Airflow (próximo projeto)

---

## Status do projeto

- [x] Extract — 4 endpoints da API FIPE
- [x] Extract — coletar_dados() com loop para múltiplos veículos
- [x] Transform — 8 funções de limpeza e extração de features
- [x] Notebooks — análise exploratória e transformações
- [x] Docker — 3 containers com rede interna e healthcheck
- [x] Modelagem — 3 tabelas dimensionais criadas no PostgreSQL
- [x] Load — 410 registros inseridos via container Python
- [x] Main — pipeline completo orquestrado
- [x] Análises — SQL e Pandas com dados reais do banco
- [ ] Airflow — próximo projeto

---

## Resultado do pipeline

```
✅ dim_marca  →  10 registros
✅ dim_modelo → 200 registros
✅ fato_preco → 200 registros
```

---

## Análises implementadas

Análises realizadas no notebook `analise/analise_fipe.ipynb` conectado
diretamente ao banco PostgreSQL via container Jupyter.

Cada análise foi feita das duas formas — SQL via `pd.read_sql` e Pandas puro:

| # | Análise | Técnica |
|---|---------|---------|
| 1 | Média de preço por marca | JOIN + GROUP BY + AVG |
| 2 | Total de veículos por tipo | GROUP BY + COUNT |
| 3 | 5 modelos mais caros | JOIN + ORDER BY + LIMIT |
| 4 | 5 modelos mais baratos | JOIN + ORDER BY + LIMIT |
| 5 | Variação de preço por marca | MAX - MIN |
| 6 | Câmbio automático vs manual | GROUP BY + AVG |
| 7 | Top 3 marcas com mais modelos 4x4 | WHERE + GROUP BY + COUNT |
| 8 | Modelos com preço acima de R$ 200.000 | WHERE + JOIN |
| 9 | Modelo mais caro, mais barato e média por marca | GROUP BY + MAX + MIN + AVG |
| 10 | Combustíveis com mais de 30 modelos | GROUP BY + HAVING |

---

## Funções Extract

- buscar_marcas()     → lista de marcas por tipo de veículo
- buscar_modelos()    → modelos de uma marca
- buscar_ano()        → anos disponíveis de um modelo
- buscar_preco()      → preço FIPE de um veículo
- coletar_dados()     → loop completo: marcas → modelos → anos → preço

---

## Transformações implementadas

- limpar_valor()       → "R$ 62.099,00" → 62099.0
- limpar_marca()       → "VW - VolksWagen" → prefixo + marca
- limpar_data()        → "julho de 2026" → mes_nome + ano_referencia
- extrair_modelo()     → "AMAROK CD2.0..." → "AMAROK"
- extrair_tracao()     → "...4x2..." → "4x2"
- extrair_cambio()     → "...Aut..." → "Automatico" / "Manual"
- extrair_cilindrada() → "...2.0..." → "2.0"
- renomear_colunas()   → padroniza nomes e reorganiza colunas

---

## Modelagem Dimensional

```
dim_marca
├── id_marca (PK)
├── prefixo
└── marca

dim_modelo
├── id_modelo (PK)
├── id_marca (FK → dim_marca)
├── codigo_fipe
├── modelo
├── tipo_veiculo
├── cilindrada
├── tracao
├── cambio
└── combustivel

fato_preco
├── id_preco (PK)
├── id_modelo (FK → dim_modelo)
├── ano_modelo
├── valor
├── mes_nome
└── ano_referencia
```

---

## Arquitetura Docker

O projeto usa três containers orquestrados via Docker Compose:

```
docker-compose up -d
        ↓
┌──────────────────────────────────────────┐
│           rede interna Docker             │
│                                          │
│  fipe-db (PostgreSQL 15)                 │
│  → healthcheck garante disponibilidade   │
│          ↓                               │
│  fipe-app (Python 3.11)                  │
│  → roda main.py automaticamente          │
│  → insere 410 registros no banco         │
│          ↓                               │
│  fipe-jupyter (Jupyter Notebook)         │
│  → análises SQL e Pandas                 │
│  → acesso via localhost:8888             │
└──────────────────────────────────────────┘
```

As credenciais ficam no arquivo `.env` — nunca commitado no GitHub.

---

## Como rodar o pipeline

### 1. Configura o `.env`
```bash
cp .env.example .env
# edita o .env com suas credenciais
```

### 2. Sobe os containers
```bash
docker-compose up -d
```

### 3. Cria as tabelas no banco
```bash
# Windows PowerShell
Get-Content SQL\fipe_db.sql | docker exec -i fipe-db psql -U postgres -d fipe

# Linux / Mac
docker exec -i fipe-db psql -U postgres -d fipe < SQL/fipe_db.sql
```

### 4. Reinicia o pipeline se necessário
```bash
docker exec -it fipe-db psql -U postgres -d fipe -c "TRUNCATE fato_preco, dim_modelo, dim_marca RESTART IDENTITY CASCADE;"
docker restart fipe-app
docker logs fipe-app
```

### 5. Acessa o Jupyter para análises
```
http://localhost:8888
```

---

## Estrutura

```
pipeline-etl-fipe/
├── analise/
│   └── analise_fipe.ipynb
├── extract/
│   ├── api.py
│   └── dados_fipe.py
├── transform/
│   └── transformar.py
├── load/
│   └── carregar.py
├── SQL/
│   └── fipe_db.sql
├── notebooks/
│   └── analise.ipynb
├── docker-compose.yml
├── .env.example
├── main.py
└── README.md
```

---

## API utilizada

Base URL: `https://parallelum.com.br/fipe/api/v1`

| Endpoint | Descrição |
|---|---|
| `/carros/marcas` | Lista todas as marcas |
| `/carros/marcas/{id}/modelos` | Modelos de uma marca |
| `/carros/marcas/{id}/modelos/{id}/anos` | Anos disponíveis |
| `/carros/marcas/{id}/modelos/{id}/anos/{id}` | Preço FIPE |

---

*Projeto desenvolvido como parte do portfólio de Engenharia de Dados — 2026*
*github.com/Maniezzi12345*
