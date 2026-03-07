# AI Thesis Workflow (适配当前毕业论文项目)

## Project Overview

你正在完成商学院本科毕业论文：

> **中国上市公司为何分红？——来自机器学习预测与准自然实验的证据**

论文采用双路径研究设计：
1. **机器学习预测（第3章）**：识别影响分红决策的关键预测因子（参考文献1数据与代码框架）。
2. **DID准自然实验（第4章）**：评估现金分红监管政策冲击（重点考虑《上市公司现金分红指引》2023年修订）的因果效应（参考文献2数据与代码框架）。

核心假设（可随结果微调）：
- H1：企业生命周期与代理成本相关变量是分红行为最重要预测因子。
- H2：监管政策冲击显著提升企业现金分红意愿与支付水平。
- H3：政策效应在成熟期企业或代理问题更突出的企业中更强。

---

## 全局执行规则（必须遵守）

1. 全文中文写作，技术术语可保留英文（如 DID、Panel FE、ALE）。
2. 不得直接复制参考论文段落；必须重写、归纳、评述。
3. 参考文献目标约 20 篇：
- CSSCI 或高质量期刊优先；
- 近三年文献不少于 1/3；
- 尽量少用学位论文。
4. 文献综述按“研究视角”组织，不按年份堆叠，不按“国内外”机械拆分。
5. 图表格式必须对齐 `商学院本科生毕业论文格式模板2025.01.docx`，具体规范如下：
   - **编号方式**：全文顺序编号（表1、表2……图1、图2……），不使用章节编号（如 ~~表3-1~~）。编号与标题之间用一个半角空格分隔，如 `表1 各模型预测性能对比`。
   - **表标题**：置于表格**上方**，居中，加粗，宋体五号。
   - **图标题**：置于图片**下方**，居中，加粗，宋体五号。
   - **表格样式**：三线表（顶线粗 1 磅、表头下细线 0.5 磅、底线粗 1 磅，无左右边框无纵线）。Markdown 阶段用普通表格，转 Word 时统一应用三线表样式。
   - **注释/来源**：紧跟图/表下方，格式为 `注：xxx`，小五号（9pt），左对齐，无首行缩进。
   - **正文引用**：必须在正文中引用每张图表，使用 `如表X所示` 或 `表X汇报了……` 格式。
   - **当前编号进度**：第3章已使用表1—表6、图1—图10；第4章已使用表7—表11、图11—图12；后续章节从表12、图13开始接续。
6. 结果不可编造；引用不可虚构；结论与实证结果保持一致。
7. 正文文献引用必须对齐 `商学院本科生毕业论文格式模板2025.01.docx`：采用“作者-年份制”（示例：`李光龙和范贤贤（2019）`、`World Bank（1994）`、`Miller and Rock（1985）`），不得使用 `R01/R02` 等占位符。
8. 章节末参考文献列表采用模板的顺序编码格式（`[1] [2] ...`）与标点规范，且与正文引用一一对应。
9. 最终格式必须对齐 `商学院本科生毕业论文格式模板2025.01.docx`。
10. 每次完成跑数据的程序后，必须同步交付可复现的 Python 或 Stata 程序（含脚本文件路径、执行命令、输入数据路径、输出结果路径）。
11. 每个 Phase 完成后，必须执行 Git 交付：`git add -A`、`git commit -m "phaseX: ..."`、`git push <remote> <branch>`。
12. 第 11 条中的 commit message 必须包含 phase 编号与 comments（本阶段关键修改、关键结果、风险/待办）。
13. 每个 Phase 完成后，必须更新仓库文档树描述文件 `DOC_TREE.md`（新增/删除目录与关键产物必须同步反映）。

---

## 可追踪日志规范（text + jsonl）

每个阶段都要留痕，日志目录统一为：

```text
logs/
  YYYYMMDD/
    run.log
    events.jsonl
```

`events.jsonl` 每行一个 JSON，建议字段：

```json
{"ts":"2026-02-25T14:40:00+08:00","phase":"Phase2","task":"train_rf","input":"data.csv","output":"rf_metrics.csv","status":"ok","note":"one-year rolling"}
```

