# Session Memory

- [2026-02-25 02:52:13 UTC] 已安装 `feishu-doc` skill，后续可直接在 Codex 中调用与飞书文档读写相关能力。
- [2026-02-25 02:52:13 UTC] 本次会话遵循工作流：执行后补充决策记录与会话记忆。
- [2026-02-25 06:43:03 UTC] 决策：将通用 VBM 复刻提示词重构为本项目专用 INSTRUCTIONS.md，采用“文献综述→第3章ML→第4章DID→统稿→格式质检”的阶段化流程，并保留 STOP AND CHECK 人工确认机制。
- [2026-02-25 06:43:03 UTC] 日志：新增 /Users/mac/Desktop/毕业论文/INSTRUCTIONS.md（论文主题、章节任务、文献约束、可追踪日志 text+jsonl 规范、各阶段交付清单与检查点）。

- [2026-02-25 07:33:32 UTC] 决策：按 INSTRUCTIONS.md 从 Phase 0 启动，先完成数据/代码清点、路径审计，再做最小复现闭环后进入 checkpoint。
- [2026-02-25 07:33:32 UTC] 日志：新增 `notes/data_code_inventory.md`（ML/DID 文件清单、入口、关键变量、路径风险与统一策略）。
- [2026-02-25 07:33:32 UTC] 日志：新增 `output/tables/phase0_minimal_repro_metrics.csv` 与 `notes/repro_env.md`，最小闭环结果为 RF(2007->2008) `R2=0.1154`；DID `did` 系数在 DivDummy/DivPayRate 上均显著为正。
- [2026-02-25 07:33:32 UTC] 日志：启用 `logs/20260225/run.log` 与 `logs/20260225/events.jsonl`，记录 Phase0 Task0.1~0.3 执行事件。
- [2026-02-25 07:37:08 UTC] 偏好更新：每完成一个 Phase，必须更新 checkpoint 状态并记录到 notes/checkpoints.md 与当日日志。
- [2026-02-25 07:39:44 UTC] 决策更新：checkpoint 统一以 INSTRUCTIONS.md 为准；每完成一步/每个 Phase 后，直接在对应 CHECKPOINT 勾选并记录更新时间。
- [2026-02-25 07:48:13 UTC] 决策：Python执行器统一采用 Miniconda (`/Users/mac/miniconda3/bin/python`)；notebook 路径统一策略落地为 `Path` 根目录定位 + `DATA_DIR/TABLE_DIR/ML_DIR`。
- [2026-02-25 07:48:13 UTC] 日志：新增 `scripts/unify_notebook_paths.py` 与 `notes/path_unification.md`，批量修复 19 个 notebook，source 绝对路径残留为 0。
- [2026-02-25 07:49:21 UTC] 规范更新：INSTRUCTIONS.md 新增强制要求：每次完成跑数据程序后，必须交付可复现的 Python/Stata 脚本（脚本路径+执行命令+输入/输出路径）。
- [2026-02-25 07:53:17 UTC] 规范更新：每个 Phase 完成后必须执行 Git 提交并推送远程仓库，commit message 必须包含 phase 编号与 comments（关键修改、关键结果、风险/待办）。
- [2026-02-25 08:35:07 UTC] 决策：定位 Git 推送失败原因为双重问题——`git push` 未配置默认 push destination，且推送到 `Grad_thesis_v0/main` 时因远端存在独立初始提交触发 non-fast-forward（无 merge-base）。
- [2026-02-25 08:35:07 UTC] 日志：执行 `git push Grad_thesis_v0 main` 复现失败；`git merge-base main Grad_thesis_v0/main` 返回空；提供两种修复路径：合并远端历史或 `--force-with-lease` 覆盖远端。
- [2026-02-25 08:50:35 UTC] 决策：针对 `Grad_thesis_v0` 推送失败，确认为远端历史分叉 + HTTPS 在 HTTP/2 下 `git-receive-pack` 二次 POST 返回 400 的组合问题；采用“先合并无关历史，再切到 HTTP/1.1 推送”的稳定方案。
- [2026-02-25 08:50:35 UTC] 日志：执行 `git merge --allow-unrelated-histories refs/remotes/Grad_thesis_v0/main` 生成合并提交 `d4b8112`；设置 `git config http.version HTTP/1.1` 与 `git config http.postBuffer 524288000` 后，`git push -u Grad_thesis_v0 main` 成功（`fa664d8..d4b8112`）。
- [2026-02-25 09:20:31 UTC] 决策：执行 Phase1 时采用“先核验文献池后写综述”的顺序，文献以可核验来源为硬约束（DOI 直连优先，其余来自核心期刊参考文献条目）。
- [2026-02-25 09:20:31 UTC] 日志：新增 `notes/literature_pool_phase1.md`（22篇文献池，近三年8篇，占比36.4%）与 `output/paper/chapter2_lit_review_draft.md`（第2章初稿，按5个视角组织）。
- [2026-02-25 09:20:31 UTC] 日志：新增 `notes/hypothesis_mapping.md`，并完成 `INSTRUCTIONS.md`、`notes/checkpoints.md` 的 CHECKPOINT 1 勾选及 `logs/20260225/*` 留痕。
- [2026-02-25 10:07:30 UTC] 纠偏：Phase1 文献池“近三年占比”存在计数不一致（表内仅4篇），已修正为 27 篇中近三年 9 篇（33.3%），并为每条文献补充可点击链接。
- [2026-02-25 10:07:30 UTC] Zotero：已生成 `notes/phase1_refs_for_zotero.bib` 并执行导入；`zotero_get_recent` 核验显示新增 27 条 journalArticle（含中英文核心条目）。
- [2026-02-26 02:00:49 UTC] 日志：新增 `output/paper/chapter2_references_gbt7714.md`（27条GB/T 7714样式+链接），并在 `output/paper/chapter2_lit_review_draft.md` 增加引用入口。
- [2026-02-27 09:07:41 UTC] 决策：文献引用格式以学校模板为准，正文采用作者-年份制（如 World Bank（1994）），章节末文献列表采用顺序编码 [1][2]...。
- [2026-02-27 09:07:41 UTC] 日志：已更新 `INSTRUCTIONS.md` 引用规范，并将 `output/paper/chapter2_lit_review_draft.md` 中 `Rxx` 占位引用全部替换为作者-年份格式。
