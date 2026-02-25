use 数据.dta,clear
global ctrl SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT

*描述性统计
sum2docx DivDummy DivPayRate treat post $ctrl using 1.docx , replace stats(N mean sd min p25 median p75 max) title("表 1: 描述性统计") 



*单变量检验
use 数据.dta,clear
keep if treat==1
ttest DivPayRate if treat==1,by(post)
use 数据.dta,clear
keep if treat==0
ttest DivPayRate,by(post)



*基准回归
use 数据.dta,clear
reghdfe  DivDummy did ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy did $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons



*平行趋势检验
use 数据.dta,clear
gen period = year - 2023    
gen pre_1 = (period == -1 & treat ==1)
gen pre_2 = (period == -2 & treat ==1)
gen pre_3 = (period == -3 & treat ==1)
gen current = (period == 0 & treat ==1)    
gen time_1 = (period == 1 & treat ==1)

reghdfe DivDummy pre_3 pre_2 current time_1  $ctrl ,a(year  stkcd )  vce(cl stkcd) keepsingletons 
coefplot,levels(99) keep(  pre_3 pre_2  current time_1  ) vertical xline(3, lp(dash)) yline(0,lcolor(edkblue*0.8)) xline(5, lwidth(vthin) lpattern(dash) lcolor(teal)) ylabel(,labsize(*0.75)) xlabel(,labsize(*0.75)) ytitle(回归系数, size(small)) xtitle(政策实施相对时间(年), size(small)) coeflabels( pre_3="t{sub:-3}" pre_2="t{sub:-2}" current="t{sub:0}" time_1="t{sub:+1}") addplot(line @b @at) ciopts(lpattern(dash) recast(rcap) msize(medium)) msymbol(circle_hollow) scheme(s1mono)

reghdfe DivPayRate pre_3 pre_2 current time_1  $ctrl ,a(year  stkcd )  vce(cl stkcd) keepsingletons 
coefplot,levels(99) keep(  pre_3 pre_2  current time_1  ) vertical xline(3, lp(dash)) yline(0,lcolor(edkblue*0.8)) xline(5, lwidth(vthin) lpattern(dash) lcolor(teal)) ylabel(,labsize(*0.75)) xlabel(,labsize(*0.75)) ytitle(回归系数, size(small)) xtitle(政策实施相对时间(年), size(small)) coeflabels( pre_3="t{sub:-3}" pre_2="t{sub:-2}" current="t{sub:0}" time_1="t{sub:+1}") addplot(line @b @at) ciopts(lpattern(dash) recast(rcap) msize(medium)) msymbol(circle_hollow) scheme(s1mono)