---

## 项目目录（当前项目语义）

```text
Grad_thesis/
├── INSTRUCTIONS.md
├── 写作框架.md
├── memory.md
├── 参考文献/
│   ├── 1/20240618102625WU_FILE_1/      # ML相关数据与notebooks
│   └── 2/                               # DID相关数据与Stata程序
├── output/
│   ├── tables/
│   ├── figures/                          # Phase2–4 原始图（200 DPI，存档不删）
│   ├── figures_v2/                       # Phase5 重新生成图（300 DPI + serif）
│   ├── models/                           # Phase5 持久化模型（rf/gbdt joblib）
│   └── paper/
├── notes/
└── logs/
```

---

## 🛑 STOP AND CHECK 机制

每个阶段结束后必须：
1. 总结已完成内容；
2. 展示关键输出（表/图/回归结果/草稿）；
3. 列出问题与风险；
4. 如本阶段包含数据跑数，提交可复现的 Python 或 Stata 脚本与运行命令；
5. 在本文件对应 `CHECKPOINT` 中勾选已完成项（`[ ] -> [x]`）并标注更新时间；
6. 完成 Git 提交并推送远程仓库，且在 commit message 写清 phase comments；
7. **等待人工确认后再进入下一阶段**。

---

## PHASE 0：项目校准与数据盘点

### Task 0.1 数据与代码清点
- 盘点参考文献1（ML）与参考文献2（DID）的数据文件、变量、脚本入口。
- 输出 `notes/data_code_inventory.md`（含文件清单、用途、关键变量）。

### Task 0.2 环境与路径统一
- 检查 notebook/脚本中的硬编码路径（如旧目录或 Windows 路径）。
- 统一为项目相对路径或项目根目录定位方案。

### Task 0.3 复现最小闭环
- 跑通一个最小样例（1个ML模型 + 1个DID基准回归）验证环境可用。
- 记录依赖与执行命令到 `notes/repro_env.md`。

### 🛑 CHECKPOINT 0
- [x] 数据与代码清点完成
- [x] 路径统一策略明确
- [x] 最小复现闭环跑通
- [x] 日志目录与规范已启用
- 更新于：2026-02-25 15:47 +08:00

---

## PHASE 1：文献综述与研究假设定稿（第2章）

### Task 1.1 文献筛选与核验
- 建立候选文献池，核验题名、作者、年份、期刊、卷期页码。
- 只保留可核验来源文献。

### Task 1.2 视角化综述写作
- 按“经典股利理论、公司治理与代理成本、生命周期与融资约束、政策监管与市场反应、方法论（ML与DID）”等视角归类。
- 每类形成“共识 + 分歧 + 可改进点”。

### Task 1.3 研究假设与理论框架
- 写出 H1/H2/H3 的理论依据、可检验命题与变量映射。
- 输出 `notes/hypothesis_mapping.md`（假设-变量-方法-预期符号）。

### 🛑 CHECKPOINT 1
- [x] 文献综述初稿完成
- [x] 文献数量与时效满足约束
- [x] 文献述评能自然引出本文动机
- [x] H1/H2/H3 表述可检验
- 更新于：2026-02-25 17:17 +08:00

---

## PHASE 2：机器学习预测分析（第3章）

### Task 2.1 样本与变量定义
- 明确样本范围、清洗规则、缺失值处理、winsorize规则（如使用）。
- 输出变量定义表到 `output/tables/变量定义表-第3章.xlsx`（或 `.md`）。

### Task 2.2 模型设定与训练
- 按“一年期训练（t 训练，t+1 测试）”执行滚动预测。
- 至少比较：Random Forest、Gradient Boosting（可补充 Lasso/OLS 作为基准）。
- 输出模型对比表（R2、MSE、MAE 或分类指标）。

### Task 2.3 特征重要性与可解释性
- 输出特征重要性排序（Top N）。
- 对核心变量绘制 ALE/PDP 图，解释经济含义。

### Task 2.4 稳健性与扩展
- 按子样本（如国有/非国有、高/低现金流等）做稳定性比较。
- 总结关键动因是否稳健。

