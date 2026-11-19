#!/usr/bin/env python3
"""RHP001 original wild Oenothera mother-heldout MLTR correlated-paternity.

Original independent Rhodes, Fant & Skogen 2017. Three arm exclusion + local
spatial isolation. Negative and positive results all retained. Only source
Zenodo-mirrored Dryad 4942351 file, record MD5 locked.
No mother identifiers, genotype, individual phenotypes or original data rows
are written to artifacts. Earlier Brassica father-contact result unchanged.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
from io import StringIO
import json
import math
from pathlib import Path
import random

import numpy as np

from audit_independent_original_parentage_source import (
    ZENODO,RHP_DOI,RHP_RECORD,fetch,META_MAX,
)
SOURCE_FILE="multiplePaternity.csv"
EXPECTED_MD5="600f6f370ffa8ad205d0ccb6bc92ab65"
SOURCE_ROWS=60
HEADER=("plantID","treatment","isolation20","correlatedPaternity")
FREEZE="research/independent_parentage_bridge/RHP001_MATERNAL_HOLDOUT_FREEZE_20261119.md"
TREATMENTS=("c","de","ne")
BOOTSTRAP=4000
BOOT_SEED=20261119

def valid_float(s):
    try:
        x=float(str(s).strip())
        return x if math.isfinite(x) else None
    except (ValueError,TypeError):return None

def get_original_families():
    record=json.loads(fetch(ZENODO+f"/api/records/{RHP_RECORD}",ZENODO,META_MAX))
    if int(record.get("id",-1))!=RHP_RECORD:
        raise ValueError("Wrong independent source original record")
    if str(record.get("doi") or "").casefold()!=RHP_DOI:
        raise ValueError("Publisher source DOI changed")
    files=record.get("files") or {}
    entries=files.get("entries",{}) if isinstance(files,dict) else files
    if isinstance(entries,list):entries={e["key"]:e for e in entries}
    if SOURCE_FILE not in entries:
        raise ValueError("Original maternal-family data file missing")
    entry=entries[SOURCE_FILE]
    if (entry.get("checksum") or "").lower()!="md5:"+EXPECTED_MD5:
        raise ValueError("Publisher original dataset declared MD5 drift")
    href=(entry.get("links") or {}).get("content") or (entry.get("links") or {}).get("self")
    if not href:raise ValueError("No verified source file URI")
    raw=fetch(href,ZENODO,8192)
    if hashlib.md5(raw).hexdigest()!=EXPECTED_MD5 or len(raw)!=entry["size"]:
        raise ValueError("Original source bytes MD5 or size mismatch")
    text=raw.decode("utf-8-sig",errors="strict")
    reader=csv.DictReader(StringIO(text,newline=""),delimiter=",")
    if tuple(reader.fieldnames or ())!=HEADER:
        raise ValueError("Original published mother data field headers drift")
    rows=list(reader)
    if len(rows)!=SOURCE_ROWS:
        raise ValueError("Published original maternal fruit family count drift")
    return rows,hashlib.sha256(raw).hexdigest()

def source_coverage():
    rows,sha=get_original_families()
    counts=Counter()
    seen=Counter()
    arm=Counter()
    treatment_mother=defaultdict(set)
    for row in rows:
        mother=str(row["plantID"]).strip()
        tr=str(row["treatment"]).strip().lower()
        isolation=valid_float(row["isolation20"])
        outcome=valid_float(row["correlatedPaternity"])
        valid=bool(mother and mother.casefold() not in ("na","none","null")
                   and tr in TREATMENTS
                   and isolation is not None and isolation>=0
                   and outcome is not None and -1<=outcome<=1)
        if not mother:counts["missing_original_mother_id"]+=1
        if tr not in TREATMENTS:counts["unknown_treatment_code"]+=1
        if isolation is None or isolation<0:counts["missing_or_invalid_isolation"]+=1
        if outcome is None or outcome < -1 or outcome > 1:
            counts["missing_or_invalid_MLTR_paternity_estimator"]+=1
        if not valid:continue
        seen[mother]+=1
        arm[tr]+=1
        treatment_mother[mother].add(tr)
        counts["source_complete_fruit_families"]+=1
    counts["source_unique_complete_maternal_plants"]=len(seen)
    counts["source_mothers_with_2plus_different_treatments"]=sum(len(v)>=2 for v in treatment_mother.values())
    counts["original_source_mother_max_fruit_family_rows"]=max(seen.values(),default=0)
    counts["original_source_mother_min_fruit_family_rows"]=min(seen.values(),default=0)
    eligible=(counts["source_complete_fruit_families"]>=48
       and counts["source_unique_complete_maternal_plants"]>=18
       and all(arm[t]>=10 for t in TREATMENTS)
       and len(arm)==3)
    return {
       "status":"RHP001_PUBLISHED_ORIGINAL_MATERNAL_COHORT_AUDIT_COMPLETE",
       "source_original_doi":RHP_DOI,
       "original_paper_doi":"10.1111/mec.14115",
       "zenodo_dryad_mirror_id":RHP_RECORD,
       "source_file_SHA256":sha,
       "source_file_publisher_MD5":EXPECTED_MD5,
       "original_source_maternal_fruit_rows":SOURCE_ROWS,
       "source_treatment_counts":dict(arm),
       "original_source_eligibility_counts":dict(counts),
       "registered_complete_source_gate_pass":eligible,
       "source_numeric_paternity_used_to_estimate_effect":False,
       "source_paternity_magnitude_or_direction_reported":False,
       "direct_father_to_mother_visit_pairs_measured":False,
       "original_source_individual_rows_or_IDs_exported":False,
       "decision":"MAY_RUN_PRELOCKED_MATERNAL_CV" if eligible else "SOURCE_MATERNAL_COVERAGE_STOP",
    }

def models(original):
    # Source gate is immutable and must be assessed *before* this endpoint
    # is ever fitted. Only exact frozen 60-row mother cohort is allowed.
    valid=[]
    for r in original:
        mo=str(r["plantID"]).strip()
        tr=str(r["treatment"]).strip().lower()
        x=valid_float(r["isolation20"])
        y=valid_float(r["correlatedPaternity"])
        if (not mo or tr not in TREATMENTS or
            x is None or x<0 or y is None or not -1<=y<=1):
            continue
        valid.append({"mother":mo,"treatment":tr,
                      "x":math.log1p(x),"y":y})
    return valid

def design(train,test,treatment):
    # Training-only standardization of original spatial isolation.
    mu=sum(x["x"] for x in train)/len(train)
    sd=(sum((x["x"]-mu)**2 for x in train)/len(train))**.5
    if sd<1e-10:raise ValueError("SOURCE_TRAIN_ISOLATION_VARIANCE_ZERO")
    def encode(items):
        return np.asarray([
           [1.,(r["x"]-mu)/sd]+(
              [float(r["treatment"]=="de"),float(r["treatment"]=="ne")]
              if treatment else [])
           for r in items],dtype=float)
    return encode(train),encode(test)

def ridge_normal(x,y,xt):
    penalty=np.eye(x.shape[1])
    penalty[0,0]=0
    beta=np.linalg.solve(x.T@x+penalty,x.T@y)
    return xt@beta

def ridge_coordinate(x,y,xt):
    # Independent coordinate-descent normal equations, intercept unpenalized;
    # synthetic and actual predictions checked against linear solver to 1e-8.
    beta=np.zeros(x.shape[1],dtype=float)
    n=x.shape[0]
    residual=y-x@beta
    for iteration in range(30000):
        maxstep=0.
        for j in range(x.shape[1]):
            col=x[:,j]
            prior=beta[j]
            residual+=col*prior
            denom=float(col@col)+(0 if j==0 else 1)
            if denom<=0:raise ValueError("Unexpected zero regularized feature")
            new=float(col@residual)/denom
            beta[j]=new
            residual-=col*new
            maxstep=max(maxstep,abs(new-prior))
        if maxstep<1e-13:break
    else:raise ValueError("Independent ridge solver did not converge")
    return xt@beta

def fit_predict(train,test,treatment):
    if not treatment:
        x,xt=design(train,test,False)
    else:
        x,xt=design(train,test,True)
    y=np.asarray([r["y"] for r in train],dtype=float)
    a=ridge_normal(x,y,xt)
    b=ridge_coordinate(x,y,xt)
    err=float(np.max(np.abs(a-b)))
    if err>1e-8:
        raise ValueError("Two independent ridge solvers disagree")
    return a,err

def heldout_source():
    gate=source_coverage()
    base={
       "programme_id":"RHP001",
       "original_publication":"Rhodes Fant Skogen 2017 Molecular Ecology",
       "original_dataset":"10.5061/dryad.p24q3",
       "source_first_stage_gate":gate,
       "previous_Barbot_father_contact_source_result_untouched":True,
       "this_is_not_partner_specific_visitation":True,
       "original_source_genotypes_parentage_values_or_mother_IDs_not_redistributed":True,
       "independent_study_count":1,
       "registered_model_specification":FREEZE,
    }
    if not gate["registered_complete_source_gate_pass"]:
        return {**base,"status":"RHP001_ORIGINAL_MATERNAL_ELIGIBILITY_STOP",
                "effect_estimated":False}
    raw,_=get_original_families()
    items=models(raw)
    if len(items)!=gate["original_source_eligibility_counts"]["source_complete_fruit_families"]:
        raise ValueError("Source original eligibility drift after source-only gate")
    mothers=sorted({r["mother"] for r in items})
    if len(mothers)!=gate["original_source_eligibility_counts"]["source_unique_complete_maternal_plants"]:
        raise ValueError("Source original mother labels drift")
    groups=defaultdict(list)
    for r in items:groups[r["mother"]].append(r)
    errors=[]
    solvermax=0.
    for mother in mothers:
        train=[r for r in items if r["mother"]!=mother]
        test=groups[mother]
        yn=np.asarray([r["y"] for r in test],dtype=float)
        out0=np.full(len(test),sum(r["y"] for r in train)/len(train),dtype=float)
        out1,e1=fit_predict(train,test,False)
        out2,e2=fit_predict(train,test,True)
        solvermax=max(solvermax,e1,e2)
        e0=out0-yn;e1v=out1-yn;e2v=out2-yn
        errors.append({
            "n_original_seed_families":len(test),
            "Mnull_MSE":float(np.mean(e0**2)),
            "M0_MSE":float(np.mean(e1v**2)),
            "M1_MSE":float(np.mean(e2v**2)),
            "Mnull_MAE":float(np.mean(abs(e0))),
            "M0_MAE":float(np.mean(abs(e1v))),
            "M1_MAE":float(np.mean(abs(e2v))),
        })
    if sum(f["n_original_seed_families"] for f in errors)!=len(items):
        raise ValueError("Group holdout did not score exactly every source family")
    for f in errors:
        f["delta_M0_minus_M1"]=f["M0_MSE"]-f["M1_MSE"]
    def meaneq(k):
        return sum(r[k] for r in errors)/len(errors)
    def familieeq(k):
        return sum(r[k]*r["n_original_seed_families"] for r in errors)/len(items)
    d=meaneq("delta_M0_minus_M1")
    rng=random.Random(BOOT_SEED)
    n=len(errors)
    draws=sorted(sum(errors[rng.randrange(n)]["delta_M0_minus_M1"]
                     for _ in range(n))/n for _ in range(BOOTSTRAP))
    def q(p):
        i=(len(draws)-1)*p
        lo=math.floor(i);hi=math.ceil(i)
        return draws[lo]+(i-lo)*(draws[hi]-draws[lo])
    wins=sum(f["delta_M0_minus_M1"]>0 for f in errors)
    supported=d>0 and q(.025)>0 and wins/n>=.60
    return {**base,
       "status":"RHP001_ORIGINAL_FAMILY_HOLDOUT_MODEL_COMPLETED",
       "effect_estimated":True,
       "source_biological_unit":"one maternal plant, repeated fruit families nested",
       "source_original_maternal_plants_n":n,
       "source_original_seed_families_n":len(items),
       "source_treatments":dict(gate["source_treatment_counts"]),
       "source_mother_equal_heldout_MSE":{
           "Mnull":meaneq("Mnull_MSE"),"M0_isolation":meaneq("M0_MSE"),
           "M1_isolation_plus_exclusion":meaneq("M1_MSE"),
           "Mnull_minus_M0":meaneq("Mnull_MSE")-meaneq("M0_MSE"),
           "M0_minus_M1":d,
       },
       "source_fruit_family_equal_M0_minus_M1":familieeq("M0_MSE")-familieeq("M1_MSE"),
       "source_mother_equal_heldout_MAE":{
           "Mnull":meaneq("Mnull_MAE"),"M0_isolation":meaneq("M0_MAE"),
           "M1_isolation_plus_exclusion":meaneq("M1_MAE")},
       "source_whole_mother_bootstrap_draws":BOOTSTRAP,
       "source_whole_mother_bootstrap_95pct_delta":[q(.025),q(.975)],
       "mother_holdout_folds_with_positive_increment":wins,
       "original_source_mother_folds_n":n,
       "source_original_outcomes_from_genotyped_seeds_not_compatible_stigma_pollen":True,
       "independent_2_solver_max_abs_predictive_disagreement":solvermax,
       "new_source_marginal_model_not_genetic_mate_identity_edge":True,
       "predeclared_one_study_predictive_rule_pass":supported,
       "decision":("ONE_STUDY_MATERNAL_HOLDOUT_TREATMENT_INCREMENT" if supported
                   else "NO_RESOLVED_ONE_STUDY_TREATMENT_PREDICTION_GAIN"),
    }

def synthetic():
    # Same-mother treatment family rows MUST remain together in heldout fold.
    data=[]
    for m in range(30):
        for tr in TREATMENTS:
            x=float(m+1)
            y=.08*math.log1p(x)+{"c":0,"de":.3,"ne":-.2}[tr]
            data.append({"mother":str(m),"treatment":tr,"x":math.log1p(x),"y":y})
    moms={r["mother"] for r in data}
    assert len(moms)==30 and len(data)==90
    mother="6"
    tr=[r for r in data if r["mother"]!=mother]
    te=[r for r in data if r["mother"]==mother]
    assert len(te)==3 and all(r["mother"]!=mother for r in tr)
    pred1,e=fit_predict(tr,te,True)
    pred0,e0=fit_predict(tr,te,False)
    assert e<1e-8 and e0<1e-8
    assert sum((a-r["y"])**2 for a,r in zip(pred1,te))<sum(
        (a-r["y"])**2 for a,r in zip(pred0,te))
    assert valid_float("NA") is None and valid_float("-0.04")==-.04
    print("RHP001_SOURCE_MATERNAL_SPLIT_AND_RIDGE_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--source-only",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:synthetic();return 0
    if args.output is None:p.error("--output required")
    try:result=source_coverage() if args.source_only else heldout_source()
    except Exception as ex:result={
         "status":"RHP001_SOURCE_OR_MODEL_STOP",
         "reason":type(ex).__name__+": "+str(ex)[:240],
         "effect_estimated":False,"original_source_genotypes_parentage_values_or_mother_IDs_not_redistributed":True}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    brief={
        "status":result["status"],"decision":result.get("decision"),
        "source_complete_fruit_families":result.get("original_source_eligibility_counts",{}).get("source_complete_fruit_families"),
        "source_original_maternal_plants_n":result.get("source_original_maternal_plants_n",result.get("original_source_eligibility_counts",{}).get("source_unique_complete_maternal_plants")),
        "source_treatment_counts":result.get("source_treatment_counts",result.get("source_treatments")),
        "source_eligible":result.get("registered_complete_source_gate_pass"),
        "mother_equal_MSE":result.get("source_mother_equal_heldout_MSE"),
        "bootstrap":result.get("source_whole_mother_bootstrap_95pct_delta"),
        "winning_mothers":result.get("mother_holdout_folds_with_positive_increment"),
        "error":result.get("reason"),
        "source_original_rows_redistributed":False,
        "direct_partner_contact_measured":False,
    }
    print("RHP001_ORIGINAL_WILD_POLLINATOR_IDENTITY_MATERNAL_TEST "+json.dumps(brief,sort_keys=True))
    return 0 if result["status"] in (
        "RHP001_PUBLISHED_ORIGINAL_MATERNAL_COHORT_AUDIT_COMPLETE",
        "RHP001_ORIGINAL_MATERNAL_ELIGIBILITY_STOP",
        "RHP001_ORIGINAL_FAMILY_HOLDOUT_MODEL_COMPLETED",
    ) else 1

if __name__=="__main__":raise SystemExit(main())
