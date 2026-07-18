import requests
import time

BASE_URL = "https://parallelum.com.br/fipe/api/v1"

def buscar_marcas(tipo_veiculo="carros"):
    url = f"{BASE_URL}/{tipo_veiculo}/marcas"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return []
    

def buscar_modelos(codigo_marca, tipo_veiculo="carros"):
    url = f"{BASE_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return []


def buscar_ano(codigo_marca, codigo_modelo, tipo_veiculo="carros"):
    url = f"{BASE_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return []


def buscar_preco(codigo_marca, codigo_modelo, codigo_ano, tipo_veiculo="carros"):
    url = f"{BASE_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro:{response.status_code}")
        return []


def coletar_dados(limite_marcas=20, limite_modelos=10, limite_anos=2):
    registros = []

    marcas = buscar_marcas()[:limite_marcas]

    for marca in marcas:
        modelos = buscar_modelos(marca["codigo"])

        for modelo in modelos["modelos"][:limite_modelos]:
            anos = buscar_ano(marca["codigo"], modelo["codigo"])

            for ano in anos[:limite_anos]:
                preco = buscar_preco(marca["codigo"], modelo["codigo"], ano["codigo"])
                registros.append(preco)
                time.sleep(0.5)

    return registros



resultado = coletar_dados()

# resultado = buscar_marcas()
# print("Resultado de buscar marcas:")
# print(resultado[:3])  

# resultado = buscar_modelos(59)  
# print("Resultado de buscar modelos:")
# print(resultado["modelos"][:3])


# print("Resultado de buscar ano:")
# resultado = buscar_ano(59, 5585)
# print(resultado[:3])

# print("Resultado codigo ano:")
# resultado = buscar_preco(59, 5585, "2011-3")
# print(resultado)