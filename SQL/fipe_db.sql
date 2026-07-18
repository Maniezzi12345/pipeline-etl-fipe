-- Modelagem Dimensional — Pipeline ETL FIPE

CREATE TABLE IF NOT EXISTS dim_marca (
    id_marca  SERIAL PRIMARY KEY,
    prefixo   VARCHAR(20),
    marca     VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_modelo (
    id_modelo    SERIAL PRIMARY KEY,
    id_marca     INT REFERENCES dim_marca(id_marca),
    codigo_fipe  VARCHAR(20),
    modelo       VARCHAR(100),
    tipo_veiculo VARCHAR(20),
    cilindrada   VARCHAR(10),
    tracao       VARCHAR(10),
    cambio       VARCHAR(20),
    combustivel  VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS fato_preco (
    id_preco       SERIAL PRIMARY KEY,
    id_modelo      INT REFERENCES dim_modelo(id_modelo),
    ano_modelo     INT,
    valor          DECIMAL(12,2),
    mes_nome       VARCHAR(20),
    ano_referencia INT
);