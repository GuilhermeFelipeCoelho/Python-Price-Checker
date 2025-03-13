import sqlite3 as db
import datetime

def inicializar_banco():
    conexao = db.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            preco REAL,
            variacao REAL,
            data_hora_lastcall TEXT
        )
    """)
    conexao.commit()
    return conexao, cursor

def calcular_variacao(cursor, nome, preco_atual):
    cursor.execute("SELECT preco FROM produtos WHERE nome = ? ORDER BY id DESC LIMIT 1", (nome,))
    ultimo_registro = cursor.fetchone()
    if ultimo_registro:
        ultimo_preco = ultimo_registro[0]
        return preco_atual - ultimo_preco
    return 0.0

def exibir_produtos(cursor):
    cursor.execute("SELECT nome, preco, variacao, data_hora_lastcall FROM produtos")
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"Nome: {produto[0]} | Preço: R${produto[1]:.2f} | Variação: R${produto[2]:.2f} | Data e Hora: {produto[4]}")

def adicionar_produto(conexao, cursor, nome, preco):
    data_hora_atual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    variacao = calcular_variacao(cursor, nome, preco)
    cursor.execute("""
        INSERT INTO produtos (nome, preco, variacao, data_hora)
        VALUES (?, ?, ?, ?)
    """, (nome, preco, variacao, data_hora_atual))
    conexao.commit()
    print(f"Produto '{nome}' adicionado com sucesso!")

if __name__ == "__main__":
    conexao, cursor = inicializar_banco()
    