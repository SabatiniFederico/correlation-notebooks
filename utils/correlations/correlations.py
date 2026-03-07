import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.feature_selection import mutual_info_regression
from itertools import combinations
from tqdm import tqdm
import os
import csv

def compute_pairwise_correlations_incremental(
    pct_change_matrix,
    max_lag=180,
    output_path="correlation_results_with_lags.csv",
    resume=True,
):
    columns = pct_change_matrix.columns
    total_pairs = (len(columns) * (len(columns) - 1)) // 2
    processed_pairs = set()

    # Si existe y queremos reanudar, cargamos pares ya procesados
    if resume and os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
        processed_pairs = set(zip(existing_df['serie1'], existing_df['serie2']))

    results = []

    for col1, col2 in tqdm(combinations(columns, 2), total=total_pairs):
        if (col1, col2) in processed_pairs or (col2, col1) in processed_pairs:
            continue

        series1 = pct_change_matrix[col1]
        series2 = pct_change_matrix[col2]

        try:
            corr_df = run_all_correlations_optimized(series1, series2, max_lag=max_lag)

            result_row = {
                'serie1': col1,
                'serie2': col2,
            }

            for _, row in corr_df.iterrows():
                method = row['method']
                result_row[f"best_{method}"] = row['score']
                result_row[f"lag_{method}"] = row['lag']

            results.append(result_row)
        except Exception as e:
            print(f"Error en par {col1}-{col2}: {e}")

    # Guardamos todo junto (menos overhead IO)
    final_df = pd.DataFrame(results)
    if os.path.exists(output_path) and resume:
        final_df.to_csv(output_path, mode='a', header=False, index=False)
    else:
        final_df.to_csv(output_path, index=False)


def run_all_correlations_optimized(series1, series2, max_lag=180):
    """
    Mutual info y distance corr se calculan solo en +/-20 lags para ahorrar tiempo
    """
    methods = {
        'pearson': best_pearson_lag,
        'spearman': best_lag_generic,
        'kendall': best_lag_generic,
        'mutual_info': best_lag_reduced_range,
        'distance_corr': best_lag_reduced_range,
    }

    results = []
    for name, func in methods.items():
        if name in ['mutual_info', 'distance_corr']:
            res = func(series1, series2, max_lag=20, corr_func=correlation_functions[name])
        elif name == 'pearson':
            res = func(series1, series2, max_lag=max_lag)
        else:
            res = func(series1, series2, max_lag=max_lag, corr_func=correlation_functions[name])
        res['method'] = name
        results.append(res)
    return pd.DataFrame(results)

def best_pearson_lag(series1, series2, max_lag=180):
    lags = np.arange(-max_lag, max_lag + 1)
    n = len(series1)
    s1 = series1.values
    s2 = series2.values

    scores = np.full(len(lags), np.nan)

    for i, lag in enumerate(lags):
        if lag > 0:
            x = s1[lag:]
            y = s2[:n - lag]
        elif lag < 0:
            x = s1[:n + lag]
            y = s2[-lag:]
        else:
            x = s1
            y = s2

        mask = ~np.isnan(x) & ~np.isnan(y)
        if np.sum(mask) < 10:
            continue
        # numpy corrcoef rápido y vectorial
        scores[i] = np.corrcoef(x[mask], y[mask])[0, 1]

    if np.all(np.isnan(scores)):
        return {'lag': None, 'score': np.nan}
    best_idx = np.nanargmax(np.abs(scores))
    return {'lag': lags[best_idx], 'score': scores[best_idx]}


def best_lag_generic(series1, series2, max_lag=180, corr_func=None):
    """
    Para Spearman y Kendall, se usa la función pasada (que usa scipy).
    """
    best_score = -np.inf
    best_lag = None
    best_raw_score = None
    lags = range(-max_lag, max_lag + 1)

    for lag in lags:
        if lag > 0:
            x = series1.shift(lag)
            y = series2
        else:
            x = series1
            y = series2.shift(-lag)

        # Índice común solo una vez por lag, con pandas eficiente
        common_idx = x.dropna().index.intersection(y.dropna().index)
        if len(common_idx) < 10:
            continue

        try:
            result = corr_func(x.loc[common_idx], y.loc[common_idx])
            score = result if isinstance(result, float) else result[0]
            score_to_compare = abs(score)
        except:
            continue

        if score_to_compare > best_score:
            best_score = score_to_compare
            best_raw_score = score
            best_lag = lag

    return {'lag': best_lag, 'score': best_raw_score}


def best_lag_reduced_range(series1, series2, max_lag=20, corr_func=None):
    """
    Para mutual_info y distance_corr que son más costosos.
    """
    best_score = -np.inf
    best_lag = None
    best_raw_score = None
    lags = range(-max_lag, max_lag + 1)

    for lag in lags:
        if lag > 0:
            x = series1.shift(lag)
            y = series2
        else:
            x = series1
            y = series2.shift(-lag)

        common_idx = x.dropna().index.intersection(y.dropna().index)
        if len(common_idx) < 20:
            continue

        try:
            result = corr_func(x.loc[common_idx], y.loc[common_idx])
            score = result if isinstance(result, float) else result[0]
            score_to_compare = abs(score)
        except:
            continue

        if score_to_compare > best_score:
            best_score = score_to_compare
            best_raw_score = score
            best_lag = lag

    return {'lag': best_lag, 'score': best_raw_score}


# Funciones de correlación (usadas dentro de best_lag_generic o reduced)

def pearson_corr(x: pd.Series, y: pd.Series):
    r, p = pearsonr(x, y)
    return r, p

def spearman_corr(x: pd.Series, y: pd.Series):
    r, p = spearmanr(x, y)
    return r, p

def kendall_corr(x: pd.Series, y: pd.Series):
    r, p = kendalltau(x, y)
    return r, p

def mutual_info_corr(x: pd.Series, y: pd.Series, n_bins=20):
    x_vals = x.values.reshape(-1, 1)
    y_vals = y.values
    mi = mutual_info_regression(x_vals, y_vals, discrete_features=False)
    return mi[0]

def distance_corr(x: pd.Series, y: pd.Series):
    def _distance_matrix(a):
        return np.linalg.norm(a[:, None] - a[None, :], axis=2)

    def _centered_matrix(D):
        n = D.shape[0]
        row_mean = D.mean(axis=1, keepdims=True)
        col_mean = D.mean(axis=0, keepdims=True)
        total_mean = D.mean()
        return D - row_mean - col_mean + total_mean

    x_vals = x.values.reshape(-1, 1)
    y_vals = y.values.reshape(-1, 1)

    A = _centered_matrix(_distance_matrix(x_vals))
    B = _centered_matrix(_distance_matrix(y_vals))

    dcov = np.sqrt(np.mean(A * B))
    dvar_x = np.sqrt(np.mean(A * A))
    dvar_y = np.sqrt(np.mean(B * B))

    return dcov / np.sqrt(dvar_x * dvar_y)

correlation_functions = {
    'pearson': pearson_corr,
    'spearman': spearman_corr,
    'kendall': kendall_corr,
    'mutual_info': mutual_info_corr,
    'distance_corr': distance_corr,
}