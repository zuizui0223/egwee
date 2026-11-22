#!/usr/bin/env python3
"""CP004 frozen source-heldout within-block CropPol yield-ranking benchmark.

M0 uses only known field-size ranks; M1 adds observed visit-rate ranks.
Source-blocked leave-one-source-out and pairwise rank concordance only.
A source component is a provisional group, NOT certified independent ecology.
All original field/yield/visitor/site values remain in memory and are not
serialized, printed, embedded into generated results, or distributed.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from decimal import Decimal
import hashlib
from http.client import HTTPException
import json
import math
from pathlib import Path
import random
from urllib.error import HTTPError

import audit_cp001_source_coverage as cp001
import audit_cp002_measurement_sources as cp002
import audit_cp003_sampling_effort as cp003

N_EXPECTED=(201,12,10)
LAMBDA=0.10
BOOT=4000
SEED=20261122
MIN_SCOREABLE=8

def midranks(values):
    n=len(values)
    if n<2:raise ValueError("Ranking requires multiple fields")
    ids=sorted(range(n),key=lambda i:values[i])
    result=[0.0]*n
    i=0
    while i<n:
        j=i+1
        while j<n and values[ids[j]]==values[ids[i]]:j+=1
        avg=(i+1+j)/2  # 1-based ranks i+1 .. j; average (i+j+1)/2
        rank=(avg-(n+1)/2)/(n-1)
        for k in range(i,j):result[ids[k]]=rank
        i=j
    return result

def source_blocks(field_raw,expected=N_EXPECTED):
    frames,fullkey=cp003.field_frames(field_raw)
    candidate=frames["strict_direct_timed_visit"]
    groups=defaultdict(list)
    for key,r in candidate:
        size=cp002.number(r["field_size"])
        if size is None or size<=0:continue
        bk=cp002.block_key(r)
        if bk is None:raise ValueError("Frozen source block metadata missing")
        groups[bk].append({"raw":r,"size":size,
                           "visit":cp002.number(r["visitation_rate"]),
                           "outcome":cp002.number(r["yield"]),
                           "key":(r["study_id"],r["site_id"],r["sampling_year"])})
    selected=[]
    all_complete=sum(len(v) for v in groups.values())
    for bk,items in groups.items():
        keys=[r["key"] for r in items]
        if len(set(keys))!=len(keys):raise ValueError("Duplicate field candidates in original comparison block")
        if len(items)<5 or len({r["size"] for r in items})<2:continue
        if any(x["visit"] is None or x["visit"]<0 or x["outcome"] is None or x["outcome"]<0 for x in items):
            raise ValueError("CP002 strict source output/visit validity drift")
        sr=midranks([x["size"] for x in items])
        vr=midranks([x["visit"] for x in items])
        pairs=[]
        ties=0
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                dy=items[i]["outcome"]-items[j]["outcome"]
                if dy==0:ties+=1;continue
                pairs.append(((sr[i]-sr[j],vr[i]-vr[j]), 1 if dy>0 else -1))
        selected.append({
          "source_component":bk[0],
          "comparison_key":bk,
          "n_fields":len(items),
          "n_nontied_outcome_pairs":len(pairs),
          "n_tied_outcome_pairs":ties,
          "visit_predictor_varies":len({x["visit"] for x in items})>1,
          "pairs":pairs,
        })
    comps={x["source_component"] for x in selected}
    actual=(sum(x["n_fields"] for x in selected),len(selected),len(comps))
    if actual!=expected:
        raise ValueError("CP002 frozen field-size block eligibility changed")
    return selected,{
      "original_strict_source_field_rows":len(candidate),
      "field_size_complete_rows_before_5row_and_variation_gate":all_complete,
      "source_field_size_selection_rows":actual[0],
      "source_comparison_blocks":actual[1],
      "provisional_source_components":actual[2],
      "visit_varying_blocks":sum(x["visit_predictor_varies"] for x in selected),
      "visit_constant_blocks_retained":sum(not x["visit_predictor_varies"] for x in selected),
      "outcome_nontied_field_pairs":sum(x["n_nontied_outcome_pairs"] for x in selected),
      "outcome_tied_pairs_excluded_from_pairwise_scores":sum(x["n_tied_outcome_pairs"] for x in selected),
      "source_study_field_ids_or_yield_values_exported":False,
    }

def ridge(pairs_by_source, heldout, use_visit):
    # Pairwise rank differences; within source equal component weight,
    # within original source each nondegenerate block equal,
    # within block each non-yield-tied unordered pair equal.
    comps=[s for s in pairs_by_source if s!=heldout and any(b["pairs"] for b in pairs_by_source[s])]
    if len(comps)<MIN_SCOREABLE-1:
        raise ValueError("Insufficient other original source components for ridge")
    p=2 if use_visit else 1
    xtx=[[0.0]*p for _ in range(p)]
    xty=[0.0]*p
    for s in comps:
        blocks=[b for b in pairs_by_source[s] if b["pairs"]]
        for b in blocks:
            w=1/(len(comps)*len(blocks)*len(b["pairs"]))
            for (xs, xv),truth in b["pairs"]:
                x=[xs,xv][:p]
                for j in range(p):
                    xty[j]+=w*x[j]*truth
                    for k in range(p):
                        xtx[j][k]+=w*x[j]*x[k]
    for j in range(p):xtx[j][j]+=LAMBDA
    if p==1:return [xty[0]/xtx[0][0]]
    a,b=xtx[0]
    c,d=xtx[1]
    determinant=a*d-b*c
    if determinant<=1e-14:raise ValueError("Regularized source paired covariance singular")
    return [(xty[0]*d-xty[1]*b)/determinant,
            (xty[1]*a-xty[0]*c)/determinant]

def concordance(pairs,beta):
    if not pairs:return None
    total=0.0
    for (x0,x1),truth in pairs:
        score=beta[0]*x0+(beta[1]*x1 if len(beta)==2 else 0.0)
        margin=score*truth
        total+=(1 if margin>1e-14 else 0.5 if abs(margin)<=1e-14 else 0)
    return total/len(pairs)

def quantile(sorted_arr,p):
    k=(len(sorted_arr)-1)*p
    lo=math.floor(k);hi=math.ceil(k)
    return sorted_arr[lo]+(k-lo)*(sorted_arr[hi]-sorted_arr[lo])

def evaluate(blocks):
    original=defaultdict(list)
    for b in blocks:original[b["source_component"]].append(b)
    source_keys=sorted(original)
    scoreable=sum(any(b["pairs"] for b in original[s]) for s in source_keys)
    if scoreable<MIN_SCOREABLE:
        return {"status":"SOURCE_HELDOUT_RANK_COVERAGE_STOP",
                "effect_estimated":False,
                "source_components_all":len(source_keys),
                "source_components_scored":scoreable,
                "source_components_unscorable_due_to_output_ties":len(source_keys)-scoreable,
                "decision":"STOP_FEWER_THAN_EIGHT_SCOREABLE_SOURCE_COMPONENTS"}
    score_rows=[]
    skipped=0
    train_visit_positive=0
    for s in source_keys:
        test=[x for x in original[s] if x["pairs"]]
        if not test:
            skipped+=1
            continue
        m0=ridge(original,s,False)
        m1=ridge(original,s,True)
        train_visit_positive+=m1[1]>0
        test_m0=sum(concordance(b["pairs"],m0) for b in test)/len(test)
        test_m1=sum(concordance(b["pairs"],m1) for b in test)/len(test)
        score_rows.append((test_m0,test_m1,test_m1-test_m0))
    if len(score_rows)<MIN_SCOREABLE:
        return {"status":"SOURCE_HELDOUT_RANK_COVERAGE_STOP",
                "effect_estimated":False,
                "source_components_all":len(source_keys),
                "source_components_scored":len(score_rows),
                "source_components_unscorable_due_to_output_ties":skipped,
                "decision":"STOP_FEWER_THAN_EIGHT_SCOREABLE_SOURCE_COMPONENTS"}
    n=len(score_rows)
    mean0=sum(r[0] for r in score_rows)/n
    mean1=sum(r[1] for r in score_rows)/n
    d=mean1-mean0
    rng=random.Random(SEED)
    bs=sorted(sum(score_rows[rng.randrange(n)][2] for _ in range(n))/n for _ in range(BOOT))
    lo,hi=quantile(bs,.025),quantile(bs,.975)
    wins=sum(r[2]>1e-12 for r in score_rows)
    losses=sum(r[2]<-1e-12 for r in score_rows)
    zeros=n-wins-losses
    supported=d>0 and lo>0 and wins/n>=.70
    return {
       "status":"SOURCE_HELDOUT_REDUCED_BASELINE_RANK_TEST_COMPLETE",
       "effect_estimated":True,
       "score":"within_homogeneous_block_pairwise_yield_order_concordance",
       "source_components_all":len(source_keys),
       "source_components_scored":n,
       "source_components_unscorable_due_to_output_ties":skipped,
       "source_equal_M0_field_size_only_concordance":mean0,
       "source_equal_M1_field_size_plus_total_visits_concordance":mean1,
       "source_equal_increment_M1_minus_M0":d,
       "source_equal_increment_bootstrap_CI95":[lo,hi],
       "whole_provisional_source_component_bootstrap_draws":BOOT,
       "source_groups_with_positive_increment":wins,
       "source_groups_with_negative_increment":losses,
       "source_groups_with_zero_increment":zeros,
       "source_holdout_folds_trained_visit_weight_positive":train_visit_positive,
       "predeclared_reduced_baseline_rule_pass":supported,
       "decision":("ONE_SOURCE_COHORT_REDUCED_BASELINE_RANK_INCREMENT_BOUNDED_PASS" if supported
          else "NO_RESOLVED_REDUCED_BASELINE_TRANSFER_GAIN")
    }

def audit(raw):
    digest=cp001.verify_bytes(raw,cp001.MANIFEST["expected_bytes"],cp001.MANIFEST["expected_git_blob_sha1"])
    blocks,summary=source_blocks(raw)
    result=evaluate(blocks)
    return {
       "source": "CropPol author v2.1.0 pinned field data",
       "source_original_commit":cp001.MANIFEST["commit"],
       "source_original_sha256":digest,
       "source_eligibility_fingerprint":summary,
       **result,
       "analysis_is_post_CP002_metadata_exploratory":True,
       "not_direct_causal_pollinator_effect":True,
       "direct_pollen_visitation_yield_endpoint_construction_independently_verified":False,
       "baseline_context":"field_size_hectares_only_management_density_soil_climate_not_adjusted",
       "model_M0":"source_equal_ridge_rank_field_size",
       "model_M1":"source_equal_ridge_rank_field_size_plus_total_visits",
       "fixed_ridge_lambda":LAMBDA,
       "within_block_rank_transform_uses_only_predictor_data":True,
       "heldout_response_moments_or_rank_transforms_used_in_training":False,
       "original_source_group_independence_confirmed":False,
       "original_source_rows_sites_locations_study_labels_or_numeric_phenotypes_redistributed":False,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    out={"status":"ORIGINAL_SOURCE_NOT_VERIFIED","effect_estimated":False,
         "original_source_rows_sites_locations_study_labels_or_numeric_phenotypes_redistributed":False}
    stage="access"
    try:
        raw=cp001.fetch_verified_source()
        stage="eligibility"
        out=audit(raw)
        code=0
    except (OSError,HTTPException,ValueError,UnicodeError) as exc:
        out.update(status="ORIGINAL_SOURCE_OR_RANK_MODEL_STOP",effect_estimated=False,
                   source_stop_stage=stage,source_stop_type=type(exc).__name__)
        if isinstance(exc,HTTPError):out["source_stop_http"]=exc.code
        code=2
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    brief={k:out.get(k) for k in ("status","decision","source_eligibility_fingerprint",
      "source_components_scored","source_equal_M0_field_size_only_concordance",
      "source_equal_M1_field_size_plus_total_visits_concordance",
      "source_equal_increment_M1_minus_M0","source_equal_increment_bootstrap_CI95",
      "source_groups_with_positive_increment","source_groups_with_negative_increment",
      "source_groups_with_zero_increment","source_holdout_folds_trained_visit_weight_positive",
      "predeclared_reduced_baseline_rule_pass","source_stop_type")}
    print("CP004_ORIGINAL_SOURCE_HELDOUT_RANK_RESULTS "+json.dumps(brief,sort_keys=True),flush=True)
    return code

if __name__=="__main__":raise SystemExit(main())