### 🛑 CHECKPOINT 2
- [x] 模型性能表完成
- [x] 特征重要性与解释图完成
- [x] 子样本稳健性结果完成
- [x] 第3章文字草稿完成
- 更新于：2026-02-27 21:50 +08:00

---

## PHASE 3：政策冲击DID评估（第4章）

### Task 3.1 准自然实验设计
- 明确政策时点、处理组/对照组划分逻辑与外生性论证。
- 输出 `notes/did_design.md`。

### Task 3.2 基准回归
- 估计双向固定效应 DID（公司 FE + 年份 FE，标准误聚类到公司层面）。
- 被解释变量至少包含：分红意愿（DivDummy）与分红水平（DivPayRate）。

### Task 3.3 识别有效性检验
- 平行趋势检验（事件研究图/回归）。
- 稳健性检验：窗口调整、替换变量、placebo、PSM-DID（按数据可得性选择）。

### Task 3.4 异质性与机制（可选增强）
- 按生命周期、代理成本、产权性质、机构持股等维度做异质性分析。
- 如可行，补充市场后果变量分析（流动性、估值偏离等）。

### 🛑 CHECKPOINT 3
- [x] DID基准回归结果稳定
- [x] 平行趋势与稳健性检验完成
- [x] 异质性结果可解释
- [x] 第4章文字草稿完成
- 更新于：2026-02-28 16:50 +08:00

---

## PHASE 4：全文章节整合（第1/5章 + 统稿）

### Task 4.1 绪论（第1章）
- 研究背景、问题、方法、技术路线、创新与不足。

### Task 4.2 结论与启示（第5章）
- 回答研究问题，提炼政策启示，说明局限与未来研究方向。

### Task 4.3 一致性校验
- 检查“研究问题-方法-结果-结论”闭环是否一致。
- 检查 H1/H2/H3 是否均被结果有效回应。

### 🛑 CHECKPOINT 4
- [x] 五章草稿完整
- [x] 摘要与正文一致
- [x] 结论不超出证据边界
- 更新于：2026-03-01 +08:00（摘要已补写并通过一致性复核）

---

## PHASE 5：图表格式规范化（重新生成全部图表）

### Phase 5 质量测试结论（2026-03-02 测试）

对全部 28 张现有 PNG 图进行逐项检测，发现以下共性问题，**必须全部重新生成**：

| 问题 | 现状 | 要求 | 影响范围 |
|------|------|------|---------|
| DPI | 全部 200 DPI | ≥300 DPI | 28/28 张 |
| 字体 | sans-serif（Arial Unicode MS / SimHei） | serif（Songti SC + Times New Roman） | 28/28 张 |
| 配色 | 彩色（steelblue/蓝/橙/红/绿） | 可保留彩色，但需保证灰度打印可辨认 | ~18 张 |
| PDP 图标签 | Y 轴英文 "Partial dependence"、X 轴英文变量名 | 全中文 | 2 张 |
| figsize | 偏大（5×4 ~ 12×5 inch） | A4 单栏 3.5×2.8、双栏 6.3×2.8~5.0 inch | ~20 张 |

> 详细测试结论已汇总在 `notes/phase6_delivery_audit.md` 与 `logs/20260302/phase5_v3figure_run.log`（原 `notes/phase5_test/` 测试资产已清理）。

### 已验证的目标绘图参数

macOS 系统字体确认可用：`Songti SC` + `Times New Roman`。

```python
# scripts/thesis_plot_config.py — 统一绘图配置
THESIS_RCPARAMS = {
    'font.family': 'serif',
    'font.serif': ['Songti SC', 'SimSong', 'Times New Roman'],
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'axes.unicode_minus': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
}
GRAY_BAR = '#555555'        # 条形图填充
GRAY_BAR_EDGE = '#333333'   # 条形图边框
BLACK_LINE = 'black'        # 折线/ALE 线
GRAY_HIST = '#888888'       # 直方图填充
GRAY_LIGHT = '#999999'      # 辅助元素
```

