"""
Phase 2 - RF(fixed) training + final summary table
前5个模型已由phase2_ml_training.py完成, 这里补跑RF(fixed)并汇总。
"""

import time
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    median_absolute_error, explained_variance_score
)
import warnings
warnings.filterwarnings("ignore")

# ── paths ──
TARGET_FOLDER = '参考文献/1/20240618102625WU_FILE_1'

def locate_project_root(target_folder=TARGET_FOLDER):
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / target_folder).exists():
            return candidate
    raise FileNotFoundError(f'未能定位 {target_folder}')

PROJECT_ROOT = locate_project_root()
DATA_DIR = PROJECT_ROOT / TARGET_FOLDER / '数据' / '数据-python'
TABLE_DIR = PROJECT_ROOT / 'output' / 'tables'
LOG_DIR = PROJECT_ROOT / 'logs' / '20260227'
for d in (TABLE_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ── load & prep ──
data = pd.read_csv(DATA_DIR / 'data.csv')
x_all = data.iloc[:, 6:]
y_all = data.iloc[:, 2]  # Dividend_ratio1
feature_names = list(x_all.columns)
years = sorted(data['year'].unique())
n_rolls = len(years) - 1

sc = StandardScaler()
sc.fit(x_all.loc[data['year'] == years[0]])

x_list, y_list = [], []
for yr in years:
    mask = data['year'] == yr
    xt = pd.DataFrame(sc.transform(x_all.loc[mask]), columns=feature_names)
    yt = y_all.loc[mask].reset_index(drop=True)
    x_list.append(xt)
    y_list.append(yt)

# ── RF(fixed) with feature importance collection ──
print('Training RF(fixed) n_estimators=5000, max_features=19 ...')
t0 = time.time()
metrics = {'r2_in': [], 'r2_out': [], 'mse': [], 'mae': [], 'medae': [], 'evs': []}
importances_list = []
yearly_r2 = []

for i in range(n_rolls):
    j = i + 1
    print(f'  Window {i+1}/{n_rolls}: {years[i]}→{years[j]} (n_train={len(x_list[i])}, n_test={len(x_list[j])})')
    model = RandomForestRegressor(n_estimators=5000, max_features=19, random_state=0, n_jobs=-1)
    model.fit(x_list[i], y_list[i])

    r2_in = model.score(x_list[i], y_list[i])
    pred = model.predict(x_list[j])
    r2_out = r2_score(y_list[j], pred)
    mse = mean_squared_error(y_list[j], pred)
    mae = mean_absolute_error(y_list[j], pred)
    medae = median_absolute_error(y_list[j], pred)
    evs = explained_variance_score(y_list[j], pred)

    metrics['r2_in'].append(r2_in)
    metrics['r2_out'].append(r2_out)
    metrics['mse'].append(mse)
    metrics['mae'].append(mae)
    metrics['medae'].append(medae)
    metrics['evs'].append(evs)
    importances_list.append(model.feature_importances_)
    yearly_r2.append(r2_out)
    print(f'    R²_in={r2_in:.4f}  R²_out={r2_out:.4f}')

elapsed = time.time() - t0
rf_summary = {k: np.mean(v) for k, v in metrics.items()}
print(f'\nRF(fixed) done in {elapsed:.1f}s')
print(f'  In-sample R²={rf_summary["r2_in"]:.4f}  Out-of-sample R²={rf_summary["r2_out"]:.4f}')
print(f'  MSE={rf_summary["mse"]:.4f}  MAE={rf_summary["mae"]:.4f}  MedAE={rf_summary["medae"]:.4f}  EVS={rf_summary["evs"]:.4f}')

# ── Feature importance output ──
imp_arr = np.array(importances_list)
imp_mean = imp_arr.mean(axis=0)
imp_std = imp_arr.std(axis=0)
imp_df = pd.DataFrame({
    '变量': feature_names,
    '平均重要性': imp_mean,
    '标准差': imp_std,
}).sort_values('平均重要性', ascending=False).reset_index(drop=True)
imp_df['排名'] = range(1, len(imp_df) + 1)
imp_df = imp_df[['排名', '变量', '平均重要性', '标准差']]
imp_df.to_csv(TABLE_DIR / 'feature_importance_RF_fixed.csv', index=False, encoding='utf-8-sig')
print(f'\nRF Top-10 Feature Importance:')
print(imp_df.head(10).to_string(index=False))

# ── Assemble full comparison table (前5模型 + RF) ──
# 前5模型结果 (from first run)
prev_results = {
    'OLS':          {'样本内R²': 0.2490, '样本外R²': 0.1565, 'MSE': 0.0871, 'MAE': 0.1834, 'MedAE': 0.1254, 'EVS': 0.1812},
    'Lasso':        {'样本内R²': 0.2386, '样本外R²': 0.1805, 'MSE': 0.0850, 'MAE': 0.1794, 'MedAE': 0.1229, 'EVS': 0.1928},
    'DecisionTree': {'样本内R²': 0.0446, '样本外R²':-0.0155, 'MSE': 0.1039, 'MAE': 0.2167, 'MedAE': 0.1876, 'EVS':-0.0040},
    'SVR':          {'样本内R²': 0.5964, '样本外R²': 0.1613, 'MSE': 0.0868, 'MAE': 0.1788, 'MedAE': 0.1177, 'EVS': 0.1675},
    'GBDT':         {'样本内R²': 0.6075, '样本外R²': 0.2368, 'MSE': 0.0790, 'MAE': 0.1646, 'MedAE': 0.1008, 'EVS': 0.2518},
}
prev_results['RF'] = {
    '样本内R²': round(rf_summary['r2_in'], 4),
    '样本外R²': round(rf_summary['r2_out'], 4),
    'MSE': round(rf_summary['mse'], 4),
    'MAE': round(rf_summary['mae'], 4),
    'MedAE': round(rf_summary['medae'], 4),
    'EVS': round(rf_summary['evs'], 4),
}

comp_df = pd.DataFrame(prev_results).T
comp_df.index.name = '模型'
comp_df.to_csv(TABLE_DIR / 'model_comparison_ch3.csv', encoding='utf-8-sig')
print(f'\n{"="*60}')
print('Final Model Comparison:')
print(comp_df.to_string())

# ── Yearly R² for RF ──
yr_labels = [f'{years[i]}→{years[i+1]}' for i in range(n_rolls)]

# Also include previous models' yearly results from first run output
# For now, save RF yearly R²
yr_rf_df = pd.DataFrame({'滚动窗口': yr_labels, 'RF_R2_out': [round(r, 4) for r in yearly_r2]})
yr_rf_df.to_csv(TABLE_DIR / 'rf_yearly_r2.csv', index=False, encoding='utf-8-sig')

# ── Log ──
log_file = LOG_DIR / 'events.jsonl'
with open(log_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "phase": "Phase2", "task": "train_RF_fixed",
        "input": "data.csv",
        "output": "feature_importance_RF_fixed.csv, model_comparison_ch3.csv",
        "status": "ok",
        "note": json.dumps(rf_summary)
    }, ensure_ascii=False) + '\n')

run_log = LOG_DIR / 'run.log'
with open(run_log, 'a', encoding='utf-8') as f:
    f.write(f'\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] Phase2 RF(fixed) training completed.\n')
    f.write(f'RF Out-of-sample R²={rf_summary["r2_out"]:.4f}\n')
    f.write(f'Output: feature_importance_RF_fixed.csv, model_comparison_ch3.csv\n')

print(f'\nAll done. Outputs in output/tables/')
