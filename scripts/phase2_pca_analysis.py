"""
Phase 5 - Task 5.3: PCA analysis with thesis-format figures (v2)
Rewritten for: 300 DPI, serif fonts, grayscale-friendly, A4 figsize.
Figures output to output/figures_v2/.
Tables still output to output/tables/ (no change needed).
"""

import sys
import time
import json
import os
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    median_absolute_error, explained_variance_score
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_plot_config import apply_thesis_style, GRAY_LIGHT

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
apply_thesis_style()

import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── runtime args ──
parser = argparse.ArgumentParser(description="Phase5 PCA analysis and plotting")
parser.add_argument(
    "--plots-only",
    action="store_true",
    help="仅重绘PCA图（碎石图+载荷热力图），跳过后续模型比较。"
)
args = parser.parse_args()

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
FIG_SUBDIR = os.getenv('THESIS_FIG_SUBDIR', 'figures_v2')
FIG_DIR = PROJECT_ROOT / 'output' / FIG_SUBDIR
LOG_DIR = PROJECT_ROOT / 'logs' / time.strftime('%Y%m%d')
for d in (TABLE_DIR, FIG_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ── EN→CN variable name mapping ──
EN_TO_CN = {
    'Managefee_ratio': '管理费用率', 'Manageshare': '管理层持股比例',
    'Indep_ratio': '独立董事比例', 'Bgender': '董事会女性比例',
    'Bshare': '董事长持股比例', 'Bage': '董事长年龄',
    'Btenure': '董事长任期', 'Bsalary': '董事长薪酬',
    'Equity': '股权激励', 'Da_abs': '财务报告质量',
    'Tunneling': '其他应收款资产比', 'Top1': '股权集中度',
    'Sharebalance': '股权制衡度', 'Minorityrate': '中小股东持股比例',
    'Institution': '机构投资者持股比例', 'Pledge': '股权质押比例',
    'Retainedearn_ratio': '留存收益资产比', 'Freecash2': '自由现金流',
    'Tax_avoid': '税收规避程度', 'Tax_ratio': '实际税率',
    'Tax_volatility': '纳税波动率', 'Constraint': '融资约束程度',
    'Refinance': '再融资动机', 'Sentiment': '投资者情绪',
    'Dividend_lag': '上一期股利水平', 'ROA': '资产收益率',
    'Cashflow': '每股经营现金流', 'Tobinq': '托宾Q',
    'BM': '账面市值比', 'Lev': '资产负债率',
    'Soe': '产权性质', 'Growth': '销售增长率',
    'Lnsize': '公司规模', 'Analyst_num': '分析师跟踪人数',
    'Market_idx': '市场化程度',
}

print(f'PROJECT_ROOT: {PROJECT_ROOT}')
print(f'DATA_DIR: {DATA_DIR}')

# ══════════════════════════════════════════════════════════════
# Module 1: Data loading
# ══════════════════════════════════════════════════════════════
data = pd.read_csv(DATA_DIR / 'data.csv')
print(f'Data shape: {data.shape}')

x_all = data.iloc[:, 6:]
y_all = data.iloc[:, 2]
feature_names = list(x_all.columns)
NON_DUMMY_IDX = 35
continuous_features = feature_names[:NON_DUMMY_IDX]

years = sorted(data['year'].unique())
n_rolls = len(years) - 1

sc = StandardScaler()
x_2006_cont = x_all.loc[data['year'] == years[0], continuous_features]
sc.fit(x_2006_cont)

x_cont_scaled = pd.DataFrame(
    sc.transform(x_all[continuous_features]),
    columns=continuous_features,
    index=x_all.index
)

log_events = []

# ══════════════════════════════════════════════════════════════
# Module 2: PCA fit (2006 baseline)
# ══════════════════════════════════════════════════════════════
print('\n' + '='*60)
print('PCA fitting on 2006 baseline data...')

x_2006_scaled = x_cont_scaled.loc[data['year'] == years[0]]
pca_full = PCA()
pca_full.fit(x_2006_scaled)

explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

K = int(np.argmax(cumulative_var >= 0.80) + 1)
print(f'K = {K}, cumulative variance = {cumulative_var[K-1]:.4f}')

var_df = pd.DataFrame({
    '主成分': [f'PC{i+1}' for i in range(len(explained_var))],
    '解释方差比': explained_var,
    '累积解释方差比': cumulative_var
}).round(4)
var_df.to_csv(TABLE_DIR / 'pca_explained_variance.csv', index=False, encoding='utf-8-sig')

log_events.append({
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "phase": "Phase5", "task": "pca_fit",
    "input": "data.csv (35 continuous features, 2006 baseline)",
    "output": "pca_explained_variance.csv",
    "status": "ok",
    "note": f"K={K}, cumvar={cumulative_var[K-1]:.4f}"
})

# ══════════════════════════════════════════════════════════════
# Module 3: Scree plot (thesis format)
# ══════════════════════════════════════════════════════════════
print('\nGenerating scree plot...')

n_show = min(20, len(explained_var))
fig, ax1 = plt.subplots(figsize=(5.5, 3.0))

x_pos = np.arange(1, n_show + 1)
# Use low-saturation color pair for better on-screen distinction while keeping print readability
SOFT_BLUE = '#4E79A7'
SOFT_RED = '#C44E52'
ax1.bar(x_pos, explained_var[:n_show] * 100, color=SOFT_BLUE, edgecolor='#345A82',
        linewidth=0.5, alpha=0.85, label='单个方差占比')
ax1.set_xlabel('主成分编号')
ax1.set_ylabel('解释方差占比 (%)')
ax1.set_xticks(x_pos)

ax2 = ax1.twinx()
ax2.plot(x_pos, cumulative_var[:n_show] * 100, 'o-', color=SOFT_RED,
         linewidth=1.2, markersize=3, label='累积方差占比')
ax2.set_ylabel('累积解释方差占比 (%)')

# 80% threshold line
ax2.axhline(y=80, color=GRAY_LIGHT, linestyle='--', linewidth=0.8, alpha=0.7)
ax2.text(n_show - 0.5, 81.5, '80%阈值', fontsize=8, color=GRAY_LIGHT, ha='right')

# K annotation
ax2.axvline(x=K, color=GRAY_LIGHT, linestyle=':', linewidth=0.8, alpha=0.7)
ax2.text(K + 0.3, cumulative_var[K-1] * 100 - 5,
         f'K={K}\n({cumulative_var[K-1]*100:.1f}%)',
         fontsize=8, color='#555555')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=8)

