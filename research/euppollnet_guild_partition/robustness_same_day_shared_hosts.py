#!/usr/bin/env python3
"""Retrospective time-concurrent and shared-plant guild-JSD source checks.

Not another preregistered ecological primary. See POSTPRIMARY_ROBUSTNESS_FREEZE_20261118.md.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import sys

import numpy as np
import estimate_guild_partition as e

SPEC="research/euppollnet_guild_partition/POSTPRIMARY_ROBUSTNESS_FREEZE_20261118.md"


def date_literal(t):
    val=t.strip()
    if not val or val.upper() in ("NA","NAN","NULL"):
        return None
    for fmt in ("%Y-%m-%d","%Y/%m/%d","%d/%m/%Y","%d-%m-%Y",
                "%Y-%m-%d %H:%M:%S","%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(val,fmt).date().isoformat()
        except ValueError:
            pass
    return None


def extract():
    date_groups=defaultdict(lambda:{"plants":defaultdict(lambda:[0,0]),"methods":set()})
    year_groups=defaultdict(lambda:{"plants":defaultdict(lambda:[0,0]),"methods":set()})
    coverage=Counter()
    for row in e.source_rows():
        coverage["original_rows"]+=1
        study=(row["Study_id"] or "").strip()
        network=(row["Network_id"] or "").strip()
        date=date_literal(row["Date"] or "")
        if not study or not network or not date:
            coverage["invalid_date_or_network"]+=1
            continue
        programme=e.programme_of(study)
        method=(row["Sampling_method"] or "").strip()
        key_date=(programme,study,network,date)
        key_year=(programme,study,network,date[:4])
        date_groups[key_date]["methods"].add(method)
        year_groups[key_year]["methods"].add(method)
        group=e.category(row)
        if group is None:
            continue
        plant=(row["Plant_accepted_name"] or "").strip()
        if plant.lower() in ("","na","null","nan","unknown"):
            coverage["focal_unresolved_plant"]+=1
            continue
        if (row["Interaction"] or "").strip() not in ("1","1.0"):
            coverage["nonunit_source_interactions"]+=1
            continue
        index=0 if group=="bee" else 1
        date_groups[key_date]["plants"][plant][index]+=1
        year_groups[key_year]["plants"][plant][index]+=1
    if coverage["original_rows"]!=e.EXPECTED_ROWS or coverage["nonunit_source_interactions"]:
        raise ValueError("SOURCE_STOP: source size or interaction-unit invariants changed")
    return date_groups,year_groups,coverage


def eligible(groups, min_each, shared_only):
    kept=[]
    excluded=Counter()
    for key,g in sorted(groups.items()):
        if len(g["methods"])!=1 or "" in g["methods"]:
            excluded["source_method_mismatch"]+=1
            continue
        labels=sorted(g["plants"])
        if shared_only:
            labels=[p for p in labels if all(v>0 for v in g["plants"][p])]
        b=np.array([g["plants"][p][0] for p in labels],dtype=np.int64)
        h=np.array([g["plants"][p][1] for p in labels],dtype=np.int64)
        if len(labels)<3 or b.sum()<min_each or h.sum()<min_each:
            excluded["below_locked_coverage"]+=1
            continue
        kept.append((key[0],b,h))
    return kept,dict(excluded)


def summarize_units(kept, excluded, seed_null, seed_boot, unit_name):
    n_studies=len({prog for prog,_,_ in kept})
    basic={"unit":unit_name,"n_eligible":len(kept),"n_original_programmes_with_eligible_units":n_studies,
           "excluded_units":excluded,"n_null_draws":199}
    if len(kept)<20 or n_studies<5:
        return {**basic,"status":"COVERAGE_STOP","effect_computed":False}
    rng=np.random.default_rng(seed_null)
    study_effects=defaultdict(list)
    raw_js=[]
    for programme,b,h in kept:
        obs,null,excess=e.sample_excess(b,h,rng,199)
        study_effects[programme].append(excess)
        raw_js.append(obs)
    means=np.array([np.mean(study_effects[k]) for k in sorted(study_effects)])
    rng_boot=np.random.default_rng(seed_boot)
    sample=rng_boot.integers(0,len(means),size=(2000,len(means)))
    boots=means[sample].mean(axis=1)
    p=int((means>0).sum())
    return {**basic,"status":"EXPLORATORY_ESTIMATED","effect_computed":True,
            "equal_programme_mean_excess":float(means.mean()),
            "whole_programme_bootstrap_95pct_CI":[float(z) for z in np.percentile(boots,[2.5,97.5])],
            "programmes_positive":p,
            "fraction_programmes_positive":p/len(means),
            "equal_unit_mean_observed_JSD":float(np.mean(raw_js)),
            "null_seed":seed_null,"bootstrap_seed":seed_boot,
            "bootstrap_replicates":2000,
            "study_network_units_nested_no_independent_replicate_claim":True}


def run():
    dates,years,source=extract()
    same,exc_a=eligible(dates,10,False)
    shared,exc_b=eligible(years,20,True)
    return {
        "status":"RETROSPECTIVE_DIAGNOSTIC_COMPLETE",
        "post_primary":True,"not_a_second_preregistration":True,
        "source_commit":e.SOURCE_SHA,"source_original_sha256":e.EXPECTED_FILE_SHA256,
        "source_row_counts":dict(source),
        "source_native_date_units":len(dates),
        "source_native_study_network_year_units":len(years),
        "same_calendar_day":summarize_units(same,exc_a,20261120,20261121,"source-study-network-date"),
        "shared_host_taxa_only":summarize_units(shared,exc_b,20261122,20261123,"source-study-network-year shared visited plant taxa"),
        "original_rows_redistributed":False,
        "claim_ceiling":"observational visitor/plant allocation, not actual flower supply, compatible pollen or seed success",
    }


def test():
    assert date_literal("2020-05-04")=="2020-05-04"
    assert date_literal("04/05/2020")=="2020-05-04"
    d=defaultdict(lambda:{"plants":defaultdict(lambda:[0,0]),"methods":set()})
    key=("study","a","site","2020-05-04")
    d[key]["methods"].add("Transect")
    d[key]["plants"]["x"]=[12,1]
    d[key]["plants"]["y"]=[8,18]
    d[key]["plants"]["z"]=[3,8]
    x,_=eligible(d,10,False)
    if len(x)!=1:
        raise AssertionError("same-day synthetic coverage should pass")
    xx,_=eligible(d,20,True)
    if len(xx)!=1:
        raise AssertionError("shared-host synthetic coverage should pass")
    print("EUPPOLLNET_POSTPRIMARY_SYNTHETIC_PASS")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        test()
        return 0
    if a.output is None:
        p.error("--output required")
    result={"spec":SPEC,"post_primary":True}
    try:
        result.update(run())
    except Exception as ex:
        result["status"]="SOURCE_OR_ROBUSTNESS_STOP"
        result["reason"]=type(ex).__name__+": "+str(ex)[:350]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("EUPPOLLNET_POSTPRIMARY_RESULT "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="RETROSPECTIVE_DIAGNOSTIC_COMPLETE" else 1


if __name__=="__main__":
    sys.exit(main())
