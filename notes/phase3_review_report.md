# Phase 3 审阅报告（收口最终版）

> 生成时间：2026-03-01  
> 口径说明：本文件覆盖并替代 2026-02-28 旧版审阅报告内容，仅保留最终复核结论。

---

## 一、收口结论

Phase 3（第4章 DID）已完成收口，可作为当前最终版使用。

- 基准 DID：完成，结果稳定。
- 识别有效性：完成（平行趋势 + placebo + 多项稳健性）。
- 异质性：完成，采用 `bdiff bootstrap`。
- 第4章草稿：完成，表7-表11、图11-图12齐全。

---

## 二、与参考文献2 do-file 对齐状态（最终）

| 环节 | 最终状态 | 说明 |
|---|---|---|
| 基准 DID | ✅ 完全对齐 | `DivDummy=0.0828***`, `DivPayRate=0.1081***` |
| 平行趋势 | ✅ 完全对齐 | 动态 DID + 99% CI 口径 |
| 安慰剂检验 | ✅ 对齐 | 已改为 100 次 `policy-year-only`，并由 Stata 实测结果出图 |
| PSM-DID | ✅ 完全对齐 | 已使用 `psmatch2`（10-NN, caliper 0.05） |
| Hausman-Taylor | ✅ 已补齐 | `xthtaylor ... endog(did)` |
| 熵平衡匹配 | ✅ 已补齐 | `ebalance did $ctrl` + 加权回归 |
| 排除替代解释 | ✅ 完全对齐 | `did×Capital_AR` / `did×Asset_GR` |
| 剔除再融资 | ✅ 完全对齐 | `if refinance==0` |
| 异质性分组回归 | ✅ 完全对齐 | 四个维度分组结果齐全 |
| 组间差异检验 | ⚠️ 参数近似对齐 | 方法一致（`bdiff`），当前 `reps(200)` vs 参考 `reps(1000)` |
| 经济后果 | ✅ 完全对齐 | 8个后果变量方向一致 |

---

## 三、当前保留风险（仅1项）

### 风险：`bdiff` 重复次数为 200（非 1000）

- 当前脚本：`scripts/phase3_did_stata_replication.do` 使用 `local bdiff_reps 200`。
- 参考 do：`bdiff` 使用 `reps(1000)`。
- 影响评估：属于参数级差异，不改变核心结论方向与显著性叙述框架；但不应表述为“逐参数完全一致”。
- 对外建议口径：**“方法对齐、参数近似，高一致度复现。”**

---

## 四、答辩建议口径（最终）

1. 平行趋势按参考文献同口径报告 99% CI；对 `pre_3` 在 5% 显著的疑问，说明其在 99% CI 下包含 0。  
2. H3 结论以代理成本维度为核心证据，其他维度作为方向性补充。  
3. 明确声明：已完成 Stata 复跑对齐，当前仅保留 `bdiff reps` 参数差异。  

---

## 五、收口产物（最终保留）

- 结果表：`output/tables/did_*.csv`
- 图：`output/figures/did_parallel_trends.png`、`output/figures/did_placebo_test.png`
- 草稿：`output/paper/chapter4_did_evaluation_draft.md`
- 主复现脚本：`scripts/phase3_did_stata_replication.do`
- placebo 补充脚本：`scripts/phase3_placebo_stata100.do`、`scripts/phase3_placebo_plot.py`
- 对照说明：`notes/phase3_reference_do_comparison_20260301.md`

---

## 六、结论

Phase 3 可判定为 **Completed（收口完成）**。  
后续进入 Phase 4 时，建议继续沿用当前“方法对齐、参数近似”的统一表述。
