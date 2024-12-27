import pandas as pd
from db import inicializar_banco
from ui import ui_c
from scraping import extrair_dados_magalu

class Main:
    def __init__(self):
        self.path = None
        self.app = ui_c()

    inicializar_banco()

    def analisar_preco(self):
        resultado = scrap
        print(resultado)
    

    def get_data():
        get = pd.read_excel()

    def path_get(self):
        self.path = self.app.locale_path()

if __name__ == "__main__":
    app = ui_c()
    app.inicializar_ui()

url = "https://www.magazineluiza.com.br/bebida-lactea-uht-com-15g-de-proteinas-yopro-chocolate-sem-lactose-zero-acucar-250ml/p/226969600/me/belc/"
scrap = extrair_dados_magalu(url)