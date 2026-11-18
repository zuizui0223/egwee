#!/usr/bin/env python3
"""QPF007 original 2026 Brassica 160-plant / 16-session Q+P -> seed holdout.

Research programme one (experimental Brassica, not 16 landscapes).
The pre-outcome protocol was separately frozen at commit 1d4b78a1...
BEFORE opening actual biological response values. Only official publisher
Zenodo files via advertised links; original checksums verified on download.
No raw source rows, plant/offspring IDs, pollen, visits or seed values are
written or printed. Outputs only session-fold predictive losses.
Two independent numeric solvers agree: Gauss-Jordan ridge and coordinate
descent ridge, held-out 16 sessions, lambda=1 on train-standardized columns.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shlex
from statistics import mean
import subprocess

from audit_brassica_rapa_zenodo_source_keys import (
    ID, load_manifest, trusted_binary, decode_table,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FREEZE_COMMIT = "1d4b78a1a0ee82cc267b287f7cc0e4a3899486c3"
FREEZE_REL = "research/qpf_independent_2026/QPF007_FROZEN_SESSION_HELDOUT_MODEL_20261118.json"
FREEZE_PATH = ROOT / FREEZE_REL
PLANT_SOURCE_FILE = "data_ABPOLL_ID_resume.txt"
POLLEN_SOURCE_FILE = "data_ABPOLL_flower_resume.txt"
PLANT_SOURCE_SHA = "5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe"
POLLEN_SOURCE_SHA = "ec7217acb683a0d0475622f3510228f3062a72a8bfd17162888f160db369a495"
REQUIRED_COLUMNS = (
    "session","ID_full","poll_treat","nb_visit","nb_flo_all",
    "height_max","pl_mean","nbGr_mean"
)


def verify_frozen_science():
    original = subprocess.check_output(
        ["git","show", FREEZE_COMMIT+":"+FREEZE_REL], cwd=ROOT
    )
    if original != FREEZE_PATH.read_bytes():
        raise RuntimeError("Frozen original Brassica scientific design byte-drift")
    subprocess.run(
        ["git","merge-base","--is-ancestor",FREEZE_COMMIT,"HEAD"],
        cwd=ROOT,check=True
    )
    frozen = json.loads(original)
    if frozen["experiment_id"] != "QPF007_Brassica_rapa_2026_plant_pollen_seed_session_CV_v1":
        raise RuntimeError("Unexpected QPF007 original experiment")
    if frozen["status"] != "PROSPECTIVE_PREDICTIVE_LOCK_BEFORE_OPENING_SOURCE_POLLEN_SEED_NUMERIC_OUTCOMES":
        raise RuntimeError("QPF007 original lock was not pre-outcome")
    return frozen


def full_source_rows(payload):
    """Parse original author R write.table output; return only in-process data.

    Some files have quoted headers separated by space, and an optional numeric
    row.names field. Duplicated nonkey output columns cannot overwrite any
    original required source key. All raw source values are kept in process only.
    """
    try:
        s=payload.decode("utf-8-sig")
    except UnicodeDecodeError:
        s=payload.decode("latin-1")
    raw=s.splitlines()
    if not raw:
        raise ValueError("Original source has zero lines")
    if any(d in raw[0] for d in ("\t",",",";","|")):
        delim = "\t" if "\t" in raw[0] else ";" if ";" in raw[0] else "," if "," in raw[0] else "|"
        iterator=csv.reader(io.StringIO(s),delimiter=delim)
    else:
        iterator=(shlex.split(line,posix=True) for line in raw)
    head=next(iterator,None)
    if head is None or len(head)<8 or len(head)>3000:
        raise ValueError("Original individual plant source header invalid")
    head=[x.strip('"').strip() for x in head]
    index={}
    for col in REQUIRED_COLUMNS:
        ix=[i for i,k in enumerate(head) if k==col]
        if len(ix)!=1:
            raise ValueError("Missing/ambiguous original required column "+col)
        index[col]=ix[0]
    rows=[]
    added_rowname=False
    for row in iterator:
        if not row or all(not x.strip() for x in row):
            continue
        if len(row)==len(head)+1 and not added_rowname and row[0].isdigit():
            index={k:v+1 for k,v in index.items()}
            added_rowname=True
        if len(row)!=(len(head)+int(added_rowname)):
            raise ValueError("Original source row width differs from key header")
        rows.append({k:row[i] for k,i in index.items()})
        if len(rows)>1000:
            raise ValueError("Original source has too many plant rows")
    if len(rows)!=160:
        raise ValueError("Original main 160-plant source denominator drifted")
    keys=[(r["session"],r["ID_full"]) for r in rows]
    if any(not s or not p for s,p in keys) or len(set(keys))!=160:
        raise ValueError("Duplicated or empty original session/plant ID")
    if len({session for session,_ in keys})!=16:
        raise ValueError("Original source must have 16 experimental populations")
    return rows


def float_or_none(v):
    if v is None or str(v).strip().casefold() in ("", "na", "nan", "null", "none","inf","-inf"):
        return None
    try:
        x=float(str(v).strip())
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def materialize_eligibility(raw, original_stigma_key_count=160):
    if len(raw)!=160 or original_stigma_key_count!=160:
        raise ValueError("Source keys not matched across 160 plant/stigma rows")
    levels=sorted({str(r["poll_treat"]).strip() for r in raw})
    if not 2<=len(levels)<=5 or any(not x or x.casefold()=="na" for x in levels):
        raise ValueError("Invalid source-defined bee-density treatment levels")
    admissible=[]
    lost=Counter()
    bysession=Counter()
    for r in raw:
        session=r["session"]
        d={}
        for col in ("nbGr_mean","nb_visit","nb_flo_all","height_max","pl_mean"):
            v=float_or_none(r[col])
            if v is None:
                d[col]=None
                lost["missing_"+col]+=1
            elif v < 0:
                raise ValueError("Negative original biological count in required column")
            else:
                d[col]=v
        if any(x is None for x in d.values()):
            lost["excluded_plant_rows"]+=1
            continue
        base = [float(r["poll_treat"]==lev) for lev in levels[1:]]
        base.extend((math.log1p(d["nb_visit"]),math.log1p(d["nb_flo_all"]),
                     math.log1p(d["height_max"])))
        pollen = math.log1p(d["pl_mean"])
        admissible.append({
            "session":session, "M0":base, "M1":base+[pollen],
            "y":math.log1p(d["nbGr_mean"])
        })
        bysession[session]+=1
    if len(admissible)<120 or len(bysession)!=16 or any(n<6 for n in bysession.values()):
        return None,{
            "status":"COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST",
            "source_plant_rows":160,
            "main_stigma_source_plant_keys":original_stigma_key_count,
            "source_complete_case_n":len(admissible),
            "source_excluded_rows":lost["excluded_plant_rows"],
            "missing_required_field_counts":dict(lost),
            "n_original_session_groups_with_eligible_mothers":len(bysession),
            "n_source_sessions_below_six_complete_plant_units":16-sum(n>=6 for n in bysession.values()),
            "treatment_levels_n":len(levels),
            "original_biology_outcomes_not_pooled":True,
            "primary_coverage_gate":"at least 120 plant units and 6 complete plants in every one of 16 sessions"
        }
    safe={
        "status":"ORIGINAL_SOURCE_160_PLANTS_ELIGIBILITY_PASSED",
        "source_plant_rows":160,
        "original_stigma_matching_source_plant_keys":original_stigma_key_count,
        "complete_plant_n":len(admissible),
        "excluded_plant_n":lost["excluded_plant_rows"],
        "missing_required_field_counts":dict(lost),
        "n_original_session_groups":16,
        "session_group_sizes_sorted":sorted(bysession.values()),
        "n_bee_density_treatment_categories":len(levels),
    }
    return admissible,safe


def gaussian(A,b):
    if len(A)!=len(b):
        raise ValueError("Wrong square ridge matrix dimensions")
    n=len(b)
    work=[list(map(float,A[i]))+[float(b[i])] for i in range(n)]
    for k in range(n):
        piv=max(range(k,n),key=lambda i:abs(work[i][k]))
        work[k],work[piv]=work[piv],work[k]
        if abs(work[k][k])<1e-12:
            raise RuntimeError("Penalized source model matrix singular")
        scale=work[k][k]
        for j in range(k,n+1):
            work[k][j]/=scale
        for i in range(n):
            if i==k:continue
            ratio=work[i][k]
            for j in range(k,n+1):
                work[i][j]-=ratio*work[k][j]
    return [row[-1] for row in work]


def ridge_predict(train,test,model,method="gaussian"):
    if model not in ("M0","M1"):
        raise ValueError("Unregistered source model")
    if method not in ("gaussian","coordinate"):
        raise ValueError("Only independent ridge solvers registered")
    raw=[r[model] for r in train]
    d=len(raw[0])
    mus=[mean(r[j] for r in raw) for j in range(d)]
    sd=[mean((r[j]-mus[j])**2 for r in raw)**.5 for j in range(d)]
    sd=[v if v>1e-10 else 1.0 for v in sd]
    X=[[(r[j]-mus[j])/sd[j] for j in range(d)] for r in raw]
    H=[[(r[model][j]-mus[j])/sd[j] for j in range(d)] for r in test]
    y=[r["y"] for r in train]
    ymean=mean(y)
    if method=="gaussian":
        design=[[1.0]+r for r in X]
        gram=[[sum(r[j]*r[k] for r in design)+(1 if j==k and j>0 else 0)
                for k in range(d+1)] for j in range(d+1)]
        rhs=[sum(r[j]*yy for r,yy in zip(design,y)) for j in range(d+1)]
        beta=gaussian(gram,rhs)
        return [beta[0]+sum(z[j]*beta[j+1] for j in range(d)) for z in H]
    beta=[0.0]*d
    residual=[yy-ymean for yy in y]
    denominators=[1+sum(r[j]*r[j] for r in X) for j in range(d)]
    for sweep in range(20000):
        maxchange=0.0
        for j in range(d):
            new=sum(X[i][j]*(residual[i]+X[i][j]*beta[j])
                    for i in range(len(X)))/denominators[j]
            change=new-beta[j]
            if change:
                for i in range(len(X)):
                    residual[i]-=X[i][j]*change
            beta[j]=new
            maxchange=max(maxchange,abs(change))
        if maxchange < 1e-13:
            break
    else:
        raise RuntimeError("Independent coordinate ridge solver did not converge")
    return [ymean+sum(z[j]*beta[j] for j in range(d)) for z in H]


def original_stigma_keys(manifest):
    files={x.get("key") or x.get("filename"):x for x in manifest["files"]}
    for name in (PLANT_SOURCE_FILE,POLLEN_SOURCE_FILE):
        if name not in files:
            raise ValueError("Original publisher does not list required main workbook")
    source=trusted_binary(files[POLLEN_SOURCE_FILE])
    if hashlib.sha256(source).hexdigest()!=POLLEN_SOURCE_SHA:
        raise RuntimeError("Original published stigma flower source SHA changed")
    _,_,n,keys,sessions=decode_table(source)
    if (n,len(keys),len(sessions))!=(1967,160,16):
        raise ValueError("Original pollen flower source grain drifted")
    return keys


def source_analysis():
    p=verify_frozen_science()
    meta=load_manifest()
    entries={f.get("key") or f.get("filename"):f for f in meta["files"]}
    if PLANT_SOURCE_FILE not in entries:
        raise RuntimeError("Original Brassica source plant file absent")
    raw=trusted_binary(entries[PLANT_SOURCE_FILE])
    if hashlib.sha256(raw).hexdigest()!=PLANT_SOURCE_SHA:
        raise RuntimeError("Original 2026 plant source SHA differs from locked receipt")
    # Verify biological source plant and stigma flower identities BEFORE
    # any outcome is fitted, but now after the frozen scientific design.
    stigma_keys=original_stigma_keys(meta)
    plants=full_source_rows(raw)
    main_keys={(r["session"],r["ID_full"]) for r in plants}
    if main_keys!=stigma_keys or len(main_keys)!=160:
        raise ValueError("Original 160 plant-pollen key match is not exact")
    usable,grain=materialize_eligibility(plants,len(stigma_keys))
    if usable is None:
        return {
            "analysis_id":p["experiment_id"],"scientific_status":"COVERAGE_STOP",
            "original_source_verified":True,"source_coverage":grain,
            "registered_original_protocol_commit":FREEZE_COMMIT,
            "original_paper_doi":"10.1371/journal.pbio.3003579",
            "source_raw_data_uploaded":False,
            "new_positive_ecological_effect_claimed":False,
        }
    sessions=sorted({r["session"] for r in usable})
    folds=[]
    max_solver_error=0.0
    for i,session in enumerate(sessions,1):
        tr=[r for r in usable if r["session"]!=session]
        te=[r for r in usable if r["session"]==session]
        if len(te)<6:
            raise RuntimeError("Original complete-case session size gate failed")
        fold={"session_fold":i,"n_plant_units":len(te)}
        for model in ("M0","M1"):
            pred=ridge_predict(tr,te,model,"gaussian")
            independent=ridge_predict(tr,te,model,"coordinate")
            max_solver_error=max(max_solver_error,max(abs(a-b) for a,b in zip(pred,independent)))
            if max_solver_error>1e-8:
                raise RuntimeError("Independent source ridge predictions fail verification")
            err=[v-r["y"] for v,r in zip(pred,te)]
            fold[model+"_MSE"]=mean(e*e for e in err)
            fold[model+"_MAE"]=mean(abs(e) for e in err)
        fold["M0_minus_M1_MSE"]=fold["M0_MSE"]-fold["M1_MSE"]
        folds.append(fold)
    n=sum(r["n_plant_units"] for r in folds)
    def pooled(k):
        return sum(r["n_plant_units"]*r[k] for r in folds)/n
    m0,m1=pooled("M0_MSE"),pooled("M1_MSE")
    delta=m0-m1
    win=sum(r["M0_minus_M1_MSE"]>0 for r in folds)
    actual_win=bool(m0>0 and delta/m0>=.05 and win>=12)
    return {
        "analysis_id":p["experiment_id"],
        "scientific_status":"ORIGINAL_2026_SOURCE_16_SESSION_FROZEN_TEST_COMPLETE",
        "original_data_doi":"10.5281/zenodo.21628183",
        "original_paper_doi":"10.1371/journal.pbio.3003579",
        "registered_original_protocol_commit":FREEZE_COMMIT,
        "original_plant_file_sha256":PLANT_SOURCE_SHA,
        "original_flower_file_sha256":POLLEN_SOURCE_SHA,
        "source_coverage":grain,
        "primary_response":"log1p(original nbGr_mean seeds per sampled fruit), NOT recruitment",
        "primary_compare":"source pollinator treatment + visits + flower display + height vs + same-plant source pl_mean",
        "heldout_session_folds":folds,
        "pooled_original_plant_scores":{
            "n_valid_plants":n,"n_experimental_sessions":len(folds),
            "M0_MSE":m0,"M1_MSE":m1,
            "M0_MAE":pooled("M0_MAE"),"M1_MAE":pooled("M1_MAE"),
            "M0_minus_M1_MSE":delta,
            "relative_mse_reduction_percent":100*delta/m0 if m0>0 else None,
            "positive_session_folds":win
        },
        "registered_decision":(
            "BOUNDED_WITHIN_PROGRAMME_POLLEN_INCREMENT" if actual_win
            else "NO_ROBUST_WITHIN_EXPERIMENT_SESSION_POLLEN_INCREMENT"
        ),
        "independent_numeric_verification":{
            "algorithms":"full ridge Gaussian normal equation versus direct coordinate descent",
            "maximum_absolute_heldout_prediction_error":max_solver_error,
            "verified_all_16_folds_both_models":True
        },
        "scope":[
            "One original experimental research programme with 16 treatment sessions, not 16 independent landscapes.",
            "Original published authors already demonstrated visitation versus genetic mating discrepancies.",
            "Plant-level stigma pollen load does not identify compatible pollen or paternal alleles.",
            "Pollen collected from flower subsample, seeds from sampled fruits of the same mother not the same stigma flower.",
            "Pairwise 18-session raw records and original 1099 offspring parentage are outside this strict source-only model.",
            "Original six natural QPF prospectively selected source registry was not expanded.",
            "No causal mediation, universal island/urban functional fragmentation or genetic-rescue claims."
        ],
        "new_independent_natural_fragmentation_landscape_replication":False,
        "source_raw_data_uploaded":False,
        "individual_source_rows_or_IDs_disclosed":False
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    out=source_analysis()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["scientific_status"],
        "source_verified":out["original_source_verified"] if "original_source_verified" in out else True,
        "source_n":out["source_coverage"].get("complete_plant_n",out["source_coverage"].get("source_complete_case_n")),
        "n_session_folds":len(out.get("heldout_session_folds",[])),
        "MSE_M0":out.get("pooled_original_plant_scores",{}).get("M0_MSE"),
        "MSE_M1":out.get("pooled_original_plant_scores",{}).get("M1_MSE"),
        "decision":out.get("registered_decision","COVERAGE_STOP"),
        "original_source_rows_republished":False,
    },indent=2))


if __name__=="__main__":
    main()
