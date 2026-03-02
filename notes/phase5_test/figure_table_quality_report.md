# Phase 5 图表质量测试报告与再生计划

> 测试日期：2026-03-02
> 目的：评估现有图表是否满足毕业论文格式要求，决定重新生成策略

---

## 一、现有图表清单

| 类别 | 文件数 | 生成脚本 | 说明 |
|------|--------|---------|------|
| ALE 图（RF） | 10 | `phase2_ale_pdp_plots.py` | 单变量 ALE，图3–6 等 |
| ALE 图（GBDT） | 10 | `phase2_ale_pdp_plots.py` | 单变量 ALE |
| 特征重要性条形图 | 2 | `phase2_ale_pdp_plots.py` | 图1–2 |
| PDP 网格图 | 2 | `phase2_ale_pdp_plots.py` | 图7–8 |
| PCA 碎石图 | 1 | `phase2_pca_analysis.py` | 图9 |
| PCA 载荷热力图 | 1 | `phase2_pca_analysis.py` | 图10 |
| DID 平行趋势图 | 1 | 无独立脚本（需新建） | 图11 |
| DID 安慰剂检验图 | 1 | `phase3_placebo_plot.py` | 图12 |
| **合计** | **28** | | |

---

## 二、质量检测结果

### 2.1 DPI 检测

| 检测项 | 现状 | 要求 | 是否达标 |
|--------|------|------|----------|
| ALE 图（20张） | 978×776px, **200 DPI** | ≥300 DPI | **不达标** |
| 特征重要性图（2张） | 1380×1577px, **200 DPI** | ≥300 DPI | **不达标** |
| PDP 网格图（2张） | 1978×1638px, **200 DPI** | ≥300 DPI | **不达标** |
| PCA 碎石图 | 1977×1079px, **200 DPI** | ≥300 DPI | **不达标** |
| PCA 载荷热力图 | 1841×1978px, **200 DPI** | ≥300 DPI | **不达标** |
| DID 平行趋势 | 2379×975px, **200 DPI** | ≥300 DPI | **不达标** |
| DID 安慰剂 | 2377×974px, **200 DPI** | ≥300 DPI | **不达标** |

**结论：全部 28 张图均为 200 DPI，不满足论文 ≥300 DPI 的要求。**

### 2.2 字体检测

| 检测项 | 现状 | 要求 | 是否达标 |
|--------|------|------|----------|
| 中文字体 | `sans-serif`（Arial Unicode MS / SimHei） | `serif`（宋体 Songti SC） | **不达标** |
| 英文/数字字体 | sans-serif 继承 | Times New Roman | **不达标** |
| 字号 | 11–13pt 混用 | 统一 8–10pt（正文）/ 10–11pt（标题） | **基本达标** |

### 2.3 配色检测

| 检测项 | 现状 | 要求 | 是否达标 |
|--------|------|------|----------|
| 特征重要性图 | steelblue 单色 | 黑白/灰度优先 | **需调整** |
| ALE 图 | 黑色线条 | 黑白方案 | 达标 |
| PDP 网格图 | 蓝色线条 | 黑白优先 | **需调整** |
| PCA 碎石图 | 蓝色柱+橙色线+绿色注释 | 灰度优先 | **需调整** |
| DID 平行趋势 | 蓝色线+红色虚线 | 黑白优先 | **需调整** |
| DID 安慰剂 | 蓝色柱+红色虚线 | 灰度优先 | **需调整** |

### 2.4 内容与标签检测

| 检测项 | 问题描述 | 严重程度 |
|--------|----------|----------|
| PDP 网格图 Y 轴 | 英文 "Partial dependence"（应为"偏依赖值"） | **高** |
| PDP 网格图 X 轴 | 英文变量名 Retainedearn_ratio 等（应为中文） | **高** |
| PCA 碎石图注释 | "80%阈值" 文字与数据点重叠 | 中 |
| DID 平行趋势 Y 轴 | 字符间距不均匀 | 低 |

