import datetime
import re
from bs4 import BeautifulSoup
import requests

from LogErro import LogErro
from db import inicializar_banco


class Scraping:
    def __init__(self):
        self.conexao, self.cursor = inicializar_banco()


def extrair_dados_magalu(self, url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        preco_elemento = soup.find("p", {"data-testid": "price-value"})
        nome_elemento = soup.find("h1", {"data-testid": "heading-product-title"})

        preco_texto = (
            preco_elemento.get_text(strip=True)
            if preco_elemento
            else "Preço indisponível"
        )
        nome_produto = (nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível")

        preco_texto = preco_texto.replace("ou ", "").strip()

        preco_match = re.search(r"(\d+,\d{2})", preco_texto)
        preco = preco_match.group(1) if preco_match else "Preço indisponível"

        data, hora = extrair_data()

        return {"nome": nome_produto, "preco": preco, "data": data, "hora": hora}

    except Exception as e:
        LogErro(self.conexao, self.cursor, e)
        return {"Erro ao extrair dados:": str(e)}

def extrair_data():
    data = datetime.datetime.now().strftime("%d-%m-%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    return data, hora
