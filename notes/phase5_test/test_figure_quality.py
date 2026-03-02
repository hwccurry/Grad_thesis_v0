#!/usr/bin/env python3
"""
Phase 5 测试脚本：验证图表输出是否满足毕业论文格式要求
测试内容：
  1. DPI 提升到 300（原为 200）
  2. 字体切换为 Songti SC + Times New Roman（原为 sans-serif）
  3. 黑白/灰度友好配色
  4. 尺寸适配 A4 版面（单栏 8-10cm，双栏 15-17cm）

输出到 notes/phase5_test/ 以供对比
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path

ROOT = Path("/Users/mac/Desktop/Grad_thesis")
OUT_DIR = ROOT / "notes" / "phase5_test"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 论文格式 rcParams（CLAUDE.md §5.1.2 规范）──
rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Songti SC', 'SimSong', 'Times New Roman'],
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'axes.unicode_minus': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# ============================================================
# TEST 1: 特征重要性条形图（模拟数据，测试字体+DPI+灰度）
# ============================================================
print("TEST 1: Feature importance bar chart (grayscale, 300dpi, serif font)")

features_cn = [
    '上一期股利水平', '资产收益率', '留存收益资产比', '税收规避程度',
    '实际税率', '销售增长率', '纳税波动率', '资产负债率',
    '自由现金流', '中小股东持股比例'
]
importances = [0.183, 0.094, 0.066, 0.047, 0.041, 0.030, 0.028, 0.027, 0.025, 0.023]

fig, ax = plt.subplots(figsize=(4.5, 3.5))  # ~11.4cm x 8.9cm => 单栏偏大，适合重要图
ax.barh(features_cn[::-1], importances[::-1], color='#555555', edgecolor='#333333', linewidth=0.5)
ax.set_xlabel('特征重要性')
ax.set_title('随机森林特征重要性排名（Top 10）')
ax.tick_params(axis='both', which='major')
plt.tight_layout()
plt.savefig(OUT_DIR / "test1_feature_importance_300dpi.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: test1_feature_importance_300dpi.png")

# ============================================================
# TEST 2: ALE 图（模拟数据，测试线图+字体+DPI）
# ============================================================
print("TEST 2: ALE plot (single variable, 300dpi, serif font)")

x_vals = np.linspace(-4, 2, 50)
y_vals = np.where(x_vals < -0.5, -0.11 + 0.04 * (x_vals + 4), 0.01 + 0.01 * x_vals)

fig, ax = plt.subplots(figsize=(3.5, 2.8))  # ~8.9cm x 7.1cm => 单栏
ax.plot(x_vals, y_vals, color='black', linewidth=1.5)
ax.set_xlabel('留存收益资产比')
ax.set_ylabel('股利支付率')
ax.set_title('ALE图 - 随机森林')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
plt.tight_layout()
plt.savefig(OUT_DIR / "test2_ale_300dpi.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: test2_ale_300dpi.png")

# ============================================================
# TEST 3: 平行趋势图（模拟事件研究，测试双面板+置信区间）
# ============================================================
print("TEST 3: Parallel trends event study (dual panel, 300dpi)")

time_labels = ['t-3', 't-2', 't-1\n(基准)', 't', 't+1']
coefs_dd = [0.04, 0.023, 0.0, 0.107, 0.096]
ci_dd = [0.05, 0.045, 0.0, 0.045, 0.04]
coefs_dp = [0.035, 0.033, 0.0, 0.13, 0.10]
ci_dp = [0.04, 0.035, 0.0, 0.06, 0.05]

fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))  # ~16cm x 7.1cm => 双栏

for idx, (coefs, ci, title) in enumerate([
    (coefs_dd, ci_dd, '分红意愿（DivDummy）'),
    (coefs_dp, ci_dp, '分红水平（DivPayRate）')
]):
    ax = axes[idx]
    ax.errorbar(range(len(coefs)), coefs, yerr=ci,
                fmt='o-', color='black', markersize=4, linewidth=1.2,
                capsize=3, capthick=0.8, elinewidth=0.8)
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.axvline(x=2.5, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
    ax.set_xticks(range(len(time_labels)))
    ax.set_xticklabels(time_labels)
    ax.set_xlabel('政策实施相对时间（年）')
    ax.set_ylabel('回归系数（99%置信区间）')
    ax.set_title(title)

plt.tight_layout()
plt.savefig(OUT_DIR / "test3_parallel_trends_300dpi.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: test3_parallel_trends_300dpi.png")

# ============================================================
# TEST 4: 安慰剂检验核密度图（测试直方图+KDE+灰度）
# ============================================================
print("TEST 4: Placebo test kernel density (grayscale, 300dpi)")
from scipy.stats import gaussian_kde

np.random.seed(42)
placebo = np.random.normal(0, 0.012, 100)
true_coef = 0.0828

fig, ax = plt.subplots(figsize=(3.5, 2.8))  # 单栏
ax.hist(placebo, bins=20, density=True, alpha=0.5, color='#888888', edgecolor='white')
kde = gaussian_kde(placebo)
x_range = np.linspace(placebo.min() - 0.01, 0.10, 200)
ax.plot(x_range, kde(x_range), color='black', linewidth=1.2)
ax.axvline(x=true_coef, color='black', linestyle='--', linewidth=1.5,
           label=f'真实DID系数 = {true_coef:.4f}')
ax.set_xlabel('估计系数')
ax.set_ylabel('密度')
ax.set_title('安慰剂检验: 分红意愿（DivDummy）')
ax.legend(fontsize=8, frameon=False)
plt.tight_layout()
plt.savefig(OUT_DIR / "test4_placebo_300dpi.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: test4_placebo_300dpi.png")

# ============================================================
# TEST 5: PCA 碎石图（测试双轴+注释+灰度）
# ============================================================
print("TEST 5: PCA scree plot (dual-axis, grayscale, 300dpi)")

n_comp = 20
var_pct = np.array([12.7, 10.5, 7.9, 5.8, 4.7, 4.1, 3.7, 3.6, 3.4, 3.3,
                     3.2, 3.0, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1])
cum_pct = np.cumsum(var_pct)

fig, ax1 = plt.subplots(figsize=(5.5, 3.0))  # ~14cm x 7.6cm
ax2 = ax1.twinx()

ax1.bar(range(1, n_comp+1), var_pct, color='#999999', edgecolor='#666666', linewidth=0.5, label='单个方差占比')
ax2.plot(range(1, n_comp+1), cum_pct, 'ko-', markersize=3, linewidth=1.2, label='累积方差占比')

ax2.axhline(y=80, color='gray', linestyle='--', linewidth=0.8)
ax2.annotate('80%阈值, K=18 (81.4%)', xy=(18, cum_pct[17]),
             xytext=(14, cum_pct[17]+4), fontsize=8,
             arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

ax1.set_xlabel('主成分编号')
ax1.set_ylabel('解释方差占比 (%)')
ax2.set_ylabel('累积解释方差占比 (%)')
ax1.set_title('PCA碎石图（35个连续金融特征）')
ax1.set_xticks(range(1, n_comp+1))

plt.tight_layout()
plt.savefig(OUT_DIR / "test5_pca_scree_300dpi.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: test5_pca_scree_300dpi.png")

# ============================================================
# 验证输出文件信息
# ============================================================
print("\n=== Output file summary ===")
for f in sorted(OUT_DIR.glob("test*.png")):
    from PIL import Image
    img = Image.open(f)
    print(f"  {f.name}: {img.size[0]}x{img.size[1]}px, DPI={img.info.get('dpi', 'N/A')}, size={f.stat().st_size/1024:.0f}KB")

print("\nAll tests completed.")
