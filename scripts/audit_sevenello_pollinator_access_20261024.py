#!/usr/bin/env python3
"""Within-quadrat four-treatment pollination-access topology in Sevenello 2026.

Empirical EGWEE, one source landscape, retrospective exploratory follow-up.
Each quadrat contains FOUR DISTINCT experimental plants assigned to OP, OPSupp,
Bag, BagSup. Site/reserve is independent landscape unit, never 4 plant records.
Bag exclusion can change microclimate and disturbance as well as pollination.
Not a causal mechanism proof or addition to the frozen fragmentation corpus.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy import stats

from audit_sevenello_pollen_addition_20261019 import read, number, mean

SPECIES=("GORO","LARO","POAR","POGN")
COMPLETE_EXPECTED={"GORO":117,"LARO":156,"POAR":112,"POGN":114}
SITE_EXPECTED={"GORO":5,"LARO":6,"POAR":4,"POGN":6}
METRICS=(
    "open_minus_bag",
    "bag_supp_minus_bag",
    "open_minus_bag_supp",
    "open_pollen_addition",
    "factorial_pollen_addition_interaction",
    "open_supp_minus_bag_supp",
)


def signflip_exact(x):
    y=np.asarray(x,float)
    n=len(y)
    obs=abs(float(y.mean()))
    numerator=0
    for signs in itertools.product((-1,1),repeat=n):
        if abs(float(np.dot(y,signs))/n)>=obs-1e-10:
            numerator+=1
    return numerator/2**n


def summarize_site(values):
    x=np.asarray(values,float)
    n=len(x)
    assert n>=4
    m=float(x.mean())
    se=float(x.std(ddof=1)/np.sqrt(n))
    delta=float(stats.t.ppf(.975,n-1)*se)
    loo=[float((x.sum()-x[j])/(n-1)) for j in range(n)]
    return {
        "n_independent_reserves":n,"reserve_equal_mean":m,
        "t95_interval_descriptive":[m-delta,m+delta],
        "exact_two_sided_site_signflip_p":signflip_exact(x),
        "positive_reserves":int(sum(x>0)), "negative_reserves":int(sum(x<0)),
        "leave_one_reserve_mean_range":[min(loo),max(loo)],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    source=read("landscape_seeds.csv") # source MD5+N verified on read
    local=read("local_seeds.csv")
    assert len(source)==2080 and len(local)==520
    rows=defaultdict(dict)
    for r in source:
        key=r["id_plot"]
        node=rows[key]
        if "species" not in node:
            node.update(
                species=r["species"],site=r["site"],crop=r["crop_type"],
                side=r["transect"])
        assert node["species"]==r["species"] and node["site"]==r["site"]
        assert node["crop"]==r["crop_type"] and node["side"]==r["transect"]
        assert r["treat"] not in node
        node[r["treat"]]=number(r["total_seeds"])
    assert len(rows)==520
    assert all(set(r)>=set(("OP","OPSupp","Bag","BagSup")) for r in rows.values())
    assert Counter(r["species"] for r in rows.values())=={
        "GORO":120,"LARO":160,"POAR":120,"POGN":120}

    result={
        "study":"Sevenello et al. 2026; one Western Australian landscape",
        "source_dataset":"10.6084/m9.figshare.31072189",
        "status":"post hoc four-different-plant contrast within one landscape",
        "source_frozen_fragmentation_admissions_changed":False,
        "full_quadrat_policy":"exclude if ANY of four seed totals missing; no zero filling",
        "species":{}
    }

    for sp in SPECIES:
        candidates=[r for r in rows.values() if r["species"]==sp]
        eligible=[r for r in candidates
                  if all(r[t] is not None for t in ("OP","OPSupp","Bag","BagSup"))]
        assert len(eligible)==COMPLETE_EXPECTED[sp]
        groups=defaultdict(list)
        for r in eligible:
            op,os,bag,bs=(r[k] for k in ("OP","OPSupp","Bag","BagSup"))
            z={
                "open_minus_bag":op-bag,
                "bag_supp_minus_bag":bs-bag,
                "open_minus_bag_supp":op-bs,
                "open_pollen_addition":os-op,
                "factorial_pollen_addition_interaction":(os-op)-(bs-bag),
                "open_supp_minus_bag_supp":os-bs,
            }
            assert abs(z["open_minus_bag"]-(z["bag_supp_minus_bag"]+
                                           z["open_minus_bag_supp"]))<1e-9
            assert abs(z["open_supp_minus_bag_supp"]-
                       (z["open_pollen_addition"]+
                        z["open_minus_bag_supp"]))<1e-9
            groups[(r["site"],r["crop"],r["side"])].append(z)
        cropmap=defaultdict(dict)
        for (site,crop,side),rr in groups.items():
            cropmap[(site,crop)][side]={
                m:mean([r[m] for r in rr]) for m in METRICS}
        bysite=defaultdict(list)
        for (site,crop),arms in cropmap.items():
            assert set(arms).issubset({"Core","Edge"})
            bysite[site].append({
                "crop":crop,"observed_sides":sorted(arms),
                "contrasts":{
                    k:mean([x[k] for x in arms.values()]) for k in METRICS}
            })
        sites=[]
        for site,crops in sorted(bysite.items()):
            sites.append({
                "site":site,"n_crop_blocks":len(crops),"crop_blocks":crops,
                "contrasts":{
                    k:mean([b["contrasts"][k] for b in crops])
                    for k in METRICS}
            })
        assert len(sites)==SITE_EXPECTED[sp]
        summary={
            k:summarize_site([z["contrasts"][k] for z in sites])
            for k in METRICS}
        natural_access=summary["open_minus_bag"]
        artificial_bag=summary["bag_supp_minus_bag"]
        natural_over_manual=summary["open_minus_bag_supp"]
        assert natural_access["positive_reserves"]==len(sites)
        assert artificial_bag["positive_reserves"]==len(sites)
        assert natural_over_manual["positive_reserves"]==len(sites)
        result["species"][sp]={
            "n_source_quadrats":len(candidates),
            "n_complete_four_treatment_quadrats":len(eligible),
            "n_incomplete_four_treatment_quadrats":len(candidates)-len(eligible),
            "n_observed_physical_reserves":len(sites),
            "reserve_level":sites,
            "contrasts":summary,
            "simple_quadrat_equal_means":{
                k:mean([rr[k] for q in groups.values() for rr in q])
                for k in METRICS}
        }
    result["cross_species_reserve_checks"]={
        "number_species_reserve_cells":sum(SITE_EXPECTED.values()),
        "positive_open_minus_bag":sum(
            z["contrasts"]["open_minus_bag"]["positive_reserves"]
            for z in result["species"].values()),
        "positive_bag_supp_minus_bag":sum(
            z["contrasts"]["bag_supp_minus_bag"]["positive_reserves"]
            for z in result["species"].values()),
        "positive_open_minus_bag_supp":sum(
            z["contrasts"]["open_minus_bag_supp"]["positive_reserves"]
            for z in result["species"].values()),
        "warning":"Species and reserves overlap within a SINGLE experiment/landscape; 21 cells are NOT 21 independent replications, and plant allocation plus bag microclimate limit causal attribution."
    }
    assert result["cross_species_reserve_checks"]["number_species_reserve_cells"]==21
    assert all(result["cross_species_reserve_checks"][k]==21
               for k in ("positive_open_minus_bag","positive_bag_supp_minus_bag",
                         "positive_open_minus_bag_supp"))
    print("SEVENELLO_FOUR_ARM_SOURCE_OK",len(rows),"complete",
          sum(x["n_complete_four_treatment_quadrats"]
              for x in result["species"].values()))
    for sp in SPECIES:
        r=result["species"][sp]
        print("SEVENELLO_FOUR_ARM",sp,"quadrats",r["n_complete_four_treatment_quadrats"],
              "reserves",r["n_observed_physical_reserves"])
        for key in METRICS:
            x=r["contrasts"][key]
            print("SEVENELLO_CONTRAST",sp,key,"mean",round(x["reserve_equal_mean"],6),
                  "site-positive",x["positive_reserves"],
                  "site-negative",x["negative_reserves"],
                  "t95",x["t95_interval_descriptive"],
                  "exact-signflip-p",x["exact_two_sided_site_signflip_p"])
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")


if __name__=="__main__":
    main()
