#!/usr/bin/env python3
"""Predeclared study-balanced CropPol guild-composition Q→F prediction.

This script runs only after source-only audited denominators 29 panels,
20 programmes, 591 unique fields. No original rows or site-level predictions
are committed, redistributed or printed.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from audit_source_field_grain import read_rows,norm,valid,num
from audit_syrphid_coverage_before_qf import SURVEYED,VISIT_SAMPLING,BANNED_YIELD_UNIT,frame_id

FREEZE="research/croppol_guild_function/GUILD_QF_PREDICTION_FREEZE_20261118.md"
SOURCE_COMMIT="99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b"
SEED_BOOT=20261118
N_BOOT=2000

def select_frozen_rows():
    fields=read_rows("field")
    panels=defaultdict(list)
    keys=set()
    for r in fields:
        k=(norm(r["study_id"]),norm(r["site_id"]),norm(r["sampling_year"]),norm(r["crop"]))
        if k in keys:raise ValueError("SOURCE_STOP: duplicate field row")
        keys.add(k)
        if any(not valid(v) for v in k):
            continue
        if norm(r["use_visits_or_abundance"])!="use visits":
            continue
        if norm(r["sampling_visitation"]) not in VISIT_SAMPLING:
            continue
        if norm(r["taxa_recorded"]) not in SURVEYED:
            continue
        yu=norm(r["yield_units"])
        vu=norm(r["visitation_rate_units"])
        if not valid(yu) or not valid(vu) or any(x in yu for x in BANNED_YIELD_UNIT):
            continue
        nums={name:num(r[name]) for name in
              ("yield","visitation_rate","visit_bombus","visit_wildbees",
               "visit_syrphids","visit_honeybee")}
        if any(v is None for v in nums.values()):
            continue
        bee=nums["visit_bombus"]+nums["visit_wildbees"]
        fly=nums["visit_syrphids"]
        if bee+fly<=0:continue
        pid=frame_id(r)
        panels[pid].append({
            "site_key":k,
            "y_log":math.log1p(nums["yield"]),
            "x_total_log":math.log1p(nums["visitation_rate"]),
            "x_syrphid_share":fly/(bee+fly),
            "bee_positive":bee>0,
            "syrphid_positive":fly>0,
        })
    selected={}
    for pid,items in panels.items():
        if len(items)<10:continue
        if sum(z["bee_positive"] for z in items)<3:continue
        if sum(z["syrphid_positive"] for z in items)<3:continue
        selected[pid]=items
    programme_count=len({k[0] for k in selected})
    row_count=sum(len(v) for v in selected.values())
    if len(selected)!=29 or programme_count!=20 or row_count!=591:
        raise ValueError(f"SOURCE_STOP: exact pre-outcome eligible denominators changed {len(selected)}/{programme_count}/{row_count}")
    return selected

def fold_of(source_key):
    s="\x1f".join(source_key).encode("utf-8")
    return int(hashlib.sha256(s).hexdigest()[:16],16)%5

def ridge_predict(x_train, y_train, x_test, lam=1.0):
    means=x_train.mean(axis=0)
    sds=x_train.std(axis=0,ddof=0)
    if np.any(sds<1e-12):
        raise ValueError("ZERO_PREDICTOR_VARIANCE_TRAIN_ONLY")
    ymu=float(y_train.mean())
    ysd=float(y_train.std(ddof=0))
    if ysd<1e-12:
        raise ValueError("ZERO_OUTCOME_VARIANCE_TRAIN_ONLY")
    train=(x_train-means)/sds
    test=(x_test-means)/sds
    XX=np.column_stack([np.ones(len(train)),train])
    Xt=np.column_stack([np.ones(len(test)),test])
    penal=np.eye(XX.shape[1])
    penal[0,0]=0
    beta=np.linalg.solve(XX.T @ XX+lam*penal,XX.T @ ((y_train-ymu)/ysd))
    return Xt @ beta, (ymu,ysd)

def score_panel(rows):
    fold=np.array([fold_of(r["site_key"]) for r in rows])
    x=np.array([[r["x_total_log"],r["x_syrphid_share"]] for r in rows])
    y=np.array([r["y_log"] for r in rows])
    squared=[[],[]]
    expected_rows=0
    for f in range(5):
        tr=np.flatnonzero(fold!=f)
        te=np.flatnonzero(fold==f)
        if len(te)==0:continue
        if len(tr)<2:raise ValueError("TOO_FEW_TRAIN_FIELDS")
        m0,center=ridge_predict(x[tr,:1],y[tr],x[te,:1])
        m1,center1=ridge_predict(x[tr,:2],y[tr],x[te,:2])
        if abs(center[0]-center1[0])>1e-12 or abs(center[1]-center1[1])>1e-12:
            raise ValueError("TRAIN_Y_STANDARDIZATION_DRIFT")
        target=(y[te]-center[0])/center[1]
        squared[0].extend(((target-m0)**2).tolist())
        squared[1].extend(((target-m1)**2).tolist())
        expected_rows+=len(te)
    if expected_rows!=len(rows) or not squared[0] or len(squared[0])!=len(squared[1]):
        raise ValueError("FOLD_LEAKAGE_OR_MISSING_PREDICTIONS")
    mse0=float(np.mean(squared[0]))
    mse1=float(np.mean(squared[1]))
    if not all(math.isfinite(x) for x in (mse0,mse1)):
        raise ValueError("NONFINITE_MODEL")
    return mse0,mse1

def run():
    source=select_frozen_rows()
    group=defaultdict(list)
    nonestimable=Counter()
    admited_nfield=0
    successes=0
    for pid,rows in sorted(source.items()):
        try:
            mse0,mse1=score_panel(rows)
        except (ValueError,np.linalg.LinAlgError) as exc:
            nonestimable[str(exc)]+=1
            continue
        admited_nfield+=len(rows)
        gains=mse0-mse1
        successes+=int(gains>0)
        group[pid[0]].append((mse0,mse1,gains))
    if (len(group)<10 or sum(map(len,group.values()))<12 or admited_nfield<200):
        return {
            "status":"POSTFREEZE_NONESTIMABLE_PANEL_COVERAGE_STOP",
            "effect_estimated":False,
            "source_admitted_pre_outcome_panels":29,
            "source_admitted_pre_outcome_study_programmes":20,
            "n_predicted_panels":sum(map(len,group.values())),
            "n_predicted_study_programmes":len(group),
            "n_predicted_fields":admited_nfield,
            "nonestimable_panel_counts":dict(nonestimable),
            "source_original_rows_redistributed":False,
            "outcome_values_redistributed":False,
        }
    keys=sorted(group)
    diffs=np.array([np.mean([p[2] for p in group[k]]) for k in keys])
    b0=np.array([np.mean([p[0] for p in group[k]]) for k in keys])
    b1=np.array([np.mean([p[1] for p in group[k]]) for k in keys])
    rng=np.random.default_rng(SEED_BOOT)
    draws=rng.integers(0,len(keys),size=(N_BOOT,len(keys)))
    bs=diffs[draws].mean(axis=1)
    ci=[float(x) for x in np.percentile(bs,[2.5,97.5])]
    mean_gain=float(np.mean(diffs))
    positive=int(np.sum(diffs>0))
    loo=(diffs.sum()-diffs)/(len(diffs)-1)
    return {
        "status":"FROZEN_CROPPOL_GUILD_QF_PREDICTIVE_COMPARISON_COMPLETE",
        "source":"ibartomeus/CropPol", "source_commit":SOURCE_COMMIT,
        "source_field_blob_sha1":"cd19a354741ac40428e6b94aa1ec2ee596ff0547",
        "freeze":FREEZE,
        "source_admitted_pre_outcome_panels":29,
        "source_admitted_pre_outcome_study_programmes":20,
        "source_admitted_pre_outcome_fields":591,
        "n_eligible_predicted_panels":sum(map(len,group.values())),
        "n_eligible_predicted_study_programmes":len(keys),
        "n_eligible_predicted_fields":admited_nfield,
        "nonestimable_panels":dict(nonestimable),
        "positive_gain_panels":successes,
        "positive_gain_independent_programmes":positive,
        "primary_equal_programme_mean_gain_M0_minus_M1":mean_gain,
        "primary_whole_programme_bootstrap_95pct":ci,
        "original_programme_LOO_mean_gain_range":[float(np.min(loo)),float(np.max(loo))],
        "baseline_programme_equal_M0_MSE":float(np.mean(b0)),
        "augmented_programme_equal_M1_MSE":float(np.mean(b1)),
        "mean_relative_programme_equal_MSE_gain_pct":100*mean_gain/float(np.mean(b0)),
        "bootstrap_programme_draws":N_BOOT,
        "bootstrap_seed":SEED_BOOT,
        "source_programme_fraction_positive":positive/len(keys),
        "predeclared_positive_support": ci[0]>0 and positive/len(keys)>=.70,
        "decision": ("BOUNDED_WITHIN_STUDY_PREDICTIVE_INCREMENT" if ci[0]>0 and positive/len(keys)>=.70
                     else "NO_RESOLVED_STUDY_GENERAL_GUILD_COMPOSITION_INCREMENT"),
        "study_hierarchy":"Study_id2, each crop/year/yield-unit/visit-unit nested; 5 source-hash stable field folds",
        "no_out_of_study_transport_assessed":True,
        "not_a_measured_compatible_pollen_or_causal_frag":True,
        "original_source_rows_redistributed":False,
        "outcome_values_redistributed":False,
        "field_level_predictions_redistributed":False,
    }

def synthetic():
    # Stable all-fold coverage and a marked share effect not hidden by scale.
    fake=[]
    for i in range(30):
        x=(i%7)/6.
        p=((i*17)%11)/10.
        fake.append({"site_key":("test","site"+str(i),"2024","crop"),
                     "y_log":0.1+0.2*x+1.5*p,
                     "x_total_log":x,
                     "x_syrphid_share":p})
    m0,m1=score_panel(fake)
    assert m1<m0
    assert fold_of(fake[0]["site_key"])==fold_of(fake[0]["site_key"])
    # Under leak-free train standardization a zero-variation feature is a stop,
    # not filled from heldout target or globally standardized source.
    bad=[dict(z,x_syrphid_share=0.5) for z in fake]
    try:
        score_panel(bad)
    except ValueError:pass
    else:raise AssertionError("zero-variation predictor was not rejected")
    print("CROPPOL_FROZEN_PREDICTION_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        synthetic();return 0
    if a.output is None:p.error("--output is required")
    try:r=run()
    except Exception as exc:
        r={"status":"SOURCE_OR_INFERENTIAL_STOP","reason":type(exc).__name__+": "+str(exc)[:350],
           "effect_estimated":False,"original_source_rows_redistributed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CROPPOL_FROZEN_QF_RESULT "+json.dumps(r,sort_keys=True),flush=True)
    return 0 if r["status"] in {
        "FROZEN_CROPPOL_GUILD_QF_PREDICTIVE_COMPARISON_COMPLETE",
        "POSTFREEZE_NONESTIMABLE_PANEL_COVERAGE_STOP",
    } else 1

if __name__=="__main__":
    raise SystemExit(main())
