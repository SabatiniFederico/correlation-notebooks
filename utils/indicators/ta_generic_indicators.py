import ta  # technical analysis indicators
from ta.trend import MACD
from ta.volatility import BollingerBands

import pandas as pd

def calc_pct_change(df, n_shift=1, name='target'):
    df[f'{name}.PctChange'] = df[f'{name}.Close'].pct_change() * 100
    df[f'{name}.PctChange'] = df[f'{name}.PctChange'].shift(n_shift)
    return df

def calc_macd(df, n_shift=1, name='target'):
  macd = MACD(close=df[f'{name}.Close'])
  df[f'{name}.MACD'] = macd.macd().shift(n_shift)
  df[f'{name}.Signal'] = macd.macd_signal().shift(n_shift)
  df[f'{name}.Hist'] = macd.macd_diff().shift(n_shift)
  return df

def calc_bollinger_bands(df, window=7, n_shift=1, name='target'):
    bb = BollingerBands(close=df[f'{name}.Close'], window=window, window_dev=2)
    df[f'{name}.UpperBand_{window}'] = bb.bollinger_hband().shift(n_shift)
    df[f'{name}.MiddleBand_{window}'] = bb.bollinger_mavg().shift(n_shift)
    df[f'{name}.LowerBand_{window}'] = bb.bollinger_lband().shift(n_shift)
    return df

def calc_bollinger_bands_percentage_change(df, window=7, name='target'):
    # Calcular el porcentaje de cambio para las Bandas de Bollinger
    df[f'{name}.UpperBand_{window}_PctChange'] = df[f'{name}.UpperBand_{window}'].pct_change() * 100
    df[f'{name}.MiddleBand_{window}_PctChange'] = df[f'{name}.MiddleBand_{window}'].pct_change() * 100
    df[f'{name}.LowerBand_{window}_PctChange'] = df[f'{name}.LowerBand_{window}'].pct_change() * 100
    return df

def calc_rsi(df, window=7, n_shift=1, name='target'):
  df[f'{name}.RSI_{window}'] = ta.momentum.RSIIndicator(close=df[f'{name}.Close'], window=window).rsi()
  df[f'{name}.RSI_{window}'] = df[f'{name}.RSI_{window}'].shift(n_shift)
  return df

def calc_ema(df, window=7, n_shift=1, name='target'):
  df[f'{name}.EMA_{window}'] = ta.trend.EMAIndicator(close=df[f'{name}.Close'], window=window).ema_indicator()
  df[f'{name}.EMA_{window}'] = df[f'{name}.EMA_{window}'].shift(n_shift)
  return df

def calc_ema_percentage_change(df, window=7, name='target'):
    df[f'{name}.EMA_{window}_PctChange'] = df[f'{name}.EMA_{window}'].pct_change() * 100
    return df

def calc_btc_over_ema(df,window=7, n_shift=1, name='target'):
  df[f'{name}.Pct_Over_EMA_{window}'] = (df[f'{name}.Close'] - df[f'{name}.EMA_{window}']) / df[f'{name}.EMA_{window}']
  df[f'{name}.Pct_Over_EMA_{window}'] = df[f'{name}.Pct_Over_EMA_{window}'].shift(n_shift)
  return df

def calc_z_score(df, window=7, n_shift=1, name='target'):
  rolling_mean = df[f'{name}.Close'].rolling(window=window).mean()
  rolling_std = df[f'{name}.Close'].rolling(window=window).std()
  df[f'{name}.ZScore_{window}'] = (df[f'{name}.Close'] - rolling_mean) / rolling_std
  df[f'{name}.ZScore_{window}'] = df[f'{name}.ZScore_{window}'].shift(n_shift)
  return df

def calc_log_ret(df, n_shift=1, name='target'):
  df[f'{name}.LogRet'] = np.log(df[f'{name}.Close'] / df[f'{name}.Close'].shift(1))
  df[f'{name}.LogRet'] = df[f'{name}.LogRet'].shift(n_shift)
  return df

def calc_volatility(df, window=7, n_shift=1, name='target'):
  df[f'{name}.Volatility_{window}'] = df[f'{name}.LogRet'].rolling(window=window).std()
  df[f'{name}.Volatility_{window}'] = df[f'{name}.Volatility_{window}'].shift(n_shift)
  return df