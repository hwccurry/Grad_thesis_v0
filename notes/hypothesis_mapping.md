# Hypothesis Mapping（Phase 1）

更新时间：2026-02-25 17:17 +08:00

## 1. 映射总表

| 假设 | 理论依据 | 被解释变量 | 核心解释变量 | 方法与模型 | 预期符号/方向 | 识别与风险 |
|---|---|---|---|---|---|---|
| H1 预测筛选假设 | 生命周期理论 + 代理成本理论 + ML预测证据 | `Dividend_ratio1`（连续）/`Dividend`（二元） | 生命周期：`Retainedearn_ratio`；代理成本：`Tunneling`；治理与约束：`Institution`,`Constraint` 等 | 第3章：RF、GBDT（一年期滚动 t->t+1）；特征重要性 + ALE/PDP | 生命周期与代理成本相关变量进入 Top 重要性，方向随定义（如 `Retainedearn_ratio` 正向，`Tunneling` 负向） | 风险：高维相关性、样本漂移；缓解：滚动外推、子样本稳健性 |
| H2 政策因果效应假设 | 监管约束提升股东回报约束强度 | `DivDummy`、`DivPayRate` | `did = treat × post` | 第4章：TWFE DID（公司 FE + 年份 FE，`cluster(stkcd)`） | `β_did > 0` | 风险：平行趋势破坏/同期政策干扰；缓解：事件研究、窗口调整、placebo |
| H3 异质性处理效应假设 | 监管效应受生命周期与代理问题调节 | `DivDummy`、`DivPayRate` | `did × Mature`、`did × HighAgency`（或分组回归） | 第4章：交互项 DID / 分组 DID | 交互项系数为正且显著；成熟组/高代理组政策效应更强 | 风险：分组内生性；缓解：替代分组口径、PSM-DID/Entropy balancing |

## 2. 变量到数据文件的落地
- ML 数据：`参考文献/1/20240618102625WU_FILE_1/数据/数据-python/data.csv`
- DID 数据：`参考文献/2/附件2：数据及程序代码/数据.dta`
- 主要控制变量（DID）：`SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT`

## 3. 可检验命题写法（论文正文可直接复用）
- H1：在滚动预测框架下，生命周期与代理成本变量在 RF/GBDT 中的平均重要性显著高于其他变量组。
- H2：在控制公司固定效应和年份固定效应后，`did` 对 `DivDummy` 与 `DivPayRate` 的影响为正。
- H3：`did` 的正向效应在成熟期企业和代理问题更突出的企业中显著更大。
