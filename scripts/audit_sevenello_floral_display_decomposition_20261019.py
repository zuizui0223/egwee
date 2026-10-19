#!/usr/bin/env python3
"""Post hoc Sevenello flowering-display × seed-yield accounting identity.

Not a causal decomposition of hand pollination: OP and OPSupp are different
plants selected within the same quadrat. Source exactly pinned by the
preceding experiment checker, which verifies original Figshare MD5 hashes.
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path
import numpy as np

from audit_sevenello_pollen_addition_20261019 import read, number, mean

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ("total_D", "perflower_yield_component", "flower_display_component",
           "seeds_per_flower_D", "flower_count_D")


def centered_slope(rows, explanatory, outcome):
    by_transect = defaultdict(list)
    for row in rows:
        by_transect[row["transect_id"]].append(row)
    top = bottom = 0.
    for group in by_transect.values():
        x = np.asarray([p[explanatory] for p in group], dtype=float)
        y = np.asarray([p[outcome] for p in group], dtype=float)
        x = x - x.mean()
        y = y - y.mean()
        top += float(x @ y)
        bottom += float(x @ x)
    assert bottom > 1e-9
    return top / bottom


def slopes(rows, explanatory, outcome, quadrat_loo=False):
    all_sites = sorted(set(p["site"] for p in rows))
    overall = centered_slope(rows, explanatory, outcome)
    by_site = {
        site: centered_slope([p for p in rows if p["site"] == site],
                             explanatory, outcome) for site in all_sites
    }
    leave_reserve = [
        centered_slope([p for p in rows if p["site"] != site], explanatory, outcome)
        for site in all_sites
    ]
    out = {
        "slope_within_site_crop_transect": overall,
        "by_independent_reserve": by_site,
        "leave_one_reserve_slope_range": [min(leave_reserve), max(leave_reserve)],
        "n_reserves": len(all_sites),
    }
    if quadrat_loo:
        leave_quadrat = []
        for j in range(len(rows)):
            leave_quadrat.append(centered_slope(
                [p for i,p in enumerate(rows) if i != j], explanatory,outcome))
        out["leave_one_quadrat_slope_range"] = [
            min(leave_quadrat), max(leave_quadrat)
        ]
    return out


def site_mean(rows, quantity):
    # Within crop block: edge and core equal weight; if two crop blocks
    # at the same physical reserve, crop blocks also receive equal weight.
    by = defaultdict(list)
    for p in rows:
        by[(p["site"],p["crop"],p["transect"])].append(p[quantity])
    by_crop = defaultdict(dict)
    for (site,crop,side), group in by.items():
        by_crop[(site,crop)][side] = mean(group)
    by_site = defaultdict(list)
    for (site,crop), two_sides in by_crop.items():
        assert set(two_sides)=={"Edge","Core"}
        by_site[site].append((two_sides["Edge"]+two_sides["Core"])/2.)
    return {site:mean(crop_values) for site,crop_values in sorted(by_site.items())}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    plants=read("landscape_seeds.csv")
    local={r["id_plot"]:r for r in read("local_seeds.csv")}
    assert len(local)==520
    q=defaultdict(dict)
    for r in plants:
        ident=r["id_plot"]
        assert ident in local
        q[ident]["species"]=r["species"]
        q[ident]["site"]=r["site"]
        q[ident]["crop"]=r["crop_type"]
        q[ident]["side"]=r["transect"]
        if r["treat"] in {"OP","OPSupp"}:
            q[ident][r["treat"]]=(number(r["flower_num"]),
                                   number(r["total_seeds"]))
    out={"status":"post_hoc_accounting_not_causal_mediation",
         "fixed_primary_edge_comparison_still_separate":True,
         "grain":"separate OP and OPSupp plants within source quadrat",
         "species":{}}
    for species in ("LARO","POAR"):
        pairs=[]
        for ident,p in q.items():
            if p["species"]!=species:
                continue
            f0,t0=p["OP"]; f1,t1=p["OPSupp"]
            if any(v is None for v in (f0,t0,f1,t1)) or f0<=0 or f1<=0:
                continue
            y0,y1=t0/f0,t1/f1
            # Exact symmetric Oaxaca/Shapley two-factor identity
            yield_part=(f0+f1)/2.*(y1-y0)
            display_part=(y0+y1)/2.*(f1-f0)
            assert abs((yield_part+display_part)-(t1-t0))<1e-9
            p2={"site":p["site"],"crop":p["crop"],"side":p["side"],
                "transect_id":(p["site"],p["crop"],p["side"]),
                "bare_ground_per10":float(local[ident]["ground_p"])/10.,
                "neighbourhood_floral_log1p":
                    float(np.log1p(float(local[ident]["total_flower"]))),
                "total_D":t1-t0,"perflower_yield_component":yield_part,
                "flower_display_component":display_part,
                "seeds_per_flower_D":y1-y0,"flower_count_D":f1-f0}
            pairs.append(p2)
        expected=157 if species=="LARO" else 115
        assert len(pairs)==expected
        overall_mean={key:mean([p[key] for p in pairs]) for key in RESULTS}
        assert abs(overall_mean["total_D"] -
                   overall_mean["perflower_yield_component"] -
                   overall_mean["flower_display_component"])<1e-9
        site_responses={k:site_mean(pairs,k) for k in RESULTS}
        for site in site_responses["total_D"]:
            assert abs(site_responses["total_D"][site] -
                       site_responses["perflower_yield_component"][site] -
                       site_responses["flower_display_component"][site])<1e-8
        reserve_equal={k:mean(list(v.values())) for k,v in site_responses.items()}
        assert abs(reserve_equal["total_D"] -
                   reserve_equal["perflower_yield_component"] -
                   reserve_equal["flower_display_component"])<1e-8
        slopes_by_context={
            x:{y:slopes(pairs,x,y,quadrat_loo=(species=="POAR"
                 and x=="neighbourhood_floral_log1p" and y=="total_D"))
               for y in RESULTS}
            for x in ("neighbourhood_floral_log1p","bare_ground_per10")}
        for x,vals in slopes_by_context.items():
            d=vals["total_D"]["slope_within_site_crop_transect"]
            a=vals["perflower_yield_component"]["slope_within_site_crop_transect"]
            b=vals["flower_display_component"]["slope_within_site_crop_transect"]
            assert abs(d-a-b)<1e-7
        out["species"][species]={
            "n_complete_pairs":len(pairs),
            "pooled_quadrat_mean":overall_mean,
            "site_equal_mean":reserve_equal,
            "site_response_contributions":site_responses,
            "within_transect_contextual_slopes":slopes_by_context
        }
    po=out["species"]["POAR"]
    assert po["pooled_quadrat_mean"]["total_D"]<0
    assert po["pooled_quadrat_mean"]["perflower_yield_component"]>0
    assert po["pooled_quadrat_mean"]["flower_display_component"]<0
    assert po["site_equal_mean"]["total_D"]>0
    assert (po["within_transect_contextual_slopes"]["neighbourhood_floral_log1p"]
             ["total_D"]["slope_within_site_crop_transect"]<0)
    result=json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding="utf-8")
    print("SEVENELLO_DECOMPOSITION_SOURCE_VALIDATED")
    for sp in ("LARO","POAR"):
        r=out["species"][sp]
        print("SEVENELLO_DECOMP_MEAN",sp,
              json.dumps(r["pooled_quadrat_mean"],sort_keys=True))
        print("SEVENELLO_DECOMP_RESERVE_EQUAL",sp,
              json.dumps(r["site_equal_mean"],sort_keys=True))
        print("SEVENELLO_DECOMP_FLORAL_SLOPES",sp,
              json.dumps({k:{"beta":z["slope_within_site_crop_transect"],
                              "by_reserve":z["by_independent_reserve"],
                              "leave_reserve_range":
                                  z["leave_one_reserve_slope_range"],
                              **({"leave_quadrat_range":
                                  z["leave_one_quadrat_slope_range"]}
                                 if "leave_one_quadrat_slope_range" in z else {})}
                 for k,z in
                 r["within_transect_contextual_slopes"]
                  ["neighbourhood_floral_log1p"].items()},
                 sort_keys=True))


if __name__=="__main__":
    main()
