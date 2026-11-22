#!/usr/bin/env python3
"""CP005 post-outcome source-heldout rank penalty and source jackknife audit.

NEVER changes CP004 source, scope, fixed original lambda or primary conclusion.
Original source rows and individual source identifiers never leave memory.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from http.client import HTTPException
import json
import math
from pathlib import Path
import random
from urllib.error import HTTPError

import audit_cp001_source_coverage as cp1
import audit_cp004_source_heldout_yield_ranks as cp4

PENALTIES=(0.01,0.10,1.00)
BOOT=4000
SEED=20261123
FROZEN_M0=.5239893283658781
FROZEN_M1=.4860390615733018

def ridge_lambda(grouped,heldout,two_feature,penalty):
    components=[s for s in grouped if s!=heldout and any(b["pairs"] for b in grouped[s])]
    p=2 if two_feature else 1
    if len(components)<7:raise ValueError("Insufficient source training components")
    xtx=[[0.0]*p for _ in range(p)]
    xty=[0.0]*p
    for s in components:
        blocks=[b for b in grouped[s] if b["pairs"]]
        for block in blocks:
            pair_w=1.0/(len(components)*len(blocks)*len(block["pairs"]))
            for (size,vis),truth in block["pairs"]:
                x=[size,vis][:p]
                for j in range(p):
                    xty[j]+=pair_w*x[j]*truth
                    for k in range(p):xtx[j][k]+=pair_w*x[j]*x[k]
    for j in range(p):xtx[j][j]+=penalty
    if p==1:return [xty[0]/xtx[0][0]]
    a,b=xtx[0]
    c,d=xtx[1]
    det=a*d-b*c
    if det<=1e-14:raise ValueError("Invalid regularized two-variable fit")
    return [(xty[0]*d-xty[1]*b)/det,(xty[1]*a-xty[0]*c)/det]

def score(blocks,penalty):
    grouped=defaultdict(list)
    for b in blocks:grouped[b["source_component"]].append(b)
    vals=[]
    for group in sorted(grouped):
        test=[b for b in grouped[group] if b["pairs"]]
        if not test:raise ValueError("Previously scored source has no true outcome rank")
        co0=ridge_lambda(grouped,group,False,penalty)
        co1=ridge_lambda(grouped,group,True,penalty)
        s0=sum(cp4.concordance(b["pairs"],co0) for b in test)/len(test)
        s1=sum(cp4.concordance(b["pairs"],co1) for b in test)/len(test)
        vals.append((s0,s1,s1-s0))
    return vals

def quantile(a,p):
    a=sorted(a)
    q=(len(a)-1)*p
    i=math.floor(q);j=math.ceil(q)
    return a[i]+(q-i)*(a[j]-a[i])

def aggregated(vals):
    n=len(vals)
    if n!=10:raise ValueError("Expected original 10 scored provisional source groups")
    mean0=sum(z[0] for z in vals)/n
    mean1=sum(z[1] for z in vals)/n
    delta=mean1-mean0
    randomizer=random.Random(SEED)
    bootstrap=[sum(vals[randomizer.randrange(n)][2] for _ in range(n))/n
               for _ in range(BOOT)]
    return {
       "score_M0":mean0,
       "score_M1":mean1,
       "source_equal_added_visitation_increment":delta,
       "bootstrap_95pct_internal_source_interval":[quantile(bootstrap,.025),quantile(bootstrap,.975)],
       "positive_source_components":sum(z[2]>1e-12 for z in vals),
       "negative_source_components":sum(z[2]<-1e-12 for z in vals),
       "zero_source_components":sum(abs(z[2])<=1e-12 for z in vals),
    }

def audit(raw):
    cp1.verify_bytes(raw,cp1.MANIFEST["expected_bytes"],cp1.MANIFEST["expected_git_blob_sha1"])
    blocks,source=cp4.source_blocks(raw)
    results={}
    raw_scores={}
    for penalty in PENALTIES:
        vals=score(blocks,penalty)
        results[str(penalty)]=aggregated(vals)
        raw_scores[penalty]=vals
    if abs(results["0.1"]["score_M0"]-FROZEN_M0)>1e-10 or abs(
         results["0.1"]["score_M1"]-FROZEN_M1)>1e-10:
        raise ValueError("Original CP004 lambda0.1 frozen score is not reproduced")
    ds=[z[2] for z in raw_scores[0.10]]
    remaining=[(sum(ds)-d)/9 for d in ds]
    neg_all=all(results[str(p)]["source_equal_added_visitation_increment"]<0 for p in PENALTIES)
    jack_neg=all(x<0 for x in remaining)
    return {
       "status":"POSTOUTCOME_REDUCED_BASELINE_RANK_SENSITIVITY_COMPLETE",
       "analysis_is_postoutcome_exploratory":True,
       "original_cp004_model_and_frozen_result_unchanged":True,
       "original_cp004_full_frozen_0p1_score_reproduced":True,
       "original_source_hash_verified_against_cp001":True,
       "frozen_source_eligibility":source,
       "all_fixed_penalty_results":results,
       "each_penalty_bootstrap_reuses_scored_sources":True,
       "n_jackknife_source_evaluation_deletions":10,
       "lambda_0p1_nine_source_jackknife_increment_min":min(remaining),
       "lambda_0p1_nine_source_jackknife_increment_max":max(remaining),
       "lambda_0p1_jackknife_negative_count":sum(x<0 for x in remaining),
       "penalty_sign_stable_negative":neg_all,
       "leave_evaluation_source_out_sign_stable_negative":jack_neg,
       "decision":("PENALTY_AND_JACKKNIFE_SIGN_STABLE_NEGATIVE" if neg_all and jack_neg
                   else "SIGN_DEPENDS_ON_PENALTY_OR_SOURCE"),
       "original_field_rows_study_names_sites_outcomes_and_visit_values_redistributed":False,
       "not_an_independent_ecological_replication":True,
       "full_context_causal_model_admitted":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    res={"status":"ORIGINAL_SOURCE_NOT_CHECKED",
         "original_field_rows_study_names_sites_outcomes_and_visit_values_redistributed":False}
    stage="access"
    try:
        raw=cp1.fetch_verified_source()
        stage="sensitivity"
        res=audit(raw)
        code=0
    except (OSError,HTTPException,ValueError,UnicodeError) as e:
        res.update(status="POSTOUTCOME_SOURCE_OR_PENALTY_AUDIT_STOP",
                   stop_type=type(e).__name__,stop_stage=stage)
        if isinstance(e,HTTPError):res["stop_http"]=e.code
        code=2
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CP005_POSTOUTCOME_ORIGINAL_SOURCE_SENSITIVITY "+json.dumps(
         {k:res.get(k) for k in ("status","decision","all_fixed_penalty_results",
          "lambda_0p1_nine_source_jackknife_increment_min",
          "lambda_0p1_nine_source_jackknife_increment_max",
          "lambda_0p1_jackknife_negative_count","penalty_sign_stable_negative",
          "leave_evaluation_source_out_sign_stable_negative","stop_type")},
         sort_keys=True),flush=True)
    return code

if __name__=="__main__":raise SystemExit(main())
