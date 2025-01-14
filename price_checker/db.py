import sqlite3 as db
import datetime

def inicializar_banco():
    conexao = db.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id_prod INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            data_hora_lastcall TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id_prec INTEGER PRIMARY KEY,
            id_prod INTEGER,
            preco REAL NOT NULL,
            variacao REAL NOT NULL,
            data_hora_lastcall_nodia TEXT NOT NULL
        )
    """)

    #                       > BOTANDO ESSE DB PRA FUNCIONAR <

    # id_prec recebe o id relacionado com o dia que está sendo feita a call
    # id_prod recebe o id do produto recebida da tabela produtos
    # preco SEMPRE recebe o preco lido na lastcall
    # variacao é: R$ (o preco atual) - R$ (o ultimo preco lido)
    # data_hora_lastcall_nodia vai checar se no dia foi feita mais alguma call e 
    #  caso sim, ele vai sobrescrever, caso nao, ele vai apenas registrar
    
    # OBS: O id_prec SÓ SE ALTERA QUANDO O data_hora_lastcall_nodia SE ALTERAR
    # OBS: O id_prod DA TABELA registros RECEBE SEMPRE O id_prod DA TABELA produtos
    # OBS: A TABELA produtos VAI SEMPRE ATUALIZAR OS DADOS CONTIDOS NELA, PORÉM SÓ IRÁ
    #   ENVIAR OS NOVOS DADOS QUANDO A data_hora_lastcall TIVER O DIA DIFERENTE 
    #   DO QUE EM data_hora_lastcall_nodia
    # OBS: A TELA QUE SERA GERADA MAIS PRA FRENTE IRÁ EXIBIR SEPARADAMENTE OS PRODUTOS
    #   DOS REGISTROS 
    # OBS: FAZER UM BOTÃO PARA CONFIRMAR SE O USUÁRIO QUER REFAZER A LEITURA DO DIA 
    # OBS: FAZER UM SISTEMA DE SEGURANÇA PARA EVITAR QUE OS DADOS SEJAM SOBRESCRITOS CASO SITE
    #   CAIA, EVITANDO ASSIM ERROS DE REGISTROS INCONSISTENTES, SUPONDO QUE A PESSOA JA TENHA 
    #   OS DADOS DO DIA GRAVADOS E CLIQUE PARA FAZER UMA NOVA LEITURA E O SITE TENHA CAIDO, 
    #   EVITAR QUE ELA PERCA OS REGISTROS QUE JA ESTAVAM LA
    
    # PERGUNTA: OS DADOS DA NOVA LEITURA NO MESMO DIA DEVEM SER ATUALIZADAS NA 
    #   TABELA registros PARA QUE SEJA MANTIDO SEMPRE A ULTIMA LEITURA COMO A PERMANENTE?

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
    cursor.execute("SELECT nome, preco, variacao, data_hora FROM produtos")
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"Nome: {produto[0]} | Preço: R${produto[1]:.2f} | Variação: R${produto[2]:.2f} | Data e Hora: {produto[3]}")

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
    conexao.close()