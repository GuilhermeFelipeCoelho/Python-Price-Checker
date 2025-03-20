import re
from db import Gerarlog


def LogErro(conexao, cursor, L):
    try:
        # Expressão regular para encontrar a URL no erro
        url_match = re.search(r"https?://[^\s]+", L)
        url = url_match.group(0) if url_match else "URL não encontrada"

        # Substituir a mensagem sem perder a URL
        if "404 Client Error" in L:
            L = f"Página não encontrada: {url}"

        if "Invalid URL" in L:
            L = f"URL inválida: {url}"

        if "Timeout" in L:
            L = f"Timeout - Por favor, tente novamente mais tarde"

        if "ConnectionError" in L:
            L = f"Erro de conexão - Por favor, tente novamente mais tarde"

        # Gerar log com a mensagem modificada
        Gerarlog(conexao, cursor, L)
        return
    
    except Exception as e:
        return {"Erro ao Gerar Log de dados:": str(e)}
