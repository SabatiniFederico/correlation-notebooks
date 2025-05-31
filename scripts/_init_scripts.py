# scripts/_init_scripts.py
# debe ser importado al inicio de cada notebook para configurar el entorno

import sys as sys
import os as os
import yfinance as yf
import pandas as pd
from datetime import datetime

print("Importes inicializado.")

def find_correlation_root():
    path = os.getcwd()
    while True:
        if "correlation-notebooks" in os.listdir(path):
            return os.path.join(path, "correlation-notebooks")
        parent = os.path.dirname(path)
        if parent == path:
            raise Exception("No se encontró la carpeta correlation-notebooks en los padres.")
        path = parent

PROJECT_ROOT = find_correlation_root()

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

print(f"Project root es: {PROJECT_ROOT}")

# Ahora imports
from utils.tests.backtesting import *
from utils.indicators.ta_generic_indicators import *
from utils.constants.stock_symbols import SYMBOL_GROUPS_YAHOO, START_DATE_2000, YAHOO_1D_DIR

print("Entorno inicializado.")