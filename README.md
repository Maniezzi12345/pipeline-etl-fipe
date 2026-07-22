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
- [x] Docker — dois containers com rede interna e healthcheck
- [x] Modelagem — 3 tabelas dimensionais criadas no PostgreSQL
- [x] Load — 410 registros inseridos via container Python
- [x] Main — pipeline completo orquestrado
- [ ] Airflow — DAG agendada

---

## Resultado do pipeline

```
✅ dim_marca  →  10 registros
✅ dim_modelo → 200 registros
✅ fato_preco → 200 registros
```

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

O projeto usa dois containers orquestrados via Docker Compose:

```
docker-compose up -d
        ↓
┌─────────────────────────────────────┐
│         rede interna Docker          │
│                                     │
│  fipe-db (PostgreSQL 15)            │
│  → aguarda healthcheck              │
│  → banco fipe pronto                │
│          ↑                          │
│          │ healthcheck OK           │
│          ↓                          │
│  fipe-app (Python 3.11)             │
│  → instala dependências             │
│  → roda main.py                     │
│  → conecta em fipe-db               │
│  → insere 410 registros             │
└─────────────────────────────────────┘
```

**fipe-db** — container do banco de dados
- Imagem: `postgres:15`
- Banco: `fipe`
- Healthcheck: verifica se aceita conexões antes de liberar o app

**fipe-app** — container do pipeline Python
- Imagem: `python:3.11`
- Monta a pasta do projeto como volume
- Só inicia após o `fipe-db` estar saudável (`condition: service_healthy`)
- Roda `main.py` automaticamente

Conectar Python do Windows ao PostgreSQL via TCP/IP causa problemas de
encoding. A solução foi rodar o Python dentro do Docker — os containers
se comunicam pela rede interna sem passar pelo Windows.

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

O `fipe-app` aguarda o banco ficar saudável (healthcheck) e roda
o pipeline automaticamente.

### 3. Cria as tabelas no banco
```bash
# Windows PowerShell
Get-Content SQL\fipe_db.sql | docker exec -i fipe-db psql -U postgres -d fipe

# Linux / Mac
docker exec -i fipe-db psql -U postgres -d fipe < SQL/fipe_db.sql
```

### 4. Reinicia o pipeline
```bash
docker restart fipe-app
```

### 5. Acompanha os logs
```bash
docker logs fipe-app
```

Output esperado:
```
Iniciando pipeline
Iniciando Transformação...
→ dim_marca:  10 registros
→ dim_modelo: 200 registros
→ fato_preco: 200 registros
Inserindo no banco...
✅ 10 registros inseridos em dim_marca
✅ 200 registros inseridos em dim_modelo
✅ 200 registros inseridos em fato_preco
```

### 6. Verifica os dados no banco
```bash
docker exec -it fipe-db psql -U postgres -d fipe -c "SELECT COUNT(*) FROM dim_marca;"
docker exec -it fipe-db psql -U postgres -d fipe -c "SELECT COUNT(*) FROM dim_modelo;"
docker exec -it fipe-db psql -U postgres -d fipe -c "SELECT COUNT(*) FROM fato_preco;"
```

---

## Estrutura

```
pipeline-etl-fipe/
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