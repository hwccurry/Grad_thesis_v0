* Phase6 compatibility patch for broken Mata function registry (r(3499))
* Safe to run multiple times.

capture noisily mata: st_numscalar("__has_strtoreal", strtoreal("1"))
if _rc {
    di as txt "[compat] patching missing Mata function: strtoreal()"
    mata:
    real matrix strtoreal(string matrix S)
    {
        real matrix R
        pragma unset R
        (void) _strtoreal(S, R)
        return(R)
    }
    end
}

capture noisily mata: st_numscalar("__has_max", max((1,2)))
if _rc {
    di as txt "[compat] patching missing Mata function: max()"
    mata:
    real scalar max(real matrix X)
    {
        real scalar i, j, m
        if (rows(X)==0 | cols(X)==0) return(.)
        m = X[1,1]
        for (i=1; i<=rows(X); i++) {
            for (j=1; j<=cols(X); j++) {
                if (X[i,j] > m) m = X[i,j]
            }
        }
        return(m)
    }
    end
}

capture noisily mata: st_numscalar("__has_min", min((1,2)))
if _rc {
    di as txt "[compat] patching missing Mata function: min()"
    mata:
    real scalar min(real matrix X)
    {
        real scalar i, j, m
        if (rows(X)==0 | cols(X)==0) return(.)
        m = X[1,1]
        for (i=1; i<=rows(X); i++) {
            for (j=1; j<=cols(X); j++) {
                if (X[i,j] < m) m = X[i,j]
            }
        }
        return(m)
    }
    end
}

capture noisily mata: st_local("__has_tokens", invtokens(tokens("a b"), ","))
if _rc {
    di as txt "[compat] patching missing Mata function: tokens()"
    mata:
    string rowvector tokens(string scalar s)
    {
        real scalar i, n, start
        string rowvector out
        out = J(1,0,"")
        n = strlen(s)
        i = 1
        while (i<=n) {
            while (i<=n & substr(s,i,1)==" ") i++
            if (i>n) break
            start = i
            while (i<=n & substr(s,i,1)!=" ") i++
            out = out, substr(s,start,i-start)
        }
        return(out)
    }
    end
}

capture noisily mata: st_local("__has_invtokens", invtokens(("a","b"), ","))
if _rc {
    di as txt "[compat] patching missing Mata function: invtokens()"
    mata:
    string scalar invtokens(string rowvector s, |string scalar separator)
    {
        real scalar i
        string scalar out, sep
        if (args()==1) sep = " "
        else sep = separator
        if (cols(s)==0) return("")
        out = s[1]
        for (i=2; i<=cols(s); i++) {
            out = out + sep + s[i]
        }
        return(out)
    }
    end
}

capture noisily mata: st_local("__has_pathlist", invtokens(pathlist(), ";"))
if _rc {
    di as txt "[compat] patching missing Mata function: pathlist()"
    mata:
    string rowvector pathlist(|string scalar dirpath)
    {
        real scalar i, n, start
        string scalar p
        string rowvector out
        if (args()==0) p = st_global("S_ADO")
        else p = dirpath

        out = J(1,0,"")
        n = strlen(p)
        i = 1
        while (i<=n) {
            start = i
            while (i<=n & substr(p,i,1)!=";") i++
            out = out, substr(p,start,i-start)
            i++
        }
        return(out)
    }
    end
}

capture noisily mata: st_local("__has_findfile", findfile("xtreg.ado"))
if _rc {
    di as txt "[compat] patching missing Mata function: findfile()"
    mata:
    string scalar findfile(string scalar fn, |string scalar p)
    {
        real scalar rc
        string scalar cmd
        if (fn=="") return("")
        if (args()==1) cmd = "capture quietly findfile " + fn
        else cmd = "capture quietly findfile " + fn + ", path(" + p + ")"
        rc = _stata(cmd, 1)
        if (rc) return("")
        return(st_global("r(fn)"))
    }
    end
}

* quick check summary
capture noisily mata: st_numscalar("__ok1", strtoreal("1.2"))
di "[compat] strtoreal_rc=" _rc
capture noisily mata: st_numscalar("__ok2", max((1,2,3)))
di "[compat] max_rc=" _rc
capture noisily mata: st_local("__ok3", invtokens(tokens("a b"), ","))
di "[compat] tokens_rc=" _rc
capture noisily mata: st_local("__ok4", findfile("xtreg.ado"))
di "[compat] findfile_rc=" _rc
