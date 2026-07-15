# Pipeline ETL — Tabela FIPE

Pipeline ETL completo em Python que extrai dados reais de veículos 
da API FIPE, transforma e carrega para análise.

## Stack
- Python 3.11+
- Pandas
- Requests
- Regex
- Docker (em breve)
- PostgreSQL (em breve)
- Apache Airflow (em breve)

## Status do projeto
- [x] Extract — 4 endpoints da API FIPE
- [x] Transform — limpeza e extração de features
- [ ] Load — salvar CSV e PostgreSQL
- [ ] Main — pipeline completo orquestrado
- [ ] Airflow — DAG agendada

## Transformações implementadas
- limpar_valor()       → "R$ 62.099,00" → 62099.0
- limpar_marca()       → "VW - VolksWagen" → prefixo + marca
- limpar_data()        → "julho de 2026" → mes_nome + ano_referencia
- extrair_modelo()     → "AMAROK CD2.0..." → "AMAROK"
- extrair_tracao()     → "...4x2..." → "4x2"
- extrair_cambio()     → "...Aut..." → "Automatico" / "Manual"

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