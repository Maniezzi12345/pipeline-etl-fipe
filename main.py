import sys
sys.path.append("/app")

from extract.dados_fipe import dados_fipe
from transform.transformar import transformar
from load.carregar import salvar_dataframe

print("Iniciando pipeline")

print("Iniciando Transformação...")

df_marca,df_modelo,df_preco = transformar(dados_fipe)

print(f"→ dim_marca:  {len(df_marca)} registros")
print(f"→ dim_modelo: {len(df_modelo)} registros")
print(f"→ fato_preco: {len(df_preco)} registros")

print("Inserindo no banco...")

salvar_dataframe(df_marca, "dim_marca")
salvar_dataframe(df_modelo, "dim_modelo")
salvar_dataframe(df_preco, "fato_preco")