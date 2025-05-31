# notebooks/_init_notebook.py
# debe ser importado al inicio de cada notebook para configurar el entorno


import sys
import os as os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import yfinance as yf

import ta  # technical analysis indicators
from ta.trend import MACD
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

# Modelos de machine learning
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils.validation import check_array
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from itertools import product
# Modelos avanzados
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso

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