plt.title('PCA碎石图（35个连续金融特征）', fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / 'pca_scree_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(f'Saved: {FIG_DIR / "pca_scree_plot.png"}')

# ══════════════════════════════════════════════════════════════
# Module 4: Loadings table
# ══════════════════════════════════════════════════════════════
print('\nBuilding loadings table...')

loadings = pca_full.components_[:K, :]
loadings_df = pd.DataFrame(
    loadings.T,
    index=continuous_features,
    columns=[f'PC{i+1}' for i in range(K)]
)
loadings_df.index.name = '变量(英文)'
loadings_df['变量(中文)'] = [EN_TO_CN.get(f, f) for f in continuous_features]

top3_info = {}
for pc in loadings_df.columns:
    if pc == '变量(中文)':
        continue
    abs_vals = loadings_df[pc].abs()
    top3_idx = abs_vals.nlargest(3).index
    top3_info[pc] = [(idx, EN_TO_CN.get(idx, idx), loadings_df.loc[idx, pc]) for idx in top3_idx]

save_cols = ['变量(中文)'] + [f'PC{i+1}' for i in range(K)]
loadings_save = loadings_df[save_cols].copy().round(4)
loadings_save.to_csv(TABLE_DIR / 'pca_loadings_top.csv', encoding='utf-8-sig')

print('\nTop 3 features per PC:')
for pc, items in top3_info.items():
    info_str = ', '.join([f'{cn}({val:+.3f})' for _, cn, val in items])
    print(f'  {pc}: {info_str}')

log_events.append({
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "phase": "Phase5", "task": "pca_loadings",
    "input": "pca_full.components_",
    "output": "pca_loadings_top.csv",
    "status": "ok",
    "note": json.dumps({pc: [(cn, round(v, 3)) for _, cn, v in items]
                        for pc, items in top3_info.items()}, ensure_ascii=False)
})

# ══════════════════════════════════════════════════════════════
# Module 5: Loading heatmap (thesis format)
# ══════════════════════════════════════════════════════════════
print('\nGenerating loading heatmap...')

n_pc_show = min(8, K)
heatmap_data = loadings_df[[f'PC{i+1}' for i in range(n_pc_show)]].copy()
heatmap_data.index = [EN_TO_CN.get(f, f) for f in heatmap_data.index]

fig, ax = plt.subplots(figsize=(max(5.5, n_pc_show * 0.9), 7.5))
sns.heatmap(
    heatmap_data.astype(float),
    cmap='RdBu_r', center=0,
    annot=True, fmt='.2f', annot_kws={'size': 7},
    linewidths=0.3,
    cbar_kws={'label': '载荷值', 'shrink': 0.8},
    ax=ax
)
ax.set_xlabel('主成分')
ax.set_ylabel('金融特征')
ax.set_title(f'PCA载荷热力图（前{n_pc_show}个主成分）', fontweight='bold')
ax.tick_params(axis='y', labelsize=8, rotation=0)
ax.tick_params(axis='x', labelsize=9)
plt.tight_layout()
plt.savefig(FIG_DIR / 'pca_loading_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print(f'Saved: {FIG_DIR / "pca_loading_heatmap.png"}')

# ══════════════════════════════════════════════════════════════
# Module 6: Dimensionality-reduced prediction comparison
# ══════════════════════════════════════════════════════════════
comp_df = None
if args.plots_only:
    print('\nSkip model comparison (--plots-only).')
else:
    print('\n' + '='*60)
    print(f'Running dimensionality-reduced prediction comparison (K={K})...')

    pca_k = PCA(n_components=K)
    pca_k.fit(x_2006_scaled)

    sc_all = StandardScaler()
    x_2006_all = x_all.loc[data['year'] == years[0]]
    sc_all.fit(x_2006_all)

    x_orig_list = []
    x_pca_list = []
    y_list = []
    for yr in years:
        mask = data['year'] == yr
        xt_all = pd.DataFrame(sc_all.transform(x_all.loc[mask]), columns=feature_names)
        x_orig_list.append(xt_all)
        xt_cont = x_cont_scaled.loc[mask]
        xt_pca = pd.DataFrame(
            pca_k.transform(xt_cont),
            columns=[f'PC{i+1}' for i in range(K)]
        )
        x_pca_list.append(xt_pca)
        y_list.append(y_all.loc[mask].reset_index(drop=True))

    def rolling_eval(model_fn, x_list, y_list, n_rolls):
        metrics = {'r2_in': [], 'r2_out': [], 'mse': [], 'mae': [], 'medae': [], 'evs': []}
        for i in range(n_rolls):
            j = i + 1
            model = model_fn(x_list[i], y_list[i])
            metrics['r2_in'].append(model.score(x_list[i], y_list[i]))
            pred = model.predict(x_list[j])
            metrics['r2_out'].append(r2_score(y_list[j], pred))
            metrics['mse'].append(mean_squared_error(y_list[j], pred))
            metrics['mae'].append(mean_absolute_error(y_list[j], pred))
            metrics['medae'].append(median_absolute_error(y_list[j], pred))
            metrics['evs'].append(explained_variance_score(y_list[j], pred))
        return {k: np.mean(v) for k, v in metrics.items()}

    rf_max_features_pca = min(19, K)

    def make_rf_orig(x, y):
        m = RandomForestRegressor(n_estimators=5000, max_features=19, random_state=0, n_jobs=-1)
        m.fit(x, y)
        return m

    def make_rf_pca(x, y):
        m = RandomForestRegressor(n_estimators=5000, max_features=rf_max_features_pca, random_state=0, n_jobs=-1)
        m.fit(x, y)
        return m

    def make_gbdt_orig(x, y):
        m = GradientBoostingRegressor(n_estimators=3000, max_depth=4, subsample=0.7, learning_rate=0.001, random_state=0)
        m.fit(x, y)
        return m

    def make_gbdt_pca(x, y):
        m = GradientBoostingRegressor(n_estimators=3000, max_depth=4, subsample=0.7, learning_rate=0.001, random_state=0)
        m.fit(x, y)
        return m

    comparisons = [
        ('RF(fixed)-原始71特征', make_rf_orig, x_orig_list),
        ('RF(fixed)-PCA特征',    make_rf_pca,  x_pca_list),
        ('GBDT-原始71特征',      make_gbdt_orig, x_orig_list),
        ('GBDT-PCA特征',         make_gbdt_pca,  x_pca_list),
    ]

    comp_results = {}
    for name, fn, x_list_used in comparisons:
        t0 = time.time()
        print(f'\n  Training: {name} ({n_rolls} rolling windows)...')
        summary = rolling_eval(fn, x_list_used, y_list, n_rolls)
        elapsed = time.time() - t0
        comp_results[name] = summary
        print(f'    Done in {elapsed:.1f}s')
        print(f'    R2_in={summary["r2_in"]:.4f}  R2_out={summary["r2_out"]:.4f}  MSE={summary["mse"]:.4f}')
        log_events.append({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "phase": "Phase5", "task": f"pca_compare_{name}",
            "input": "data.csv",
            "output": "pca_model_comparison.csv",
            "status": "ok",
            "note": json.dumps(summary, ensure_ascii=False)
        })

    comp_df = pd.DataFrame(comp_results).T
    comp_df.columns = ['样本内R²', '样本外R²', 'MSE', 'MAE', 'MedAE', 'EVS']
    comp_df.index.name = '模型-特征组合'
    comp_df = comp_df.round(4)
    comp_df.to_csv(TABLE_DIR / 'pca_model_comparison.csv', encoding='utf-8-sig')
    print(f'\nSaved: {TABLE_DIR / "pca_model_comparison.csv"}')
    print('\nModel comparison:')
    print(comp_df.to_string())

# ══════════════════════════════════════════════════════════════
# Module 7: Logging
# ══════════════════════════════════════════════════════════════
log_file = LOG_DIR / 'run.log'
jsonl_file = LOG_DIR / 'events.jsonl'

with open(log_file, 'a', encoding='utf-8') as f:
    f.write(f'\n{"="*60}\n')
    f.write(f'PCA Analysis (Phase5 v2) - {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write(f'K={K}, cumulative_var={cumulative_var[K-1]:.4f}\n')
    if comp_df is not None:
        f.write(f'Model comparison:\n{comp_df.to_string()}\n')
    else:
        f.write('Model comparison: skipped (--plots-only)\n')

with open(jsonl_file, 'a', encoding='utf-8') as f:
    for evt in log_events:
        f.write(json.dumps(evt, ensure_ascii=False) + '\n')

print(f'\nLogs appended to: {log_file}')
print('PCA analysis (v2) complete.')
