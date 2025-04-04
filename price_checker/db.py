import sqlite3 as db
import datetime
import os

def inicializar_banco():
    conexao = db.connect("produtos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            preco REAL,
            variacao_preco TEXT,
            data_hora TEXT 
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log TEXT,
            data_hora TEXT 
        )
    """
    )
    
    conexao.commit()

    if os.path.exists("produtos.db"):
        print("Banco de dados 'produtos.db' criado com sucesso!")
    else:
        print("Falha ao criar o banco de dados.")

    return conexao, cursor

def calcular_variacao(cursor, nome, preco_atual):
    cursor.execute(
        "SELECT preco FROM produtos WHERE nome = ? ORDER BY id DESC LIMIT 1", (nome,)
    )
    ultimo_registro = cursor.fetchone()

    if ultimo_registro:
        ultimo_preco = float(str(ultimo_registro[0]).replace(',', '.'))  # Converte para float
        preco_atual = float(str(preco_atual).replace(',', '.'))  # Converte para float
        
        variacao = round(((preco_atual - ultimo_preco) / ultimo_preco) * 100, 2)
        return variacao
    return 0.0



def adicionar_produto(conexao, cursor, nome, preco):

    # Obtém a variação de preço antes da inserção
    variacao = calcular_variacao(cursor, nome, preco)

    data_hora_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO produtos (nome, preco, variacao_preco, data_hora)
        VALUES (?, ?, ?, ?)
        """,
        (nome, preco, variacao, data_hora_atual),
    )

    conexao.commit()
    cursor.execute("SELECT last_insert_rowid()")
    id_ultimo_produto = cursor.fetchone()[0]
    print(f"Produto inserido com ID: {id_ultimo_produto}")
    
def exibir_produtos(cursor):
    cursor.execute("SELECT nome, preco, variacao_preco, data_hora FROM produtos")
    produtos = cursor.fetchall()
    for produto in produtos:
        print(
            f"Nome: {produto[0]} | Preço: R${produto[1]:.2f} | Variação: R${produto[2]:.2f} | Data e Hora: {produto[3]}"
        )

def obter_produtos(cursor):
    cursor.execute("SELECT DISTINCT nome FROM Produtos")  # Ajuste conforme sua tabela
    return [row[0] for row in cursor.fetchall()]


def calcular_variacao_preco(conexao, cursor, produto, data_inicio, data_fim):
    try:
        # Converte as datas para o formato de data sem hora
        data_inicio = datetime.datetime.strptime(data_inicio, '%d-%m-%Y').strftime('%d-%m-%Y')
        data_fim = datetime.datetime.strptime(data_fim, '%d-%m-%Y').strftime('%d-%m-%Y')

        # Consulta no banco de dados, ignorando o horário
        query = """
            SELECT preco, data_hora FROM produtos
            WHERE nome = ? AND data_hora BETWEEN ? AND ?
            ORDER BY data_hora ASC
        """
        cursor.execute(query, (produto, data_inicio, data_fim))
        precos = cursor.fetchall()


        # Verifica se encontrou resultados
        if not precos:
            return "Nenhum dado encontrado para o produto no intervalo de datas."
        
        # Inicializa uma lista para armazenar as variações de preço
        variacoes = []

        # Percorre todos os preços e calcula as variações entre os valores consecutivos
        for i in range(1, len(precos)):
            preco_inicial = float(str(precos[i-1][0]).replace(',', '.'))  # Preço do item anterior
            preco_final = float(str(precos[i][0]).replace(',', '.'))     # Preço do item atual
            data_inicial = precos[i-1][1]  # Data do item anterior
            data_final = precos[i][1]     # Data do item atual

            # Calcula a variação percentual entre os dois preços consecutivos
            variacao = round(((preco_final - preco_inicial) / preco_inicial) * 100, 2)
            
            # Formata a variação como uma string
            variacao_formatada = f"Data: {data_inicial} -> {data_final} | Variação: {variacao}%"
            variacoes.append(variacao_formatada)


        # Se houver variações, retorna todas formatadas
        if variacoes:
            return "\n".join(variacoes)  # Junta as variações em uma única string para exibir todas

        # Caso não haja variações, retorna um valor informativo
        return "Nenhuma variação calculada."

    except Exception as e:
        return {"Erro ao calcular variação de preços": str(e)}

def Gerarlog(conexao, cursor, e):
    try:
        data_hora_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cursor.execute(
            "INSERT INTO Logs(log, data_hora) VALUES (?, ?)", (e, data_hora_atual)
        )
        conexao.commit()
    except Exception as erro:
        return "Erro ao Gerar LOG"


def obter_logs(cursor):
    try:

        cursor.execute("SELECT * FROM Logs ORDER BY data_hora DESC")
        logs = cursor.fetchall()

        logs_formatados = []
        for log in logs:
            if isinstance(log[2], datetime.datetime):
                data_hora_formatada = log[2].strftime("%d/%m/%Y %H:%M:%S")
            else:
                data_hora_formatada = log[2]

            logs_formatados.append(
                f"ID: {log[0]} - Mensagem: {log[1]} - Data: {data_hora_formatada}"
            )

        return logs_formatados

    except Exception as e:
        print(f"Erro ao obter logs: {e}")
        return []


if __name__ == "__main__":
    conexao, cursor = inicializar_banco()
    adicionar_produto(conexao, cursor)
    conexao.close()
