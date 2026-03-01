#!/usr/bin/env python3
"""
Phase 3 补充：基于已导出的 placebo 系数重绘核密度分布图
输入文件：
- output/tables/did_placebo_DivDummy.csv
- output/tables/did_placebo_DivPayRate.csv
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import gaussian_kde
from pathlib import Path

rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "Heiti SC"]
rcParams["axes.unicode_minus"] = False

ROOT = Path("/Users/mac/Desktop/Grad_thesis")
TABLE_DIR = ROOT / "output" / "tables"
FIG_PATH = ROOT / "output" / "figures" / "did_placebo_test.png"

placebo_DivDummy = pd.read_csv(TABLE_DIR / "did_placebo_DivDummy.csv")["placebo_coef"].dropna().to_numpy()
placebo_DivPayRate = pd.read_csv(TABLE_DIR / "did_placebo_DivPayRate.csv")["placebo_coef"].dropna().to_numpy()

true_coefs = {"DivDummy": 0.0828, "DivPayRate": 0.1081}

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for idx, (y_var, coefs) in enumerate([("DivDummy", placebo_DivDummy),
                                       ("DivPayRate", placebo_DivPayRate)]):
    ax = axes[idx]
    ax.hist(coefs, bins=25, density=True, alpha=0.6, color='#3498db', edgecolor='white')

    kde = gaussian_kde(coefs)
    x_range = np.linspace(min(coefs) - 0.01, max(coefs) + 0.01, 200)
    ax.plot(x_range, kde(x_range), color='#2c3e50', linewidth=1.5)

    ax.axvline(x=true_coefs[y_var], color='red', linestyle='--', linewidth=2,
               label=f"真实DID系数 = {true_coefs[y_var]:.4f}")

    title = "分红意愿（DivDummy）" if y_var == "DivDummy" else "分红水平（DivPayRate）"
    ax.set_title(f"安慰剂检验: {title}")
    ax.set_xlabel("估计系数")
    ax.set_ylabel("密度")
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_PATH, dpi=200, bbox_inches="tight")
plt.close()
print(
    "安慰剂检验图已更新:",
    FIG_PATH,
    f"| DivDummy mean={placebo_DivDummy.mean():.6f} sd={placebo_DivDummy.std(ddof=1):.6f} n={len(placebo_DivDummy)}",
    f"| DivPayRate mean={placebo_DivPayRate.mean():.6f} sd={placebo_DivPayRate.std(ddof=1):.6f} n={len(placebo_DivPayRate)}",
)