### 2.5 尺寸检测

| 图类型 | 现 figsize | 现像素@200dpi | 建议（A4版面） |
|--------|-----------|-------------|---------------|
| ALE 单图 | 5×4 inch | 978×776 | 3.5×2.8 inch（单栏 ~8.9cm） |
| 特征重要性 | 7×8 inch | 1380×1577 | 4.5×3.5 inch（单栏 ~11.4cm） |
| PDP 网格 | 10×8 inch | 1978×1638 | 6.3×5 inch（双栏 ~16cm） |
| PCA 碎石 | 10×5.5 inch | 1977×1079 | 5.5×3.0 inch（双栏 ~14cm） |
| DID 双面板 | 12×5 inch | 2379×975 | 6.3×2.8 inch（双栏 ~16cm） |

**现有图大多偏大，插入 Word 后会被缩放，导致字体变小。建议按 A4 版面目标尺寸设定 figsize。**

---

## 三、测试图输出验证

使用新参数（300 DPI + Songti SC serif + 灰度 + A4 尺寸）生成 5 张测试图：

| 测试图 | 像素 | DPI | 文件大小 | 视觉质量 |
|--------|------|-----|---------|---------|
| test1_feature_importance_300dpi.png | 1320×1019 | 300 | 103 KB | 中文宋体清晰，灰度打印友好 |
| test2_ale_300dpi.png | 1037×809 | 300 | 62 KB | 线条锐利，标签清晰 |
| test3_parallel_trends_300dpi.png | 1830×809 | 300 | 105 KB | 双面板紧凑，误差线清楚 |
| test4_placebo_300dpi.png | 1018×809 | 300 | 67 KB | 灰度直方图+黑色KDE线对比度佳 |
| test5_pca_scree_300dpi.png | 1619×870 | 300 | 105 KB | 灰度柱+黑色折线，注释不重叠 |

**测试结论：新参数方案可行，输出质量满足论文格式要求。**

---

## 四、可用系统字体确认

已验证 macOS 系统可用的关键字体：
- **中文 serif**: `Songti SC`, `SimSong`, `STFangsong`, `Kaiti SC`
- **英文 serif**: `Times New Roman`, `Times`
- **候选**: `Songti SC` + `Times New Roman`（与 CLAUDE.md 规范一致）

---

## 五、再生计划（推荐方案）

### 方案对比

| 方案 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| A. 全部重新生成 | 修改 3 个 Python 脚本 + 新建 1 个 DID 绘图脚本，重跑 | 输出一致、干净 | 需重训 RF/GBDT 模型 |
| B. 仅改 DPI 元数据 | sips 改 DPI 标签不改像素 | 最快 | **不推荐**：实际打印尺寸变小，字体模糊 |
| C. 修改脚本参数+重跑 | 同 A，但保持数据和模型逻辑不变 | 数据一致性有保障 | 同 A |

### 推荐：方案 A/C（本质相同）

**理由**：
1. 所有 28 张图都不达标，必须全部重新生成
2. 数据（CSV）和模型参数不需要改，只改绘图参数
3. 表格（CSV 格式）本身不需要重新生成，转 Word 时格式化即可

### 具体执行步骤

#### Step 1: 创建共享绘图配置模块

新建 `scripts/thesis_plot_config.py`，统一 rcParams：
```python
# 300 DPI + Songti SC + Times New Roman + 灰度方案
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
# 标准灰度色板
GRAY_BAR = '#555555'
GRAY_BAR_EDGE = '#333333'
BLACK_LINE = 'black'
GRAY_HIST = '#888888'
GRAY_LIGHT = '#999999'
```

#### Step 2: 修改 `phase2_ale_pdp_plots.py`（生成 24 张图）

