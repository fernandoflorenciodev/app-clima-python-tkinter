import requests
from datetime import datetime, timezone, timedelta
import json 
import pytz
import pycountry_convert as pc

traducao_paises = {
    "Brazil": "Brasil",
    "China": "China",
    "United States": "Estados Unidos",
    "Japan": "Japão",
    "Mexico": "México"
}

traducao_continentes = {
    "South America": "América do Sul",
    "North America": "América do Norte",
    "Asia": "Ásia",
    "Europe": "Europa",
    "Africa": "África",
    "Oceania": "Oceania"
}




chave = '351f1a857211b16d74a0f5b7ec4b2248'
cidade = 'São Paulo'
api_link = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang=pt_br'.format(cidade, chave)

# Fazendo chamada de API usando requests
r = requests.get(api_link)

# Convertendo os dados presentes na variável r em dicionário 
dados = r.json()
print(dados)

# Obtendo país, horas e região 
pais_codigo = dados['sys']['country']

# ---- País ----
pais = pytz.country_names[pais_codigo]
pais = traducao_paises.get(pais, pais)

# ---- Data ----

timezone_segundos = dados['timezone']

fuso = timezone(timedelta(seconds=timezone_segundos))

regiao_horas = datetime.now(fuso)
regiao_horas = regiao_horas.strftime("%d %m %Y │ %H:%M:%S")

# ---- Tempo ----
tempo = dados['main']['temp']
pressao = dados['main']['pressure']
umidade = dados['main']['humidity']
velocidade = dados['wind']['speed'] * 3.6
velocidade = round(velocidade, 1)
descricao = dados['weather'][0]['description']

# Mudando Informações

def pais_para_continente(i):
    pais_alpha = pc.country_name_to_country_alpha2(i)
    pais_continent_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
    pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continent_codigo)

    return  pais_continente_nome

continente = pais_para_continente(pais)
continente = traducao_continentes.get(continente, continente)




