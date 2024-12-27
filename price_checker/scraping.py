import datetime
from bs4 import BeautifulSoup
import requests

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
            preco1 = preco_elemento.get_text(strip=True) if preco_elemento else "Preço indisponível"
            preco = preco1.replace("\xa0", " ") if preco1 != "Preço indisponível" else preco1
            nome_produto = nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível"
            data, hora = extrair_data()
            
            def extrair_data():
                data = datetime.now().strftime('%d-%m-%Y')
                hora = datetime.now().strftime('%H:%M:%S')
                return data, hora

            return {
                'nome': nome_produto,
                'preco': preco,
                'data': data,
                'hora': hora
            }
    
        except Exception as e:
            return {"Erro ao extrair dados:": str(e)}