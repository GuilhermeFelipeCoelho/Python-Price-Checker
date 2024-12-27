import tkinter as tk
from tkinter.filedialog import askopenfilename

class ui_c:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Análise de Preços")
        self.root.geometry("400x300")
        
        self.setup_gui(self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        

    def on_closing(self):
        # Salvar os dados por aqui (opção)
        print("Fechando a aplicação...")
        self.root.destroy()


    def setup_gui(self, root):
        label_titulo = tk.Label(self.root, text="Analisador de Preços", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)
        
        self.localizar_button = tk.Button(self.root, text = "Selecionar arquivo XLSX", command=self.locale_path)
        self.localizar_button.pack(pady=10)

        self.caminho_arquivo = tk.StringVar()
        self.label_caminho = tk.Label(self.root, textvariable=self.caminho_arquivo)
        self.label_caminho.pack()

        self.analisar_button = tk.Button(self.root, text="Analisar Preço", command=self.analisar_preco)
        self.analisar_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left", wraplength=380)
        self.result_label.pack(pady=10)

    def locale_path(self):
        tipos_arquivos = [("Arquivos CSV e Excel", "*.csv;*.xlsx")]
        filename = askopenfilename(title="Selecionar Arquivo",filetypes=tipos_arquivos)
        print(filename)
        if filename:
            self.caminho_arquivo.set(filename)
        return filename
    
    def analisar_preco(self):
        self.result_label.config(text="Concluido!")

    def inicializar_ui(self):
        self.root.mainloop()