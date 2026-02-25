global dir0 "D:\111学习资料\111论文\股利分配理论\陈运森+论文附件\数据"
global dir1 "D:\111学习资料\111论文\股利分配理论\陈运森+论文附件\程序"

cd $dir1

global var Managefee_ratio Manageshare Indep_ratio Bgender Bshare Bage Btenure Bsalary ///
Equity Da_abs Tunneling Top1 Sharebalance Minorityrate Institution Pledge Retainedearn_ratio Freecash2 ///
Tax_avoid Tax_ratio Tax_volatility Constraint Refinance Sentiment Dividend_lag ROA Cashflow Tobinq   ///
BM Lev Soe Growth Lnsize Analyst_num Market_idx ind1-ind5 ind7 ind8 ind11-ind12 ind15-ind35 ind37-ind42


global lianxu Managefee_ratio Manageshare Indep_ratio Bgender Bshare Bage Btenure Bsalary ///
Equity Tunneling Top1 Sharebalance Minorityrate Institution Pledge Da_abs Retainedearn_ratio Freecash2 ///
Tax_avoid Tax_ratio Tax_volatility Constraint Refinance Sentiment Dividend_lag ROA Cashflow Tobinq   ///
BM Lev Soe Growth Lnsize Analyst_num Market_idx

*********************主结果
use $dir0\数据,clear
order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var
cap drop miss
egen miss = rmiss(Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var)
keep if miss == 0
drop miss

winsor2 Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 $lianxu, replace cuts(1 99) by(year)
drop if year <2006
tab year Dividend 

preserve
keep Dividend_ratio1  $var
order Dividend_ratio1  $var
drop ind1-ind5 ind7 ind8 ind11-ind12 ind15-ind35 ind37-ind42
outreg2 using miaoshuxing.xls,replace sum(detail) eqkeep(N mean sd min p50 max) bdec(4) 
restore


***导出结果
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\data.csv", replace


preserve
keep if year <2012
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\dataqian.csv", replace
restore

preserve
keep if year >2013
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datahou.csv", replace
restore

***股利情绪划分
preserve
keep if year == 2007 | year == 2008 | year == 2010 | year == 2011 | year == 2012 | year == 2013 | year == 2017 | year == 2020
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\data-guliup.csv", replace
restore

preserve
drop if year == 2007 | year == 2008 | year == 2010 | year == 2011 | year == 2012 | year == 2013 | year == 2017 | year == 2020
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\data-gulidown.csv", replace
restore


global var1 Managefee_ratio Manageshare Indep_ratio Bgender Bshare Bage Btenure Bsalary ///
Equity Da_abs Tunneling Top1 Sharebalance Minorityrate Institution Pledge Retainedearn_ratio Freecash2 ///
Tax_avoid Tax_ratio Tax_volatility Constraint Refinance Sentiment Dividend_lag ROA Cashflow Tobinq   ///
BM Lev Growth Lnsize Analyst_num Market_idx ind1-ind5 ind7 ind8 ind11-ind12 ind15-ind35 ind37-ind42 
 
***国有
preserve
keep if Soe == 1
order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var1
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var1
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\dataguoyou.csv", replace
restore

***非国有
preserve
keep if Soe == 0
order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var1
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var1
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datafeiguoyou.csv", replace
restore

***补充异质性分析
use $dir0\数据,clear
order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var ind_1
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var ind_1
cap drop miss
egen miss = rmiss(Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var)
keep if miss == 0
drop miss

winsor2 Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 $lianxu, replace cuts(1 99) by(year)
tab year Dividend 
drop if year <2006
tab year Dividend 
sort year ind_1
by year ind_1 : egen median_cash = median(Freecash2)

preserve
keep if Freecash2 < median_cash
drop ind_1  median_cash
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\data-smallcash.csv", replace
restore

preserve
keep if Freecash2 > median_cash
drop ind_1 median_cash
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datan-bigcash.csv", replace
restore


***保留相同数量
global varsame1 Da_abs Tunneling Retainedearn_ratio Tax_ratio Constraint Sentiment Dividend_lag ROA Cashflow Tobinq   ///
BM Lev Soe Growth Lnsize Analyst_num  Market_idx ind1-ind5 ind7 ind8 ind11-ind12 ind15-ind35 ind37-ind42


***保留同一特征
use $dir0\main,clear

order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $varsame1
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $varsame1
cap drop miss
egen miss = rmiss(Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $varsame1)
keep if miss == 0
drop miss

winsor2 Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 $varsame1, replace cuts(1 99) by(year)
tab year Dividend 
drop if year <2006
tab year Dividend 

export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datasame1.csv", replace


***可分配利润划分
use $dir0\数据,clear

gen fenpei = stock*Dividend_per
gen rule = 3*(fenpei+l.fenpei+l2.fenpei)/(A003105000+l.A003105000+l2.A003105000)
gen isfenpei = 0
replace isfenpei = 1 if rule <=0.4 & rule >=0.3
order Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var isfenpei
keep Stkcd year Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var isfenpei

cap drop miss
egen miss = rmiss(Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 Dividend $var isfenpei)
keep if miss == 0
drop miss

winsor2 Dividend_ratio1 Dividend_ratio2 Dividend_ratio3 $lianxu isfenpei , replace cuts(1 99) by(year)
tab year Dividend 
drop if year <2006
tab year isfenpei 

preserve
keep if isfenpei == 1
drop isfenpei
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datacater.csv", replace
restore

preserve
keep if isfenpei == 0
drop isfenpei
export delimited using "C:\Users\zjy19\Desktop\notebook\股利分配\rawdata\datauncater.csv", replace
restore

