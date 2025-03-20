import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db import obter_produtos, calcular_variacao_preco

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db import obter_produtos, calcular_variacao_preco

def tela_variacao_precos(root, conexao, cursor):
    var_window = tk.Toplevel(root)
    var_window.title("Calcular Variação de Preço")
    var_window.geometry("400x300")
    

    # Rótulo e ComboBox para seleção de produto
    tk.Label(var_window, text="Selecione o Produto:").pack(pady=5)
    produtos = obter_produtos(cursor)  # Busca os produtos no banco de dados
    produto_var = tk.StringVar()
    produto_combobox = ttk.Combobox(var_window, textvariable=produto_var, values=produtos, state="readonly")
    produto_combobox.pack(pady=5)

    # Seleção de intervalo de datas
    tk.Label(var_window, text="Data Inicial:").pack(pady=5)
    data_inicio = DateEntry(var_window, date_pattern="dd-mm-yyyy")
    data_inicio.pack()

    tk.Label(var_window, text="Data Final:").pack(pady=5)
    data_fim = DateEntry(var_window, date_pattern="dd-mm-yyyy")
    data_fim.pack()

    # Rótulo para exibir resultado
    resultado_label = tk.Label(var_window, text="")
    resultado_label.pack(pady=10)

    def calcular():
        produto_selecionado = produto_combobox.get()  # Pega o produto selecionado
        data_inicio_str = data_inicio.get()  # Obtém a data de início
        data_fim_str = data_fim.get()  # Obtém a data de fim

        # Chama a função para calcular a variação de preço
        variacao = calcular_variacao_preco(conexao, cursor, produto_selecionado, data_inicio_str, data_fim_str)

        # Verifique se o retorno é um número ou um erro
        if isinstance(variacao, str):  # Se for uma mensagem de erro
            resultado_label.config(text=variacao)
        else:  # Se for um valor numérico, mostre a variação
            try:
                resultado_label.config(text=f"Variação: {variacao:.2f}%")
            except Exception as e:
                resultado_label.config(text=f"Erro ao formatar a variação: {str(e)}")

    # Botão para calcular a variação
    calcular_btn = tk.Button(var_window, text="Calcular Variação", command=calcular)
    calcular_btn.pack(pady=10)
