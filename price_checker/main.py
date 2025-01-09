import pandas as pd
from db import adicionar_produto, inicializar_banco, check_data, add_data
from ui import ui_c
from scraping import extrair_dados_magalu

class Main:
    def __init__(self):
        self.path = None
        self.app = ui_c(self.request)
        self.conexao, self.cursor = inicializar_banco(), check_data()

    def request(self):
        try:
            self.path = self.app.locale_path()
            if self.path:
                df = pd.read_excel(self.path)
                link = df['LINK']
                resultados = []
                add_data()
                for url in link:
                    print(f"Extraindo dados do link: {url}")
                    dados = extrair_dados_magalu(url)
                    if "Erro ao extrair dados:" not in dados:
                        adicionar_produto(self.conexao, self.cursor, dados['nome'], dados['preco'])
                        resultados.append(dados)
                    else:
                        resultados.append(dados)
                return resultados
            return "Nenhum arquivo selecionado."
        except Exception as e:
            return {"Erro": str(e)}

    def start(self):
        self.app.inicializar_ui()

def path_get(self):
    self.path = self.app.locale_path()

if __name__ == "__main__":
    main_app = Main()
    main_app.start()