"""
将随机森林和梯度提升树特征重要性 Top 10 合并为一张左右并排双面板图。
直接从已有 CSV 表格读取（output/tables/），无需重新训练。
输出到 output/figures_v2/feature_importance_combined.png
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_plot_config import apply_thesis_style, GRAY_BAR, GRAY_BAR_EDGE

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
apply_thesis_style()

import pandas as pd

# ── 路径 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / 'output' / 'figures_v2'
TABLE_DIR = PROJECT_ROOT / 'output' / 'tables'

# ── 英文→中文变量映射 ──
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

# ── 从 CSV 读取 Top 10 ──
def load_top10(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    df = df.head(10).sort_values('平均重要性', ascending=True)
    df['feature_cn'] = df['变量'].map(en_to_cn).fillna(df['变量'])
    return df

top10_rf = load_top10(TABLE_DIR / 'feature_importance_RF_fixed.csv')
top10_gbdt = load_top10(TABLE_DIR / 'feature_importance_GBDT.csv')

# ── 双面板绘图 ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 3.5))

# 左面板：随机森林
ax1.barh(top10_rf['feature_cn'], top10_rf['平均重要性'],
         color=GRAY_BAR, edgecolor=GRAY_BAR_EDGE, linewidth=0.5)
ax1.set_xlabel('特征重要性')
ax1.set_title('(a) 随机森林', fontsize=10)

# 右面板：梯度提升树
ax2.barh(top10_gbdt['feature_cn'], top10_gbdt['平均重要性'],
         color=GRAY_BAR, edgecolor=GRAY_BAR_EDGE, linewidth=0.5)
ax2.set_xlabel('特征重要性')
ax2.set_title('(b) 梯度提升树', fontsize=10)

plt.tight_layout(w_pad=2.0)
out_path = FIG_DIR / 'feature_importance_combined.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print(f'已保存: {out_path}')
