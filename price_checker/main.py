import pandas as pd
from db import adicionar_produto, inicializar_banco
from ui import ui_c
from scraping import extrair_dados_magalu
import time

class Main:
    def __init__(self):
        self.path = None
        self.app = ui_c(self.request)
        self.conexao, self.cursor = inicializar_banco()

    def request(self):
        try:
            self.path = self.app.locale_path()
            if self.path:
                df = pd.read_excel(self.path, engine='openpyxl')
                link = df['LINK'].dropna()
                resultados = []
                total_links = len(link)
                sucesso = 0  # Para contar o número de links com sucesso
                
                # Itera sobre todos os links
                for idx, url in enumerate(link, start=1):
                    print(f"Extraindo dados do link {idx}/{total_links}: {url}")
                    
                    try:
                        dados = extrair_dados_magalu(url)
                        
                        if "Erro ao extrair dados:" in dados:
                            print(f"Erro ao extrair dados do link {url}: {dados['Erro ao extrair dados:']}")
                            continue  # Continua para o próximo link se houver erro
                        
                        # Inserir os dados no banco de dados
                        adicionar_produto(self.conexao, self.cursor, dados['nome'], dados['preco'])
                        resultados.append(dados)
                        sucesso += 1
                        print(f"Dados do link {idx}/{total_links} inseridos com sucesso.")
                    
                    except Exception as e:
                        print(f"Erro ao processar o link {url}: {str(e)}")
                        continue  # Caso ocorra qualquer outro erro, continua para o próximo link
                    
                    # Pausa para evitar problemas com rate limit
                    time.sleep(1)  # Ajuste o tempo de espera conforme necessário
                
                print(f"\nProcessamento concluído. {sucesso}/{total_links} links processados com sucesso.")
                return resultados
            else:
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