*随机时间的安慰剂检验
mat b = J(1000,1,0)
mat se = J(1000,1,0)
mat p = J(1000,1,0)
forvalues i=1/1000{
 use 数据.dta, clear
 xtset stkcd year
 sample 1, count by(stkcd)
 keep stkcd year
 rename year policy_year
 save match_id_year.dta, replace
 merge 1:m stkcd using 数据.dta
 xtset stkcd year
 gen treatment = (_merge == 3)
 gen period = (year >= policy_year)
 gen did0 = treatment*period
 qui reghdfe  DivDummy did0 $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons
 mat b[`i',1] = _b[did0]
 mat se[`i',1] = _se[did0]
 mat p[`i',1] = 2*ttail(e(df_r), abs(_b[did0]/_se[did0]))
}
svmat b, names(coef)
svmat se, names(se)
svmat p, names(pvalue)
drop if pvalue1 == .
label var pvalue1 p值
label var coef1 估计系数
keep coef1 se1 pvalue1
kdensity coef1,normal scheme(qleanmono)

mat b = J(1000,1,0)
mat se = J(1000,1,0)
mat p = J(1000,1,0)
forvalues i=1/1000{
 use 数据.dta, clear
 xtset stkcd year
 sample 1, count by(stkcd)
 keep stkcd year
 rename year policy_year
 save match_id_year.dta, replace
 merge 1:m stkcd using 数据.dta
 xtset stkcd year
 gen treatment = (_merge == 3)
 gen period = (year >= policy_year)
 gen did0 = treatment*period
 qui reghdfe  DivPayRate did0 $ctrl ,a(year stkcd)  cl(stkcd)  keepsingletons
 mat b[`i',1] = _b[did0]
 mat se[`i',1] = _se[did0]
 mat p[`i',1] = 2*ttail(e(df_r), abs(_b[did0]/_se[did0]))
}
svmat b, names(coef)
svmat se, names(se)
svmat p, names(pvalue)
drop if pvalue1 == .
label var pvalue1 p值
label var coef1 估计系数
keep coef1 se1 pvalue1 
kdensity coef1,normal scheme(qleanmono)



*Hausman-Taylor估计模型
use 数据.dta,clear
tab year,gen(year)
tab Industry,gen(industry)
xthtaylor DivDummy did  $ctrl  year2-year5 industry2-industry20,endog(did)
xthtaylor DivPayRate did  $ctrl  year2-year5 industry2-industry20,endog(did)



*PSM
use 数据.dta,clear
psmatch2 treat $ctrl, out(DivDummy) logit ties neighbor(10) common caliper(.05)  odds 
drop if _weight == .
reghdfe DivDummy did $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons

use 数据.dta,clear
psmatch2 treat $ctrl, out(DivPayRate) logit ties neighbor(10) common caliper(.05)  odds 
drop if _weight == .
reghdfe DivPayRate did $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons



*熵平衡匹配
use 数据.dta,clear
ebalance  did $ctrl, target(1) keep(baltable) replace  
reghdfe DivDummy did $ctrl [pweight=_webal] ,a(year stkcd)   vce(cl stkcd) keepsingletons
reghdfe DivPayRate did $ctrl [pweight=_webal] ,a(year stkcd)   vce(cl stkcd) keepsingletons



*排除替代性解释
use 数据.dta,clear
reghdfe  DivDummy i.did##c.Capital_AR $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate i.did##c.Capital_AR $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy i.did##c.Asset_GR $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate i.did##c.Asset_GR $ctrl ,a(year stkcd)  cl(stkcd) keepsingletons



*剔除再融资样本
use 数据.dta,clear
reghdfe  DivDummy did $ctrl if refinance==0,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl if refinance==0,a(year stkcd)  cl(stkcd) keepsingletons



*异质性分析——法治化水平
use 数据.dta,clear
reghdfe  DivDummy did $ctrl if law_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy did $ctrl if law_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(law_high) model(cap reghdfe DivDummy did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs
reghdfe  DivPayRate did $ctrl if law_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl if law_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(high1) model(cap reghdfe DivPayRate did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs



*异质性分析——产权性质
use 数据.dta,clear
reghdfe  DivDummy did $ctrl if SOE==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy did $ctrl if SOE==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(SOE) model(cap reghdfe DivDummy did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs
reghdfe  DivPayRate did $ctrl if SOE==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl if SOE==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(SOE) model(cap reghdfe DivPayRate did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs



*异质性分析——大股东代理成本
use 数据.dta,clear
reghdfe  DivDummy did $ctrl if agc_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy did $ctrl if agc_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(agc_high) model(cap reghdfe DivDummy did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs
reghdfe  DivPayRate did $ctrl if agc_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl if agc_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(agc_high) model(cap reghdfe DivPayRate did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs



*异质性分析——机构持股
use 数据.dta,clear
reghdfe  DivDummy did $ctrl if insinv_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivDummy did $ctrl if insinv_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(insinv_high) model(cap reghdfe DivDummy did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs
reghdfe  DivPayRate did $ctrl if insinv_high==0 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  DivPayRate did $ctrl if insinv_high==1 ,a(year stkcd)  cl(stkcd) keepsingletons
bdiff, group(insinv_high) model(cap reghdfe DivPayRate did $ctrl ,absorb(year stkcd) cl(stkcd)  keepsingletons) seed(123) reps(1000) bs



*进一步讨论
use 数据.dta,clear
global ctrl1 SIZE1 AGE LEV ROA CFO INDEP TOP MH MB PRICE BETA
global ctrl2 SIZE1 AGE LEV ROA CFO INDEP TOP MH BETA
*1.交易量
reghdfe  Volume did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  Volume_1 did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
*2.换手率
reghdfe  Turnover did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  Turnover_1 did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
*3.买卖价差
reghdfe  Spread did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  Spread_1 did $ctrl1 ,a(year stkcd)  cl(stkcd) keepsingletons
*4.错误定价
reghdfe  Misvaluation did $ctrl2 ,a(year stkcd)  cl(stkcd) keepsingletons
reghdfe  Misvaluation_1 did $ctrl2 ,a(year stkcd)  cl(stkcd) keepsingletons














