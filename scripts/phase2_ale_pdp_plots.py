"""
Phase 5 - Task 5.2: ALE + PDP + Feature Importance plots (v2)
Rewritten for thesis format: 300 DPI, serif fonts, grayscale-friendly, A4 figsize.
Models saved to output/models/ for future reuse.
All figures output to output/figures_v2/ by default.

Optional env:
  THESIS_FIG_SUBDIR=figures_v3
  THESIS_COLOR_MODE=color  # default: mono
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Ensure scripts/ is on path for thesis_plot_config import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_plot_config import apply_thesis_style, GRAY_BAR, GRAY_BAR_EDGE, BLACK_LINE

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
apply_thesis_style()

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import partial_dependence
from sklearn.model_selection import train_test_split
import joblib
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
FIG_SUBDIR = os.getenv('THESIS_FIG_SUBDIR', 'figures_v2')
FIG_DIR = PROJECT_ROOT / 'output' / FIG_SUBDIR
MODEL_DIR = PROJECT_ROOT / 'output' / 'models'
FIG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
COLOR_MODE = os.getenv('THESIS_COLOR_MODE', 'mono').lower()
if COLOR_MODE == 'color':
    LINE_COLOR_RF = '#4E79A7'
    LINE_COLOR_GBDT = '#E15759'
    BAR_COLOR_RF = '#4E79A7'
    BAR_COLOR_GBDT = '#E15759'
    BAR_EDGE_RF = '#2F4B6A'
    BAR_EDGE_GBDT = '#9C2F2F'
else:
    LINE_COLOR_RF = BLACK_LINE
    LINE_COLOR_GBDT = BLACK_LINE
    BAR_COLOR_RF = GRAY_BAR
    BAR_COLOR_GBDT = GRAY_BAR
    BAR_EDGE_RF = GRAY_BAR_EDGE
    BAR_EDGE_GBDT = GRAY_BAR_EDGE

# ── ALE helper functions ──
def _get_quantiles(train_set, feature, bins):
    quantiles = np.unique(
        np.quantile(train_set[feature], np.linspace(0, 1, bins + 1), method="lower")
    )
    bins = len(quantiles) - 1
    return quantiles, bins

def _get_centres(x):
    return (x[1:] + x[:-1]) / 2

def _first_order_ale_quant(predictor, train_set, feature, bins):
    quantiles, _ = _get_quantiles(train_set, feature, bins)
    indices = np.clip(
        np.digitize(train_set[feature], quantiles, right=True) - 1, 0, None
    )
    predictions = []
    for offset in range(2):
        mod_train_set = train_set.copy()
        mod_train_set[feature] = quantiles[indices + offset]
        predictions.append(predictor(mod_train_set))
    effects = predictions[1] - predictions[0]
    index_groupby = pd.DataFrame({"index": indices, "effects": effects}).groupby("index")
    mean_effects = index_groupby.mean().to_numpy().flatten()
    ale = np.array([0, *np.cumsum(mean_effects)])
    ale = _get_centres(ale)
    ale -= np.sum(ale * index_groupby.size() / train_set.shape[0])
    return ale, quantiles

def ale_plot(model, train_set, feature, feature_cn, model_name, save_path, line_color, bins=10):
    """Plot ALE for a single feature — thesis format."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ale, quantiles = _first_order_ale_quant(model.predict, train_set, feature, bins)
    centres = _get_centres(quantiles)
    ax.plot(centres, ale, color=line_color, linewidth=1.2)
    ax.set_xlim(train_set[feature].min(), train_set[feature].max())
    min_ale, max_ale = min(ale), max(ale)
    buffer = (max_ale - min_ale) * 0.1 if max_ale != min_ale else 0.01
    ax.set_ylim(min_ale - buffer, max_ale + buffer)
    ax.set_xlabel(feature_cn)
    ax.set_ylabel('股利支付率')
    ax.set_title(f'ALE图\u2014{model_name}')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {save_path.name}')

# ── Load data ──
data = pd.read_csv(DATA_DIR / 'data.csv')
x = data.iloc[:, 6:]
y = data.iloc[:, 2]  # Dividend_ratio1

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=0)
sc = StandardScaler()
sc.fit(x_train)
x_train_sc = pd.DataFrame(sc.transform(x_train), columns=x.columns)
x_test_sc = pd.DataFrame(sc.transform(x_test), columns=x.columns)

# ── Top features to plot ──
top_features = [
    ('Retainedearn_ratio', '留存收益资产比'),
    ('Tunneling',          '其他应收款资产比'),
    ('Dividend_lag',       '上一期股利水平'),
    ('Constraint',         '融资约束程度'),
    ('Tax_ratio',          '实际税率'),
    ('Tax_volatility',     '纳税波动率'),
    ('Institution',        '机构投资者持股比例'),
    ('Freecash2',          '自由现金流'),
    ('ROA',                '资产收益率'),
    ('Cashflow',           '每股经营活动现金流量'),
]

