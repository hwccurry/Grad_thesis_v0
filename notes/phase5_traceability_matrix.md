# Phase 5 图表-结论追溯矩阵

- 生成时间：2026-03-02 13:14:13 +0800
- 用途：答辩前快速核对“结论-表图-脚本-正文位置”一致性。

| 结论 | 对应表格 | 对应图形 | 复现脚本 | 正文位置 |
| --- | --- | --- | --- | --- |
| H1：生命周期/代理成本是关键动因 | output/tables/model_comparison_ch3.csv; output/tables/feature_importance_RF_fixed.csv; output/tables/feature_importance_GBDT.csv; output/tables/subsample_robustness_ch3.csv; output/tables/pca_model_comparison.csv | output/figures/feature_importance_bar_rf.png; output/figures/feature_importance_bar_gbdt.png; output/figures/pca_scree_plot.png; output/figures/pca_loading_heatmap.png | scripts/phase2_ml_training.py; scripts/phase2_rf_and_summary.py; scripts/phase2_ale_pdp_plots.py; scripts/phase2_subsample.py; scripts/phase2_pca_analysis.py | output/paper/chapter3_ml_prediction_draft.md |
| H2：政策显著提高分红意愿与水平 | output/tables/did_baseline_regression.csv; output/tables/did_event_study_DivDummy.csv; output/tables/did_event_study_DivPayRate.csv; output/tables/did_robustness_checks.csv; output/tables/did_placebo_DivDummy.csv; output/tables/did_placebo_DivPayRate.csv | output/figures/did_parallel_trends.png; output/figures/did_placebo_test.png | scripts/phase3_did_stata_replication.do; scripts/phase3_placebo_stata100.do; scripts/phase3_placebo_plot.py | output/paper/chapter4_did_evaluation_draft.md |
| H3：高代理成本组政策效应更强 | output/tables/did_heterogeneity.csv | （无独立图，结论来自表10） | scripts/phase3_did_stata_replication.do | output/paper/chapter4_did_evaluation_draft.md |
| 市场后果：流动性提升、错误定价下降 | output/tables/did_economic_consequences.csv | （当前无单独图，必要时可补绘） | scripts/phase3_did_stata_replication.do | output/paper/chapter4_did_evaluation_draft.md; output/paper/chapter5_conclusion_draft.md |

