#!/usr/bin/env python3
"""
Phase 5 - Task 5.4: Placebo test density plot (v2)
Rewritten for thesis format: 300 DPI, serif fonts, grayscale-friendly.
Input:  output/tables/did_placebo_DivDummy.csv, did_placebo_DivPayRate.csv
Output: output/figures_v2/did_placebo_test.png
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import gaussian_kde

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_plot_config import apply_thesis_style, GRAY_HIST, GRAY_BAR_EDGE, BLACK_LINE, GRAY_LIGHT

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
apply_thesis_style()

ROOT = Path("/Users/mac/Desktop/Grad_thesis")
TABLE_DIR = ROOT / "output" / "tables"
FIG_SUBDIR = os.getenv("THESIS_FIG_SUBDIR", "figures_v2")
FIG_DIR = ROOT / "output" / FIG_SUBDIR
FIG_DIR.mkdir(parents=True, exist_ok=True)
COLOR_MODE = os.getenv("THESIS_COLOR_MODE", "mono").lower()
if COLOR_MODE == "color":
    HIST_COLORS = ["#4E79A7", "#E15759"]
    KDE_COLORS = ["#2F4B6A", "#9C2F2F"]
else:
    HIST_COLORS = [GRAY_HIST, GRAY_HIST]
    KDE_COLORS = [BLACK_LINE, BLACK_LINE]

placebo_DivDummy = pd.read_csv(TABLE_DIR / "did_placebo_DivDummy.csv")["placebo_coef"].dropna().to_numpy()
placebo_DivPayRate = pd.read_csv(TABLE_DIR / "did_placebo_DivPayRate.csv")["placebo_coef"].dropna().to_numpy()

true_coefs = {"DivDummy": 0.0828, "DivPayRate": 0.1081}

fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))

for idx, (y_var, coefs) in enumerate([("DivDummy", placebo_DivDummy),
                                       ("DivPayRate", placebo_DivPayRate)]):
    ax = axes[idx]
    ax.hist(coefs, bins=25, density=True, alpha=0.7,
            color=HIST_COLORS[idx], edgecolor=GRAY_BAR_EDGE, linewidth=0.5)

    kde = gaussian_kde(coefs)
    x_range = np.linspace(min(coefs) - 0.01, max(coefs) + 0.01, 200)
    ax.plot(x_range, kde(x_range), color=KDE_COLORS[idx], linewidth=1.2)

    ax.axvline(x=true_coefs[y_var], color=BLACK_LINE, linestyle='--', linewidth=1.5,
               label=f"真实DID系数 = {true_coefs[y_var]:.4f}")

    title = "分红意愿（DivDummy）" if y_var == "DivDummy" else "分红水平（DivPayRate）"
    ax.set_title(f"安慰剂检验: {title}")
    ax.set_xlabel("估计系数")
    ax.set_ylabel("密度")
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(axis='y', alpha=0.2, color=GRAY_LIGHT)

plt.tight_layout()
FIG_PATH = FIG_DIR / "did_placebo_test.png"
plt.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
plt.close()
print(
    "Saved:", FIG_PATH,
    f"| DivDummy mean={placebo_DivDummy.mean():.6f} sd={placebo_DivDummy.std(ddof=1):.6f} n={len(placebo_DivDummy)}",
    f"| DivPayRate mean={placebo_DivPayRate.mean():.6f} sd={placebo_DivPayRate.std(ddof=1):.6f} n={len(placebo_DivPayRate)}",
)
