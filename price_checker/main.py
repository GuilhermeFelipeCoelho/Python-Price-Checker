import pandas as pd
from db import adicionar_produto, inicializar_banco
from LogErro import LogErro
from ui import ui_c
from scraping import extrair_dados_magalu
import time

class Main:
    def __init__(self):
        self.path = None
        self.conexao, self.cursor = inicializar_banco()
        self.app = ui_c(self.conexao,self.cursor,self.request)
        

    def request(self):
        try:
            self.path = self.app.locale_path()
            if self.path:
                df = pd.read_excel(self.path, engine="openpyxl")
                link = df["LINK"].dropna()
                resultados = []
                total_links = len(link)
                sucesso = 0
                for idx, url in enumerate(link, start=1):
                    print(f"Extraindo dados do link {idx}/{total_links}: {url}")
                    try:
                        dados = extrair_dados_magalu(self, url)
                        if "Erro ao extrair dados:" in dados:
                            L = f"Erro ao extrair dados do link: {dados['Erro ao extrair dados:']}"
                            LogErro(self.conexao, self.cursor, L)
                            continue

                        adicionar_produto(self.conexao, self.cursor, dados["nome"], dados["preco"])
                        resultados.append(dados)
                        sucesso += 1
                        print(f"Dados do link {idx}/{total_links} inseridos com sucesso.")

                    except Exception as e:
                        L = f"Erro ao processar o link {url}: {str(e)}"
                        LogErro(self.conexao, self.cursor, L)
                        continue

                    time.sleep(1)

                print(f"\nProcessamento concluído. {sucesso}/{total_links} links processados com sucesso.")
                return
            else:
                return "Nenhum arquivo selecionado."

        except Exception as e:
            print(f"Erro geral no processamento: {str(e)}")
            LogErro(self.conexao, self.cursor, e)
            return {"Erro": str(e)}

    def start(self):
        self.app.inicializar_ui()

def path_get(self):
    self.path = self.app.locale_path()

if __name__ == "__main__":
    main_app = Main()
    main_app.start()