### Task 5.1 创建共享绘图配置模块
- [x] 新建 `scripts/thesis_plot_config.py`，写入上述参数。
- [x] 所有绘图脚本统一导入此配置。

### Task 5.2 修改并重跑 `phase2_ale_pdp_plots.py`（24 张图）

改动清单：
- [x] 导入 `THESIS_RCPARAMS` 替换现有 `plt.rcParams`
- [x] `dpi=200` → `dpi=300`（共 5 处 `savefig`）
- [x] ALE 图 `figsize=(5,4)` → `(3.5, 2.8)`
- [x] 特征重要性条形图 `figsize=(7,8)` → `(4.5, 3.5)`，缩减为 Top 10
- [x] PDP 网格图 `figsize=(10,8)` → `(6.3, 5.0)`
- [x] PDP 网格 Y 轴 "Partial dependence" → "偏依赖值"
- [x] PDP 网格 X 轴英文变量名 → 中文标签
- [x] 条形图配色改为论文友好配色（可彩色；需保证灰度打印可辨认）
- [x] PDP 线色 → 黑色
- [x] **训练后保存模型到 `output/models/`**（RF → `rf_model.joblib`，GBDT → `gbdt_model.joblib`），后续重绘直接加载，无需重训
- [x] 所有新图输出到 **`output/figures_v2/`**（旧图保留在 `output/figures/` 不动）
- [x] 重新运行（需训练 RF 5000 trees + GBDT 3000 trees，计算密集；训练完成后模型持久化）

### Task 5.3 修改并重跑 `phase2_pca_analysis.py`（2 张图）

改动清单：
- [x] 导入 `THESIS_RCPARAMS`
- [x] `dpi=200` → `dpi=300`
- [x] 碎石图配色优化（可彩色；需保证灰度打印可辨认）
- [x] 注释位置优化（避免文字与数据点重叠）
- [x] `figsize` → `(5.5, 3.0)`
- [x] 热力图配色优化（可彩色或灰度；需保证灰度打印可辨认）
- [x] 所有新图输出到 **`output/figures_v2/`**
- [x] 重新运行（PCA 拟合轻量，快速完成）

### Task 5.4 修改并重跑 `phase3_placebo_plot.py`（1 张图）

改动清单：
- [x] 导入 `THESIS_RCPARAMS`
- [x] `dpi=200` → `dpi=300`
- [x] 柱色优化为论文友好配色（可彩色；需保证灰度打印可辨认）
- [x] 真实系数线 `color='red'` → `color='black', linewidth=1.5`
- [x] `figsize=(12,5)` → `(6.3, 2.8)`
- [x] 新图输出到 **`output/figures_v2/`**
- [x] 重新运行（读已有 CSV，无需重新计算）

### Task 5.5 新建 DID 平行趋势绘图脚本（1 张图）

- [x] 已补齐原缺口：`did_parallel_trends.png` 现已具备独立生成脚本（不再依赖 Stata 会话内导出）。
- [x] 新建 `scripts/phase5_did_trends_plot.py`，从 `output/tables/did_event_study_DivDummy.csv` + `did_event_study_DivPayRate.csv` 读取系数与置信区间，用 Python + `THESIS_RCPARAMS` 统一绘制。
- [x] 格式：双面板 `figsize=(6.3, 2.8)`，黑色误差线，灰色参考线。
- [x] 新图输出到 **`output/figures_v2/`**。

### Task 5.6 验证全部输出

重新生成后逐项验证（全部图位于 `output/figures_v2/`）：
- [x] 28 张 PNG 均为 ≥300 DPI
- [x] 字体为 Songti SC + Times New Roman（serif）
- [x] 黑白打印可辨认
- [x] 所有标签为中文
- [x] figsize 适配 A4 版面
- [x] 模型文件已保存至 `output/models/`（`rf_model.joblib`、`gbdt_model.joblib`）

### 表格说明（无需重跑）

CSV 表格数据（19 个文件）经核验数值正确，**不需要重新生成**。格式化工作在 Phase 6（Word 转排版）阶段完成：
- 三线表样式
- 系数精度 3–4 位小数
- 变量标签中文化
- esttab `.rtf` 输出 → Word 微调

