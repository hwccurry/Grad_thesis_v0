# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chinese undergraduate thesis (商学院本科毕业论文):

> **上市公司为何分红？——来自机器学习预测与准自然实验的证据**

Investigates the "dividend puzzle" in China's A-share market through two complementary approaches:
1. **Machine learning prediction** (Chapter 3): Random Forest + Gradient Boosting to identify key predictors of dividend payout (replicating 陈运森等, 中国工业经济 2024)
2. **DID quasi-natural experiment** (Chapter 4): Causal effects of cash dividend "hard constraint" policies (《现金分红指引》2023 revision) using difference-in-differences (replicating 卿小权等, 财经研究 2025)

Three hypotheses: H1 (ML feature importance screening), H2 (policy causal effect via DID), H3 (heterogeneous treatment effects by lifecycle stage and agency costs).

## Repository Structure

```
参考文献/1/20240618102625WU_FILE_1/
├── 数据/数据-python/          # 12 CSV files (data.csv = full sample, subsets by ownership/cash flow/catering/etc.)
├── 程序/程序-python/          # ~20 Jupyter notebooks (ML analysis)
│   ├── results/               # Output PNG figures
│   ├── figures/               # ALE/PDP plot outputs
│   └── _exec_logs/            # Auto-execution logs and rendered notebooks
└── 程序/程序.do               # Stata do-file (data export from .dta to CSV)

参考文献/2/
├── 附件1：拆解数据压缩包/     # 10 Excel files for DID analysis (2020-2024 沪深A股主板)
├── 附件2：数据及程序代码/     # 数据.dta + 程序代码.do (Stata DID analysis)
└── 附件3：图表.docx           # Reference tables and figures

写作框架.md                    # Thesis chapter outline from advisor
商学院本科生毕业论文格式模板2025.01.docx  # Official format template
memory.md                      # Session memory log
```

## ML Analysis Architecture (Chapter 3)

**Data layout**: `data.csv` columns are `Stkcd, year, Dividend_ratio1, Dividend_ratio2, Dividend_ratio3, Dividend, [43 features]`. Features start at column index 6; response variables are at indices 1-5.

**Column index mapping**:
- `iloc[:, 2]` = `Dividend_ratio1` (股利支付率 / payout ratio) — primary regression target
- `iloc[:, 5]` = `Dividend` (是否发放现金股利 / binary) — classification target
- `iloc[:, 6:]` = all 43 predictor features (35 continuous + ind1-ind42 industry dummies with gaps)

**Training paradigm — "一年期训练" (1-year rolling)**:
- Train on year `t`, predict year `t+1`, rolling from 2006 to 2022 (16 iterations)
- StandardScaler fitted on `x_train1` (first year), applied to all subsequent years
- Loop: `for i in range(0,16): j=i+1; model.fit(x_train[i], y_train[i]); score(x_train[j], y_train[j])`

**Models and default hyperparameters**:
- `GradientBoostingRegressor(n_estimators=3000, max_depth=4, subsample=0.7, learning_rate=0.001)`
- `RandomForestRegressor(n_estimators=5000, max_features=10|19)` with `RandomizedSearchCV` for tuning
- Also benchmarked: Lasso, SVR, DecisionTree, MLP, LinearRegression (OLS)
- Classification variants: `GradientBoostingClassifier`, `RandomForestClassifier`

**Interpretability**: Custom ALE (Accumulated Local Effects) implementation in notebooks (functions `_first_order_ale_quant`, `ale_plot`); also `PartialDependenceDisplay` from sklearn.

**Key feature names** (English column names → Chinese labels):
- `Retainedearn_ratio` = 留存收益资产比, `Tunneling` = 其他应收款资产比, `Freecash2` = 自由现金流
- `Constraint` = 融资约束程度, `Institution` = 机构投资者持股比例, `Dividend_lag` = 上一期股利水平
- `Tax_ratio` = 实际税率, `Analyst_num` = 分析师跟踪人数, `Cashflow` = 每股经营活动现金流量

**Notebook naming**: `主检验-{训练方式}-{响应变量}[-{子样本/方法}].ipynb`
**CSV naming**: `data.csv` (full), `dataqian/datahou` (pre/post 2012), `dataguoyou/datafeiguoyou` (SOE/non-SOE), `datan-bigcash/data-smallcash` (high/low cash flow), `datacater/datauncater` (catering/non-catering), `data-guliup/data-gulidown` (dividend sentiment up/down)

## DID Analysis Architecture (Chapter 4)

**Stata workflow** (参考文献/2/附件2/程序代码.do):
- Policy shock: 2023 revision of《上市公司现金分红指引》
- Sample: 沪深A股主板 2020-2024, panel `xtset stkcd year`
- Controls: `SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT`
- Core command: `reghdfe DivDummy|DivPayRate did $ctrl, a(year stkcd) cl(stkcd) keepsingletons`
- Robustness: parallel trends (`coefplot`), placebo (1000 random permutations), Hausman-Taylor, PSM-DID (`psmatch2`), entropy balancing (`ebalance`), exclude refinancing samples
- Heterogeneity splits: `law_high` (法治水平), `SOE` (产权性质), `agc_high` (大股东代理成本), `insinv_high` (机构持股)
- Economic consequences: Volume, Turnover, Spread, Misvaluation

## Notebook Execution

Notebooks use a path-finding pattern for portability:
```python
TARGET_FOLDER = '参考文献/1/20240618102625WU_FILE_1'
PROJECT_ROOT = locate_project_root()  # walks up from cwd
DATA_DIR = PROJECT_ROOT / TARGET_FOLDER / '数据' / '数据-python'
```

Some older notebooks still hardcode `/Users/mac/Desktop/Grad_thesis/...` or Windows paths `D:\Users\...` — these need updating to the `locate_project_root()` pattern.

**Python dependencies**: pandas, numpy, scikit-learn, matplotlib, seaborn (no requirements.txt).

**Chinese font rendering**: Notebooks set `plt.rcParams['font.sans-serif']=['SimHei']` and `plt.rcParams['axes.unicode_minus']=False`.

## Thesis Writing Constraints

- Format: 商学院本科生毕业论文格式模板 2025.01
- References: ~20 total; CSSCI journals with impact factor >= 2; at least 1/3 from recent 3 years; avoid degree theses
- Literature review: Organize by thematic perspectives (not chronologically or domestic/foreign); include critical commentary (文献述评)
- Plagiarism: Do not copy-paste from references; paraphrase and restructure
- Figures/tables: Numbered consecutively; cite data sources
- All thesis text is in Chinese
