# Data & Code Inventory (Phase 0.1)

## 1) 目录与入口
- ML 主目录: `参考文献/1/20240618102625WU_FILE_1`
- DID 主目录: `参考文献/2`
- ML Stata 预处理入口: `参考文献/1/20240618102625WU_FILE_1/程序/程序.do`
- DID 回归入口: `参考文献/2/附件2：数据及程序代码/程序代码.do`
- ML Notebook 数量: 25

## 2) ML 数据文件（CSV）
| 文件 | 行数 | 列数 | 前8列 |
|---|---:|---:|---|
| data-gulidown.csv | 19284 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| data-guliup.csv | 12185 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| data-smallcash.csv | 15588 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| data.csv | 31469 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| datacater.csv | 2411 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| datafeiguoyou.csv | 18175 | 76 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| dataguoyou.csv | 13294 | 76 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| datahou.csv | 22421 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| datan-bigcash.csv | 15588 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| dataqian.csv | 5722 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |
| datasame1.csv | 31469 | 58 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Minorityrate', 'Tunneling', 'Retainedearn_ratio']` |
| datauncater.csv | 29058 | 77 | `['Stkcd', 'year', 'Dividend_ratio1', 'Dividend_ratio2', 'Dividend_ratio3', 'Dividend', 'Managefee_ratio', 'Manageshare']` |

## 3) DID 主数据（Stata）
- 文件: `参考文献/2/附件2：数据及程序代码/数据.dta`
- 维度: 9004 行 × 38 列
- 年份范围: 2020.0 - 2024.0
- 关键变量（存在）: `['DivDummy', 'DivPayRate', 'did', 'treat', 'post', 'SIZE', 'AGE', 'LEV', 'ROA', 'GROWTH', 'CFO', 'TOP', 'INDEP', 'MH', 'HHI_BANK', 'MKT', 'stkcd', 'year']`

## 4) 路径审计（Task 0.2）
- 含硬编码绝对路径的 Notebook: 19 个
- 已使用 `locate_project_root` 动态定位的 Notebook: 2 个
- `程序.do` 存在大量 Windows 输出路径（`C:\Users\...`）与旧目录配置（`D:\...`）。
- `程序代码.do` 使用相对路径 `use 数据.dta, clear`，迁移成本较低。

## 5) 建议的统一路径策略
- Python: 统一加入 `Path.cwd()` 向上查找 `Grad_thesis` 根目录，再拼接相对路径。
- Stata: 在 do-file 顶部定义项目根目录宏（如 `global proj_root`），所有输入输出改为 `$proj_root/...`。
- 输出统一落到 `output/tables`、`output/figures`，中间日志落到 `logs/YYYYMMDD`。