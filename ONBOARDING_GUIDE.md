# 新手上手指南（仓库结构 + 快速复现 + 改稿）

适用对象：第一次接手本仓库的写作者。目标是在 30 分钟内完成三件事：
1. 看懂仓库结构
2. 快速确认结果可复核
3. 能修改并导出论文终稿

## 1. 一眼看懂仓库

```text
Grad_thesis/
├── 参考文献/                 # 外部基准材料（原文+数据+程序）
├── scripts/                  # 复现脚本（Phase2~Phase6）
├── output/
│   ├── tables/               # 回归与统计结果表（csv）
│   ├── figures_v2/           # 论文当前主用图片（300 DPI）
│   ├── models/               # 训练后模型（joblib）
│   └── paper/                # 章节草稿（论文完整版*为按需生成产物）
├── notes/                    # 审计、追溯矩阵、说明文档
├── logs/                     # 运行日志（run.log + events.jsonl）
├── INSTRUCTIONS.md           # 项目规则与阶段验收标准
├── DOC_TREE.md               # 仓库文档树
└── ONBOARDING_GUIDE.md       # 本指南
```

关键文件（先看这 6 个）：
- `INSTRUCTIONS.md`
- `DOC_TREE.md`
- `notes/repro_env.md`
- `notes/phase5_traceability_matrix.md`
- `output/paper/chapter1_introduction_draft.md`
- `notes/phase6_delivery_audit.md`

说明：`output/paper/论文完整版.md` 与 `output/paper/论文完整版_phase6.docx` 为可再生产物，当前仓库若缺失属正常；按第 3 节和第 5 节命令链可重建。

## 2. 环境与前置

固定 Python 解释器：
- `/Users/mac/miniconda3/bin/python`

建议工具：
- Python 包：`pandas numpy scikit-learn matplotlib linearmodels pillow python-docx`
- `pandoc`（用于 md -> docx）
- Stata（完整 DID 重跑需要）

## 3. 快速复现（推荐先跑）

说明：这条路径不追求“从原始数据全量重跑”，只验证当前论文产物链条可用。

### Step 1) 进入仓库

```bash
cd /Users/mac/Desktop/Grad_thesis
```

### Step 2) 重建主稿与追溯矩阵

```bash
/Users/mac/miniconda3/bin/python scripts/phase5_prepare.py
```

产物：
- `output/paper/论文完整版.md`
- `notes/phase5_traceability_matrix.md`

### Step 3) 复核 DID 核心系数（快速）

```bash
/Users/mac/miniconda3/bin/python scripts/phase5_did_quickcheck.py
```

产物：
- `output/tables/phase5_did_repro_check.csv`

### Step 4) 导出 docx 并做自动审计

```bash
pandoc output/paper/论文完整版.md \
  --reference-doc=商学院本科生毕业论文格式模板2025.01.docx \
  -o output/paper/论文完整版_phase6.docx

/Users/mac/miniconda3/bin/python scripts/phase6_format_tables.py
/Users/mac/miniconda3/bin/python scripts/phase6_audit.py
```

产物：
- `output/paper/论文完整版_phase6.docx`
- `notes/phase6_delivery_audit.md`

如果 `phase6_delivery_audit.md` 显示通过（占位符/图像DPI/编号连续性），快速复现就算完成。

## 4. 完整复现（需要重跑模型/回归）

### 4.1 第三章（ML）

```bash
cd /Users/mac/Desktop/Grad_thesis
/Users/mac/miniconda3/bin/python scripts/phase2_ml_training.py
/Users/mac/miniconda3/bin/python scripts/phase2_rf_and_summary.py
/Users/mac/miniconda3/bin/python scripts/phase2_subsample.py
/Users/mac/miniconda3/bin/python scripts/phase2_pca_analysis.py
/Users/mac/miniconda3/bin/python scripts/phase2_ale_pdp_plots.py
```

主要输出：
- `output/tables/model_comparison_ch3.csv`
- `output/tables/feature_importance_RF_fixed.csv`
- `output/tables/feature_importance_GBDT.csv`
- `output/figures_v2/*.png`

### 4.2 第四章（DID）

Stata 内执行：
- `do scripts/phase3_did_stata_replication.do`

然后补图：

```bash
/Users/mac/miniconda3/bin/python scripts/phase3_placebo_plot.py
/Users/mac/miniconda3/bin/python scripts/phase5_did_trends_plot.py
```

已知风险：本仓库历史上出现过 Stata `r(3499)`（环境/ado 问题）。若你遇到同样报错，先不要改模型逻辑，优先使用快速复现路径并保留日志到 `logs/YYYYMMDD/`。

## 5. 如何修改论文终稿（推荐流程）

### 5.1 改稿入口

优先改章节草稿（不要直接改 docx）：
- `output/paper/abstract_draft.md`
- `output/paper/chapter1_introduction_draft.md`
- `output/paper/chapter2_lit_review.md`
- `output/paper/chapter3_ml_prediction_draft.md`
- `output/paper/chapter4_did_evaluation_draft.md`
- `output/paper/chapter5_conclusion_draft.md`

### 5.2 合并主稿

```bash
/Users/mac/miniconda3/bin/python scripts/phase5_prepare.py
```

主稿文件：
- `output/paper/论文完整版.md`

### 5.3 导出提交版

```bash
pandoc output/paper/论文完整版.md \
  --reference-doc=商学院本科生毕业论文格式模板2025.01.docx \
  -o output/paper/论文完整版_phase6.docx

/Users/mac/miniconda3/bin/python scripts/phase6_format_tables.py
/Users/mac/miniconda3/bin/python scripts/phase6_audit.py
```

### 5.4 最后人工终检（Word）

至少检查：
1. 页眉页脚和页码
2. 表题/图题位置与字号
3. 三线表线宽是否正常
4. 中英文混排字体
5. 参考文献格式

## 6. 哪个文件算“终稿”

- 写作主稿：`output/paper/论文完整版.md`（由 `scripts/phase5_prepare.py` 生成）
- 交付主文件：`output/paper/论文完整版_phase6.docx`（由 `pandoc + scripts/phase6_format_tables.py` 生成）
- `output/paper/论文终稿.md` 作为历史版本参考，不作为默认主入口。

## 7. 新写作者最小工作清单

1. 先读 `INSTRUCTIONS.md` 和本指南
2. 运行一次“快速复现”全流程
3. 只在 `output/paper/chapter*.md` 改稿
4. 每次改稿后重跑：`phase5_prepare -> pandoc -> phase6_format_tables -> phase6_audit`
5. 更新 `logs/` 和 `memory.md`
