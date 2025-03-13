import sqlite3 as db
import datetime
import os

def inicializar_banco():
    conexao = db.connect("produtos.db")
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            variacao REAL NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)
    
    conexao.commit()
    
    if os.path.exists('produtos.db'):
        print("Banco de dados 'produtos.db' criado com sucesso!")
    else:
        print("Falha ao criar o banco de dados.")
    
    return conexao, cursor

def calcular_variacao(cursor, nome, preco_atual):
    cursor.execute("SELECT preco FROM produtos WHERE nome = ? ORDER BY id DESC LIMIT 1", (nome,))
    ultimo_registro = cursor.fetchone()
    
    if ultimo_registro:
        ultimo_preco = ultimo_registro[0]
        variacao = preco_atual - ultimo_preco
        print(f"Variação calculada: {variacao}")
        return variacao
    print("Nenhum registro anterior encontrado. Variação: 0.0")
    return 0.0

def adicionar_produto(conexao, cursor, nome, preco):
    print(f"Adicionando produto: {nome} | Preço: {preco}")
    
    data_hora_atual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    variacao = calcular_variacao(cursor, nome, preco)
    
    cursor.execute("""
        INSERT INTO produtos (nome, preco, variacao, data_hora)
        VALUES (?, ?, ?, ?)
    """, (nome, preco, variacao, data_hora_atual))
    
    conexao.commit()  # Confirma a inserção no banco
    cursor.execute("SELECT last_insert_rowid()")  # Obtém o ID do último item inserido
    id_ultimo_produto = cursor.fetchone()[0]
    print(f"Produto inserido com ID: {id_ultimo_produto}")

def exibir_produtos(cursor):
    cursor.execute("SELECT nome, preco, variacao, data_hora FROM produtos")
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"Nome: {produto[0]} | Preço: R${produto[1]:.2f} | Variação: R${produto[2]:.2f} | Data e Hora: {produto[3]}")

if __name__ == "__main__":
    conexao, cursor = inicializar_banco()   
    adicionar_produto(conexao, cursor) 
    conexao.close()