改动清单：
- [x] `plt.rcParams` → 导入 `THESIS_RCPARAMS`
- [x] `dpi=200` → `dpi=300`（共 5 处）
- [x] ALE 图 `figsize=(5,4)` → `(3.5, 2.8)`
- [x] 特征重要性图 `figsize=(7,8)` → `(4.5, 3.5)`，缩减为 Top 10
- [x] PDP 网格 `figsize=(10,8)` → `(6.3, 5.0)`
- [x] PDP 网格 Y 轴 "Partial dependence" → "偏依赖值"
- [x] PDP 网格 X 轴英文变量名 → 中文标签
- [x] 条形图 `color='steelblue'` → `'#555555'`
- [x] PDP 线色 → 黑色

#### Step 3: 修改 `phase2_pca_analysis.py`（生成 2 张图）

改动清单：
- [x] `plt.rcParams` → 导入 `THESIS_RCPARAMS`
- [x] `dpi=200` → `dpi=300`
- [x] 碎石图柱色 → 灰度，折线 → 黑色
- [x] 注释位置优化（避免重叠）
- [x] `figsize` → `(5.5, 3.0)`
- [x] 热力图配色 → 灰度 cmap（如 `'Greys'` 或 `'RdBu'`）

#### Step 4: 修改 `phase3_placebo_plot.py`（生成 1 张图）

改动清单：
- [x] `plt.rcParams` → 导入 `THESIS_RCPARAMS`
- [x] `dpi=200` → `dpi=300`
- [x] 柱色 `'#3498db'` → `'#888888'`
- [x] 真实系数线 `color='red'` → `color='black', linewidth=1.5`
- [x] `figsize=(12,5)` → `(6.3, 2.8)`

#### Step 5: 新建 DID 平行趋势绘图脚本（生成 1 张图）

从 `did_event_study_DivDummy.csv` 和 `did_event_study_DivPayRate.csv` 读取数据，用 Python 重新绘制（替代原 Stata 输出），应用统一格式。

#### Step 6: 运行全部脚本

```bash
cd /Users/mac/Desktop/Grad_thesis
python3 scripts/phase2_ale_pdp_plots.py      # 24 张图（需训练 RF+GBDT）
python3 scripts/phase2_pca_analysis.py        # 2 张图
python3 scripts/phase3_placebo_plot.py        # 1 张图
python3 scripts/phase5_did_trends_plot.py     # 1 张图（新建）
```

### 关于表格

CSV 表格数据本身**不需要重新生成**（数据正确），但转 Word 时需要：
- 按三线表格式化
- 系数精度统一为 3–4 位小数
- 变量标签换为中文
- 这些是 Word 排版阶段的工作，不涉及重跑程序

---

## 六、工作量评估

| 步骤 | 内容 | 是否需要重新跑数据 |
|------|------|-------------------|
| 创建共享配置 | 新建 1 个文件 | 否 |
| 修改 ALE/PDP 脚本 | 改绘图参数 | **是**（需训练 RF+GBDT 各 1 次） |
| 修改 PCA 脚本 | 改绘图参数 | **是**（需 PCA 拟合，很快） |
| 修改安慰剂脚本 | 改绘图参数 | 否（读已有 CSV） |
| 新建平行趋势脚本 | 新建 | 否（读已有 CSV） |
| Word 表格排版 | 手工 + esttab | 否 |

**核心瓶颈**：`phase2_ale_pdp_plots.py` 需要训练 RF(5000 trees) + GBDT(3000 trees)，这是计算密集步骤，其余均为轻量操作。

---

## 七、最终结论

**必须重新生成全部 28 张图。** 主要原因：
1. DPI 全部不达标（200 vs 要求 ≥300）
2. 字体不符合论文规范（sans-serif vs 要求 serif/宋体）
3. PDP 图标签为英文（需改为中文）
4. 配色不利于黑白打印

建议在确认启动 Phase 5 后，按上述 Step 1–6 顺序执行。
