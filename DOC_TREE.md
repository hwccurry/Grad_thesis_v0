# Repository Document Tree

更新时间：2026-02-27
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
│   ├── chapter2_lit_review_draft.md
│   ├── chapter2_references_with_links.md
│   └── chapter2_references_gbt7714.md
└── tables/
    └── phase0_minimal_repro_metrics.csv
```
- `output/paper/`：论文草稿与参考文献输出。
- `output/tables/`：实证结果表与中间结果。

## logs/
```text
logs/
└── 20260225/
    ├── run.log
    └── events.jsonl
```
- `run.log`：可读执行日志。
- `events.jsonl`：结构化事件日志（phase/task/input/output/status/note）。

## scripts/
```text
scripts/
└── unify_notebook_paths.py
```
- `unify_notebook_paths.py`：批量修复 notebook 路径脚本。

## 参考文献/
```text
参考文献/
├── 1/
│   ├── 中国上市公司分红的动因研究——基于机器学习的证据.pdf
│   └── 20240618102625WU_FILE_1/
└── 2/
    ├── 现金分红“硬约束”政策与上市公司股利分配行为_卿小权.pdf
    ├── 附件1：拆解数据压缩包/
    ├── 附件2：数据及程序代码/
    └── 附件3：图表.docx
```
- `参考文献/1/`：第3章 ML 复刻数据与程序来源。
- `参考文献/2/`：第4章 DID 数据、程序与图表来源。

## 更新约定
- 新增/删除关键文件或目录后，立即更新本文件。
- 每个 Phase 完成后，至少更新：
  - `output/` 新产物
  - `notes/` 新决策文档
  - `logs/` 新日志目录（如有）
