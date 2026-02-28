"""
Phase 2 - Task 2.2: 机器学习模型一年期滚动训练与性能对比
响应变量: Dividend_ratio1 (股利支付率)
训练方式: t年训练 → t+1年测试, 2006→2007 至 2021→2022 (16轮)
模型: OLS, Lasso, DecisionTree, SVR, GBDT, RF(tuned), RF(fixed)

输出:
  - output/tables/model_comparison_ch3.csv  (模型对比总表)
  - output/tables/model_yearly_r2.csv       (逐年样本外R²)
  - output/tables/feature_importance_gbdt.csv
  - output/tables/feature_importance_rf.csv
"""

import time
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV, KFold
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

print(f'PROJECT_ROOT: {PROJECT_ROOT}')
print(f'DATA_DIR: {DATA_DIR}')

# ── load & prep ──
data = pd.read_csv(DATA_DIR / 'data.csv')
print(f'Data shape: {data.shape}')

x_all = data.iloc[:, 6:]          # 71 features (35 continuous + 36 ind dummies)
y_all = data.iloc[:, 2]           # Dividend_ratio1
feature_names = list(x_all.columns)
n_features = len(feature_names)
non_dummy_idx = 35                # first 35 are non-industry features

years = sorted(data['year'].unique())  # 2006..2022
n_rolls = len(years) - 1              # 16

# StandardScaler fit on 2006
sc = StandardScaler()
x_2006 = x_all.loc[data['year'] == years[0]]
sc.fit(x_2006)

# prepare per-year data
x_train_list, y_train_list = [], []
for yr in years:
    mask = data['year'] == yr
    xt = pd.DataFrame(sc.transform(x_all.loc[mask]), columns=feature_names)
    yt = y_all.loc[mask].reset_index(drop=True)
    x_train_list.append(xt)
    y_train_list.append(yt)

# ── helper: run rolling evaluation ──
def rolling_eval(model_fn, x_list, y_list, n_rolls, collect_importances=False):
    """Run rolling t→t+1 evaluation. model_fn(x,y) returns fitted model."""
    metrics = {'r2_in': [], 'r2_out': [], 'mse': [], 'mae': [], 'medae': [], 'evs': []}
    importances_list = []
    best_params_list = []
    for i in range(n_rolls):
        j = i + 1
        model = model_fn(x_list[i], y_list[i])
        # in-sample
        metrics['r2_in'].append(model.score(x_list[i], y_list[i]))
        # out-of-sample
        pred = model.predict(x_list[j])
        metrics['r2_out'].append(r2_score(y_list[j], pred))
        metrics['mse'].append(mean_squared_error(y_list[j], pred))
        metrics['mae'].append(mean_absolute_error(y_list[j], pred))
        metrics['medae'].append(median_absolute_error(y_list[j], pred))
        metrics['evs'].append(explained_variance_score(y_list[j], pred))
        if collect_importances and hasattr(model, 'feature_importances_'):
            importances_list.append(model.feature_importances_)
        elif collect_importances and hasattr(model, 'best_estimator_'):
            importances_list.append(model.best_estimator_.feature_importances_)
        if hasattr(model, 'best_params_'):
            best_params_list.append(model.best_params_)
    summary = {k: np.mean(v) for k, v in metrics.items()}
    yearly_r2 = metrics['r2_out']
    return summary, yearly_r2, importances_list, best_params_list

# ── define models ──
kfold = KFold(n_splits=5, shuffle=True, random_state=0)

def make_lasso(x, y):
    param_dist = {'alpha': [0.01, 0.1, 1, 10, 100, 1000]}
    m = RandomizedSearchCV(Lasso(), param_distributions=param_dist, cv=kfold, random_state=0)
    m.fit(x, y)
    return m

def make_gbdt(x, y):
    m = GradientBoostingRegressor(
        n_estimators=3000, max_depth=4, subsample=0.7,
        learning_rate=0.001, random_state=0
    )
    m.fit(x, y)
    return m

def make_rf_tuned(x, y):
    param_dist = {
        'n_estimators': [1000, 2000, 3000, 4000, 5000],
        'max_features': range(10, 20)
    }
    m = RandomizedSearchCV(
        RandomForestRegressor(random_state=0),
        param_distributions=param_dist, n_iter=10,
        cv=kfold, random_state=0, n_jobs=-1
    )
    m.fit(x, y)
    return m

def make_rf_fixed(x, y):
    m = RandomForestRegressor(n_estimators=5000, max_features=19, random_state=0, n_jobs=-1)
    m.fit(x, y)
    return m

def make_svr(x, y):
    m = SVR(kernel='rbf', C=1, gamma=0.01)
    m.fit(x, y)
    return m

