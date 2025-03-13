import datetime
from bs4 import BeautifulSoup
import requests

def extrair_dados_magalu(url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            soup = BeautifulSoup(response.content, 'html.parser')
            

            preco_elemento = soup.find('p', {'data-testid': 'price-value'}) 
            nome_elemento = soup.find('h1', {'data-testid': 'heading-product-title'})
                
            if preco_elemento:
                preco_span = preco_elemento.find('span')
                if preco_span:
                    preco1 = preco_span.get_text(strip=True)
                else:
                    preco1 = "Preço indisponível"
            else:
                preco1 = "Preço indisponível"

            preco = preco1.replace("\xa0", " ") if preco1 != "Preço indisponível" else preco1
            nome_produto = nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível"
            data, hora = extrair_data()

            preco1 = preco_elemento.get_text(strip=True) if preco_elemento else "Preço indisponível"
            preco = preco1.replace("\xa0", " ") if preco1 != "Preço indisponível" else preco1
            nome_produto = nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível"
            data, hora = extrair_data()
            print(f"Dados extraídos com sucesso: {preco_elemento}")
            print(f"Dados extraídos com sucesso: {nome_elemento}")
            return {
                'nome': nome_produto,
                'preco': preco,
                'data': data,
                'hora': hora
            }
    
        except Exception as e:
            return {"Erro ao extrair dados:": str(e)}
        
def extrair_data():
    data = datetime.datetime.now().strftime('%d-%m-%Y')
    hora = datetime.datetime.now().strftime('%H:%M:%S')
    return data, hora