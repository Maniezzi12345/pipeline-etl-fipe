import psycopg2
import pandas as pd 
from sqlalchemy import create_engine

def criar_engine():
    engine = create_engine(
        "postgresql+psycopg2://admin:admin123@localhost:5432/fipe"
    )
    return engine

def salvar_dataframe(df,tabela,engine):
    df.to_sql(
        name=tabela,
        con=engine,
        df_exists="append",
        Index=False
    )

print(f"{len(df)} registros inseridos em {tabela}")