def make_dtree(x, y):
    m = DecisionTreeRegressor(max_depth=3, max_features=6, random_state=0, splitter='random')
    m.fit(x, y)
    return m

# OLS uses only first 35 features (no industry dummies)
x_ols_list = [xt.iloc[:, :non_dummy_idx] for xt in x_train_list]

def make_ols(x, y):
    m = LinearRegression()
    m.fit(x, y)
    return m

# ── run all models ──
results = {}
yearly_r2_all = {}
importances = {}

models_config = [
    ('OLS',           make_ols,      x_ols_list,    False),
    ('Lasso',         make_lasso,    x_train_list,  False),
    ('DecisionTree',  make_dtree,    x_train_list,  False),
    ('SVR',           make_svr,      x_train_list,  False),
    ('GBDT',          make_gbdt,     x_train_list,  True),
    ('RF(tuned)',     make_rf_tuned, x_train_list,  True),
    ('RF(fixed)',     make_rf_fixed, x_train_list,  True),
]

log_events = []
for name, fn, x_list, collect_imp in models_config:
    t0 = time.time()
    print(f'\n{"="*60}')
    print(f'Training: {name} ({n_rolls} rolling windows)...')
    summary, yearly_r2, imp_list, bp_list = rolling_eval(fn, x_list, y_train_list, n_rolls, collect_imp)
    elapsed = time.time() - t0
    results[name] = summary
    yearly_r2_all[name] = yearly_r2
    if imp_list:
        importances[name] = imp_list
    print(f'  Done in {elapsed:.1f}s')
    print(f'  In-sample R²={summary["r2_in"]:.4f}  Out-of-sample R²={summary["r2_out"]:.4f}')
    print(f'  MSE={summary["mse"]:.4f}  MAE={summary["mae"]:.4f}  MedAE={summary["medae"]:.4f}  EVS={summary["evs"]:.4f}')
    if bp_list:
        print(f'  Sample best_params: {bp_list[0]}')
    log_events.append({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "phase": "Phase2", "task": f"train_{name}",
        "input": "data.csv", "output": f"model_comparison_ch3.csv",
        "status": "ok",
        "note": json.dumps(summary, ensure_ascii=False)
    })

# ── output: model comparison table ──
comp_df = pd.DataFrame(results).T
comp_df.columns = ['样本内R²', '样本外R²', 'MSE', 'MAE', 'MedAE', 'EVS']
comp_df.index.name = '模型'
comp_df = comp_df.round(4)
comp_df.to_csv(TABLE_DIR / 'model_comparison_ch3.csv', encoding='utf-8-sig')
print(f'\n{"="*60}')
print('Model comparison table:')
print(comp_df.to_string())

# ── output: yearly out-of-sample R² ──
yr_labels = [f'{years[i]}→{years[i+1]}' for i in range(n_rolls)]
yr_df = pd.DataFrame(yearly_r2_all, index=yr_labels)
yr_df.index.name = '滚动窗口'
yr_df = yr_df.round(4)
yr_df.to_csv(TABLE_DIR / 'model_yearly_r2.csv', encoding='utf-8-sig')
print(f'\nYearly R² saved.')

# ── output: feature importance ──
for model_name, imp_list in importances.items():
    imp_arr = np.array(imp_list)  # (16, n_features)
    imp_mean = imp_arr.mean(axis=0)
    imp_std = imp_arr.std(axis=0)
    imp_df = pd.DataFrame({
        '变量': feature_names,
        '平均重要性': imp_mean,
        '标准差': imp_std,
    }).sort_values('平均重要性', ascending=False).reset_index(drop=True)
    imp_df['排名'] = range(1, len(imp_df) + 1)
    imp_df = imp_df[['排名', '变量', '平均重要性', '标准差']]
    safe_name = model_name.replace('(', '_').replace(')', '')
    out_path = TABLE_DIR / f'feature_importance_{safe_name}.csv'
    imp_df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f'\n{model_name} Top-10 Feature Importance:')
    print(imp_df.head(10).to_string(index=False))

# ── log events ──
log_file = LOG_DIR / 'events.jsonl'
with open(log_file, 'a', encoding='utf-8') as f:
    for evt in log_events:
        f.write(json.dumps(evt, ensure_ascii=False) + '\n')

run_log = LOG_DIR / 'run.log'
with open(run_log, 'a', encoding='utf-8') as f:
    f.write(f'\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] Phase2 Task2.2 model training completed.\n')
    f.write(f'Models: {list(results.keys())}\n')
    f.write(f'Output: model_comparison_ch3.csv, model_yearly_r2.csv, feature_importance_*.csv\n')

print(f'\n{"="*60}')
print('Phase 2 Task 2.2 complete. All outputs in output/tables/')