### 回归结果表规范（适用于 Phase 6 Word 排版）

- **三线表**：顶线 1 磅、表头下细线 0.5 磅、底线 1 磅，无左右边框无纵线。必要时可加辅助线（如分隔面板），仍称三线表。
- **系数精度**：统一保留 3–4 位小数（`%9.3f` 或 `%9.4f`），同一张表内位数一致。
- **括号内容**：默认报告**标准误**（se），置于系数正下方圆括号中。若报告 t/z 统计量需在注释说明。
- **显著性星号**：`*** p<0.01, ** p<0.05, * p<0.1`，星号跟在系数后方（不在括号内）。注释置于表格底部。
- **控制变量/固定效应行**：用 `Yes` / `No` 标注，不输出系数。
- **底部统计量**：至少报告 N（观测值数）、R²（或 adj-R²/Pseudo-R²），可选 F 统计量。
- **数字对齐**：小数点对齐，缺失值用 `—` 而非空白。
- **变量标签**：使用中文经济含义标签（如"资产负债率"而非 `Lev`），英文缩写可在首次出现处括注。

### 描述性统计与相关系数表规范

- 同样使用三线表格式。
- 描述性统计至少报告：N、Mean、SD、Min、Median、Max。
- 相关系数矩阵：下三角列出 Pearson 相关系数，上三角列出 Spearman（如适用），对角线为 1 或空。
- 显著性用星号标注，规则同回归表。

### Stata / Python 工具链参考

**Stata**：
- 推荐 `esttab`（`estout` 包）或 `outreg2`，输出 `.rtf` 后在 Word 中微调。
- 常用命令模板：
  ```stata
  esttab m1 m2 m3 using "table.rtf", replace ///
      b(%9.3f) se(%9.3f) star(* 0.1 ** 0.05 *** 0.01) ///
      r2 ar2 N compress nogap ///
      mtitles("模型1" "模型2" "模型3") ///
      title("表X 基准回归结果") ///
      note("注：括号内为聚类稳健标准误；*** p<0.01, ** p<0.05, * p<0.1。")
  ```
- 输出 `.rtf` 后用 Word 打开 → 全选表格 → 套用三线表样式 → 调整字体为宋体五号/Times New Roman 10.5pt。

**Python**：
- 推荐 `stargazer`（`pip install stargazer`）输出 HTML → 粘贴到 Word；或用 `pandas.DataFrame.to_latex()` + LaTeX 编译。
- 替代方案：`statsmodels` 的 `summary2.summary_col()` 合并多模型 → `.as_latex()` 或手动转 DataFrame → `.to_csv()` → Excel → Word。
- 图表（matplotlib）保存时统一 `plt.savefig("fig.png", dpi=300, bbox_inches='tight')`。

### 🛑 CHECKPOINT 5
- [x] 共享绘图配置模块已创建
- [x] 全部 28 张图重新生成至 `output/figures_v2/`（300 DPI + serif）
- [x] PDP 图中文标签修复
- [x] DID 平行趋势图由独立 Python 脚本生成
- [x] 训练模型已持久化至 `output/models/`（rf_model.joblib + gbdt_model.joblib）
- [x] 逐图验证 DPI / 字体 / 配色 / 尺寸通过
- 更新于：2026-03-02 +08:00
---

## PHASE 6：风险排查与最终交付

### Task 6.1 Markdown → Word 转换与格式校对
转排版时逐项检查：
- [x] 所有表格已转为三线表（`phase6_format_tables.py` 自动应用 1pt/0.5pt/1pt 边框）
- [x] 表标题在表上方居中、图标题在图下方居中（审计脚本逐项验证通过）
- [x] 字体统一：表内宋体五号 / 英文数字 Times New Roman（`phase6_format_tables.py` 应用）
- [x] 注释格式 `注：xxx` 小五号左对齐（11 条注释全部格式化）
- [ ] 页码、页眉、目录已按模板设置（需人工在 Word 中最终确认）
- [x] 参考文献格式对齐 GB/T 7714（23 条，中文按拼音排序+英文按字母排序）
- [x] 图片分辨率 ≥ 300 dpi，无模糊/锯齿
- [x] 图标题不重复（已修复 Pandoc alt text 重复问题）

