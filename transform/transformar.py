import re
import sys
import pandas as pd

sys.path.append("..")

from extract.dados_fipe import dados_fipe


# ─────────────────────────────────────────
# FUNÇÕES DE TRANSFORMAÇÃO
# ─────────────────────────────────────────

def limpar_valor(valor_str):
    valor = valor_str.replace("R$ ", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    return float(valor)


def limpar_marca(marca_str):
    partes = marca_str.split(" - ")
    if len(partes) == 2:
        return {"prefixo": partes[0].strip(), "marca": partes[1].strip()}
    return {"prefixo": None, "marca": partes[0].strip()}


def limpar_data(mes_ref_str):
    partes = mes_ref_str.split()
    return {"mes_nome": partes[0].strip(), "ano_referencia": int(partes[2].strip())}


def extrair_modelo(modelo_str):
    return modelo_str.split()[0]


def extrair_tracao(modelo_str):
    resultado = re.search(r"4x\d", modelo_str)
    return resultado.group() if resultado else None


def extrair_cambio(modelo_str):
    return "Automatico" if re.search(r"Aut", modelo_str) else "Manual"


def extrair_cilindrada(modelo_str):
    resultado = re.search(r"\d+\.\d+", modelo_str)
    return resultado.group() if resultado else None


def mapear_tipo(tipo):
    mapa = {1: "carro", 2: "moto", 3: "caminhao"}
    return mapa.get(tipo, "desconhecido")


def renomear_colunas(df):
    df = df.rename(columns={
        "TipoVeiculo": "tipo_veiculo",
        "AnoModelo":   "ano_modelo",
        "CodigoFipe":  "codigo_fipe",
        "Tracao":      "tracao",
        "Valor":       "valor",
        "Combustivel": "combustivel"
    })
    return df[[
        "codigo_fipe", "tipo_veiculo", "modelo", "marca",
        "valor", "prefixo", "ano_modelo", "tracao",
        "cambio", "cilindrada", "combustivel", "ano_referencia"
    ]]


# ─────────────────────────────────────────
# PIPELINE DE TRANSFORMAÇÃO
# ─────────────────────────────────────────

def transformar(dados):
    df = pd.DataFrame(dados)

    # limpeza de colunas
    df["Valor"] = df["Valor"].apply(limpar_valor)

    marca_exp        = df["Marca"].apply(limpar_marca).apply(pd.Series)
    df["prefixo"]    = marca_exp["prefixo"]
    df["marca"]      = marca_exp["marca"]
    df               = df.drop(columns=["Marca"])

    data_exp             = df["MesReferencia"].apply(limpar_data).apply(pd.Series)
    df["mes_nome"]       = data_exp["mes_nome"]
    df["ano_referencia"] = data_exp["ano_referencia"]
    df                   = df.drop(columns=["MesReferencia"])

    df["modelo"]     = df["Modelo"].apply(extrair_modelo)
    df["Tracao"]     = df["Modelo"].apply(extrair_tracao)
    df["cambio"]     = df["Modelo"].apply(extrair_cambio)
    df["cilindrada"] = df["Modelo"].apply(extrair_cilindrada)
    df["TipoVeiculo"]= df["TipoVeiculo"].apply(mapear_tipo)
    df               = df.drop(columns=["Modelo", "SiglaCombustivel"])

    df = renomear_colunas(df)

    # separação em tabelas dimensionais
    df_marca = df[["prefixo", "marca"]].drop_duplicates().reset_index(drop=True)
    df_marca["id_marca"] = df_marca.index + 1

    df_modelo = df[["codigo_fipe", "modelo", "tipo_veiculo",
                    "cilindrada", "tracao", "cambio", "combustivel", "marca"]].drop_duplicates()
    df_modelo = df_modelo.merge(df_marca[["id_marca", "marca"]], on="marca")
    df_modelo = df_modelo.drop(columns=["marca"])
    df_modelo["id_modelo"] = df_modelo.index + 1

    df_preco = df[["codigo_fipe", "valor", "ano_referencia", "ano_modelo"]]
    df_preco = df_preco.merge(df_modelo[["id_modelo", "codigo_fipe"]], on="codigo_fipe")
    df_preco = df_preco.drop(columns=["codigo_fipe"])

    return df_marca, df_modelo, df_preco


# ─────────────────────────────────────────
# EXECUÇÃO DIRETA (teste)
# ─────────────────────────────────────────

if __name__ == "__main__":
    df_marca, df_modelo, df_preco = transformar(dados_fipe)
    print("dim_marca:", df_marca.shape)
    print("dim_modelo:", df_modelo.shape)
    print("fato_preco:", df_preco.shape)