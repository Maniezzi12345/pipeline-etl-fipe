# Pipeline ETL — Tabela FIPE

Pipeline ETL completo em Python que extrai dados reais de veículos da API FIPE, transforma e carrega para análise.

## Stack
- Python 3.11+
- Pandas
- Requests
- Docker
- PostgreSQL
- Apache Airflow

## Status do projeto
- [x] Extract — 4 endpoints da API FIPE
- [ ] Transform — limpeza e features
- [ ] Load — PostgreSQL
- [ ] Orquestração — Airflow

## Como rodar
```bash
pip install requests pandas
python main.py
```

## Estrutura
```
pipeline-etl-fipe/
├── extract/
│   └── api.py
├── transform/
│   └── transformar.py
├── load/
│   └── carregar.py
├── notebooks/
│   └── analise.ipynb
├── main.py
└── README.md
```