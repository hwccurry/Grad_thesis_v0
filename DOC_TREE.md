# Repository Document Tree

更新时间：2026-03-03（文档一致性维护：清理失效路径并同步当前产物命名）
维护规则：每个 Phase 完成后必须同步更新本文件。

## 根目录
```text
Grad_thesis/
├── INSTRUCTIONS.md
├── DOC_TREE.md
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
├── data_code_inventory.md
├── path_unification.md
├── repro_env.md
├── literature_pool_phase1.md
├── hypothesis_mapping.md
├── phase1_refs_for_zotero.bib
├── did_design.md                                 # [Phase3新增] DID准自然实验设计文档
├── phase3_review_report.md                       # [Phase3收口] 风险审阅与答辩口径
├── phase3_reference_do_comparison_20260301.md   # [Phase3收口] 与参考do复跑对照
├── phase4_consistency_check.md                   # [Phase4] 统稿一致性校验（含摘要复核）
├── phase5_traceability_matrix.md                 # [Phase5收口] 结论-图表-脚本追溯矩阵
├── phase6_delivery_audit.md                      # [Phase6新增] 自动化交付审计报告
├── reference_verification/                       # [参考文献核验] Crossref与二次核验证据
├── references_final_31_verified.bib              # [参考文献核验] 31条最终校正文献
├── references_final_missing8_for_zotero.bib      # [参考文献核验] Zotero增量导入包(8条)
└── zotero_entry_management_final31.md            # [参考文献核验] final31条目管理台账
```
- `data_code_inventory.md`：数据/代码盘点。
- `path_unification.md`：路径统一策略与改造记录。
- `repro_env.md`：最小复现环境与命令。
- `literature_pool_phase1.md`：Phase1 文献池与核验链接。
- `hypothesis_mapping.md`：H1/H2/H3 映射。
- `phase1_refs_for_zotero.bib`：Zotero 导入用 BibTeX。
- `did_design.md`：Phase3 DID实验设计（政策背景、处理组定义、模型设定、检验策略）。
- `phase3_review_report.md`：Phase3 风险复核、答辩解释口径与收口结论。
- `phase3_reference_do_comparison_20260301.md`：参考文献2 do-file 复跑对照与剩余参数差异说明。
- `phase4_consistency_check.md`：Phase4 一致性校验记录（研究闭环、H1-H3映射、证据边界、摘要一致性复核）。
- `phase5_traceability_matrix.md`：Phase5 图表-结论-脚本追溯关系表（已切换至 `figures_v2`）。
- `phase6_delivery_audit.md`：Phase6 自动化审计（图像、编号、DID复验、docx 结构摘要）。
- `reference_verification/`：参考文献真实性核验证据（Crossref 与二次核验）。
- `references_final_31_verified.bib`：31条终稿参考文献 BibTeX（已校正）。
- `references_final_missing8_for_zotero.bib`：Zotero 增量导入 BibTeX（8条）。
- `zotero_entry_management_final31.md`：编号到 Zotero item key 映射台账。

