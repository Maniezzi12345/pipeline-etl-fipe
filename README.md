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
- Apache Airflow (em breve)

---

## Status do projeto

- [x] Extract — 4 endpoints da API FIPE
- [x] Extract — coletar_dados() com loop para múltiplos veículos
- [x] Transform — limpeza e extração de features
- [x] Notebooks — análise exploratória e transformações
- [x] Docker — PostgreSQL containerizado com Docker Compose
- [x] Modelagem — 3 tabelas dimensionais criadas no PostgreSQL
- [ ] Load — inserir dados nas tabelas
- [ ] Main — pipeline completo orquestrado
- [ ] Airflow — DAG agendada

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

Arquitetura dimensional com 3 tabelas no PostgreSQL:

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

## Como rodar

### 1. Sobe o banco
```bash
docker-compose up -d
```

### 2. Cria as tabelas
```bash
Get-Content SQL\fipe_db.sql | docker exec -i fipe-db psql -U admin -d fipe
```

### 3. Instala dependências
```bash
pip install requests pandas psycopg2-binary
```

### 4. Roda o pipeline
```bash
python main.py
```

---

## Estrutura

```
pipeline-etl-fipe/
├── extract/
│   └── api.py
├── transform/
│   └── transformar.py
├── load/
│   └── carregar.py
├── SQL/
│   └── fipe_db.sql
├── notebooks/
│   └── analise.ipynb
├── docker-compose.yml
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