# ── Train GBDT ──
gbdt_model_path = MODEL_DIR / 'gbdt_model.joblib'
rf_model_path = MODEL_DIR / 'rf_model.joblib'
if gbdt_model_path.exists() and rf_model_path.exists():
    print('Loading existing models from output/models/ ...')
    model_gbdt = joblib.load(gbdt_model_path)
    model_rf = joblib.load(rf_model_path)
    print(f'  Loaded: {gbdt_model_path.name}, {rf_model_path.name}')
else:
    print('Training GBDT (n_estimators=3000)...')
    model_gbdt = GradientBoostingRegressor(
        n_estimators=3000, max_depth=4, subsample=0.7,
        learning_rate=0.001, random_state=0
    )
    model_gbdt.fit(x_train_sc, y_train)
    joblib.dump(model_gbdt, gbdt_model_path)
    print(f'  GBDT done. Saved to {gbdt_model_path}')

    print('Training RF (n_estimators=5000)...')
    model_rf = RandomForestRegressor(n_estimators=5000, max_features=19, random_state=0, n_jobs=-1)
    model_rf.fit(x_train_sc, y_train)
    joblib.dump(model_rf, rf_model_path)
    print(f'  RF done. Saved to {rf_model_path}')

# ── Generate ALE plots (20 figures) ──
print('\nGenerating ALE plots (20 figures)...')
for feat, feat_cn in top_features:
    ale_plot(model_rf, x_test_sc, feat, feat_cn, '随机森林',
             FIG_DIR / f'ale_rf_{feat}.png', line_color=LINE_COLOR_RF)
    ale_plot(model_gbdt, x_test_sc, feat, feat_cn, '梯度提升树',
             FIG_DIR / f'ale_gbdt_{feat}.png', line_color=LINE_COLOR_GBDT)

# ── Feature importance bar chart (Top 10, 2 figures) ──
print('\nGenerating feature importance bar charts (Top 10)...')

en_to_cn = {
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

for model, model_name, fname, bar_color, edge_color in [
    (model_rf, '随机森林', 'feature_importance_bar_rf.png', BAR_COLOR_RF, BAR_EDGE_RF),
    (model_gbdt, '梯度提升树', 'feature_importance_bar_gbdt.png', BAR_COLOR_GBDT, BAR_EDGE_GBDT),
]:
    imp = model.feature_importances_
    feat_imp = pd.DataFrame({'feature': x.columns, 'importance': imp})
    feat_imp = feat_imp[~feat_imp['feature'].str.startswith('ind')]
    feat_imp = feat_imp.sort_values('importance', ascending=True).tail(10)
    feat_imp['feature_cn'] = feat_imp['feature'].map(en_to_cn).fillna(feat_imp['feature'])

    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.barh(feat_imp['feature_cn'], feat_imp['importance'],
            color=bar_color, edgecolor=edge_color, linewidth=0.5)
    ax.set_xlabel('特征重要性')
    ax.set_title(f'{model_name}特征重要性排名（Top 10）')
    plt.tight_layout()
    plt.savefig(FIG_DIR / fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {fname}')

# ── PDP grid (2x2) for each model (2 figures) ──
print('\nGenerating PDP grid plots...')
top4 = ['Retainedearn_ratio', 'Tunneling', 'Dividend_lag', 'Constraint']
top4_cn = ['留存收益资产比', '其他应收款资产比', '上一期股利水平', '融资约束程度']

for model, model_name, fname, line_color in [
    (model_rf, '随机森林', 'pdp_grid_rf.png', LINE_COLOR_RF),
    (model_gbdt, '梯度提升树', 'pdp_grid_gbdt.png', LINE_COLOR_GBDT),
]:
    fig, axes = plt.subplots(2, 2, figsize=(6.3, 5.0))
    for idx, (feat, feat_cn) in enumerate(zip(top4, top4_cn)):
        ax = axes[idx // 2][idx % 2]
        # Compute PDP manually to control labels and line color
        pdp_result = partial_dependence(
            model, x_test_sc, features=[feat],
            grid_resolution=50, method='brute'
        )
        grid_values = pdp_result['grid_values'][0]
        avg_preds = pdp_result['average'][0]
        ax.plot(grid_values, avg_preds, color=line_color, linewidth=1.2)
        ax.set_xlabel(feat_cn)
        ax.set_ylabel('偏依赖值')
        ax.set_title(f'{model_name}\u2014{feat_cn}')
    plt.suptitle(f'{model_name}偏依赖图（PDP）', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {fname}')

print(f'\nAll ALE/PDP/FI plots generated in {FIG_DIR}/')
print(f'Models saved in {MODEL_DIR}/')
