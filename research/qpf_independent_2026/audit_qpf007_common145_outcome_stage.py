#!/usr/bin/env python3
"""Post-outcome common-original-mother cohort control: seed vs genetic mates.

Only 145 original source mothers with both genetic & per-fruit-seed outcomes
and matched visit/stigma pollen are admitted. This cannot be reported as a
preregistered separate study, universal process/function double dissociation,
or proof of compatible-pollen transfer.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
from statistics import mean

from audit_brassica_rapa_zenodo_source_keys import load_manifest,trusted_binary
from audit_qpf007_genetic_mates_source import parse_source_required
from run_qpf007_brassica_2026_session_holdout import (
    PLANT_SOURCE_FILE, PLANT_SOURCE_SHA, original_stigma_keys,full_source_rows,
    materialize_eligibility, float_or_none, ridge_predict,
)
from run_qpf007_genetic_mates_session_holdout import verify_genetic_freeze

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FREEZE_REL="research/qpf_independent_2026/QPF007_POSTOUTCOME_COMMON145_FREEZE_20261118.md"
FREEZE_COMMIT="13cf3f392e11e709772f2df2233b426ad2ced41c"
OLD_RESULT=HERE/"QPF007_ORIGINAL_POSTSTOP_EXPLORATORY_RESULT_20261118.json"

def cohort():
    verify_genetic_freeze()
    exact=subprocess.check_output(["git","show",FREEZE_COMMIT+":"+FREEZE_REL],cwd=ROOT)
    if exact!=(ROOT/FREEZE_REL).read_bytes():
        raise ValueError("Common145 post-outcome contract altered after freeze")
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE_COMMIT,"HEAD"],
                   cwd=ROOT,check=True)
    manifest=load_manifest()
    files={x.get("key") or x.get("filename"):x for x in manifest["files"]}
    raw=trusted_binary(files[PLANT_SOURCE_FILE])
    if hashlib.sha256(raw).hexdigest()!=PLANT_SOURCE_SHA:
        raise ValueError("Original author individual file SHA changed")
    old=full_source_rows(raw)
    genetic,keys=parse_source_required(raw)
    if keys!=original_stigma_keys(manifest):
        raise ValueError("Exact author stigma/mother plant keys altered")
    glookup={(r["session"],r["ID_full"]):r for r in genetic}
    oldeligible,coverage=materialize_eligibility(old,160,strict_coverage=False)
    if oldeligible is None or len(oldeligible)!=145:
        raise ValueError("Original published seed endpoint source 145 STOP drift")
    levels=sorted({r["poll_treat"] for r in old})
    if len(levels)!=3:
        raise ValueError("Wrong original bee abundance classes")
    source=[]
    for r in old:
        direct={k:float_or_none(r[k]) for k in
                ("nbGr_mean","nb_visit","nb_flo_all","height_max","pl_mean")}
        if any(x is None or x<0 for x in direct.values()):
            continue
        genetic_source=glookup[(r["session"],r["ID_full"])]
        outcome=float_or_none(genetic_source["gMS_fem_all"])
        if outcome is None or outcome<0:
            # New missing genetic outcome is NOT silently imputed to zero.
            continue
        base=[float(r["poll_treat"]==lev) for lev in levels[1:]]
        base.extend((math.log1p(direct["nb_visit"]),math.log1p(direct["nb_flo_all"]),
                     math.log1p(direct["height_max"])))
        source.append({
            "session":r["session"],"M0":base,
            "M1":base+[math.log1p(direct["pl_mean"])],
            "seed":math.log1p(direct["nbGr_mean"]),
            "genetic":math.log1p(outcome)
        })
    if len(source)!=145:
        raise ValueError("Common cohort is not exact original seed 145")
    groups=Counter(r["session"] for r in source)
    if len(groups)!=16 or min(groups.values())!=5:
        raise ValueError("Same original low-coverage five-mother session not retained")
    return source

def forecast(source,target):
    groups=sorted({r["session"] for r in source})
    folds=[]
    worst=0.
    for idx,session in enumerate(groups,1):
        training=[{**r,"y":r[target]} for r in source if r["session"]!=session]
        heldout=[{**r,"y":r[target]} for r in source if r["session"]==session]
        fold={"anonymous_session":idx,"n_original_mothers":len(heldout)}
        for model in ("M0","M1"):
            x=ridge_predict(training,heldout,model,"gaussian")
            x2=ridge_predict(training,heldout,model,"coordinate")
            divergence=max(abs(a-b) for a,b in zip(x,x2))
            worst=max(worst,divergence)
            if worst>1e-8:raise ValueError("Independent solvers diverged on original source")
            errs=[v-r["y"] for v,r in zip(x,heldout)]
            fold[model+"_MSE"]=mean(err*err for err in errs)
            fold[model+"_MAE"]=mean(abs(err) for err in errs)
        fold["gain_M0_minus_M1"]=fold["M0_MSE"]-fold["M1_MSE"]
        folds.append(fold)
    if sum(x["n_original_mothers"] for x in folds)!=145:
        raise ValueError("Fold coverage not complete")
    def weighted(k):
        return sum(r["n_original_mothers"]*r[k] for r in folds)/145
    m0=weighted("M0_MSE")
    m1=weighted("M1_MSE")
    delta=m0-m1
    nwin=sum(f["gain_M0_minus_M1"]>0 for f in folds)
    loo=[(145*delta - f["n_original_mothers"]*f["gain_M0_minus_M1"])/(145-f["n_original_mothers"])
         for f in folds]
    return {
      "response_target":target,
      "frozen_original_sample_n":145,
      "n_original_sessions":16,
      "M0_MSE":m0,"M1_MSE":m1,"M0_minus_M1":delta,
      "gain_percent_of_M0_MSE":100*delta/m0 if m0>0 else None,
      "n_positive_sessions":nwin,
      "session_LOO_aggregate_only_range":[min(loo),max(loo)],
      "solver_max_abs_difference":worst,
      "anonymous_session_folds":folds,
    }

def run():
    source=cohort()
    seed=forecast(source,"seed")
    genetic=forecast(source,"genetic")
    expected=(.5335444986695099,.5258374883185953)
    if (abs(seed["M0_MSE"]-expected[0])>1e-10 or
        abs(seed["M1_MSE"]-expected[1])>1e-10 or
        seed["n_positive_sessions"]!=7):
        raise ValueError("Prior 145 source seed score was not independently reproduced")
    old=json.loads(OLD_RESULT.read_text(encoding="utf-8"))
    if (len(old["session_folds"])!=16 or old["pooled"]["eligible_plant_n"]!=145):
        raise ValueError("Original publication-grade derivative result missing")
    for f,new in zip(old["session_folds"],seed["anonymous_session_folds"]):
        if (f["n_maternal_source_plants"]!=new["n_original_mothers"] or
            abs(f["M0_MSE"]-new["M0_MSE"])>1e-10 or
            abs(f["M1_MSE"]-new["M1_MSE"])>1e-10):
            raise ValueError("Historical original source session-level seed score drift")
    return {
        "status":"QPF007_POSTOUTCOME_COMMON145_ENDPOINT_COMPARISON_COMPLETE",
        "source_original_plant_sha256":PLANT_SOURCE_SHA,
        "frozen_after_outcomes":True,
        "protocol_commit":FREEZE_COMMIT,
        "independent_original_studies":1,
        "mother_sample_n":145,
        "session_count":16,
        "original_seed_prediction_gate_remains_COVERAGE_STOP":True,
        "historical_seed_145_score_reproduced_every_fold":True,
        "same_source_mother_rows_and_folds_for_both_outcomes":True,
        "endpoint_effects_not_same_scale":True,
        "seed_target":seed,
        "genetic_mating_target":genetic,
        "separately_observed_157_genetic_score":{
            "M0_MSE":0.2196917846303042,
            "M1_MSE":0.22334284036399235,
            "M0_minus_M1":-0.003651055733688152
        },
        "no_pvalue_or_significance_claim":True,
        "not_an_independent_confirmatory_replication":True,
        "no_compatible_pollen_or_offspring_survival_measured":True,
        "original_source_rows_genotypes_individuals_not_redistributed":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    try:info=run()
    except Exception as e:
        info={"status":"SOURCE_OR_ENDPOINT_COMPARISON_STOP",
              "error_type":type(e).__name__,"reason":str(e)[:350],
              "original_source_rows_genotypes_individuals_not_redistributed":True}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(info,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    brief={"status":info["status"],
           "historical_seed_folds_reproduced":info.get("historical_seed_145_score_reproduced_every_fold"),
           "seed_145_gain":info.get("seed_target",{}).get("M0_minus_M1"),
           "seed_145_wins":info.get("seed_target",{}).get("n_positive_sessions"),
           "genetic_145_gain":info.get("genetic_mating_target",{}).get("M0_minus_M1"),
           "genetic_145_wins":info.get("genetic_mating_target",{}).get("n_positive_sessions"),
           "genetic_145_percent_gain":info.get("genetic_mating_target",{}).get("gain_percent_of_M0_MSE"),
           "error":info.get("reason"),
           "comparison_postoutcome_not_independent":True}
    print("QPF007_COMMON145_REPRO "+json.dumps(brief,sort_keys=True))
    return 0 if info["status"]=="QPF007_POSTOUTCOME_COMMON145_ENDPOINT_COMPARISON_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
