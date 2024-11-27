import tkinter as tk
from tkinter import messagebox
import requests

def consulta_django():
    try:
        # Exemplo de requisição ao backend do Django
        response = requests.get("http://127.0.0.1:8000/api/exemplo/")
        if response.status_code == 200:
            dados = response.json()
            messagebox.showinfo("Resposta do Django", f"Dados recebidos: {dados}")
        else:
            messagebox.showerror("Erro", f"Erro na API: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao conectar ao servidor: {e}")

def iniciar_gui():
    # Criar a janela principal
    root = tk.Tk()
    root.title("Interface GUI com Tkinter")

    # Adicionar botões e elementos
    label = tk.Label(root, text="Bem-vindo à GUI integrada com Django!")
    label.pack(pady=10)

    botao = tk.Button(root, text="Consultar Backend", command=consulta_django)
    botao.pack(pady=10)

    # Executar o loop principal do Tkinter
    root.mainloop()
