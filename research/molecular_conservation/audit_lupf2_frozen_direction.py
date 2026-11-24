#!/usr/bin/env python3
"""POSTHOC descriptive direction of the EXACT five frozen LUPF2 ridge models.

Never optimize or add new models; reproduce every archived fold's MSE before
allowing coefficient signs to be published. No individual source rows exported.
"""
from __future__ import annotations
import hashlib
import json
import math
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError,URLError
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import run_lupf1_genotype_holdout as base
import run_lupf2_exploratory_continuous_seed as exp

LOCK = "d9e2f7aa9c8179158d49b55637aa18e4ca178f4a"
SOURCE_SHA = "7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734"
EXPECTED_FOLDS = [
  (503,20,1.2738646610165942,0.9428773378613668),
  (244,11,0.7455840268640365,0.579755289221744),
  (244,11,1.2377124215434983,0.9621466437273917),
  (482,20,1.118446947666473,0.9244935322529652),
  (535,22,1.1493878650271332,0.8452670423579371),
]
EXPECTED_POOLED = (1.134806869754752,0.8706748619478497)
TOL=1e-8

def frozen_fit(train, add_onset):
    mu = sum(x[3] for x in train)/len(train)
    sd = math.sqrt(sum((x[3]-mu)**2 for x in train)/len(train))
    if not math.isfinite(sd) or sd < 1e-12:
        sd = 1.0
    X=[base.features(row,add_onset,mu,sd) for row in train]
    p=len(X[0]); A=[[0.0]*p for _ in range(p)]; b=[0.0]*p
    for x,row in zip(X,train):
        y=math.log1p(row[4])
        for i in range(p):
            b[i]+=x[i]*y
            for j in range(p):
                A[i][j]+=x[i]*x[j]
    for i in range(1,p):
        A[i][i]+=1.0
    beta=base.solve(A,b)
    return beta,mu,sd

def predict(test,model,add_onset):
    beta,mu,sd=model
    return [sum(v*w for v,w in zip(base.features(r,add_onset,mu,sd),beta)) for r in test]

def audit_frozen_predictions(records):
    if len(records)!=2008 or len({r[2] for r in records})!=84:
        raise base.SourceStop("ORIGINAL_GROUP_OR_CASE_COUNT_CHANGED")
    signed=[]; pooled_num0=0.; pooled_num1=0.
    seen_keys=set()
    for fold, (expected_n,expected_g,expected_m0,expected_m1) in enumerate(EXPECTED_FOLDS):
        train=[r for r in records if base.fold_of(r[2])!=fold]
        test=[r for r in records if base.fold_of(r[2])==fold]
        test_groups={r[2] for r in test}
        if len(test)!=expected_n or len(test_groups)!=expected_g:
            raise base.SourceStop("FOLD_MEMBERSHIP_MISMATCH")
        if seen_keys & test_groups:
            raise base.SourceStop("FOLD_LEAKAGE")
        seen_keys.update(test_groups)
        model0=frozen_fit(train,False)
        model1=frozen_fit(train,True)
        p0,p1=predict(test,model0,False),predict(test,model1,True)
        error0=sum((math.log1p(r[4])-q)**2 for r,q in zip(test,p0))
        error1=sum((math.log1p(r[4])-q)**2 for r,q in zip(test,p1))
        m0=error0/len(test);m1=error1/len(test)
        if abs(m0-expected_m0)>TOL or abs(m1-expected_m1)>TOL:
            raise base.SourceStop("FROZEN_MSE_NOT_REPRODUCED")
        # Compare to original fit_predict, independently exercising the existing
        # prediction implementation in addition to archived source-fold scores.
        original=base.fit_predict(train,test,True)
        if max(abs(x-y) for x,y in zip(p1,original))>TOL:
            raise base.SourceStop("ORIGINAL_MODEL_REPRODUCTION_FAILED")
        beta=model1[0][-1];sd=model1[2]
        signed.append({
            "fold":fold, "n_heldout":len(test),
            "n_heldout_label_groups":len(test_groups),
            "training_onset_sd_source_units":sd,
            "ridge_onset_coefficient_standardized":beta,
            "ridge_onset_coefficient_per_source_unit":beta/sd,
            "reproduced_M1_MSE":m1
        })
        pooled_num0+=error0;pooled_num1+=error1
    if len(seen_keys)!=84:
        raise base.SourceStop("GROUP_PARTITION_INCOMPLETE")
    pooled=(pooled_num0/len(records),pooled_num1/len(records))
    if any(abs(x-y)>TOL for x,y in zip(pooled,EXPECTED_POOLED)):
        raise base.SourceStop("POOLED_FROZEN_MSE_MISMATCH")
    coefs=[x["ridge_onset_coefficient_per_source_unit"] for x in signed]
    if all(x<0 for x in coefs):
        direction="EARLIER_ONSET_ASSOCIATED_WITH_HIGHER_SOURCE_REPRODUCTIVE_INDEX"
    elif all(x>0 for x in coefs):
        direction="LATER_ONSET_ASSOCIATED_WITH_HIGHER_SOURCE_REPRODUCTIVE_INDEX"
    else:
        direction="FOLD_SLOPE_SIGN_NOT_STABLE"
    return {
        "status":"LUPF2_POSTHOC_FROZEN_DIRECTION_REPRODUCED",
        "data_scope":"same 2026 source complete cases; exploratory T to W proxy",
        "previous_lupf2_result_unchanged":True,
        "original_lupf1_status":"SOURCE_ENDPOINT_INVALID_STOP",
        "no_new_predictive_model_or_parameter_tuning":True,
        "new_confirmatory_p_value_computed":False,
        "intervention_codebook_verified":False,
        "snp_genotypes_read":False,
        "same_mother_pollen_or_recruitment_measured":False,
        "genetic_rescue_claim":False,
        "natural_GxIxF_model_transfer_claim":False,
        "original_individual_values_redistributed":False,
        "n_complete_cases":len(records), "n_label_groups":len(seen_keys),
        "matched_original_mse":True,
        "reproduced_pooled_M0_MSE":pooled[0],
        "reproduced_pooled_M1_MSE":pooled[1],
        "folds":signed,
        "descriptive_direction":direction,
        "source_onset_units_verified_in_this_audit":False,
        "interpretation":"Signed coefficient after source population and unmapped line category adjustment; may reflect selection, resources, season length and missingness, not causal floral timing advantage."
    }

