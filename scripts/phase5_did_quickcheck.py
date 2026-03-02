#!/usr/bin/env python3
"""
Phase 5 quick reproducibility check for DID baseline coefficients.

Uses linearmodels.PanelOLS with entity/time fixed effects and firm-clustered SE.
Outputs:
  - output/tables/phase5_did_repro_check.csv
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
from linearmodels.panel import PanelOLS


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "参考文献" / "2" / "附件2：数据及程序代码" / "数据.dta"
OUT_PATH = ROOT / "output" / "tables" / "phase5_did_repro_check.csv"

CONTROLS = ["SIZE", "AGE", "LEV", "ROA", "GROWTH", "CFO", "TOP", "INDEP", "MH", "HHI_BANK", "MKT"]


def fit_one(df: pd.DataFrame, y: str, with_controls: bool) -> dict:
    cols = [y, "did", "stkcd", "year"] + (CONTROLS if with_controls else [])
    d = df[cols].dropna().copy()
    d["stkcd"] = d["stkcd"].astype(int)
    d["year"] = d["year"].astype(int)
    d = d.set_index(["stkcd", "year"])

    exog_cols = ["did"] + (CONTROLS if with_controls else [])
    model = PanelOLS(
        d[y],
        d[exog_cols],
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
    )
    res = model.fit(cov_type="clustered", cluster_entity=True)
    return {
        "outcome": y,
        "spec": "with_controls" if with_controls else "did_only",
        "did_coef": float(res.params["did"]),
        "did_t": float(res.tstats["did"]),
        "did_p": float(res.pvalues["did"]),
        "nobs": int(res.nobs),
    }


def main() -> None:
    df = pd.read_stata(DATA_PATH)
    rows = []
    for y in ["DivDummy", "DivPayRate"]:
        rows.append(fit_one(df, y, with_controls=False))
        rows.append(fit_one(df, y, with_controls=True))

    out = pd.DataFrame(rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print(f"saved: {OUT_PATH}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
