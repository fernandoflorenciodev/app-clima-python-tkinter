import tkinter 
from tkinter import *
from tkinter import ttk

# Importando
import requests
from datetime import datetime, timezone, timedelta
import json 
import pytz
import pycountry_convert as pc

# Importando Pillow
from PIL import Image, ImageTk


# Cores
cor0 = "#444466" # Preto
cor1 = "#feffff" # Branco
cor2 = "#6f9fbd" # Azul

fundo_dia = "#57b2f2" 
fundo_noite = "#1a1333"
fundo_tarde = "#ff9e57"
fundo = fundo_dia

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


janela = Tk()
janela.title('')
janela.geometry('320x350')
janela.configure(bg=fundo)
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

# Criando os frames
frame_top = Frame(janela, width=320, height=50, bg=cor1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use('clam')

global imagem

# Função retornando informações
def informação():
    
    chave = '351f1a857211b16d74a0f5b7ec4b2248'
    cidade = e_local.get()
    api_link = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang=pt_br'.format(cidade, chave)

    # Fazendo chamada de API usando requests
    r = requests.get(api_link)

    # Convertendo os dados presentes na variável r em dicionário 
    dados = r.json()
    print(dados)

    # Obtendo país, horas e região 
    pais_codigo = dados['sys']['country']

    # ---- País ----
    pais_original = pytz.country_names[pais_codigo]

    # ---- Data ----

    timezone_segundos = dados['timezone']

    fuso = timezone(timedelta(seconds=timezone_segundos))

    regiao_horas = datetime.now(fuso)
    regiao_horas = regiao_horas.strftime("%d/%m/%Y │ %H:%M:%S")

    # ---- Tempo ----
    tempo = dados['main']['temp']
    pressao = dados['main']['pressure']
    umidade = dados['main']['humidity']
    velocidade = dados['wind']['speed']
    descricao = dados['weather'][0]['description']

    # Mudando Informações

    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continent_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continent_codigo)

        return  pais_continente_nome

    continente = pais_para_continente(pais_original)
    continente = traducao_continentes.get(continente, continente)

    pais = traducao_paises.get(pais_original, pais_original)

    # Passando Informações nas Labels

    l_cidade['text'] = cidade + " - " + pais + " │ " + continente
    l_data['text'] = regiao_horas
    l_umidade['text'] = umidade 
    l_u_simbol['text'] = '%'
    l_u_nome['text'] = 'Umidade'
    l_pressao['text'] = "Pressao : "+str(pressao)
    l_velocidade['text'] = "Velocidade do vento : "+str(velocidade)+" km/h "
    l_descricao['text'] = descricao
    l_temperatura['text'] = str(round(tempo)) + "°C"


    # Troca de Fundo

    regiao_periodo = datetime.now(fuso)
    regiao_periodo = regiao_periodo.strftime("%H")

    global imagem

    regiao_periodo = int(regiao_periodo)

    if regiao_periodo <= 5: 
        imagem = Image.open('imagens.clima/lua2.png')
        novo_fundo = fundo_noite
    elif regiao_periodo <= 11:
        imagem = Image.open('imagens.clima/sol2.png')
        novo_fundo = fundo_dia
    elif regiao_periodo <= 17:
        imagem = Image.open('imagens.clima/tarde2.png')
        novo_fundo = fundo_tarde
    elif regiao_periodo <= 23:
        imagem = Image.open('imagens.clima/lua2.png')
        novo_fundo = fundo_noite
    else:
        pass
    

        
    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_corpo, image=imagem, bg=novo_fundo)
    l_icon.place(x=175, y=65)

    # Passando Informações nas Labels

    janela.configure(bg=novo_fundo)
    frame_top.configure(bg=novo_fundo)
    frame_corpo.configure(bg=novo_fundo)

    l_cidade['bg'] = novo_fundo
    l_data['bg'] = novo_fundo
    l_umidade['bg'] = novo_fundo
    l_u_simbol['bg'] = novo_fundo
    l_u_nome['bg'] = novo_fundo
    l_pressao['bg'] = novo_fundo
    l_velocidade['bg'] = novo_fundo
    l_descricao['bg'] = novo_fundo
    l_temperatura['bg'] = novo_fundo



# Configurando Frame Top
e_local = Entry(frame_top, width=20, justify='left', font=("", 14), highlightthickness=1, relief='solid')
e_local.place(x=15, y=10)
b_ver = Button(frame_top,command=informação, text='Ver Clima', bg=cor1, fg=cor2, font=("Ivy 9 bold"), relief='raised', overrelief=RIDGE)
b_ver.place(x=250, y=10)

# Configurando Frame Corpo
l_cidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 14"), wraplength=300, justify='center')
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 10"))
l_data.place(x=10, y=54)

l_umidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 45 underline"))
l_umidade.place(x=10, y=100)

l_u_simbol = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 15 bold"))
l_u_simbol.place(x=85, y=110)

l_u_nome = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 10"))
l_u_nome.place(x=85, y=140)

l_pressao = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 10"))
l_pressao.place(x=10, y=184)

l_velocidade = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 10"))
l_velocidade.place(x=10, y=212)

l_descricao = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 10 bold"))
l_descricao.place(x=205, y=200)

l_temperatura = Label(frame_corpo, text='', anchor='center', bg=fundo, fg=cor1, font=("Arial 18 bold underline"))
l_temperatura.place(x=250, y=245)



janela.mainloop()