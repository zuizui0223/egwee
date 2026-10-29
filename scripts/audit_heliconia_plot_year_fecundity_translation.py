#!/usr/bin/env python3
"""Exploratory Heliconia plot/year decomposition of documented flowering vs recruits.

What survives additive plot and year effects? All candidate lag measures use
the SAME ten fixed plots x five years. The effects are correlational and
strongly post-outcome-exposure; no p-values or causal mediation are estimated.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from audit_heliconia_forward_lag_prediction import archive_rows

YEARS=tuple(range(2001,2006))
X_FIELDS={
    "lag1_flowering": "fl1",
    "lag2_flowering": "fl2",
    "lag3_flowering": "fl3",
    "lag1_inflorescences": "inflo1",
    "lag2_inflorescences": "inflo2",
}

def correlation(x: list[float], y: list[float]) -> float | None:
    assert len(x)==len(y)
    n=len(x)
    if n<3:
        return None
    mx=sum(x)/n
    my=sum(y)/n
    denom=math.sqrt(sum((v-mx)**2 for v in x)*sum((v-my)**2 for v in y))
    if denom<1e-12:
        return None
    return sum((v-mx)*(w-my) for v,w in zip(x,y))/denom

def residualize(rows: list[dict], var: str, effects: str) -> list[float]:
    """Unbalanced-safe algebra for one or two fixed-effect sets via projection.

    In this program every ranch/year deletion still contains the same number
    of plots in every retained year, so the direct two-way mean projection
    is exact; assert this balance to avoid silently using an invalid formula.
    """
    values=[r[var] for r in rows]
    if effects=="none":
        a=sum(values)/len(rows)
        return [v-a for v in values]
    if effects=="plot":
        counts=defaultdict(list)
        for r,v in zip(rows,values):
            counts[r["plot"]].append(v)
        mu={k:sum(v)/len(v) for k,v in counts.items()}
        return [v-mu[r["plot"]] for r,v in zip(rows,values)]
    if effects=="year":
        counts=defaultdict(list)
        for r,v in zip(rows,values):
            counts[r["year"]].append(v)
        mu={k:sum(v)/len(v) for k,v in counts.items()}
        return [v-mu[r["year"]] for r,v in zip(rows,values)]
    assert effects=="plot_and_year"
    plots=sorted({r["plot"] for r in rows})
    years=sorted({r["year"] for r in rows})
    assert len(rows)==len(plots)*len(years)
    assert len({(r["plot"],r["year"]) for r in rows})==len(rows)
    total=sum(values)/len(values)
    ps={p:sum(v for r,v in zip(rows,values) if r["plot"]==p)/len(years) for p in plots}
    ys={y:sum(v for r,v in zip(rows,values) if r["year"]==y)/len(plots) for y in years}
    resid=[v-ps[r["plot"]]-ys[r["year"]]+total for r,v in zip(rows,values)]
    assert abs(sum(resid))<1e-8
    return resid

def regress_out(y: list[float], x: list[float]) -> list[float]:
    assert len(y)==len(x)
    xx=sum(v*v for v in x)
    if xx<1e-12:
        return y[:]
    slope=sum(a*b for a,b in zip(y,x))/xx
    return [a-slope*b for a,b in zip(y,x)]

def diagnostics(rows: list[dict], xfield: str) -> dict:
    assert len(rows)>=15
    yy=[math.log1p(r["y"]) for r in rows]
    xx=[math.log1p(r[xfield]) for r in rows]
    zz=[math.log1p(r["stock"]) for r in rows]
    enriched=[dict(r, Y=a,X=b,Z=c) for r,a,b,c in zip(rows,yy,xx,zz)]
    output={}
    for effects in ("none","plot","year","plot_and_year"):
        x=residualize(enriched,"X",effects)
        y=residualize(enriched,"Y",effects)
        z=residualize(enriched,"Z",effects)
        xr=regress_out(x,z)
        yr=regress_out(y,z)
        output[effects]={
            "correlation_log1p_counts":correlation(x,y),
            "partial_correlation_after_prior_living_stock":correlation(xr,yr),
            "additive_in_sample_residual_gain_given_stock":(
                (correlation(xr,yr)**2) if correlation(xr,yr) is not None else None
            ),
            "n_plot_years":len(rows),
            "n_plots":len({r["plot"] for r in rows}),
            "n_years":len({r["year"] for r in rows}),
        }
    yearwise={}
    for year in sorted({r["year"] for r in rows}):
        sub=[r for r in rows if r["year"]==year]
        yearwise[str(year)]={
            "unadjusted_cross_plot_corr":correlation(
                [math.log1p(r[xfield]) for r in sub],
                [math.log1p(r["y"]) for r in sub]),
            "n":len(sub),
        }
    output["per_year_cross_plot"]=yearwise
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    all_rows,prov=archive_rows(None)
    plots=set.intersection(*[{r["plot"] for r in all_rows if r["year"]==year} for year in YEARS])
    assert len(plots)==10
    rows=[r for r in all_rows if r["plot"] in plots and r["year"] in YEARS]
    assert len(rows)==50
    results={key:diagnostics(rows,field) for key,field in X_FIELDS.items()}
    robustness={}
    for name,omit_key,groups in (
        ("omit_year","year",sorted({r["year"] for r in rows})),
        ("omit_ranch","ranch",sorted({r["ranch"] for r in rows})),
        ("omit_plot","plot",sorted(plots))):
        robustness[name]={}
        for held in groups:
            sample=[r for r in rows if r[omit_key]!=held]
            if name=="omit_year":
                assert len(sample)==40
            robustness[name][str(held)]={
                key:diagnostics(sample,field)["plot_and_year"]["partial_correlation_after_prior_living_stock"]
                for key,field in X_FIELDS.items()
            }
    # Marginal explanatory contributions of plot and year effects, but
    # differences in R^2 are not causal variance shares.
    effects={}
    for name,field in (("new_seedlings","y"),("lag1_flowering","fl1"),
                       ("prior_living_stock","stock")):
        transformed=[dict(r,V=math.log1p(r[field])) for r in rows]
        full=residualize(transformed,"V","none")
        denom=sum(v*v for v in full)
        assert denom>0
        effects[name]={
            e:1-sum(v*v for v in residualize(transformed,"V",e))/denom
            for e in ("plot","year","plot_and_year")
        }
    # These are purely descriptive; the lead-lag choice is not identified
    # by archival year labels or mother-to-seedling tracking.
    report={
        "status":"EXPLORATORY_TWO_WAY_DECOMPOSITION_NOT_CONFIRMATORY",
        "source":"Bruna et al 2023 DOI 10.1002/ecy.4174 source-hash-pinned HDP archives",
        "same_plot_panel_2001_2005":sorted(plots),
        "n_plot_years":50,
        "source_coverage":prov,
        "effect_explanatory_R2":effects,
        "flowering_recruitment":results,
        "leave_one_year_ranch_plot_out_partials":robustness,
        "causal_and_novelty_limits":[
            "Both plot and year fixed effects are fitted on outcome-observed data: this is an explanatory diagnostic, not independent future-year prediction.",
            "No verified same-mother offspring or seed-to-recruit transition is measured.",
            "Year fixed effects may remove climate-induced plant responses that are ecologically real.",
            "Prior measured living stock is post-fragmentation, can mediate effects and contains nonreproductive juveniles.",
            "A shared denominator in rates could induce spurious correlation; use log-counts plus explicit stock adjustment instead.",
            "Three ranches, ten plots and five years are one published ecological programme; leave-one-out sensitivities are not independent replication.",
            "Comparing lag 1, 2, 3 post hoc cannot identify a true seed-bank or mating delay.",
            "Plot/year selection due to all-missing records may bias ecological contrasts.",
            "No significance/p-values or general causal theorem; all candidate model results post exposure.",
            "All frozen EGWEE meta-analytic denominators remain unchanged.",
        ]
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("HELICONIA_WITHIN_PLOT_YEAR_FALSIFICATION: PASS")
    print(json.dumps({
        "n_plot_years":50,
        "effect_R2":effects,
        "effects":{key:{e:d[e] for e in ("plot","year","plot_and_year")}
                   for key,d in results.items()},
        "sensitivity":robustness,
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
