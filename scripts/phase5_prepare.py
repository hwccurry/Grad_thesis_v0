#!/usr/bin/env python3
"""
Phase 5 preparation helper.

Actions:
1) Build output/paper/论文完整版.md from chapter drafts.
2) Build notes/phase5_traceability_matrix.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "output" / "paper"
NOTES_DIR = ROOT / "notes"


FULL_PAPER_PARTS = [
    ("摘要", PAPER_DIR / "abstract_draft.md"),
    ("第一章 绪论", PAPER_DIR / "chapter1_introduction_draft.md"),
    ("第二章 文献综述与理论基础", PAPER_DIR / "chapter2_lit_review.md"),
    ("第三章 机器学习预测分析", PAPER_DIR / "chapter3_ml_prediction_draft.md"),
    ("第四章 DID因果评估", PAPER_DIR / "chapter4_did_evaluation_draft.md"),
    ("第五章 结论与启示", PAPER_DIR / "chapter5_conclusion_draft.md"),
]

FULL_PAPER_OUTPUT = PAPER_DIR / "论文完整版.md"
TRACEABILITY_OUTPUT = NOTES_DIR / "phase5_traceability_matrix.md"

PLACEHOLDER_PATTERN = re.compile(r"\bR\d{2}\b|TODO|TBD|待补|待定|xxx|XXX")


@dataclass
class CheckItem:
    name: str
    ok: bool
    detail: str


def now_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_full_paper() -> list[CheckItem]:
    missing = [str(p.relative_to(ROOT)) for _, p in FULL_PAPER_PARTS if not p.exists()]
    if missing:
        return [CheckItem("论文合并源文件齐全", False, f"缺失: {', '.join(missing)}")]

    chunks: list[str] = []
    chunks.append("# 论文完整版（Phase5 合并稿）")
    chunks.append("")
    chunks.append(f"- 生成时间：{now_str()}")
    chunks.append("- 说明：该文件为答辩前质检与格式迁移用主稿，排版以学校模板 docx 为准。")
    chunks.append("")

    for title, p in FULL_PAPER_PARTS:
        body = read_text(p).strip()
        chunks.append(f"<!-- SOURCE: {p.relative_to(ROOT)} -->")
        chunks.append(f"<!-- SECTION: {title} -->")
        chunks.append(body)
        chunks.append("")

    merged = "\n".join(chunks).rstrip() + "\n"
    write_text(FULL_PAPER_OUTPUT, merged)

    placeholder_hits = PLACEHOLDER_PATTERN.findall(merged)
    items = [
        CheckItem("生成论文完整版", True, str(FULL_PAPER_OUTPUT.relative_to(ROOT))),
        CheckItem(
            "占位符扫描",
            len(placeholder_hits) == 0,
            "未发现占位符" if len(placeholder_hits) == 0 else f"命中 {len(placeholder_hits)} 处",
        ),
    ]
    return items


def build_traceability() -> CheckItem:
    rows = [
        (
            "H1：生命周期/代理成本是关键动因",
            "output/tables/model_comparison_ch3.csv; output/tables/feature_importance_RF_fixed.csv; output/tables/feature_importance_GBDT.csv; output/tables/subsample_robustness_ch3.csv; output/tables/pca_model_comparison.csv",
            "output/figures_v2/feature_importance_bar_rf.png; output/figures_v2/feature_importance_bar_gbdt.png; output/figures_v2/pca_scree_plot.png; output/figures_v2/pca_loading_heatmap.png",
            "scripts/phase2_ml_training.py; scripts/phase2_rf_and_summary.py; scripts/phase2_ale_pdp_plots.py; scripts/phase2_subsample.py; scripts/phase2_pca_analysis.py",
            "output/paper/chapter3_ml_prediction_draft.md",
        ),
        (
            "H2：政策显著提高分红意愿与水平",
            "output/tables/did_baseline_regression.csv; output/tables/did_event_study_DivDummy.csv; output/tables/did_event_study_DivPayRate.csv; output/tables/did_robustness_checks.csv; output/tables/did_placebo_DivDummy.csv; output/tables/did_placebo_DivPayRate.csv",
            "output/figures_v2/did_parallel_trends.png; output/figures_v2/did_placebo_test.png",
            "scripts/phase3_did_stata_replication.do; scripts/phase5_did_trends_plot.py; scripts/phase3_placebo_plot.py",
            "output/paper/chapter4_did_evaluation_draft.md",
        ),
        (
            "H3：高代理成本组政策效应更强",
            "output/tables/did_heterogeneity.csv",
            "（无独立图，结论来自表10）",
            "scripts/phase3_did_stata_replication.do",
            "output/paper/chapter4_did_evaluation_draft.md",
        ),
        (
            "市场后果：流动性提升、错误定价下降",
            "output/tables/did_economic_consequences.csv",
            "（当前无单独图，必要时可补绘）",
            "scripts/phase3_did_stata_replication.do",
            "output/paper/chapter4_did_evaluation_draft.md; output/paper/chapter5_conclusion_draft.md",
        ),
    ]

    lines = [
        "# Phase 5 图表-结论追溯矩阵",
        "",
        f"- 生成时间：{now_str()}",
        "- 用途：答辩前快速核对“结论-表图-脚本-正文位置”一致性。",
        "",
        "| 结论 | 对应表格 | 对应图形 | 复现脚本 | 正文位置 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
    lines.append("")

    write_text(TRACEABILITY_OUTPUT, "\n".join(lines) + "\n")
    return CheckItem("生成追溯矩阵", True, str(TRACEABILITY_OUTPUT.relative_to(ROOT)))


def main() -> None:
    _ = build_full_paper()
    build_traceability()
    print("Phase5 preparation artifacts generated:")
    print(f"- {FULL_PAPER_OUTPUT.relative_to(ROOT)}")
    print(f"- {TRACEABILITY_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
