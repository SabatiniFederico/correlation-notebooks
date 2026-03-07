import pandas as pd
import numpy as np
from scipy.stats import kendalltau, rankdata
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

    if resume and os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
        processed_pairs = set(zip(existing_df['serie1'], existing_df['serie2']))

    file_exists = os.path.exists(output_path)
    with open(output_path, "a", newline="") as csvfile:
        fieldnames = ['serie1', 'serie2'] + [
            f"best_{m}" for m in ['pearson', 'spearman', 'kendall']
        ] + [
            f"lag_{m}" for m in ['pearson', 'spearman', 'kendall']
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for col1, col2 in tqdm(combinations(columns, 2), total=total_pairs):
            if (col1, col2) in processed_pairs or (col2, col1) in processed_pairs:
                continue

            s1 = pct_change_matrix[col1]
            s2 = pct_change_matrix[col2]

            try:
                corr_df = run_all_correlations(s1, s2, max_lag=max_lag)

                result_row = {
                    'serie1': col1,
                    'serie2': col2,
                }
                for _, row in corr_df.iterrows():
                    method = row['method']
                    result_row[f"best_{method}"] = row['score']
                    result_row[f"lag_{method}"] = row['lag']

                writer.writerow(result_row)
                csvfile.flush()
            except Exception as e:
                print(f"Error en par {col1}-{col2}: {e}")

def run_all_correlations(series1, series2, max_lag=180):
    methods = {
        'pearson': best_lag_pearson,
        'spearman': best_lag_spearman,
        'kendall': best_lag_kendall,
    }
    results = []
    for name, func in methods.items():
        res = func(series1, series2, max_lag=max_lag)
        res['method'] = name
        results.append(res)
    return pd.DataFrame(results)

def best_lag_pearson(series1, series2, max_lag=180):
    return pearson_corr_lags(series1, series2, max_lag)

def best_lag_spearman(series1, series2, max_lag=180):
    x_rank = pd.Series(rankdata(series1.values), index=series1.index)
    y_rank = pd.Series(rankdata(series2.values), index=series2.index)
    return pearson_corr_lags(x_rank, y_rank, max_lag)

def best_lag_kendall(series1, series2, max_lag=180):
    x = series1.values
    y = series2.values
    lags = np.arange(-max_lag, max_lag + 1)
    best_score = -np.inf
    best_lag = None

    for lag in lags:
        if lag > 0:
            x_lag = x[:-lag]
            y_lag = y[lag:]
        elif lag < 0:
            x_lag = x[-lag:]
            y_lag = y[:lag]
        else:
            x_lag = x
            y_lag = y

        mask = (~np.isnan(x_lag)) & (~np.isnan(y_lag))
        if mask.sum() < 2:
            continue
        try:
            score, _ = kendalltau(x_lag[mask], y_lag[mask])
        except:
            continue

        if abs(score) > best_score:
            best_score = abs(score)
            best_lag = lag

    if best_lag is None:
        return {'lag': None, 'score': np.nan}
    return {'lag': best_lag, 'score': best_score}

def pearson_corr_lags(series1, series2, max_lag=180):
    x = series1.values
    y = series2.values
    n = len(x)
    lags = np.arange(-max_lag, max_lag + 1)
    corrs = np.full(len(lags), np.nan)

    for i, lag in enumerate(lags):
        if lag > 0:
            x_lag = x[:-lag]
            y_lag = y[lag:]
        elif lag < 0:
            x_lag = x[-lag:]
            y_lag = y[:lag]
        else:
            x_lag = x
            y_lag = y

        mask = ~np.isnan(x_lag) & ~np.isnan(y_lag)
        if mask.sum() < 2:
            continue

        corrs[i] = np.corrcoef(x_lag[mask], y_lag[mask])[0, 1]

    if np.all(np.isnan(corrs)):
        return {'lag': None, 'score': np.nan}

    best_idx = np.nanargmax(np.abs(corrs))
    return {'lag': lags[best_idx], 'score': corrs[best_idx]}