### Task 6.2 风险排查
- [x] 查重风险段落重写（第二轮深度改写：1.1开头段、2.1经典理论、2.2.3政策监管、2.2.4机器学习引入、3.1样本描述、3.3.1预测框架、4.1.1政策背景，共 8 处 HIGH 风险区域）；
- [x] 图表来源与口径复核；
- [x] 关键回归结果可重复运行；
- [x] 正文引用与参考文献列表一一对应（23 篇，无占位符）。

### Task 6.3 交付包
- [x] `output/paper/论文完整版.md`（含参考文献 + 后记 + 独创性声明）
- [x] `output/paper/论文终稿.docx`（postprocess_docx.py 全格式化）
- [x] `output/tables/`（19 个 CSV 文件）与 `output/figures_v3/`（28 张 300 DPI PNG）
- [x] `notes/` 全部方法与决策说明
- [x] `logs/` 完整执行日志（text + jsonl）
- 说明：`output/paper/论文完整版.md` 与 `论文终稿.docx` 属可再生产物，可按 Quick Run List 重建。

### 🛑 FINAL CHECKPOINT
- [x] 论文可提交版本完成（Markdown + DOCX 双版本，含参考文献+后记+独创性声明）
- [x] 全部图表与结论可追溯
- [x] 日志与复现材料齐全
- [x] phase6_audit.py 自动审计通过（8项门禁）
- [ ] 页眉/目录需人工在 Word 中最终确认
- 更新于：2026-03-03（补齐参考文献/后记/声明，更新改稿流程与审计门禁）


---

## 正文改动后的快速改稿清单（默认复用 Phase5/6 产物）

适用范围：仅修改正文文字、结构、表述、引用、脚注，不改数据与模型。

### 论文合并源文件清单

合并顺序如下（`scripts/phase5_prepare.py` 中 `FULL_PAPER_PARTS` 定义）：

| 序号 | 章节名 | 源文件 |
|------|--------|--------|
| 1 | 摘要 | `output/paper/abstract_draft.md` |
| 2 | 第一章 绪论 | `output/paper/chapter1_introduction_draft.md` |
| 3 | 第二章 文献综述与理论基础 | `output/paper/chapter2_lit_review.md` |
| 4 | 第三章 机器学习预测分析 | `output/paper/chapter3_ml_prediction_draft.md` |
| 5 | 第四章 DID因果评估 | `output/paper/chapter4_did_evaluation_draft.md` |
| 6 | 第五章 结论与启示 | `output/paper/chapter5_conclusion_draft.md` |
| 7 | 参考文献 | `output/paper/references_final.md` |
| 8 | 后记 | `output/paper/acknowledgment.md` |
| 9 | 论文独创性及授权声明 | `output/paper/declaration.md` |

### 复用基线（默认不重跑）
- 图表：`output/figures_v3/`（28 张 300 DPI，最新版本）
- 表格：`output/tables/`（现有结果表直接复用）
- 模型：`output/models/rf_model.joblib`、`output/models/gbdt_model.joblib`
- 脚本：`scripts/phase5_prepare.py`、`scripts/postprocess_docx.py`、`scripts/phase6_audit.py`

### 改稿前门禁（Quick Run 之前必须检查）

每次改稿前，Claude Code 必须逐项确认以下门禁：

1. [ ] 正文中所有文献引用使用"作者-年份"格式（无 R01/R02 占位符）
2. [ ] 正文中每条引用在 `references_final.md` 中有对应条目
3. [ ] `references_final.md` 中每条文献在正文中被引用
4. [ ] 图片路径统一指向 `../figures_v3/`（不混用 figures_v2）
5. [ ] 图编号全文连续（图1—图12），表编号全文连续（表1—表11）
6. [ ] 所有 9 个源文件均存在且非空

