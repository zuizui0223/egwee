#!/usr/bin/env python3
"""All adjacent-year Heliconia transitions, fixed-site numerator and stock-ratio audit.

This guards against cherry-picking the 2002->2003 event. Purely descriptive,
post hoc, same published plant programme. No causal/independent replication.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from audit_heliconia_forward_lag_prediction import archive_rows

YEARS=tuple(range(2001,2006))
def corr(x:list[float],y:list[float])->float|None:
    assert len(x)==len(y)
    if len(x)<3:return None
    a=sum(x)/len(x);b=sum(y)/len(y)
    vx=sum((v-a)**2 for v in x);vy=sum((v-b)**2 for v in y)
    if vx==0 or vy==0:return None
    return sum((u-a)*(v-b) for u,v in zip(x,y))/math.sqrt(vx*vy)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    rows,pin=archive_rows(None)
    plots=set.intersection(*[{r["plot"] for r in rows if r["year"]==y} for y in YEARS])
    assert len(plots)==10
    rs={(r["plot"],r["year"]):r for r in rows if r["plot"] in plots}
    assert len(rs)==50
    trends=[]
    for first,second in zip(YEARS,YEARS[1:]):
        A=[rs[(p,first)] for p in sorted(plots)]
        B=[rs[(p,second)] for p in sorted(plots)]
        diffs=[{
            "plot":x["plot"],"ranch":x["ranch"],"habitat":"fragment" if x["fragment"] else "continuous",
            "delta_recruits":y["y"]-x["y"],"delta_prior_flowers":y["fl1"]-x["fl1"],
            "delta_prior_stock":y["stock"]-x["stock"],
            "delta_recruits_per_stock":y["y"]/y["stock"]-x["y"]/x["stock"],
            "delta_flowering_fraction":y["fl1"]/y["stock"]-x["fl1"]/x["stock"],
        } for x,y in zip(A,B)]
        def avg(key,z):
            return sum(r[key] for r in z)/len(z)
        rn1,rn2=avg("y",A),avg("y",B)
        fl1,fl2=avg("fl1",A),avg("fl1",B)
        st1,st2=avg("stock",A),avg("stock",B)
        result={
            "start_year":first,"end_year":second,
            "n_same_plots":10,
            "mean_new_seedlings_start":rn1,
            "mean_new_seedlings_end":rn2,
            "mean_prior_flowering_start":fl1,
            "mean_prior_flowering_end":fl2,
            "mean_prior_live_stock_start":st1,
            "mean_prior_live_stock_end":st2,
            "n_plots_recruit_records_decrease":sum(r["delta_recruits"]<0 for r in diffs),
            "n_plots_prior_flowering_decrease":sum(r["delta_prior_flowers"]<0 for r in diffs),
            "n_plots_prior_stock_increase":sum(r["delta_prior_stock"]>0 for r in diffs),
            "mean_recruits_change":rn2-rn1,
            "mean_prior_flowering_change":fl2-fl1,
            "mean_prior_live_stock_change":st2-st1,
            "corr_plot_change_recruits_and_flowering":corr(
                [r["delta_recruits"] for r in diffs],[r["delta_prior_flowers"] for r in diffs]),
            "corr_plot_change_recruits_and_stock":corr(
                [r["delta_recruits"] for r in diffs],[r["delta_prior_stock"] for r in diffs]),
            "corr_plot_change_recruits_per_stock_and_flowering_fraction":corr(
                [r["delta_recruits_per_stock"] for r in diffs],
                [r["delta_flowering_fraction"] for r in diffs]),
            "per_plot":diffs
        }
        trends.append(result)
    assert [(r["start_year"],r["end_year"]) for r in trends]==[(2001,2002),(2002,2003),(2003,2004),(2004,2005)]
    assert trends[1]["n_plots_recruit_records_decrease"]==9
    assert trends[1]["n_plots_prior_flowering_decrease"]==10
    summary=[{k:v for k,v in r.items() if k!="per_plot"} for r in trends]
    out={"status":"EXPLORATORY_ALL_FOUR_TIME_TRANSITIONS_NOT_INDEPENDENT",
         "fixed_10_plots":sorted(plots),"n_adjacent_pairs":4,
         "transitions":trends,
         "novelty_and_causal_boundaries":[
            "All four transitions in the balanced source archive must be reported; do not pick the largest post hoc.",
            "10 plots share years/three ranches; 40 plot changes are NOT independent climate or population replication.",
            "Counts and ratios use positive archival flowering and first detected recruits, NOT linked progeny cohorts.",
            "Simple correlations are unadjusted descriptive quantities, not validated mediator effects.",
            "Lag 1 and yearly census date/seed bank observation can be mismatched.",
            "No external independent case and no primary EGWEE corpus changes."
         ]}
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("HELICONIA_ALL_TRANSITION_PULSE: PASS")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
