import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
import sqlite3
import pandas as pd

class PriceChecker:

    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Preços")
        self.root.geometry("400x300")
        
        self.setup_gui()

    def setup_gui(self):
        # Label principal
        label_titulo = tk.Label(self.root, text="Analisador de Preços", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)

        self.selecionar_arquivo = tk.Button(self.root, text='Selecionar', )
        Tk().withdraw() # Isto torna oculto a janela principal
        filename = askopenfilename() # Isto te permite selecionar um arquivo
        print(filename) # printa o arquivo selecionado

        # Botão para Analisar
        self.analisar_button = tk.Button(self.root, text="Analisar Preço", command=self.extrair_dados_magalu)
        self.analisar_button.pack(pady=10)

        # Label para exibir resultado
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def extrair_dados_magalu(url):

        def extrair_data():
            data = datetime.now().strftime('%d-%m-%Y')
            hora = datetime.now().strftime('%H:%M:%S')
            return data, hora

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

            return {
                'nome': nome_produto,
                'preco': preco,
                'data': data,
                'hora': hora
            }
        except Exception as e:
            return {'erro': str(e)}

    # url = "https://www.magazineluiza.com.br/kit-composto-lacteo-milnutri-profutura-original-800g-2-unidades/p/229864500/me/cptl/"
    url = "https://www.magazineluiza.com.br/bebida-lactea-uht-com-15g-de-proteinas-yopro-morango-sem-lactose-zero-acucar-250ml/p/234133400/me/bebp/"

    dados = extrair_dados_magalu(url)
    print(dados)

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceChecker(root)
    root.mainloop()
