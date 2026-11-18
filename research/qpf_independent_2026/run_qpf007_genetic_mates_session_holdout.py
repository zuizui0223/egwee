#!/usr/bin/env python3
"""QPF007: postprimary exploratory visit/pollen -> genetic mating success.

Source-provenance gate: genetic-outcome protocol committed BEFORE this
outcome's heldout coefficients. Same original 160×16 mother key, 157
complete genotype-mating outcome/visit/pollen rows; source 2026 paper
already established mating-stage differences. No raw source rows or IDs
redistributed. NEVER upgrade preexisting QPF007 145-seed COVERAGE_STOP.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import subprocess
from statistics import mean

from audit_brassica_rapa_zenodo_source_keys import load_manifest,trusted_binary
from audit_qpf007_genetic_mates_source import parse_source_required,coverage,COLUMNS
from run_qpf007_brassica_2026_session_holdout import (
    PLANT_SOURCE_FILE,PLANT_SOURCE_SHA,original_stigma_keys,
    float_or_none,ridge_predict,verify_frozen_science,
)

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FREEZE_REL="research/qpf_independent_2026/QPF007_GENETIC_MATES_PREDICTION_FREEZE_20261118.md"
FREEZE_COMMIT="2e28165b8be0149c9e4f8258619886a8b9ad31c4"
EXPECTED_MOTHERS=157
EXPECTED_SESSIONS=16

def verify_genetic_freeze():
    # Main seed-result protocol is frozen and remains prior-coverage STOP.
    verify_frozen_science()
    orig=subprocess.check_output(["git","show",FREEZE_COMMIT+":"+FREEZE_REL],cwd=ROOT)
    if orig!=(ROOT/FREEZE_REL).read_bytes():
        raise ValueError("Source genetic target scientific protocol was edited after lock")
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE_COMMIT,"HEAD"],
                   cwd=ROOT,check=True)
    if b"gMS_fem_all" not in orig or b"post-primary" not in orig.lower():
        raise ValueError("Genetic outcome original target/origin missing")
    return True

def materialize():
    gate=coverage()
    if (gate["status"]!="SOURCE_ONLY_GENETIC_TARGET_COVERAGE_VERIFIED"
        or not gate["postprimary_genetic_source_gate_pass"]):
        return None,gate
    if (gate["complete_source_mothers_for_genetic_target"]!=EXPECTED_MOTHERS
        or gate["min_complete_mothers_per_source_session"]!=9):
        raise ValueError("Original source-only genetic target 157/16/9 grain drift")
    files={x.get("key") or x.get("filename"):x for x in load_manifest()["files"]}
    original=trusted_binary(files[PLANT_SOURCE_FILE])
    if hashlib.sha256(original).hexdigest()!=PLANT_SOURCE_SHA:
        raise ValueError("Original source mother SHA mismatch")
    rows,keys=parse_source_required(original)
    stigma=original_stigma_keys(load_manifest())
    if keys!=stigma or len(keys)!=160:
        raise ValueError("Source matched mother/pollen IDs drift")
    labels=sorted({row["poll_treat"].strip() for row in rows})
    if len(labels)!=3:
        raise ValueError("Original bee abundance treatment category count drift")
    out=[]
    for row in rows:
        d={col:float_or_none(row[col]) for col in COLUMNS[3:]}
        if any(v is None or v<0 for v in d.values()):
            continue
        base=[float(row["poll_treat"]==k) for k in labels[1:]]
        base.extend([math.log1p(d["nb_visit"]),math.log1p(d["nb_flo_all"]),
                     math.log1p(d["height_max"])])
        out.append({
            "session":row["session"],
            "M0":base,
            "M1":base+[math.log1p(d["pl_mean"])],
            "y":math.log1p(d["gMS_fem_all"]),
        })
    sessions=sorted({r["session"] for r in out})
    count=Counter(r["session"] for r in out)
    if len(out)!=157 or len(sessions)!=16 or min(count.values())!=9:
        raise ValueError("Genetic mate complete original mother key 157/16/9 drift")
    return out,gate

def analysis():
    verify_genetic_freeze()
    source,gate=materialize()
    base={
        "analysis_id":"QPF007_postprimary_same_mother_gMS_fem_all_heldout_v1",
        "original_data_doi":"10.5281/zenodo.21628183",
        "original_paper_doi":"10.1371/journal.pbio.3003579",
        "original_source_plant_sha256":PLANT_SOURCE_SHA,
        "genetic_target_frozen_commit":FREEZE_COMMIT,
        "independent_study_count":1,
        "post_primary_genetic_endpoint":True,
        "original_145_seed_forecast_coverage_gate":"COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST",
        "new_registered_confirmatory_claim":False,
        "data_generation":"original author gMS_fem_all inferred from sampled offspring, not viable recruits",
        "biological_unit":"one mother×experimental session, not same flower or whole independent landscape",
        "source_raw_genotypes_and_individual_ids_uploaded":False,
        "outside_study_replication":False,
    }
    if source is None:
        return {**base,"status":"SOURCE_GENETIC_TARGET_COVERAGE_STOP",
                "source_coverage":gate,"effect_fitted":False}
    folds=[]
    solverdifference=0
    for idx,ses in enumerate(sorted({r["session"] for r in source}),1):
        tr=[r for r in source if r["session"]!=ses]
        te=[r for r in source if r["session"]==ses]
        if not 9<=len(te)<=10:
            raise ValueError("Unanticipated original experiment group")
        fold={"anonymous_session_index":idx,"n_mother_plants":len(te)}
        for model in ("M0","M1"):
            gauss=ridge_predict(tr,te,model,"gaussian")
            coord=ridge_predict(tr,te,model,"coordinate")
            localdiff=max(abs(x-y) for x,y in zip(gauss,coord))
            solverdifference=max(solverdifference,localdiff)
            if localdiff>1e-8:
                raise ValueError("Two independent ridge solvers disagree")
            residual=[pred-r["y"] for pred,r in zip(gauss,te)]
            fold[model+"_MSE"]=mean(e*e for e in residual)
            fold[model+"_MAE"]=mean(abs(e) for e in residual)
        fold["gain_M0_minus_M1_MSE"]=fold["M0_MSE"]-fold["M1_MSE"]
        folds.append(fold)
    denom=sum(f["n_mother_plants"] for f in folds)
    if denom!=157:
        raise ValueError("Original mother fitted sample unexpectedly changed")
    def weighted(key):
        return sum(f["n_mother_plants"]*f[key] for f in folds)/denom
    m0,m1=weighted("M0_MSE"),weighted("M1_MSE")
    gain=m0-m1
    wins=sum(f["gain_M0_minus_M1_MSE"]>0 for f in folds)
    total_weighted=sum(f["gain_M0_minus_M1_MSE"]*f["n_mother_plants"] for f in folds)
    loo=[
        (total_weighted-f["gain_M0_minus_M1_MSE"]*f["n_mother_plants"])/(denom-f["n_mother_plants"])
        for f in folds
    ]
    return {**base,
        "status":"QPF007_POSTPRIMARY_GENETIC_MATES_PREDICTIVE_SCORES_COMPUTED",
        "source_genetic_coverage":{
            "source_mothers":160,"source_stigma_mothers":160,
            "complete_genetic_predictive_mothers":denom,
            "source_excluded_for_missing_stigma_pollen":3,
            "source_experimental_sessions":len(folds),
            "session_min_n":min(f["n_mother_plants"] for f in folds),
        },
        "models":{
            "response":"log1p(gMS_fem_all) genotypically inferred female mating success",
            "M0":"pollinator treatment + log1p source nb_visit,nb_flo_all,height_max",
            "M1":"M0 + log1p source pl_mean",
            "fitting":"ridge lambda1, train-only standardized predictors, heldout complete session"
        },
        "anonymous_whole_session_fold_scores":folds,
        "pooled_mother_equal_scores":{
            "M0_MSE":m0,"M1_MSE":m1,
            "M0_MAE":weighted("M0_MAE"),"M1_MAE":weighted("M1_MAE"),
            "delta_M0_minus_M1_MSE":gain,
            "relative_gain_percent":100*gain/m0 if m0>0 else None,
            "session_folds_with_positive_delta":wins,
            "original_5percent_and_12of16_benchmark_descriptive_only":
                gain/m0>=.05 and wins>=12 if m0>0 else False
        },
        "postoutcome_aggregate_only_influence":{
            "min_leave_one_scored_session_gain":min(loo),
            "max_leave_one_scored_session_gain":max(loo),
            "n_sign_reverse_deletions":sum(v*gain<=0 for v in loo)
        },
        "independent_ridge_solver_max_abs_error":solverdifference,
        "numeric_source_check_pass":solverdifference<1e-8,
        "no_original_source_rows_uploaded":True,
        "claim_ceiling":"one study, within experiment heldout session genetic-mating proxy, not compatible pollen or wild fragmentation"
    }

def synthetic():
    # This test exercises *the same* independent solvers on a known positive
    # incremental association without substituting any real source outcome.
    fake=[]
    for i in range(65):
        vis=i%13
        p=(i*7)%17
        fake.append({"session":str(i%5),"M0":[math.log1p(vis)],
                     "M1":[math.log1p(vis),math.log1p(p)],
                     "y":0.2+0.4*math.log1p(vis)+0.7*math.log1p(p)})
    tr=fake[:50];te=fake[50:]
    scores=[]
    for model in ("M0","M1"):
        x=ridge_predict(tr,te,model,"gaussian")
        x2=ridge_predict(tr,te,model,"coordinate")
        assert max(abs(a-b) for a,b in zip(x,x2))<1e-8
        scores.append(mean((a-r["y"])**2 for a,r in zip(x,te)))
    assert scores[1]<scores[0]
    print("QPF007_GENETIC_MATES_MODEL_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:synthetic();return 0
    if a.output is None:p.error("--output required")
    try:r=analysis()
    except Exception as ex:
        r={"status":"GENETIC_TARGET_SOURCE_OR_MODEL_STOP",
           "error_type":type(ex).__name__,
           "error":str(ex)[:300],
           "new_registered_confirmatory_claim":False,
           "source_raw_genotypes_and_individual_ids_uploaded":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    summary={
        "status":r["status"],
        "total_genotyped_mothers":r.get("source_genetic_coverage",{}).get("complete_genetic_predictive_mothers"),
        "n_original_sessions":r.get("source_genetic_coverage",{}).get("source_experimental_sessions"),
        "M0_MSE":r.get("pooled_mother_equal_scores",{}).get("M0_MSE"),
        "M1_MSE":r.get("pooled_mother_equal_scores",{}).get("M1_MSE"),
        "M0_minus_M1":r.get("pooled_mother_equal_scores",{}).get("delta_M0_minus_M1_MSE"),
        "relative_gain_pct":r.get("pooled_mother_equal_scores",{}).get("relative_gain_percent"),
        "positive_sessions":r.get("pooled_mother_equal_scores",{}).get("session_folds_with_positive_delta"),
        "LOO_range":r.get("postoutcome_aggregate_only_influence"),
        "source_error":r.get("error"),
        "always_exploratory_not_independent_replication":True,
    }
    print("QPF007_GENETIC_MATES_HELDOUT "+json.dumps(summary,sort_keys=True),flush=True)
    return 0 if r["status"] in (
        "QPF007_POSTPRIMARY_GENETIC_MATES_PREDICTIVE_SCORES_COMPUTED",
        "SOURCE_GENETIC_TARGET_COVERAGE_STOP"
    ) else 1

if __name__=="__main__":
    raise SystemExit(main())
