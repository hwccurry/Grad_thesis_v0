# Phase5/6 图表格式审查（2026-03-02）

## 本地产物检测结论
- output/figures 共 28 张 PNG，28/28 为约 200 DPI（非 300 DPI）。
- 彩色图 8 张：did_parallel_trends、did_placebo_test、feature_importance_bar_*、pca_*、pdp_grid_*。
- scripts 中主绘图脚本仍使用 `font.sans-serif` 与 `dpi=200`，未切到统一 `THESIS_RCPARAMS`。
- `scripts/phase5_did_trends_plot.py` 尚不存在。

## 与 INSTRUCTIONS 对照
- Phase5 与 Phase6 的“目标规范”条款本身方向基本合理，但当前实现未完成。
- 需要补充“GB/T 7714 切换时点”说明：
  - 2026-03-02 当前仍以 GB/T 7714-2015 为现行。
  - GB/T 7714-2025 将于 2026-07-01 实施。

## 官方/权威来源（链接）
- GB/T 7713.1-2025（学位论文编写规则，2026-02-01 实施）
  - https://std.samr.gov.cn/gb/search/gbDetailed?id=CFDB404CCA18D6FCE06397BE0A0AFD4D
- GB/T 7713.1-2006（已被 2025 版替代）
  - https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D80174D3A7E05397BE0A0AB82A
- GB/T 7714-2015（文后参考文献著录规则，现行至 2026-06-30）
  - https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8055ED3A7E05397BE0A0AB82A
- GB/T 7714-2025（文后参考文献著录规则，2026-07-01 实施）
  - https://std.samr.gov.cn/gb/search/gbDetailed?id=CC993D3BE0003650E06397BE0A0A1BA4
- Springer Nature 图表技术要求（图表需在正文顺序引用，表题在上，图题/图例在下，彩色与灰度图分辨率建议 300dpi）
  - https://www.springer.com/gp/authors-editors/authorandreviewertutorials/submitting-to-a-journal-and-peer-review/figures-and-tables/10285556
