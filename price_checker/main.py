import pandas as pd
from db import adicionar_produto, inicializar_banco
from ui import ui_c
from scraping import extrair_dados_magalu

class Main:
    def __init__(self):
        self.path = None
        self.app = ui_c(self.request)
        self.conexao, self.cursor = inicializar_banco()

    def request(self):
        try:
            self.path = self.app.locale_path()
            if self.path:
                df = pd.read_excel(self.path)
                link = df['LINK']
                resultados = []
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

    def close_db(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")
    
    def start(self):
        self.app.inicializar_ui()
        self.close_db() # Fechar a conexão quando a interface for fechada

    def path_get(self):
        self.path = self.app.locale_path()
    
if __name__ == "__main__":
    main_app = Main()
    main_app.start()