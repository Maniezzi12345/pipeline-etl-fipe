import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def criar_conexao():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def salvar_dataframe(df, tabela):
    conn = criar_conexao()
    cursor = conn.cursor()

    colunas = ", ".join(df.columns)
    valores = ", ".join(["%s"] * len(df.columns))

    for _, row in df.iterrows():
        valores_linha = tuple(None if pd.isna(v) else v for v in row)
        cursor.execute(
            f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})",
            valores_linha
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(df)} registros inseridos em {tabela}")