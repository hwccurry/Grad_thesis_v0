"""
thesis_plot_config.py — Phase 5 shared plotting configuration

All thesis figures must import and apply this config for consistency:
  - 300 DPI
  - Serif fonts: Songti SC (Chinese) + Times New Roman (English/numbers)
  - Grayscale-friendly color palette
  - A4-compatible figure sizes

Usage:
    from thesis_plot_config import apply_thesis_style, GRAY_BAR, BLACK_LINE, ...
    apply_thesis_style()
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── rcParams for thesis figures ──
THESIS_RCPARAMS = {
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
}

# ── Grayscale-friendly color palette ──
GRAY_BAR = '#555555'        # bar chart fill
GRAY_BAR_EDGE = '#333333'   # bar chart edge
BLACK_LINE = 'black'        # line plots / ALE curves
GRAY_HIST = '#888888'       # histogram fill
GRAY_LIGHT = '#999999'      # auxiliary elements (reference lines, etc.)
GRAY_DARK = '#444444'       # secondary emphasis

# For multi-category plots (still print-friendly)
PALETTE_PRINT_FRIENDLY = ['#333333', '#777777', '#AAAAAA', '#DDDDDD']


def apply_thesis_style():
    """Apply THESIS_RCPARAMS to matplotlib globally."""
    plt.rcParams.update(THESIS_RCPARAMS)
