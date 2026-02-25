# Repro Environment (Phase 0.3)

## 环境
- OS: macOS-15.6-arm64-arm-64bit-Mach-O
- python解释器：`/Users/mac/miniconda3/bin/python`

## 最小闭环执行
- ML: 在 `data.csv` 上执行 `t=2007` 训练、`t+1=2008` 测试的 RandomForestRegressor。
- DID: 在 `数据.dta` 上执行 `DivDummy/DivPayRate ~ did + controls + year FE + stkcd FE`（cluster by stkcd）。
- 结果文件: `output/tables/phase0_minimal_repro_metrics.csv`

## 备注
- 该步骤用于验证可运行性，不替代正式章节回归设定。
## Miniconda 执行器
- Python 解释器：`/Users/mac/miniconda3/bin/python`
- 路径统一脚本：`/Users/mac/miniconda3/bin/python /Users/mac/Desktop/Grad_thesis/scripts/unify_notebook_paths.py`
