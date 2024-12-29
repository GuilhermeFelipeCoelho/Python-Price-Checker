import pandas as pd
from db import inicializar_banco
from ui import ui_c
from scraping import extrair_dados_magalu

class Main:
    def __init__(self):
        self.path = None
        self.app = ui_c(self.request)

    inicializar_banco()

    def request(self):
        try:
            url = "https://www.magazineluiza.com.br/bebida-lactea-uht-com-15g-de-proteinas-yopro-chocolate-sem-lactose-zero-acucar-250ml/p/226969600/me/belc/"
            resultado = extrair_dados_magalu(url)
            print(resultado)
        except Exception as e:
            return {"Erro": str(e)}
    
    def get_data():
        get = pd.read_excel()

    def path_get(self):
        self.path = self.app.locale_path()


    def start(self):
        self.app.inicializar_ui()

if __name__ == "__main__":
    main_app = Main()
    main_app.start()