## output/
```text
output/
├── paper/
│   ├── chapter2_lit_review.md                # [Phase1]第2章文献综述材料
│   ├── references_with_links.md
│   ├── references_gbt7714_nonmain.md         # 参考文献材料（非正文，供Phase5参考）
│   ├── chapter3_ml_prediction_draft.md       # [Phase2] 第3章ML预测分析草稿
│   ├── chapter4_did_evaluation_draft.md      # [Phase3新增] 第4章DID因果评估草稿
│   ├── chapter1_introduction_draft.md        # [Phase4新增] 第1章绪论草稿
│   ├── chapter5_conclusion_draft.md          # [Phase4新增] 第5章结论与启示草稿
│   ├── abstract_draft.md                     # [Phase4收口] 中英文摘要
│   ├── references_final.md                   # [Phase6新增] 正文参考文献主清单(31条)
│   ├── references_authenticity_check.md      # [Phase6新增] 参考文献真实性核验报告
│   ├── acknowledgment.md                     # [Phase6新增] 后记
│   ├── declaration.md                        # [Phase6新增] 独创性与授权声明
│   ├── 论文完整版.md                          # [可再生] 由 `scripts/phase5_prepare.py` 按需生成
│   ├── 论文终稿.docx                          # [可再生] 由 `pandoc + scripts/postprocess_docx.py` 按需生成
│   └── 论文终稿_base.docx                     # [可再生] Pandoc中间产物（可删除）
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
│   ├── did_economic_consequences.csv          # [Phase3新增] 经济后果分析(表11)
│   └── phase5_did_repro_check.csv             # [Phase5准备] DID基准快速复验系数
├── figures/                                       # [Phase2–4 原始图，200 DPI，存档保留]
│   ├── ale_rf_*.png (10张)                    # [Phase2] RF ALE图(10个关键变量)
│   ├── ale_gbdt_*.png (10张)                  # [Phase2] GBDT ALE图(10个关键变量)
│   ├── feature_importance_bar_rf.png          # [Phase2] RF特征重要性条形图
│   ├── feature_importance_bar_gbdt.png        # [Phase2] GBDT特征重要性条形图
│   ├── pdp_grid_rf.png                        # [Phase2] RF PDP网格图(Top4)
│   ├── pdp_grid_gbdt.png                      # [Phase2] GBDT PDP网格图(Top4)
│   ├── pca_scree_plot.png                     # [Phase2-PCA] 碎石图(图9)
│   ├── pca_loading_heatmap.png                # [Phase2-PCA] 载荷热力图(图10)
│   ├── did_parallel_trends.png                # [Phase3新增] 平行趋势事件研究图(图11)
│   └── did_placebo_test.png                   # [Phase3新增] 安慰剂检验核密度图(图12)
├── figures_v2/                                    # [Phase5] 重新生成（300 DPI + serif + 灰度友好）
│   ├── ale_rf_*.png (10张)                    # [Phase5] RF ALE图（300 DPI, serif, black line）
│   ├── ale_gbdt_*.png (10张)                  # [Phase5] GBDT ALE图
│   ├── feature_importance_bar_rf.png          # [Phase5] RF特征重要性Top10（灰色条形图）
│   ├── feature_importance_bar_gbdt.png        # [Phase5] GBDT特征重要性Top10
│   ├── pdp_grid_rf.png                        # [Phase5] RF PDP网格（中文标签, 黑色线）
│   ├── pdp_grid_gbdt.png                      # [Phase5] GBDT PDP网格
│   ├── pca_scree_plot.png                     # [Phase5] PCA碎石图（灰度友好）
│   ├── pca_loading_heatmap.png                # [Phase5] PCA载荷热力图（灰度色板）
│   ├── did_parallel_trends.png                # [Phase5] DID平行趋势图（Python独立脚本生成）
│   └── did_placebo_test.png                   # [Phase5] 安慰剂检验图（灰色直方图+黑色KDE）
├── figures_v3/                                    # [Phase5测试] 备份迭代图（保留，不用于正文引用）
│   └── *.png
└── models/                                        # [Phase5] 持久化训练模型（避免重训）
    ├── rf_model.joblib                        # RF 5000 trees 模型
    └── gbdt_model.joblib                      # GBDT 3000 trees 模型
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
├── 20260301/
│   ├── run.log                                # [Phase3收口 + Phase4统稿留痕]
│   └── events.jsonl                           # [Phase3复跑收口 + Phase4统稿留痕]
└── 20260302/
    ├── run.log                                # [Phase5/6] 主稿合并、审计与复验留痕
    ├── events.jsonl                           # [Phase5/6] 过程化事件留痕
    ├── phase5_v3figure_run.log                # [Phase5测试] v3图批量生成日志
    ├── stata_update_all.log                   # [Phase5排障] Stata 更新与Mata修复入口日志
    ├── stata_restore_mata_funcs.log           # [Phase5排障] Mata函数恢复日志
    ├── stata_mata_function_battery2.log       # [Phase5排障] Mata函数兼容性测试日志
    ├── stata_phase5_smoke.log                 # [Phase5准备] Stata CLI smoke 结果
    ├── stata_phase5_baseline_check.log        # [Phase5准备] Stata reghdfe 报错留痕(r3499)
    └── stata_phase5_baseline_xtreg_check.log  # [Phase5准备] Stata xtreg 报错留痕(r3499)
```

## scripts/
```text
scripts/
├── thesis_plot_config.py                      # [Phase5] 共享绘图配置（300 DPI, serif, 灰度色板）
├── unify_notebook_paths.py
├── phase2_ml_training.py                      # [Phase2] ML模型训练主脚本
├── phase2_rf_and_summary.py                   # [Phase2] RF训练+汇总脚本
├── phase2_ale_pdp_plots.py                    # [Phase5改写] ALE/PDP/FI绘图+模型持久化
├── phase2_subsample.py                        # [Phase2] 子样本稳健性脚本
├── phase2_pca_analysis.py                     # [Phase5改写] PCA碎石图+热力图+预测对比
├── phase3_did_stata_replication.do            # [Phase3收口] Stata高一致度复现主脚本
├── phase3_placebo_stata100.do                 # [Phase3收口] placebo 100次真实回归导出脚本
├── phase3_placebo_stata100_mcp.log            # [Phase3收口] placebo实跑日志留档
├── phase3_placebo_plot.py                     # [Phase5改写] 安慰剂检验密度图
├── phase5_did_trends_plot.py                  # [Phase5新建] DID平行趋势事件研究图
├── phase5_prepare.py                          # [Phase5准备] 生成完整版/追溯矩阵
├── phase5_did_quickcheck.py                   # [Phase5准备] PanelOLS复验DID基准系数
├── phase6_audit.py                            # [Phase6新增] 自动化交付审计脚本
├── phase6_format_tables.py                    # [Phase6新增] DOCX三线表格式化脚本
├── postprocess_docx.py                        # [Phase6新增] Word后处理脚本（样式/页码/图片缩放）
└── stata_mata_compat.do                       # [Phase5排障] Mata 库兼容修复脚本
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
- 对可再生产物（如 `output/paper/论文完整版*`）需显式标注“生成方式”，避免误判为丢失文件。
- 每个 Phase 完成后，至少更新：
  - `output/` 新产物
  - `notes/` 新决策文档
  - `logs/` 新日志目录（如有）
