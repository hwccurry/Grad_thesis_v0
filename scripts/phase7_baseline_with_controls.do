* Phase 7: Export baseline DID regression with full control variable coefficients
* Workaround: Use xtreg fe to avoid areg/reghdfe Mata bug
set more off

use "/Users/mac/Desktop/Grad_thesis/参考文献/2/附件2：数据及程序代码/数据.dta", clear

global ctrl SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT
tab year, gen(yr_)

* Set panel
xtset stkcd year

* Model 2: DivDummy with controls (FE + year dummies + cluster)
xtreg DivDummy did $ctrl yr_*, fe vce(cluster stkcd)
