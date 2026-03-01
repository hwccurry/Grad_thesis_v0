/*==============================================================================
  Phase 3: DID准自然实验 —— Stata 高一致度复现脚本

  说明：本脚本按参考文献2的 Stata 路径复现核心分析，使用
       reghdfe/psmatch2/ebalance/xthtaylor/bdiff 等命令。
       当前 bdiff 默认 reps(200) 作为计算折中（参考 do 为 reps(1000)）。

  数据：参考文献/2/附件2：数据及程序代码/数据.dta
  执行：逐段通过 Stata MCP (stata_run_selection) 执行，或本地 Stata 全量执行

  日期：2026-03-01
==============================================================================*/

clear all
set more off

* ─── 路径与全局宏 ──────────────────────────────────────────
local datapath "/Users/mac/Desktop/Grad_thesis/参考文献/2/附件2：数据及程序代码/数据.dta"
global ctrl SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT
local bdiff_reps 200


*==============================================================================
* 1. 描述性统计
*==============================================================================
use "`datapath'", clear
sum DivDummy DivPayRate treat post $ctrl, detail


*==============================================================================
* 2. 基准回归 (4个规格)
*==============================================================================
use "`datapath'", clear
reghdfe DivDummy did, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy did $ctrl, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl, a(year stkcd) cl(stkcd) keepsingletons


*==============================================================================
* 3. 平行趋势检验 (事件研究)
*==============================================================================
use "`datapath'", clear
gen period = year - 2023
gen pre_1 = (period == -1 & treat == 1)
gen pre_2 = (period == -2 & treat == 1)
gen pre_3 = (period == -3 & treat == 1)
gen current = (period == 0 & treat == 1)
gen time_1 = (period == 1 & treat == 1)

reghdfe DivDummy pre_3 pre_2 current time_1 $ctrl, a(year stkcd) vce(cl stkcd) keepsingletons
coefplot, levels(99) keep(pre_3 pre_2 current time_1) vertical ///
    xline(3, lp(dash)) yline(0, lcolor(edkblue*0.8)) ///
    ylabel(, labsize(*0.75)) xlabel(, labsize(*0.75)) ///
    ytitle(回归系数, size(small)) xtitle(政策实施相对时间(年), size(small)) ///
    coeflabels(pre_3="t{sub:-3}" pre_2="t{sub:-2}" current="t{sub:0}" time_1="t{sub:+1}") ///
    addplot(line @b @at) ciopts(lpattern(dash) recast(rcap) msize(medium)) ///
    msymbol(circle_hollow) scheme(s1mono)

reghdfe DivPayRate pre_3 pre_2 current time_1 $ctrl, a(year stkcd) vce(cl stkcd) keepsingletons
coefplot, levels(99) keep(pre_3 pre_2 current time_1) vertical ///
    xline(3, lp(dash)) yline(0, lcolor(edkblue*0.8)) ///
    ylabel(, labsize(*0.75)) xlabel(, labsize(*0.75)) ///
    ytitle(回归系数, size(small)) xtitle(政策实施相对时间(年), size(small)) ///
    coeflabels(pre_3="t{sub:-3}" pre_2="t{sub:-2}" current="t{sub:0}" time_1="t{sub:+1}") ///
    addplot(line @b @at) ciopts(lpattern(dash) recast(rcap) msize(medium)) ///
    msymbol(circle_hollow) scheme(s1mono)


*==============================================================================
* 4. 安慰剂检验 (100次随机政策时间)
*==============================================================================