def source_records():
    metadata=json.loads(base.download(f"https://api.figshare.com/v2/articles/{base.ARTICLE}").decode("utf8"))
    doi=str(metadata.get("doi","")).lower().removeprefix("https://doi.org/")
    if doi!="10.6084/m9.figshare.29606180" and not doi.startswith("10.6084/m9.figshare.29606180.v"):
        raise base.SourceStop("SOURCE_DOI_CHANGED")
    f=[r for r in metadata.get("files",[]) if r.get("name")==base.NAME]
    if len(f)!=1:
        raise base.SourceStop("SOURCE_FILE_NOT_UNIQUE")
    url=f[0].get("download_url","")
    if urlparse(url).scheme!="https" or urlparse(url).hostname not in {
       "api.figshare.com","ndownloader.figshare.com","figshare.com"}:
        raise base.SourceStop("SOURCE_HOST_NOT_ALLOWED")
    raw=base.download(url)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
        raise base.SourceStop("ORIGINAL_FILE_SHA_CHANGED")
    rows=base.decode_source_sheet(raw)
    records,miss,flags,ngroups=exp.source_prepare(rows)
    if miss["missing_seed_index"]!=990 or flags["fractional_nonnegative_seed_index"]!=153:
        raise base.SourceStop("SOURCE_MISSINGNESS_COUNTS_CHANGED")
    return records

def main():
    from argparse import ArgumentParser
    a=ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    try:
        base.freeze_gate()
        exp.freeze_gate()
        subprocess.run(["git","merge-base","--is-ancestor",LOCK,"HEAD"],
                       cwd=base.ROOT,check=True,stdout=subprocess.DEVNULL)
        result=audit_frozen_predictions(source_records())
        result["protocol_sha"]=LOCK
        result["original_source_sha256"]=SOURCE_SHA
    except (base.SourceStop,HTTPError,URLError,ValueError,KeyError,TypeError,IndexError,
            subprocess.CalledProcessError) as exc:
        result={
            "status":"LUPF2_POSTHOC_DIRECTION_STOP",
            "reason_type":type(exc).__name__,
            "reason":str(exc)[:140] if isinstance(exc,base.SourceStop) else type(exc).__name__,
            "protocol_sha":LOCK,
            "original_lupf1_status":"SOURCE_ENDPOINT_INVALID_STOP",
            "new_confirmatory_p_value_computed":False,
            "no_new_predictive_model_or_parameter_tuning":True,
            "original_individual_values_redistributed":False,
        }
        if isinstance(exc,HTTPError):
            result["http_status"]=exc.code
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
