# Repository Document Tree

更新时间：2026-02-27 (Phase 2 完成后)
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
└── phase1_refs_for_zotero.bib
```
- `checkpoints.md`：各阶段完成状态。
- `data_code_inventory.md`：数据/代码盘点。
- `path_unification.md`：路径统一策略与改造记录。
- `repro_env.md`：最小复现环境与命令。
- `literature_pool_phase1.md`：Phase1 文献池与核验链接。
- `hypothesis_mapping.md`：H1/H2/H3 映射。
- `phase1_refs_for_zotero.bib`：Zotero 导入用 BibTeX。

## output/
```text
output/
├── paper/
│   ├── chapter2_lit_review_draft.md          # 第2章文献综述草稿
│   ├── chapter2_references_with_links.md
│   ├── chapter2_references_gbt7714.md
│   └── chapter3_ml_prediction_draft.md       # [Phase2新增] 第3章ML预测分析草稿
├── tables/
│   ├── phase0_minimal_repro_metrics.csv
│   ├── 变量定义表-第3章.md                    # [Phase2新增] 变量定义与样本说明
│   ├── model_comparison_ch3.csv               # [Phase2新增] 6模型性能对比表
│   ├── rf_yearly_r2.csv                       # [Phase2新增] RF逐年样本外R²
│   ├── feature_importance_RF_fixed.csv        # [Phase2新增] RF特征重要性排名
│   ├── feature_importance_GBDT.csv            # [Phase2新增] GBDT特征重要性排名
│   └── subsample_robustness_ch3.csv           # [Phase2新增] 7子样本稳健性对比
└── figures/
    ├── ale_rf_*.png (10张)                    # [Phase2新增] RF ALE图(10个关键变量)
    ├── ale_gbdt_*.png (10张)                  # [Phase2新增] GBDT ALE图(10个关键变量)
    ├── feature_importance_bar_rf.png          # [Phase2新增] RF特征重要性条形图
    ├── feature_importance_bar_gbdt.png        # [Phase2新增] GBDT特征重要性条形图
    ├── pdp_grid_rf.png                        # [Phase2新增] RF PDP网格图(Top4)
    └── pdp_grid_gbdt.png                      # [Phase2新增] GBDT PDP网格图(Top4)
```

## logs/
```text
logs/
├── 20260225/
│   ├── run.log
│   └── events.jsonl
└── 20260227/
    ├── run.log                                # [Phase2新增]
    └── events.jsonl                           # [Phase2新增]
```

## scripts/
```text
scripts/
├── unify_notebook_paths.py
├── phase2_ml_training.py                      # [Phase2新增] ML模型训练主脚本
├── phase2_rf_and_summary.py                   # [Phase2新增] RF训练+汇总脚本
├── phase2_ale_pdp_plots.py                    # [Phase2新增] ALE/PDP绘图脚本
└── phase2_subsample.py                        # [Phase2新增] 子样本稳健性脚本
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