### Quick Run List（正文每改一轮执行一次）
1. 修改章节草稿（源文件见上表）。
2. 运行以下最小命令链（不重训、不重画）：
   ```bash
   cd /Users/mac/Desktop/Grad_thesis
   # Step 1: 合并章节 → 论文完整版.md
   /Users/mac/miniconda3/bin/python scripts/phase5_prepare.py
   # Step 2: Pandoc 导出 base docx（从 output/paper/ 目录运行以解析相对图片路径）
   cd output/paper && pandoc 论文完整版.md --reference-doc=../../商学院本科生毕业论文格式模板2025.01.docx --resource-path=. -o 论文终稿_base.docx && cd ../..
   # Step 3: 后处理格式化（三线表 + 段落格式 + 页码 + 图片缩放）
   /Users/mac/miniconda3/bin/python scripts/postprocess_docx.py
   # Step 4: 审计检查
   /Users/mac/miniconda3/bin/python scripts/phase6_audit.py
   ```
3. 检查 `notes/phase6_delivery_audit.md` 全部通过（8项门禁：占位符、图像DPI、编号连续性、DID复验、章节完整性、参考文献数量、DOCX导出）。
4. 若审计未通过，修复问题后重跑 Step 1—4。
5. Word 人工终检：页眉/页码/目录/封面。

### 最终产出文件
- `output/paper/论文完整版.md` — Markdown 合并稿（自动生成，勿手动编辑）
- `output/paper/论文终稿.docx` — 最终 Word 版（postprocess_docx.py 全格式化）
- `output/paper/论文终稿_base.docx` — Pandoc 直接输出（中间文件，可删除）

### 触发重跑规则（避免重复操作）
- 仅改文字/结构/引用：只跑 Quick Run List。
- 改图题、表题、编号、引用顺序：只跑 Quick Run List。
- 仅需重绘 DID 图：跑 `scripts/phase3_placebo_plot.py` 或 `scripts/phase5_did_trends_plot.py`，无需重训模型。
- 仅需重绘 PCA 图：跑 `scripts/phase2_pca_analysis.py --plots-only`。
- 需重绘 ALE/PDP/FI 图但不改数据：跑 `scripts/phase2_ale_pdp_plots.py`（优先加载 `output/models/` 已有模型）。
- 仅当数据、特征工程、模型参数或识别策略变更时，才允许重跑 Phase2/3 全量脚本。

### 默认禁止动作（正文改稿场景）
- 不执行 `scripts/phase2_ml_training.py`、`scripts/phase2_rf_and_summary.py`、`scripts/phase2_subsample.py`。
- 不执行 `scripts/phase3_did_stata_replication.do` 全量重跑。
- 不重复生成 `output/figures_v3/` 全部 28 张图，除非触发上述重跑条件。
---

## 执行优先级与容错策略

1. 优先保证“可复现 + 可解释 + 可提交”，再追求扩展分析。
2. 如数据缺失或口径不一致，先保留基准可运行版本，并在 `notes/` 记录限制。
3. 如 ML 与 DID 结论不一致，必须在讨论部分解释潜在机制，不得强行统一结论。

---

## Phase 5/6 执行后仍可能存在的残余风险

1. **人工排版偏差风险（Word）**  
   即使图表与表格按规范生成，Markdown→Word 及人工微调过程中仍可能出现字号、行距、题注位置、三线表线宽等细节偏差。

2. **本地环境依赖风险（Stata ado / 字体）**  
   结果复现仍依赖本机 Stata ado 包版本与 macOS 字体环境；在新机器或新账号下可能出现 `r(3499)` 或字体替代导致版式变化。

3. **随机过程微小波动风险（ML 重训练）**  
   RF/GBDT 在不同硬件线程或库版本下即使固定随机种子，仍可能出现极小数值波动；通常不影响结论方向，但会影响逐位比对。

4. **查重与表述规范风险（人工写作环节）**  
   查重高风险段落改写、证据边界措辞、引用格式一致性仍属于人工质量控制范围，自动化流程无法完全替代。

5. **外部规范变更风险（标准更新时点）**  
   当前（2026-03-02）参考文献仍按 GB/T 7714-2015 执行；GB/T 7714-2025 将于 2026-07-01 实施，后续提交时间若跨时点需再核对学校口径。
