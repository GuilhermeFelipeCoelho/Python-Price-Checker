import tkinter as tk
from tkinter.filedialog import askopenfilename
from db import obter_logs, inicializar_banco
from Tela_calVariacao import tela_variacao_precos


class ui_c:
    def __init__(self,conexao, cursor, on_analyze_callback=None):
        self.root = tk.Tk()
        self.root.title("Análise de Preços")
        self.root.geometry("400x300")
        self.setup_gui(self.root)
        self.on_analyze_callback = on_analyze_callback
        self.conexao = conexao
        self.cursor = cursor

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Fechando a aplicação...")
        self.root.destroy()

    def setup_gui(self, root):
        label_titulo = tk.Label(self.root, text="Analisador de Preços", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)

        self.localizar_button = tk.Button(self.root, text="Selecionar arquivo XLSX", command=self.locale_path)
        self.localizar_button.pack(pady=10)

        self.caminho_arquivo = tk.StringVar()
        self.label_caminho = tk.Label(self.root, textvariable=self.caminho_arquivo)
        self.label_caminho.pack()

        self.analisar_button = tk.Button(self.root, text="Analisar Preço", command=self.analisar_preco)
        self.analisar_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left", wraplength=380)
        self.result_label.pack(pady=10)

        self.logs_button = tk.Button(self.root, text="Logs", command=self.telaLog)
        self.logs_button.pack(pady=5)
        botao_variacao = tk.Button(root, text="Calcular Variação de Preço", command=lambda: tela_variacao_precos(root, self.conexao, self.cursor))
        botao_variacao.pack(pady=10)

    def locale_path(self):
        tipos_arquivos = [("Arquivos CSV e Excel", "*.csv;*.xlsx")]
        filename = askopenfilename(title="Selecionar Arquivo", filetypes=tipos_arquivos)
        print(filename)
        if filename:
            self.caminho_arquivo.set(filename)
        return filename

    def analisar_preco(self):
        self.result_label.config(text="Analisando...")

        if self.on_analyze_callback:
            resultado = self.on_analyze_callback()

        if isinstance(resultado, dict):
            resultado_formatado = "Concluído com sucesso!"
            self.result_label.config(text=resultado_formatado)
        else:
            mensagem_erro = f"Erro detectado: {resultado}\nUm log foi gerado. Verifique os registros."
            self.result_label.config(text="Erro: Verifique os logs!")

    def telaLog(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Logs")
        log_window.geometry("600x400")

        logs = obter_logs(self.cursor)

        if logs:
            header_frame = tk.Frame(log_window)
            header_frame.pack(fill="x")

            tk.Label(header_frame, text="ID", width=10, anchor="w").grid(row=0, column=0)
            tk.Label(header_frame, text="Log", width=55, anchor="w").grid(row=0, column=1)
            tk.Label(header_frame, text="Data", width=20, anchor="w").grid(row=0, column=2)

            for i, log in enumerate(logs):
                log_frame = tk.Frame(log_window)
                log_frame.pack(fill="x", pady=2)

                log_parts = log.split(" - ")

                log_id = log_parts[0].replace("ID: ", "")
                log_message = log_parts[1].replace("Mensagem: ", "")
                log_data = log_parts[2].replace("Data: ", "")

                tk.Label(log_frame, text=log_id, width=10, anchor="w").grid(row=i, column=0)
                tk.Label(log_frame, text=log_message, width=55, anchor="w", wraplength=380).grid(row=i, column=1)
                tk.Label(log_frame, text=log_data, width=20, anchor="w").grid(row=i, column=2)

        else:
            tk.Label(log_window, text="Não há logs para exibir", font=("Arial", 12)).pack(pady=20)

    def inicializar_ui(self):
        self.root.mainloop()