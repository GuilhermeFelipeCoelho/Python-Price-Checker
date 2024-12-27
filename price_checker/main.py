import pandas as pd
from db import inicializar_banco
from ui import ui_c

class PriceChecker:
    inicializar_banco()

if __name__ == "__main__":
    app = ui_c()
    app.inicializar_ui()
