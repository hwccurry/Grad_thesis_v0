# Python 路径统一（Miniconda）

更新时间：2026-02-25 15:47 +08:00

## 执行器
- 统一使用 Miniconda Python：`/Users/mac/miniconda3/bin/python`

## 已执行
- 脚本：`scripts/unify_notebook_paths.py`
- 批量处理目录：`参考文献/1/20240618102625WU_FILE_1/程序/程序-python/*.ipynb`
- 实际改动：19 个 notebook

## 统一规则
- 在 notebook 顶部加入项目根目录定位逻辑（`Path.cwd()` 向上查找 `Grad_thesis`）。
- 统一数据目录变量：`DATA_DIR`
- 统一输出目录变量：`TABLE_DIR`、`FIG_DIR`、`ML_DIR`
- 绝对路径替换为：
  - `pd.read_csv(DATA_DIR / 'xxx.csv', header=0)`
  - `open(TABLE_DIR / 'xxx.xls','w')`
  - `plt.savefig(ML_DIR / 'xxx.png', dpi=...)`

## 校验结果
- source 代码中的绝对路径残留：0
- notebook JSON 完整性：20/20 可正常解析

## 后续执行命令
```bash
/Users/mac/miniconda3/bin/python /Users/mac/Desktop/Grad_thesis/scripts/unify_notebook_paths.py
```
