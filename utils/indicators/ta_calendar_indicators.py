import pandas as pd

def apply_utility_indicators(df):
  df.index = pd.to_datetime(df.index)
  df['Utils.DayOfWeek'] = df.index.dayofweek  # 0 = lunes
  df['Utils.IsWeekend'] = df['Utils.DayOfWeek'] >= 5

  # Para detectar si es primera semana del mes
  df['Utils.IsFirstWeek'] = df.index.isin(
      df.groupby([df.index.year, df.index.month]).head(7).index
  )

  # Para detectar si es última semana del mes
  df['Utils.IsLastWeek'] = df.index.isin(
    df.groupby([df.index.year, df.index.month]).tail(7).index
  )

  df['Utils.IsMonthStart'] = df.index.is_month_start
  df['Utils.IsMonthEnd'] = df.index.is_month_end
  df['Utils.MonthOfYear'] = df.index.month
  df['Utils.DayOfYear'] = df.index.dayofyear
  df['Utils.WeekOfYear'] = df.index.isocalendar().week
  #df['Utils.Quarter'] = df.index.quarter

  df["Utils.DayOfWeek"] = df.index.dayofweek
  df["Utils.DayOfMonth"] = df.index.day

  df["Utils.DayOfMonth_sin"] = np.sin(2 * np.pi * df["Utils.DayOfMonth"] / 31)
  df["Utils.DayOfMonth_cos"] = np.cos(2 * np.pi * df["Utils.DayOfMonth"] / 31)
  df["Utils.DayOfWeek_sin"] = np.sin(2 * np.pi * df["Utils.DayOfWeek"] / 7)
  df["Utils.DayOfWeek_cos"] = np.cos(2 * np.pi * df["Utils.DayOfWeek"] / 7)
  df["Utils.MonthOfYear_sin"] = np.sin(2 * np.pi * df["Utils.MonthOfYear"] / 12)
  df["Utils.MonthOfYear_cos"] = np.cos(2 * np.pi * df["Utils.MonthOfYear"] / 12)
  df['Utils.DayOfYear_Sin'] = np.sin(2 * np.pi * df['Utils.DayOfYear'] / 365)
  df['Utils.DayOfYear_Cos'] = np.cos(2 * np.pi * df['Utils.DayOfYear'] / 365)
  df["Utils.WeekOfYear_sin"] = np.sin(2 * np.pi * df["Utils.WeekOfYear"] / 52)
  df["Utils.WeekOfYear_cos"] = np.cos(2 * np.pi * df["Utils.WeekOfYear"] / 52)
  return df