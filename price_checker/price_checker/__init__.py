import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

def extrair_data():
    data = datetime.now().strftime('%d-%m-%Y')
    hora = datetime.now().strftime('%H:%M:%S')
    return data, hora

def extrair_dados_magalu(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, 'html.parser')

        preco_elemento = soup.find('p', {'data-testid': 'price-value'}) 
        nome_elemento = soup.find('h1', {'data-testid': 'heading-product-title'})
        preco = preco_elemento.get_text(strip=True) if preco_elemento else "Preço indisponível"
        nome_produto = nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível"
        data, hora = extrair_data()

        return {
            'nome': nome_produto,
            'preco': preco,
            'data': data,
            'hora': hora
        }
    except Exception as e:
        return {'erro': str(e)}

# url = "https://www.magazineluiza.com.br/kit-composto-lacteo-milnutri-profutura-original-800g-2-unidades/p/229864500/me/cptl/"
# url = "https://www.magazineluiza.com.br/bebida-lactea-uht-com-15g-de-proteinas-yopro-morango-sem-lactose-zero-acucar-250ml/p/234133400/me/bebp/"
url = ""
dados = extrair_dados_magalu(url)
print(dados)
