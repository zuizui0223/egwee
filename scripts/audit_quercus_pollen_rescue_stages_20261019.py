#!/usr/bin/env python3
"""Empirical EGWEE Quercus ilex within-tree pollen-addition timing audit.

Uses true source-tree as independent unit (80 distinct IDs, 160 tree-years),
not three shoots as independent pollination replicates. Excludes incomplete
shoots without imputing NA; both arms require measured flower exposure.
Year-specific effects are compared within trees measured in both years.
The original paper already established synchrony-linked pollen limitation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"evidence/meta_extraction/quercus_ilex_pollen_2021/pollen_addition_results.csv"
MD5="ec3ccf2901ab6f6de0bca9b90eafec86"  # stored text copy, original Zenodo MD5 differs


def load():
    source=SOURCE.read_bytes()
    assert len(source)==31609,(len(source),"source byte mismatch")
    digest=hashlib.md5(source).hexdigest()
    assert digest==MD5,digest
    with SOURCE.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh,delimiter=";"))
    assert len(rows)==960
    assert set(rows[0])=={"TreeID","year","Treatment","Tag","flowers","acorns_june","acorns_final"}
    assert {r["year"] for r in rows}=={"2018","2019"}
    assert {r["Treatment"] for r in rows}=={"Control","Pollen-addition"}
    assert len({r["TreeID"] for r in rows})==80
    assert "62" not in {r["TreeID"] for r in rows}
    return rows

def number(v):
    if v is None or v.strip() in {"","NA"}:return None
    return int(v)

def summarise(data):
    v=np.asarray(data,float)
    n=len(v)
    assert n>=4
    avg=float(v.mean());sd=float(v.std(ddof=1))
    se=sd/np.sqrt(n)
    q=float(stats.t.ppf(.975,n-1))
    p=float(2*stats.t.sf(abs(avg/se),n-1)) if se>0 else None
    loo=[float((v.sum()-v[i])/(n-1)) for i in range(n)]
    return {"n_trees":n,"mean":avg,"sd":sd,
            "t95_interval":[float(avg-q*se),float(avg+q*se)],
            "paired_t_p_nominal":p,
            "leave_one_tree_mean_range":[min(loo),max(loo)],
            "positive":int((v>0).sum()),"negative":int((v<0).sum()),
            "exact_zero":int((v==0).sum())}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    rows=load()
    by=defaultdict(list)
    for r in rows:
        by[(r["TreeID"],r["year"],r["Treatment"])].append(r)
    assert len(by)==320
    assert all(len(z)==3 for z in by.values())

    shoot_patterns=defaultdict(int)
    tree_years=[]
    for id in sorted({r["TreeID"] for r in rows},key=int):
        for year in ("2018","2019"):
            rr={"tree":id,"year":year}
            for treatment,key in (("Control","control"),("Pollen-addition","added")):
                raw=by[(id,year,treatment)]
                valid=[]
                for v in raw:
                    fl,june,final=(
                        number(v[k]) for k in ("flowers","acorns_june","acorns_final"))
                    mask="".join("1" if x is not None else "0" for x in (fl,june,final))
                    shoot_patterns[mask]+=1
                    if all(x is not None for x in (fl,june,final)):
                        assert fl>=june>=final>=0
                        if fl>0:valid.append((fl,june,final))
                rr[key]={
                    "complete_positive_exposure_shoots":len(valid),
                    "flowers":sum(v[0] for v in valid),
                    "early":sum(v[1] for v in valid),
                    "late":sum(v[2] for v in valid)}
            c=rr["control"];a=rr["added"]
            rr["strict_three"]= c["complete_positive_exposure_shoots"]==3 and a["complete_positive_exposure_shoots"]==3
            if min(c["flowers"],a["flowers"])<=0:continue
            rr["early_contrast"]=a["early"]/a["flowers"]-c["early"]/c["flowers"]
            rr["late_contrast"]=a["late"]/a["flowers"]-c["late"]/c["flowers"]
            rr["attrition_contrast"]=rr["early_contrast"]-rr["late_contrast"]
            tree_years.append(rr)

    assert len(tree_years)==137
    assert sum(v["strict_three"] for v in tree_years)==109

    result={
        "status":"post_hoc_two_year_experimental_context_audit",
        "published_sources":"Bogdziewicz et al. 2020 Ecology Letters and Dryad 2021",
        "source_md5":MD5,"source_shoot_records":len(rows),
        "raw_tree_count":80, "potential_tree_years":160,
        "n_treeyears_with_two_complete_exposures":len(tree_years),
        "n_treeyears_strict_all_three_shoots":sum(v["strict_three"] for v in tree_years),
        "shoot_numeric_availability":dict(shoot_patterns),
        "year_specific":{},"same_tree_year_difference":{},
        "frozen_fragmentation_programmes_changed":False
    }
    for year in ("2018","2019"):
        sub=[z for z in tree_years if z["year"]==year]
        strict=[z for z in sub if z["strict_three"]]
        result["year_specific"][year]={
            "n":len(sub),"n_strict_3_each_arm":len(strict),
            "mean_source_exposures": {
                name:{"control":float(np.mean([x["control"][key] for x in sub])),
                      "pollen_added":float(np.mean([x["added"][key] for x in sub]))}
                for name,key in (("flowers","flowers"),("June_acorns","early"),
                                 ("September_acorns","late"))
            },
            "all_measured_shoots": {metric:summarise([z[metric] for z in sub]) for metric
                in ("early_contrast","late_contrast","attrition_contrast")},
            "strict_three_shoots_each_arm": {metric:summarise([z[metric] for z in strict]) for metric
                in ("early_contrast","late_contrast","attrition_contrast")}
        }
    by_tree=defaultdict(dict)
    for z in tree_years:by_tree[z["tree"]][z["year"]]=z
    paired={k:v for k,v in by_tree.items() if set(v)=={"2018","2019"}}
    assert len(paired)==62
    result["same_tree_year_difference"]["n_matched_trees"]=len(paired)
    for outcome in ("early_contrast","late_contrast","attrition_contrast"):
        delta=[v["2019"][outcome]-v["2018"][outcome] for v in paired.values()]
        result["same_tree_year_difference"]["2019_minus_2018_"+outcome]=summarise(delta)
        result["same_tree_year_difference"]["2018_matched_"+outcome]=summarise(
            [v["2018"][outcome] for v in paired.values()])
        result["same_tree_year_difference"]["2019_matched_"+outcome]=summarise(
            [v["2019"][outcome] for v in paired.values()])
    # Expected headroom: point direction changes in source but year interaction unresolved.
    assert result["year_specific"]["2018"]["all_measured_shoots"]["early_contrast"]["mean"]<0
    assert result["year_specific"]["2019"]["all_measured_shoots"]["early_contrast"]["mean"]>0
    assert result["same_tree_year_difference"]["2019_minus_2018_early_contrast"]["mean"]>0

    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    print("QUERCUS_SOURCE_MD5_OK",MD5,"trees",80,"tree-years",len(tree_years),
          "strict3",sum(z["strict_three"] for z in tree_years),"matched_both_years",len(paired))
    for year in ("2018","2019"):
        y=result["year_specific"][year]
        print("QUERCUS_YEAR",year,"n",y["n"],
              "June",y["all_measured_shoots"]["early_contrast"],
              "September",y["all_measured_shoots"]["late_contrast"],
              "strict3_June",y["strict_three_shoots_each_arm"]["early_contrast"]["mean"],
              "strict3_September",y["strict_three_shoots_each_arm"]["late_contrast"]["mean"])
    for outcome in ("early_contrast","late_contrast","attrition_contrast"):
        print("QUERCUS_SAME_TREE_CHANGE",outcome,
              result["same_tree_year_difference"]["2019_minus_2018_"+outcome])


if __name__=="__main__":main()
