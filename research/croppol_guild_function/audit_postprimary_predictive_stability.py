#!/usr/bin/env python3
"""Post-outcome Q-F model complexity and fold-stability diagnostic, same source."""

from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import test_frozen_qf_guild_increment as q

FREEZE="research/croppol_guild_function/POSTPRIMARY_PREDICTIVE_DIAGNOSTIC_FREEZE_20261118.md"
N_SPLIT=50
SEED_BOOT=20261128
BOOT_REPLICATES=2000

def folds_other(key,seed):
    text=("seed="+str(seed)+"\x1f"+"\x1f".join(key)).encode()
    return int(hashlib.sha256(text).hexdigest()[:16],16)%5

def fold_scores(rows,seed=None):
    folds=np.array([q.fold_of(row["site_key"]) if seed is None
                    else folds_other(row["site_key"],seed) for row in rows])
    x=np.asarray([[r["x_total_log"],r["x_syrphid_share"]] for r in rows])
    y=np.asarray([r["y_log"] for r in rows])
    null,m0,m1=[],[],[]
    for f in range(5):
        tr=np.where(folds!=f)[0]
        te=np.where(folds==f)[0]
        if len(te)==0:continue
        if len(tr)<2:
            raise ValueError("TOO_FEW_TRAIN_FIELDS")
        pred0,center=q.ridge_predict(x[tr,:1],y[tr],x[te,:1])
        pred1,center1=q.ridge_predict(x[tr,:2],y[tr],x[te,:2])
        if center!=center1:
            raise ValueError("MODEL_TRAIN_Y_INCONSISTENCY")
        zy=(y[te]-center[0])/center[1]
        null.extend((zy**2).tolist())
        m0.extend(((zy-pred0)**2).tolist())
        m1.extend(((zy-pred1)**2).tolist())
    if len(null)!=len(rows) or len(null)!=len(m0) or len(null)!=len(m1):
        raise ValueError("NO_COMPLETE_HELDOUT_VALIDATION")
    return tuple(float(np.mean(arr)) for arr in (null,m0,m1))

def report():
    data=q.select_frozen_rows()
    base=defaultdict(list)
    source_qual={p[0] for p in data}
    if (len(data),len(source_qual),sum(map(len,data.values())))!=(29,20,591):
        raise ValueError("source eligible panel sample changed")
    primary_diffs=[]
    for pid,rows in sorted(data.items()):
        null,m0,m1=fold_scores(rows)
        original0,original1=q.score_panel(rows)
        if max(abs(m0-original0),abs(m1-original1))>1e-10:
            raise ValueError("original M0 M1 reproduction drift")
        base[pid[0]].append((null,m0,m1))
    programs=sorted(base)
    orig_delta=np.array([np.mean([p[1]-p[2] for p in base[prog]]) for prog in programs])
    total_delta=np.array([np.mean([p[0]-p[1] for p in base[prog]]) for prog in programs])
    if abs(float(orig_delta.mean())+0.4472056338953386)>1e-10:
        raise ValueError("original primary result was altered")
    rng=np.random.default_rng(SEED_BOOT)
    boot=total_delta[rng.integers(0,len(programs),size=(BOOT_REPLICATES,len(programs)))].mean(axis=1)
    seed_results=[]
    failed={}
    for seed in range(N_SPLIT):
        per_prog=defaultdict(list)
        try:
            for pid,rows in sorted(data.items()):
                null,m0,m1=fold_scores(rows,seed)
                per_prog[pid[0]].append(m0-m1)
            if len(per_prog)!=len(programs):
                raise ValueError("SOURCE_PROGRAMME_LOSS")
            values=np.array([np.mean(per_prog[p]) for p in programs])
            seed_results.append(float(np.mean(values)))
        except (ValueError,np.linalg.LinAlgError) as ex:
            failed[str(seed)]=str(ex)[:100]
    a=np.array(seed_results)
    result={
        "status":"POSTPRIMARY_CROPPOL_PREDICTION_DIAGNOSTIC_COMPLETED",
        "this_is_after_positive_or_negative_primary_outcome":True,
        "source_commit":q.SOURCE_COMMIT,
        "source_original_fields":591,
        "source_original_panels":29,
        "source_original_programmes":20,
        "unchanged_original_primary_M0_minus_M1_gain":float(orig_delta.mean()),
        "null_intercept_only_equal_programme_MSE":float(np.mean([np.mean([p[0] for p in base[s]]) for s in programs])),
        "original_total_visit_M0_equal_programme_MSE":float(np.mean([np.mean([p[1] for p in base[s]]) for s in programs])),
        "original_guild_share_M1_equal_programme_MSE":float(np.mean([np.mean([p[2] for p in base[s]]) for s in programs])),
        "posthoc_baseline_Mnull_minus_total_visit_M0_gain":float(np.mean(total_delta)),
        "posthoc_baseline_gain_whole_programme_bootstrap_95pct":[float(x) for x in np.percentile(boot,[2.5,97.5])],
        "posthoc_baseline_positive_original_programmes":int(sum(x>0 for x in total_delta)),
        "requested_alternative_fold_seeds":N_SPLIT,
        "completed_alternative_fold_seeds":len(a),
        "not_estimable_alternative_fold_seeds":failed,
        "alt_fivefold_programme_equal_delta_positive_seeds":int(sum(x>0 for x in a)),
        "alt_fivefold_programme_equal_delta_negative_seeds":int(sum(x<0 for x in a)),
        "alt_fivefold_programme_equal_delta_min":float(np.min(a)) if len(a) else None,
        "alt_fivefold_programme_equal_delta_median":float(np.median(a)) if len(a) else None,
        "alt_fivefold_programme_equal_delta_max":float(np.max(a)) if len(a) else None,
        "alt_fivefold_programme_equal_delta_p10_p90":[float(x) for x in np.percentile(a,[10,90])] if len(a) else None,
        "posthoc_fold_deltas_not_independent_replication":True,
        "no_feature_outcome_scale_or_ridge_tuning":True,
        "original_outcomes_or_individual_predictions_redistributed":False,
        "established_causal_or_effective_pollen_mechanism":False,
        "freeze":FREEZE,
        "decision":"PRESERVE_ORIGINAL_PRIMARY_NEGATIVE_WITH_POSTHOC_PREDICTIVE_QUALIFICATION",
    }
    return result

def self_test():
    x=[{"site_key":("x",str(i),"2025","crop"),
        "x_total_log":float(i%9),
        "x_syrphid_share":float((i*17)%11)/11,
        "y_log":1+0.03*i+float((i*17)%11)/11} for i in range(30)]
    assert len(fold_scores(x))==3
    assert folds_other(x[0]["site_key"],0)==folds_other(x[0]["site_key"],0)
    assert folds_other(x[0]["site_key"],0)!=folds_other(x[0]["site_key"],1) or (
        folds_other(x[1]["site_key"],0)!=folds_other(x[1]["site_key"],1))
    print("CROPPOL_POSTPRIMARY_FOLD_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        self_test();return 0
    if args.output is None:
        p.error("--output required")
    try:result=report()
    except Exception as e:
        result={"status":"SOURCE_OR_DIAGNOSTIC_STOP","reason":type(e).__name__+": "+str(e)[:300],
                "original_outcomes_or_individual_predictions_redistributed":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CROPPOL_POSTPRIMARY_QF_DIAGNOSTIC "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="POSTPRIMARY_CROPPOL_PREDICTION_DIAGNOSTIC_COMPLETED" else 1

if __name__=="__main__":
    raise SystemExit(main())
