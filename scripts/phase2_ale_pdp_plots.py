"""
Phase 2 - Task 2.3: ALE + PDP plots for top features
训练 GBDT 和 RF 在全样本上, 对 Top-6 关键变量绘制 ALE 图。
输出到 output/figures/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import PartialDependenceDisplay
from sklearn.model_selection import train_test_split
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
FIG_DIR = PROJECT_ROOT / 'output' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── Chinese font setup ──
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Heiti SC', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

# ── ALE helper functions (from reference notebook) ──
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

def ale_plot(model, train_set, feature, feature_cn, model_name, save_path, bins=10):
    """Plot ALE for a single feature."""
    fig, ax = plt.subplots(figsize=(5, 4))
    ale, quantiles = _first_order_ale_quant(model.predict, train_set, feature, bins)
    centres = _get_centres(quantiles)
    ax.plot(centres, ale, color='black', linewidth=1.5)
    ax.set_xlim(train_set[feature].min(), train_set[feature].max())
    min_ale, max_ale = min(ale), max(ale)
    buffer = (max_ale - min_ale) * 0.1 if max_ale != min_ale else 0.01
    ax.set_ylim(min_ale - buffer, max_ale + buffer)
    ax.set_xlabel(feature_cn, fontsize=13)
    ax.set_ylabel('股利支付率', fontsize=13)
    ax.set_title(f'ALE图-{model_name}', fontsize=13)
    ax.tick_params(labelsize=11)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
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

# ── Top features to plot (based on reference paper + H1 hypothesis) ──
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
print('Training GBDT for ALE/PDP plots...')
model_gbdt = GradientBoostingRegressor(
    n_estimators=3000, max_depth=4, subsample=0.7,
    learning_rate=0.001, random_state=0
)
model_gbdt.fit(x_train_sc, y_train)
print('  GBDT done.')

# ── Train RF ──
print('Training RF for ALE/PDP plots...')
model_rf = RandomForestRegressor(n_estimators=5000, max_features=19, random_state=0, n_jobs=-1)
model_rf.fit(x_train_sc, y_train)
print('  RF done.')

# ── Generate ALE plots ──
print('\nGenerating ALE plots...')
for feat, feat_cn in top_features:
    ale_plot(model_rf, x_test_sc, feat, feat_cn, '随机森林',
             FIG_DIR / f'ale_rf_{feat}.png')
    ale_plot(model_gbdt, x_test_sc, feat, feat_cn, '梯度提升树',
             FIG_DIR / f'ale_gbdt_{feat}.png')

# ── Generate feature importance bar chart ──
print('\nGenerating feature importance bar charts...')

# English→Chinese mapping for non-dummy features
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

for model, model_name, fname in [
    (model_rf, '随机森林', 'feature_importance_bar_rf.png'),
    (model_gbdt, '梯度提升树', 'feature_importance_bar_gbdt.png'),
]:
    imp = model.feature_importances_
    feat_imp = pd.DataFrame({'feature': x.columns, 'importance': imp})
    # Only show non-dummy features (top 20)
    feat_imp = feat_imp[~feat_imp['feature'].str.startswith('ind')]
    feat_imp = feat_imp.sort_values('importance', ascending=True).tail(20)
    feat_imp['feature_cn'] = feat_imp['feature'].map(en_to_cn).fillna(feat_imp['feature'])

    fig, ax = plt.subplots(figsize=(7, 8))
    ax.barh(feat_imp['feature_cn'], feat_imp['importance'], color='steelblue')
    ax.set_xlabel('特征重要性', fontsize=13)
    ax.set_title(f'{model_name}特征重要性排名（非行业变量Top 20）', fontsize=13)
    ax.tick_params(labelsize=11)
    plt.tight_layout()
    plt.savefig(FIG_DIR / fname, dpi=200, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {fname}')

# ── PDP for top 4 features (2x2 grid) for each model ──
print('\nGenerating PDP grid plots...')
top4 = ['Retainedearn_ratio', 'Tunneling', 'Dividend_lag', 'Constraint']
top4_cn = ['留存收益资产比', '其他应收款资产比', '上一期股利水平', '融资约束程度']

for model, model_name, fname in [
    (model_rf, '随机森林', 'pdp_grid_rf.png'),
    (model_gbdt, '梯度提升树', 'pdp_grid_gbdt.png'),
]:
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for idx, (feat, feat_cn) in enumerate(zip(top4, top4_cn)):
        ax = axes[idx // 2][idx % 2]
        PartialDependenceDisplay.from_estimator(
            model, x_test_sc, [feat],
            grid_resolution=50, n_jobs=-1, method='brute', ax=ax
        )
        ax.set_xlabel(feat_cn, fontsize=11)
        ax.set_ylabel('偏依赖值', fontsize=11)
        ax.set_title(f'{model_name} - {feat_cn}', fontsize=11)
    plt.suptitle(f'{model_name}偏依赖图（PDP）', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / fname, dpi=200, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {fname}')

print('\nAll ALE/PDP plots generated in output/figures/')
