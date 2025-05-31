import matplotlib.pyplot as plt
import pandas as pd

"""
Realiza un backtest profesional comparando una estrategia contra un benchmark.

Args:
    capital (float): Capital inicial en USD.
    start_date (str): Fecha de inicio del backtest ("YYYY-MM-DD").
    strategy_series (pd.Series): Serie de precios o retornos acumulados de la estrategia.
    benchmark_series (pd.Series): Serie de precios o retornos acumulados del benchmark.
    title (str): Título del gráfico.

Returns:
    pd.DataFrame: DataFrame con los valores acumulados de la estrategia y el benchmark.
"""
def run_backtest(capital, start_date, strategy_series, benchmark_series, title="Backtesting Results"):

    strategy_series = strategy_series[strategy_series.index >= start_date]
    benchmark_series = benchmark_series[benchmark_series.index >= start_date]

    data = pd.DataFrame({
        'strategy': strategy_series,
        'benchmark': benchmark_series
    }).dropna()

    data['strategy_value'] = capital * (data['strategy'] / data['strategy'].iloc[0])
    data['benchmark_value'] = capital * (data['benchmark'] / data['benchmark'].iloc[0])

    # Graficar
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['strategy_value'], label='Strategy', color='green')
    plt.plot(data.index, data['benchmark_value'], label='Benchmark', color='blue')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return data[['strategy_value', 'benchmark_value']]