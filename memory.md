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
