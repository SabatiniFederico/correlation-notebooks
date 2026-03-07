# CLAUDE.md - Market Research & Correlation Analysis Project

## Objetivo del proyecto

Plataforma de research financiero con tres ejes:
1. **Recolección y almacenamiento** de datos de mercados (cripto, stocks, commodities, bonds, forex, índices)
2. **Análisis de correlaciones** entre mercados con distintos lags para identificar relaciones predictivas
3. **Modelos de predicción** (futuro): LLMs y ML para anticipar movimientos de mercado y asistir en decisiones operativas (long/short, take profit, stop loss)

El proyecto está en etapa temprana. La fase actual se centra en correlaciones en velas de 1 día.

---

## Estructura del proyecto

```
correlation-notebooks/
├── data/
│   └── yahoo_1d/              # Datos OHLCV descargados de Yahoo Finance (velas 1d)
│       ├── cripto/            # BTC-USD, ETH-USD, SOL-USD, XRP-USD, ADA-USD
│       ├── commodities/       # Oro, Plata, Crudo, Gas, Cobre, Trigo, Maíz, Soja
│       ├── indexes/           # S&P500, NASDAQ, DJI, VIX, DXY, Nikkei, FTSE, DAX, etc.
│       ├── bonds/             # Treasuries 2y, 5y, 10y, 30y
│       └── stocks/            # ~40 acciones large-cap (tech, finanzas, salud, energía, consumo)
├── notebooks/                 # Jupyter notebooks de análisis
│   ├── _init_notebook.py      # Inicializador: importa todo lo necesario, setea PROJECT_ROOT
│   ├── data_correlations.ipynb
│   ├── pct_changes_matrix.ipynb
│   ├── VIX.ipynb
│   └── example_backtesting.ipynb
├── scripts/
│   └── yahoo_1d_collector.ipynb  # Descarga datos de Yahoo Finance y los guarda en data/
├── utils/
│   ├── constants/
│   │   └── stock_symbols.py      # SYMBOL_GROUPS_YAHOO: dict categoria -> {ticker: descripcion}
│   │                             # También: YAHOO_1D_DIR, START_DATE_2000
│   ├── correlations/
│   │   ├── correlations.py           # Versión con más métodos (pearson, spearman, kendall, mutual_info, distance_corr)
│   │   └── correlations_vectorized.py # Versión optimizada (solo pearson, spearman, kendall) — la que se usa en producción
│   ├── indicators/
│   │   ├── ta_generic_indicators.py  # Indicadores técnicos: MACD, BB, RSI, EMA, ZScore, LogRet, Volatilidad
│   │   └── ta_calendar_indicators.py
│   └── tests/
│       └── backtesting.py
└── venv/                      # Entorno virtual Python (ignorar al leer el proyecto)
```

---

## Convenciones y patrones clave

### Notebooks
- Todo notebook debe empezar importando `_init_notebook.py` (configura PROJECT_ROOT y hace los imports estándar)
- Los resultados temporales (CSVs de correlaciones) se guardan en `notebooks/` por ahora

### Datos
- Fuente principal: **Yahoo Finance via yfinance**
- Frecuencia actual: **velas diarias (1d)**
- Formato: CSV con columnas OHLCV, fecha desde 2000-01-01 donde esté disponible
- Los tickers están definidos en `utils/constants/stock_symbols.py` → `SYMBOL_GROUPS_YAHOO`
- Categorías: `cripto`, `commodities`, `indexes`, `bonds`, `forex`, `stocks`

### Correlaciones
- Se trabaja sobre **pct_change** (porcentaje de cambio diario) de los precios de cierre
- La función principal es `compute_pairwise_correlations_incremental()` en `correlations_vectorized.py`
- Soporta **resume**: si el CSV ya existe, continúa desde donde quedó
- `max_lag=180` días para pearson/spearman/kendall; métodos más costosos (mutual_info, distance_corr) solo en ±20 lags
- Resultados se guardan en CSV con columnas: `serie1`, `serie2`, `best_pearson`, `lag_pearson`, `best_spearman`, `lag_spearman`, `best_kendall`, `lag_kendall`
- **Preferir `correlations_vectorized.py`** sobre `correlations.py` (más rápida, escribe fila a fila sin acumular en RAM)

### Indicadores técnicos (`ta_generic_indicators.py`)
- Todas las funciones reciben `df`, `n_shift`, `name` y retornan el df modificado
- El `n_shift` evita data leakage (shift de 1 por defecto)
- Naming convention de columnas: `{name}.{Indicador}_{window}` (ej: `target.RSI_7`)

---

## Stack tecnológico

- Python 3.13, **Poetry 2.3** (gestor de dependencias)
- **yfinance**: descarga de datos
- **pandas, numpy**: manipulación de datos
- **scipy**: correlaciones estadísticas
- **scikit-learn**: ML (mutual_info, modelos de regresión, PCA)
- **lightgbm, xgboost**: modelos de boosting
- **ta**: indicadores técnicos (MACD, BB, RSI, EMA)
- **matplotlib, seaborn**: visualización
- **tqdm**: progreso en loops largos

### Comandos de entorno

```bash
# Instalar dependencias (en máquina nueva)
poetry install

# Correr jupyter
poetry run jupyter lab

# Correr un script
poetry run python script.py

# Agregar una dependencia nueva
poetry add nombre-paquete

# El venv lo gestiona Poetry automáticamente (carpeta global, no en el proyecto)
```

> **Nota macOS**: lightgbm requiere `libomp` instalado via `brew install libomp`

---

## Estado actual y roadmap

### Hecho
- Recolección de datos 1d para ~70 instrumentos (cripto, stocks, commodities, bonds, índices)
- Motor de correlaciones con lags (pearson, spearman, kendall, mutual_info, distance_corr)
- Análisis exploratorio inicial de correlaciones (sin resultados significativos con lags aún)
- Indicadores técnicos básicos y backtesting inicial

### Pendiente / Próximos pasos
- Ordenar estructura del proyecto (separar resultados temporales de código)
- Agregar datos forex (están en `stock_symbols.py` pero no descargados aún)
- Explorar correlaciones con otras frecuencias (1h, 4h)
- Modelos predictivos con LLMs y ML
- Operativa automatizada (señales de entrada, TP/SL)

---

## Notas importantes

- El proyecto está en evolución — actualizar este archivo con cada cambio estructural relevante
- No hacer commits de archivos grandes de datos; los CSVs en `notebooks/` son resultados temporales
- `venv/` debe ignorarse siempre al analizar el código
