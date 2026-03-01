# Repository Document Tree

更新时间：2026-03-01 (Phase 3 收口复核后)
维护规则：每个 Phase 完成后必须同步更新本文件。

## 根目录
```text
Grad_thesis/
├── INSTRUCTIONS.md
├── DOC_TREE.md
├── CLAUDE.md
├── README.md
├── memory.md
├── 写作框架.md
├── 商学院本科生毕业论文格式模板2025.01.docx
├── notes/
├── output/
├── logs/
├── scripts/
└── 参考文献/
```

## 关键文件说明
- `INSTRUCTIONS.md`：项目总流程、Phase 任务、检查点、全局约束。
- `DOC_TREE.md`：仓库结构说明（本文件）。
- `memory.md`：跨会话决策与执行日志。
- `写作框架.md`：导师给出的章节框架与写作要求。
- `商学院本科生毕业论文格式模板2025.01.docx`：学校格式模板（排版与引用规则基准）。

## notes/
```text
notes/
├── checkpoints.md
├── data_code_inventory.md
├── path_unification.md
├── repro_env.md
├── literature_pool_phase1.md
├── hypothesis_mapping.md
├── phase1_refs_for_zotero.bib
├── did_design.md                                 # [Phase3新增] DID准自然实验设计文档
├── phase3_review_report.md                       # [Phase3收口] 风险审阅与答辩口径
└── phase3_reference_do_comparison_20260301.md   # [Phase3收口] 与参考do复跑对照
```
- `checkpoints.md`：各阶段完成状态。
- `data_code_inventory.md`：数据/代码盘点。
- `path_unification.md`：路径统一策略与改造记录。
- `repro_env.md`：最小复现环境与命令。
- `literature_pool_phase1.md`：Phase1 文献池与核验链接。
- `hypothesis_mapping.md`：H1/H2/H3 映射。
- `phase1_refs_for_zotero.bib`：Zotero 导入用 BibTeX。
- `did_design.md`：Phase3 DID实验设计（政策背景、处理组定义、模型设定、检验策略）。
- `phase3_review_report.md`：Phase3 风险复核、答辩解释口径与收口结论。
- `phase3_reference_do_comparison_20260301.md`：参考文献2 do-file 复跑对照与剩余参数差异说明。

## output/
```text
output/
├── paper/
│   ├── chapter2_lit_review_draft.md          # 第2章文献综述草稿
│   ├── chapter2_references_with_links.md
│   ├── chapter2_references_gbt7714.md
│   ├── chapter3_ml_prediction_draft.md       # [Phase2] 第3章ML预测分析草稿
│   └── chapter4_did_evaluation_draft.md      # [Phase3新增] 第4章DID因果评估草稿
├── tables/
│   ├── phase0_minimal_repro_metrics.csv
│   ├── 变量定义表-第3章.md                    # [Phase2] 变量定义与样本说明
│   ├── model_comparison_ch3.csv               # [Phase2] 6模型性能对比表
│   ├── rf_yearly_r2.csv                       # [Phase2] RF逐年样本外R²
│   ├── feature_importance_RF_fixed.csv        # [Phase2] RF特征重要性排名
│   ├── feature_importance_GBDT.csv            # [Phase2] GBDT特征重要性排名
│   ├── subsample_robustness_ch3.csv           # [Phase2] 7子样本稳健性对比
│   ├── pca_explained_variance.csv             # [Phase2-PCA] 各主成分解释方差
│   ├── pca_loadings_top.csv                   # [Phase2-PCA] 载荷矩阵+Top3变量
│   ├── pca_model_comparison.csv               # [Phase2-PCA] PCA vs 原始特征预测对比
│   ├── did_descriptive_stats.csv              # [Phase3新增] DID样本描述性统计
│   ├── did_baseline_regression.csv            # [Phase3新增] 基准DID回归(表8)
│   ├── did_event_study_DivDummy.csv           # [Phase3新增] 事件研究系数(DivDummy)
│   ├── did_event_study_DivPayRate.csv         # [Phase3新增] 事件研究系数(DivPayRate)
│   ├── did_placebo_DivDummy.csv               # [Phase3收口] 安慰剂检验系数(100次，policy-year-only)
│   ├── did_placebo_DivPayRate.csv             # [Phase3收口] 安慰剂检验系数(100次，policy-year-only)
│   ├── did_robustness_checks.csv              # [Phase3新增] 稳健性检验汇总(表9)
│   ├── did_heterogeneity.csv                  # [Phase3新增] 异质性分析(表10)
│   └── did_economic_consequences.csv          # [Phase3新增] 经济后果分析(表11)
└── figures/
    ├── ale_rf_*.png (10张)                    # [Phase2] RF ALE图(10个关键变量)
    ├── ale_gbdt_*.png (10张)                  # [Phase2] GBDT ALE图(10个关键变量)
    ├── feature_importance_bar_rf.png          # [Phase2] RF特征重要性条形图
    ├── feature_importance_bar_gbdt.png        # [Phase2] GBDT特征重要性条形图
    ├── pdp_grid_rf.png                        # [Phase2] RF PDP网格图(Top4)
    ├── pdp_grid_gbdt.png                      # [Phase2] GBDT PDP网格图(Top4)
    ├── pca_scree_plot.png                     # [Phase2-PCA] 碎石图(图9)
    ├── pca_loading_heatmap.png                # [Phase2-PCA] 载荷热力图(图10)
    ├── did_parallel_trends.png                # [Phase3新增] 平行趋势事件研究图(图11)
    └── did_placebo_test.png                   # [Phase3新增] 安慰剂检验核密度图(图12)
```

## logs/
```text
logs/
├── 20260225/
│   ├── run.log
│   └── events.jsonl
├── 20260227/
│   ├── run.log                                # [Phase2]
│   └── events.jsonl                           # [Phase2]
├── 20260228/
│   ├── run.log                                # [Phase2-PCA + Phase3 DID]
│   └── events.jsonl                           # [Phase2-PCA + Phase3 DID]
└── 20260301/
    └── events.jsonl                           # [Phase3复跑与收口]
```

## scripts/
```text
scripts/
├── unify_notebook_paths.py
├── phase2_ml_training.py                      # [Phase2] ML模型训练主脚本
├── phase2_rf_and_summary.py                   # [Phase2] RF训练+汇总脚本
├── phase2_ale_pdp_plots.py                    # [Phase2] ALE/PDP绘图脚本
├── phase2_subsample.py                        # [Phase2] 子样本稳健性脚本
├── phase2_pca_analysis.py                     # [Phase2-PCA] PCA降维+碎石图+热力图+预测对比
├── phase3_did_stata_replication.do            # [Phase3收口] Stata高一致度复现主脚本
├── phase3_placebo_stata100.do                 # [Phase3收口] placebo 100次真实回归导出脚本
└── phase3_placebo_plot.py                     # [Phase3收口] 基于CSV实测系数绘制图12
```

## 参考文献/
```text
参考文献/
├── 1/
│   ├── 中国上市公司分红的动因研究——基于机器学习的证据.pdf
│   └── 20240618102625WU_FILE_1/
└── 2/
    ├── 现金分红"硬约束"政策与上市公司股利分配行为_卿小权.pdf
    ├── 附件1：拆解数据压缩包/
    ├── 附件2：数据及程序代码/
    └── 附件3：图表.docx
```

## 更新约定
- 新增/删除关键文件或目录后，立即更新本文件。
- 每个 Phase 完成后，至少更新：
  - `output/` 新产物
  - `notes/` 新决策文档
  - `logs/` 新日志目录（如有）
