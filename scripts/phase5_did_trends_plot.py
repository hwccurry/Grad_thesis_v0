#!/usr/bin/env python3
"""
Phase 5 - Task 5.5: DID parallel trends (event study) plot
Reads event study coefficients from CSV and plots dual-panel figure.
Input:  output/tables/did_event_study_DivDummy.csv
        output/tables/did_event_study_DivPayRate.csv
Output: output/figures_v2/did_parallel_trends.png
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_plot_config import apply_thesis_style, BLACK_LINE, GRAY_LIGHT

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
    PANEL_COLORS = ["#4E79A7", "#E15759"]
else:
    PANEL_COLORS = [BLACK_LINE, BLACK_LINE]

# ── Load event study data ──
df_dummy = pd.read_csv(TABLE_DIR / "did_event_study_DivDummy.csv")
df_rate = pd.read_csv(TABLE_DIR / "did_event_study_DivPayRate.csv")

# Map variable names to relative time periods
time_map = {'pre_3': -3, 'pre_2': -2, 'current': 0, 'time_1': 1}

def prepare_data(df):
    """Add time period and pre_1 baseline row (coef=0, CI=0)."""
    df = df.copy()
    df['time'] = df['Variable'].map(time_map)
    # Add baseline period (pre_1, t=-1) with coef=0
    baseline = pd.DataFrame({
        'Variable': ['pre_1'], 'Coef': [0.0], 'SE': [0.0],
        't-stat': [np.nan], 'p-value': [np.nan],
        'CI_low': [0.0], 'CI_high': [0.0], 'time': [-1]
    })
    df = pd.concat([df, baseline], ignore_index=True)
    df = df.sort_values('time').reset_index(drop=True)
    return df

df_dummy = prepare_data(df_dummy)
df_rate = prepare_data(df_rate)

# ── Plot dual-panel event study ──
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))

time_labels = {-3: 't-3', -2: 't-2', -1: 't-1\n(基期)', 0: 't', 1: 't+1'}

for idx, (ax, df, title) in enumerate([
    (axes[0], df_dummy, '分红意愿（DivDummy）'),
    (axes[1], df_rate, '分红水平（DivPayRate）'),
]):
    panel_color = PANEL_COLORS[idx]
    t = df['time'].values
    coef = df['Coef'].values
    ci_low = df['CI_low'].values
    ci_high = df['CI_high'].values

    # Reference line at y=0
    ax.axhline(y=0, color=GRAY_LIGHT, linestyle='-', linewidth=0.6)

    # Vertical line separating pre/post
    ax.axvline(x=-0.5, color=GRAY_LIGHT, linestyle=':', linewidth=0.6)

    # Error bars: coefficient +/- CI
    ax.errorbar(t, coef, yerr=[coef - ci_low, ci_high - coef],
                fmt='o', color=panel_color, markersize=4,
                capsize=3, capthick=1, linewidth=1, elinewidth=0.8)

    # Connect points
    ax.plot(t, coef, '-', color=panel_color, linewidth=0.8, alpha=0.6)

    ax.set_xticks(sorted(time_labels.keys()))
    ax.set_xticklabels([time_labels[k] for k in sorted(time_labels.keys())])
    ax.set_xlabel('相对时期')
    ax.set_ylabel('DID估计系数')
    ax.set_title(title)

plt.tight_layout()
FIG_PATH = FIG_DIR / "did_parallel_trends.png"
plt.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {FIG_PATH}")
