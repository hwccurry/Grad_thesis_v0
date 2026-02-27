"""
Phase 2 - Task 2.4: 子样本稳健性 (RF + GBDT)
对各子样本做一年期滚动预测, 输出样本外R²对比表 + 特征重要性Top5
"""
import time, json
import pandas as pd, numpy as np
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings("ignore")

PROJECT_ROOT = Path('/Users/mac/Desktop/Grad_thesis')
DATA_DIR = PROJECT_ROOT / '参考文献/1/20240618102625WU_FILE_1/数据/数据-python'
TABLE_DIR = PROJECT_ROOT / 'output' / 'tables'
TABLE_DIR.mkdir(parents=True, exist_ok=True)

# subsample files & their year ranges
subsamples = [
    ('全样本',       'data.csv',           2006, 2022),
    ('国有企业',     'dataguoyou.csv',     2006, 2022),
    ('非国有企业',   'datafeiguoyou.csv',  2006, 2022),
    ('高现金流',     'datan-bigcash.csv',  2006, 2022),
    ('低现金流',     'data-smallcash.csv', 2006, 2022),
    ('2012年之前',   'dataqian.csv',       2006, 2011),
    ('2012年及之后', 'datahou.csv',        2012, 2022),
]

def rolling_eval(data, start_year, end_year, model_cls, model_kwargs):
    """Run one-year rolling and return mean out-of-sample R², feature importance."""
    x_all = data.iloc[:, 6:]
    y_all = data.iloc[:, 2]
    feature_names = list(x_all.columns)
    years = sorted(data['year'].unique())
    years = [y for y in years if start_year <= y <= end_year]

    if len(years) < 2:
        return None, None, None, None

    sc = StandardScaler()
    sc.fit(x_all.loc[data['year'] == years[0]])

    x_list, y_list = [], []
    for yr in years:
        mask = data['year'] == yr
        xt = pd.DataFrame(sc.transform(x_all.loc[mask]), columns=feature_names)
        yt = y_all.loc[mask].reset_index(drop=True)
        x_list.append(xt)
        y_list.append(yt)

    n_rolls = len(years) - 1
    r2_list, imp_list = [], []
    for i in range(n_rolls):
        model = model_cls(**model_kwargs)
        model.fit(x_list[i], y_list[i])
        pred = model.predict(x_list[i+1])
        r2_list.append(r2_score(y_list[i+1], pred))
        if hasattr(model, 'feature_importances_'):
            imp_list.append(model.feature_importances_)

    mean_r2 = np.mean(r2_list)
    if imp_list:
        mean_imp = np.mean(imp_list, axis=0)
        top5_idx = np.argsort(mean_imp)[::-1][:5]
        top5 = [(feature_names[j], mean_imp[j]) for j in top5_idx]
    else:
        top5 = []
    return mean_r2, n_rolls, len(data), top5

# run all subsamples
results = []
for label, fname, yr_start, yr_end in subsamples:
    fpath = DATA_DIR / fname
    if not fpath.exists():
        print(f'SKIP: {fpath} not found')
        continue
    data = pd.read_csv(fpath)
    # Handle column count differences (SOE subsets have 76 cols, missing Soe)
    n_cols = data.shape[1]

    print(f'\n--- {label} ({fname}, {data.shape[0]} rows, {n_cols} cols) ---')

    # RF
    t0 = time.time()
    rf_r2, rf_rolls, n_obs, rf_top5 = rolling_eval(
        data, yr_start, yr_end,
        RandomForestRegressor, dict(n_estimators=2000, max_features=15, random_state=0, n_jobs=-1)
    )
    rf_time = time.time() - t0

    # GBDT
    t0 = time.time()
    gbdt_r2, gbdt_rolls, _, gbdt_top5 = rolling_eval(
        data, yr_start, yr_end,
        GradientBoostingRegressor, dict(n_estimators=3000, max_depth=4, subsample=0.7, learning_rate=0.001, random_state=0)
    )
    gbdt_time = time.time() - t0

    print(f'  RF  R²_out={rf_r2:.4f} ({rf_rolls} windows, {rf_time:.0f}s)')
    print(f'  GBDT R²_out={gbdt_r2:.4f} ({gbdt_rolls} windows, {gbdt_time:.0f}s)')
    print(f'  RF Top5:   {", ".join(f"{n}({v:.3f})" for n,v in rf_top5)}')
    print(f'  GBDT Top5: {", ".join(f"{n}({v:.3f})" for n,v in gbdt_top5)}')

    results.append({
        '子样本': label,
        '观测数': n_obs,
        '滚动窗口数': rf_rolls,
        'RF样本外R²': round(rf_r2, 4) if rf_r2 else None,
        'GBDT样本外R²': round(gbdt_r2, 4) if gbdt_r2 else None,
        'RF_Top1': rf_top5[0][0] if rf_top5 else '',
        'RF_Top2': rf_top5[1][0] if len(rf_top5) > 1 else '',
        'RF_Top3': rf_top5[2][0] if len(rf_top5) > 2 else '',
        'GBDT_Top1': gbdt_top5[0][0] if gbdt_top5 else '',
        'GBDT_Top2': gbdt_top5[1][0] if len(gbdt_top5) > 1 else '',
        'GBDT_Top3': gbdt_top5[2][0] if len(gbdt_top5) > 2 else '',
    })

res_df = pd.DataFrame(results)
res_df.to_csv(TABLE_DIR / 'subsample_robustness_ch3.csv', index=False, encoding='utf-8-sig')
print(f'\n{"="*60}')
print('Subsample robustness results:')
print(res_df[['子样本', '观测数', 'RF样本外R²', 'GBDT样本外R²', 'RF_Top1', 'RF_Top2', 'RF_Top3']].to_string(index=False))
print(f'\nSaved to output/tables/subsample_robustness_ch3.csv')
