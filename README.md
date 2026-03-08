# correlation-notebooks

Plataforma de research financiero, con datos de múltiples mercados y análisis estadístico para identificar patrones y relaciones predictivas.

Es un proyecto de juguete para hacer análisis de correlaciones y de estadística mayoritariamente, con setup configurado para trabajar con LLms en el futuro.
---

## Objetivo

El proyecto tiene tres ejes principales:

1. **Recolección de datos** — descarga y almacenamiento de datos OHLCV diarios de Yahoo Finance para ~70 instrumentos (cripto, stocks, commodities, bonds, forex, índices)
2. **Análisis de correlaciones** — correlaciones con distintos lags entre mercados para identificar relaciones predictivas (pearson, spearman, kendall)
3. **Research de dirección** — análisis estadístico y modelos predictivos para anticipar la dirección del precio en cripto (enfoque actual: BTC-USD)

---

## Estructura del proyecto

```
correlation-notebooks/
├── data/
│   └── yahoo_1d/              # Datos OHLCV diarios descargados de Yahoo Finance
│       ├── cripto/            # BTC-USD, ETH-USD, SOL-USD, XRP-USD, ADA-USD
│       ├── commodities/       # Oro, Plata, Crudo, Gas, Cobre, Trigo, Maíz, Soja
│       ├── indexes/           # S&P500, NASDAQ, DJI, VIX, DXY, Nikkei, FTSE, DAX, etc.
│       ├── bonds/             # Treasuries 5y, 10y, 30y, IRX
│       ├── forex/             # 15 pares: EURUSD, USDJPY, GBPUSD, AUDUSD, etc.
│       └── stocks/            # ~40 acciones large-cap (tech, finanzas, salud, energía, consumo)
│
├── notebooks/
│   ├── _init_notebook.py      # Inicializador: imports estándar + PROJECT_ROOT
│   ├── data_research/         # Análisis estadístico y exploratorio
│   │   ├── btc_direction_research.ipynb     # Frecuencia alcista de BTC vs N días atrás
│   │   ├── btc_monthly_seasonality.ipynb    # Estacionalidad mensual: abril, agosto, bull/bear
│   │   └── data_correlations.ipynb          # Correlaciones entre mercados con lags
│   └── ml_research/           # Modelos predictivos
│       └── btc_direction_predictor.ipynb    # Predictor de dirección BTC (ML)
│
├── scripts/
│   └── yahoo_1d_collector.ipynb  # Descarga datos de Yahoo Finance y los guarda en data/
│
├── utils/
│   ├── constants/
│   │   └── stock_symbols.py      # SYMBOL_GROUPS_YAHOO: todos los tickers organizados por categoría
│   ├── correlations/
│   │   ├── correlations.py               # Motor de correlaciones (pearson, spearman, kendall, mutual_info, distance_corr)
│   │   └── correlations_vectorized.py    # Versión optimizada — la que se usa en producción
│   ├── indicators/
│   │   └── ta_generic_indicators.py      # MACD, BB, RSI, EMA, ZScore, LogRet, Volatilidad
│   └── tests/
│       └── backtesting.py
│
└── results/                   # Outputs: CSVs de correlaciones, gráficos, curvas de equity
```

---

## Notebooks principales

### `btc_direction_research.ipynb`
Análisis estadístico base: ¿con qué frecuencia el precio de BTC está más alto que hace N días?
- Frecuencia alcista global y por año, mes, día de la semana
- Comparación entre distintos lags (1d, 3d, 7d, 14d, 30d)
- Análisis de rachas consecutivas (streaks)
- Evolución temporal rolling de la frecuencia

### `btc_monthly_seasonality.ipynb`
Análisis exhaustivo de estacionalidad mensual considerando los ciclos de Bitcoin:
- Heatmap año × mes con retorno de cada mes histórico
- Estadísticas por mes: promedio, mediana, win rate, distribución
- Separación por ciclos bull/bear para validar si los patrones son robustos
- Foco en los meses más relevantes (ej: abril históricamente alcista, agosto bajista)
- Volatilidad intra-mes vs retorno final

### `data_correlations.ipynb`
Correlaciones con lags entre todos los mercados para identificar relaciones predictivas entre instrumentos.

---

## Setup

```bash
# Instalar dependencias (requiere Poetry)
poetry install

# Correr Jupyter Lab
poetry run jupyter lab

# Agregar una dependencia
poetry add nombre-paquete
```

> **Nota macOS:** `lightgbm` requiere `brew install libomp`

---

## Stack

- **Python 3.13** + **Poetry 2.3**
- `yfinance` — descarga de datos
- `pandas`, `numpy`, `scipy` — análisis de datos y estadística
- `scikit-learn`, `lightgbm`, `xgboost` — modelos ML
- `ta` — indicadores técnicos
- `matplotlib`, `seaborn` — visualización

---

## Estado

| Área | Estado |
|---|---|
| Recolección de datos 1d (~70 instrumentos) | Listo |
| Motor de correlaciones con lags | Listo |
| Análisis estadístico de dirección BTC | En progreso |
| Estacionalidad mensual BTC | En progreso |
| Modelos predictivos ML | En progreso |
| Datos intraday (1h, 4h) | Pendiente |
| Operativa automatizada (señales, TP/SL) | Pendiente |
