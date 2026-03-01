clear all
set more off

local datapath "/Users/mac/Desktop/Grad_thesis/参考文献/2/附件2：数据及程序代码/数据.dta"
local outdir "/Users/mac/Desktop/Grad_thesis/output/tables"

global ctrl SIZE AGE LEV ROA GROWTH CFO TOP INDEP MH HHI_BANK MKT

set seed 123

tempfile match_id
tempfile placebo_divdummy_dta
tempfile placebo_divpayrate_dta

tempname post_divdummy
postfile `post_divdummy' placebo_coef using "`placebo_divdummy_dta'", replace

forvalues i = 1/100 {
    quietly {
        use "`datapath'", clear
        xtset stkcd year
        sample 1, count by(stkcd)
        keep stkcd year
        rename year policy_year
        save "`match_id'", replace

        merge 1:m stkcd using "`datapath'"
        xtset stkcd year
        gen treatment = (_merge == 3)
        gen period = (year >= policy_year)
        gen did0 = treatment * period

        reghdfe DivDummy did0 $ctrl, a(year stkcd) cl(stkcd) keepsingletons
        post `post_divdummy' (_b[did0])
    }
}
postclose `post_divdummy'

use "`placebo_divdummy_dta'", clear
export delimited placebo_coef using "`outdir'/did_placebo_DivDummy.csv", replace
summarize placebo_coef
display "PLACEBO100|DivDummy|mean=" %9.6f r(mean) "|sd=" %9.6f r(sd) "|n=" r(N)

tempname post_divpay
postfile `post_divpay' placebo_coef using "`placebo_divpayrate_dta'", replace

forvalues i = 1/100 {
    quietly {
        use "`datapath'", clear
        xtset stkcd year
        sample 1, count by(stkcd)
        keep stkcd year
        rename year policy_year
        save "`match_id'", replace

        merge 1:m stkcd using "`datapath'"
        xtset stkcd year
        gen treatment = (_merge == 3)
        gen period = (year >= policy_year)
        gen did0 = treatment * period

        reghdfe DivPayRate did0 $ctrl, a(year stkcd) cl(stkcd) keepsingletons
        post `post_divpay' (_b[did0])
    }
}
postclose `post_divpay'

use "`placebo_divpayrate_dta'", clear
export delimited placebo_coef using "`outdir'/did_placebo_DivPayRate.csv", replace
summarize placebo_coef
display "PLACEBO100|DivPayRate|mean=" %9.6f r(mean) "|sd=" %9.6f r(sd) "|n=" r(N)
