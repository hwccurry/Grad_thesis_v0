# Phase 6 交付审计报告

- 生成时间：2026-03-02 19:56:05 +0800
- 审计对象：`output/paper/论文完整版.md`、`output/paper/论文完整版_phase6.docx`

## 1. 文本占位符检查
- 结果：通过
- 命中数量：0
- 命中明细：无

## 2. 图像链接与分辨率检查
- 图像总数：12
- 结果：通过

| 链接 | 文件 | 存在 | DPI | 通过 |
| --- | --- | --- | --- | --- |
| `../figures_v2/feature_importance_bar_rf.png` | `output/figures_v2/feature_importance_bar_rf.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/feature_importance_bar_gbdt.png` | `output/figures_v2/feature_importance_bar_gbdt.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/ale_rf_Retainedearn_ratio.png` | `output/figures_v2/ale_rf_Retainedearn_ratio.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/ale_rf_Tunneling.png` | `output/figures_v2/ale_rf_Tunneling.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/ale_rf_Constraint.png` | `output/figures_v2/ale_rf_Constraint.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/ale_rf_ROA.png` | `output/figures_v2/ale_rf_ROA.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/pdp_grid_rf.png` | `output/figures_v2/pdp_grid_rf.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/pdp_grid_gbdt.png` | `output/figures_v2/pdp_grid_gbdt.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/pca_scree_plot.png` | `output/figures_v2/pca_scree_plot.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/pca_loading_heatmap.png` | `output/figures_v2/pca_loading_heatmap.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/did_parallel_trends.png` | `output/figures_v2/did_parallel_trends.png` | 是 | 300.0x300.0 | 是 |
| `../figures_v2/did_placebo_test.png` | `output/figures_v2/did_placebo_test.png` | 是 | 300.0x300.0 | 是 |

## 3. 表图编号连续性
- 图编号检查：通过（1–12 连续）
- 表编号检查：通过（1–11 连续）

## 4. DID 关键系数复验
- 结果：通过
- DivDummy/否: Δcoef=0.000023, Δt=0.000004, ok
- DivDummy/是: Δcoef=0.000001, Δt=0.000046, ok
- DivPayRate/否: Δcoef=0.000031, Δt=0.000009, ok
- DivPayRate/是: Δcoef=0.000026, Δt=0.000045, ok

## 5. DOCX 导出结构摘要
- 结果：已导出
- 文件大小：1793791 bytes
- 段落数：263
- 表格数：11
- 图片数：12
- Heading 段落数：58

## 6. 结论
- 自动化审计结论：通过
- 说明：Word 版式细节（页眉页脚、三线表线宽、字体混排）仍需人工终检。