* DivDummy
mat b = J(100,1,0)
mat se = J(100,1,0)
mat p = J(100,1,0)
forvalues i=1/100 {
    use "`datapath'", clear
    xtset stkcd year
    sample 1, count by(stkcd)
    keep stkcd year
    rename year policy_year
    tempfile match_tmp
    save `match_tmp', replace
    merge 1:m stkcd using "`datapath'"
    xtset stkcd year
    gen treatment = (_merge == 3)
    gen period = (year >= policy_year)
    gen did0 = treatment * period
    qui reghdfe DivDummy did0 $ctrl, a(year stkcd) cl(stkcd) keepsingletons
    mat b[`i',1] = _b[did0]
    mat se[`i',1] = _se[did0]
    mat p[`i',1] = 2*ttail(e(df_r), abs(_b[did0]/_se[did0]))
}
svmat b, names(coef)
svmat se, names(se)
svmat p, names(pvalue)
drop if pvalue1 == .
keep coef1 se1 pvalue1
sum coef1
kdensity coef1, normal scheme(qleanmono)

* DivPayRate
mat b = J(100,1,0)
mat se = J(100,1,0)
mat p = J(100,1,0)
forvalues i=1/100 {
    use "`datapath'", clear
    xtset stkcd year
    sample 1, count by(stkcd)
    keep stkcd year
    rename year policy_year
    tempfile match_tmp
    save `match_tmp', replace
    merge 1:m stkcd using "`datapath'"
    xtset stkcd year
    gen treatment = (_merge == 3)
    gen period = (year >= policy_year)
    gen did0 = treatment * period
    qui reghdfe DivPayRate did0 $ctrl, a(year stkcd) cl(stkcd) keepsingletons
    mat b[`i',1] = _b[did0]
    mat se[`i',1] = _se[did0]
    mat p[`i',1] = 2*ttail(e(df_r), abs(_b[did0]/_se[did0]))
}
svmat b, names(coef)
svmat se, names(se)
svmat p, names(pvalue)
drop if pvalue1 == .
keep coef1 se1 pvalue1
sum coef1
kdensity coef1, normal scheme(qleanmono)


*==============================================================================
* 5. Hausman-Taylor估计
*==============================================================================
use "`datapath'", clear
tab year, gen(year)
tab Industry, gen(industry)
xthtaylor DivDummy did $ctrl year2-year5 industry2-industry20, endog(did)
xthtaylor DivPayRate did $ctrl year2-year5 industry2-industry20, endog(did)


*==============================================================================
* 6. PSM-DID
*==============================================================================
use "`datapath'", clear
psmatch2 treat $ctrl, out(DivDummy) logit ties neighbor(10) common caliper(.05) odds
drop if _weight == .
reghdfe DivDummy did $ctrl, a(year stkcd) cl(stkcd) keepsingletons

use "`datapath'", clear
psmatch2 treat $ctrl, out(DivPayRate) logit ties neighbor(10) common caliper(.05) odds
drop if _weight == .
reghdfe DivPayRate did $ctrl, a(year stkcd) cl(stkcd) keepsingletons


*==============================================================================
* 7. 熵平衡匹配
*==============================================================================
use "`datapath'", clear
ebalance did $ctrl, target(1)
reghdfe DivDummy did $ctrl [pweight=_webal], a(year stkcd) vce(cl stkcd) keepsingletons
reghdfe DivPayRate did $ctrl [pweight=_webal], a(year stkcd) vce(cl stkcd) keepsingletons


*==============================================================================
* 8. 排除替代性解释
*==============================================================================
use "`datapath'", clear
reghdfe DivDummy i.did##c.Capital_AR $ctrl, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate i.did##c.Capital_AR $ctrl, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy i.did##c.Asset_GR $ctrl, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate i.did##c.Asset_GR $ctrl, a(year stkcd) cl(stkcd) keepsingletons


*==============================================================================
* 9. 剔除再融资样本
*==============================================================================
use "`datapath'", clear
reghdfe DivDummy did $ctrl if refinance==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl if refinance==0, a(year stkcd) cl(stkcd) keepsingletons


*==============================================================================
* 10. 异质性分析 + Bootstrap组间差异检验
* 注：当前默认 reps(200) 为计算折中；如需逐参数严格同参考 do，可改为 reps(1000)
*==============================================================================

* 10a. 代理成本 (agc_high)
use "`datapath'", clear
reghdfe DivDummy did $ctrl if agc_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy did $ctrl if agc_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(agc_high) model(cap reghdfe DivDummy did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

reghdfe DivPayRate did $ctrl if agc_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl if agc_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(agc_high) model(cap reghdfe DivPayRate did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

* 10b. 产权性质 (SOE)
use "`datapath'", clear
reghdfe DivDummy did $ctrl if SOE==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy did $ctrl if SOE==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(SOE) model(cap reghdfe DivDummy did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

reghdfe DivPayRate did $ctrl if SOE==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl if SOE==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(SOE) model(cap reghdfe DivPayRate did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

* 10c. 法治化水平 (law_high)
use "`datapath'", clear
reghdfe DivDummy did $ctrl if law_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy did $ctrl if law_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(law_high) model(cap reghdfe DivDummy did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

reghdfe DivPayRate did $ctrl if law_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl if law_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(law_high) model(cap reghdfe DivPayRate did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

* 10d. 机构持股 (insinv_high)
use "`datapath'", clear
reghdfe DivDummy did $ctrl if insinv_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivDummy did $ctrl if insinv_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(insinv_high) model(cap reghdfe DivDummy did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs

reghdfe DivPayRate did $ctrl if insinv_high==0, a(year stkcd) cl(stkcd) keepsingletons
reghdfe DivPayRate did $ctrl if insinv_high==1, a(year stkcd) cl(stkcd) keepsingletons
bdiff, group(insinv_high) model(cap reghdfe DivPayRate did $ctrl, absorb(year stkcd) cl(stkcd) keepsingletons) seed(123) reps(`bdiff_reps') bs


*==============================================================================
* 11. 经济后果分析
*==============================================================================
use "`datapath'", clear
global ctrl1 SIZE1 AGE LEV ROA CFO INDEP TOP MH MB PRICE BETA
global ctrl2 SIZE1 AGE LEV ROA CFO INDEP TOP MH BETA

* 交易量
reghdfe Volume did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
reghdfe Volume_1 did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
* 换手率
reghdfe Turnover did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
reghdfe Turnover_1 did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
* 买卖价差
reghdfe Spread did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
reghdfe Spread_1 did $ctrl1, a(year stkcd) cl(stkcd) keepsingletons
* 错误定价
reghdfe Misvaluation did $ctrl2, a(year stkcd) cl(stkcd) keepsingletons
reghdfe Misvaluation_1 did $ctrl2, a(year stkcd) cl(stkcd) keepsingletons
