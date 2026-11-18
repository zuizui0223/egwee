#!/usr/bin/env python3
"""Apple AA001: source-locked open treatment P→F orchard-context region holdout.

Separate *post Q-P-F coverage failure* narrower estimand with pre-effect
freeze. Original 2023 sampled pollen and final fruits are NOT same flowers.
No original orchard/site/flower records redistributed.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import json
import math
from pathlib import Path

import numpy as np
import audit_AA001_source_grain as a

FREEZE="research/apple_orchard_qpf/AA001_PF_CONTEXT_PREDICTION_FREEZE_20261118.md"

def num(x):
    if not a.numeric_nonneg(x):return None
    return float(x)

def fnum(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (TypeError,ValueError):return None

def prepare():
    orig=a.rows_from_author_record()
    p=defaultdict(lambda:{"p":[],"temp":[]})
    f=defaultdict(lambda:{"s":0.0,"fail":0.0,"temp":[],"rows":0})
    counts=Counter()
    for z in orig["GerminatedPollen.txt"]:
        if a.norm(z["Treatment"])!="o" or not all(a.has(z[k]) for k in ("Region","Site","Plot")):
            continue
        pollen=num(z["Nbr_germinated_pollen"])
        temp=fnum(z["Temp"])
        if pollen is None or temp is None:
            counts["p_unusable_original_cell"]+=1;continue
        key=(a.norm(z["Region"]),a.norm(z["Site"]),a.norm(z["Plot"]))
        p[key]["p"].append(pollen)
        p[key]["temp"].append(temp)
    for z in orig["initial_final_fruitset.txt"]:
        if a.numeric_valid_year(z["Year"])!="2023" or a.norm(z["Treatment"])!="o":
            continue
        if not all(a.has(z[k]) for k in ("Region","Site","Plot")):
            continue
        su=num(z["Final_nb_fruit"])
        fa=num(z["Nb_Failure_Final"])
        temp=fnum(z["Temp"])
        if su is None or fa is None or su+fa<=0 or temp is None:
            counts["f_unusable_original_cell"]+=1;continue
        key=(a.norm(z["Region"]),a.norm(z["Site"]),a.norm(z["Plot"]))
        f[key]["s"]+=su
        f[key]["fail"]+=fa
        f[key]["temp"].append(temp)
        f[key]["rows"]+=1
    overlap=set(p)&set(f)
    counts["original_p_2023_open_plot_keys"]=len(p)
    counts["original_f_2023_open_plot_keys"]=len(f)
    counts["original_p_and_f_2023_open_plot_keys"]=len(overlap)
    orch=defaultdict(lambda:{"p":[],"s":0.0,"fail":0.0,"temp":[],"plots":0})
    for k in sorted(overlap):
        pv=p[k]
        fv=f[k]
        if not pv["p"] or not fv["temp"]:continue
        alltemps=pv["temp"]+fv["temp"]
        if max(alltemps)-min(alltemps)>1.0:
            raise ValueError("SOURCE_TEMP_HETEROGENEITY_ON_MATCHED_P_F_PLOT")
        dest=orch[k[:2]]
        dest["p"].extend(pv["p"])
        dest["s"]+=fv["s"]
        dest["fail"]+=fv["fail"]
        dest["temp"].extend(fv["temp"])
        dest["plots"]+=1
    cohorts=[]
    for key,z in sorted(orch.items()):
        if z["s"]+z["fail"]<=0 or not z["p"] or not z["temp"]:
            counts["incomplete_matched_orchard"]+=1
            continue
        if max(z["temp"])-min(z["temp"])>1.0:
            raise ValueError("SOURCE_TEMP_HETEROGENEITY_WITHIN_ORCHARD")
        cohorts.append({
            "orchard":key, "region":key[0], "n_plots":z["plots"],
            "n_p_original_styles":len(z["p"]),
            "n_f_original_denominator":z["s"]+z["fail"],
            "temp":sum(z["temp"])/len(z["temp"]),
            "pmean":sum(z["p"])/len(z["p"]),
            "y":math.log((z["s"]+0.5)/(z["fail"]+0.5))
        })
    byregion=defaultdict(list)
    for row in cohorts:byregion[row["region"]].append(row)
    counts["complete_orchards"]=len(cohorts)
    counts["original_regions_with_complete_orchards"]=len(byregion)
    counts["region_min_complete_orchards"]=min(map(len,byregion.values())) if byregion else 0
    counts["total_contributing_plot_keys"]=sum(x["n_plots"] for x in cohorts)
    counts["total_contributing_original_p_style_rows"]=sum(x["n_p_original_styles"] for x in cohorts)
    qualifies=(len(cohorts)>=12 and len(byregion)>=3 and
               min(map(len,byregion.values()),default=0)>=2)
    return cohorts,byregion,counts,qualifies

def ridge(x_train,y_train,x_test):
    means=np.mean(x_train,axis=0)
    std=np.std(x_train,axis=0)
    if np.any(std<1e-10):
        raise ValueError("ZERO_ORCHARD_TRAINING_FEATURE_VARIANCE")
    ym=float(np.mean(y_train))
    ys=float(np.std(y_train))
    if ys<1e-10:
        raise ValueError("ZERO_ORCHARD_TRAINING_TARGET_VARIANCE")
    a_train=np.column_stack([np.ones(len(x_train)),(x_train-means)/std])
    a_test=np.column_stack([np.ones(len(x_test)),(x_test-means)/std])
    reg=np.eye(a_train.shape[1])
    reg[0,0]=0
    beta=np.linalg.solve(a_train.T@a_train + reg,a_train.T@((y_train-ym)/ys))
    return a_test@beta,ym,ys

def run():
    cohorts,byregion,counts,qualifies=prepare()
    base={
       "source":"Riva et al. 2026, 10.5281/zenodo.19403906",
       "reference_freeze":FREEZE,
       "date_stage":"post_QPF_coverage_stop_2023_open_treatment_only",
       "original_source_record_SHA256s":{key:val[0] for key,val in a.EXPECTED.items()},
       "coverage":dict(counts),
       "third_same_flower_qpf_study_admitted":False,
       "visitation_Q_used":False,
       "P_and_F_measured_on_distinct_flower_samples":True,
       "origin_is_one_original_research_programme":True,
       "original_orchard_flower_pollen_fruit_rows_redistributed":False,
       "out_of_study_generalization_estimated":False,
    }
    if not qualifies:
        return {**base,"status":"PF_CONTEXT_COVERAGE_STOP",
                "effect_estimated":False,
                "decision":"NO_PF_CONTEXT_MODEL_OR_QPF_ADMISSION"}
    all_rows=sorted(cohorts,key=lambda r:r["orchard"])
    regions=sorted(byregion)
    x=np.array([[r["temp"],math.log1p(r["pmean"])] for r in all_rows],dtype=float)
    y=np.array([r["y"] for r in all_rows],dtype=float)
    folds=[]
    pred_errors=[]
    for f,region in enumerate(regions):
        tr=np.array([i for i,r in enumerate(all_rows) if r["region"]!=region],dtype=int)
        te=np.array([i for i,r in enumerate(all_rows) if r["region"]==region],dtype=int)
        if len(tr)<8 or len(te)<2:
            return {**base,"status":"PF_REGION_FOLD_COVERAGE_STOP",
                    "effect_estimated":False,"decision":"SOURCE_REGION_REPLICATION_TOO_SMALL"}
        try:
            b,mean,sd=ridge(x[tr,:1],y[tr],x[te,:1])
            full,mean1,sd1=ridge(x[tr,:2],y[tr],x[te,:2])
        except (np.linalg.LinAlgError,ValueError) as exc:
            return {**base,"status":"PF_CONTEXT_NONESTIMABLE_REGION_STOP",
                    "effect_estimated":False,"error_type":type(exc).__name__,
                    "decision":"DO_NOT_REPAIR_FOLD_AFTER_OUTCOMES"}
        if abs(mean-mean1)>1e-10 or abs(sd-sd1)>1e-10:
            raise ValueError("TRAINING_TARGET_SCALE_MISMATCH")
        target=(y[te]-mean)/sd
        sq0=(target-b)**2
        sq1=(target-full)**2
        folds.append({"held_out_original_region_index":f+1,
                      "n_original_orchards":len(te),
                      "M0_MSE":float(np.mean(sq0)),"M1_MSE":float(np.mean(sq1)),
                      "M0_minus_M1":float(np.mean(sq0-sq1))})
        pred_errors.extend(zip(sq0.tolist(),sq1.tolist()))
    avgm0=float(np.mean([a0 for a0,a1 in pred_errors]))
    avgm1=float(np.mean([a1 for a0,a1 in pred_errors]))
    pooled=avgm0-avgm1
    study_weighted=float(np.mean([f["M0_minus_M1"] for f in folds]))
    npositive=sum(z["M0_minus_M1"]>0 for z in folds)
    return {**base,"status":"PF_SOURCE_ONE_STUDY_REGION_HOLDOUT_COMPLETE",
        "effect_estimated":True,"one_study_support_scope":"orchard_context_only",
        "primary_orchard_equal_train_z_M0_MSE":avgm0,
        "primary_orchard_equal_train_z_M1_MSE":avgm1,
        "primary_M0_minus_M1_gain":pooled,
        "secondary_original_region_equal_M0_minus_M1_gain":study_weighted,
        "positive_region_folds":npositive,
        "total_original_regions":len(regions),
        "heldout_region_folds_anonymized":folds,
        "registered_bounded_positive_support":pooled>0 and npositive>=3,
        "decision":("ONE_STUDY_BOUNDED_POLLEN_CONTEXT_PREDICTIVE_INCREMENT" if pooled>0 and npositive>=3
                    else "NO_RESOLVED_INTERREGION_POLLEN_CONTEXT_INCREMENT"),
        "biological_claim_ceiling":"One study, distinct flowers measured for germination and fruit, no causal stage or wild-plant fragmentation mechanism"
    }

def synthetic():
    x=np.array([[1.0],[2.0],[3.0],[4.0]])
    y=np.array([0.0,1.0,2.0,3.0])
    p,mean,sd=ridge(x,y,x)
    assert len(p)==4 and math.isfinite(mean+sd)
    assert (math.log((0.0+0.5)/(0.0+0.5))==0)
    print("AA001_PF_REGION_MODEL_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:synthetic();return 0
    if a.output is None:p.error("--output required")
    try:r=run()
    except Exception as exc:
        r={"status":"SOURCE_OR_ESTIMAND_STOP","reason":type(exc).__name__+": "+str(exc)[:300],
           "effect_estimated":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
    print("AA001_PF_CONTEXT_HELDOUT "+json.dumps(r,sort_keys=True),flush=True)
    return 0 if r["status"] in ("PF_CONTEXT_COVERAGE_STOP","PF_REGION_FOLD_COVERAGE_STOP",
             "PF_CONTEXT_NONESTIMABLE_REGION_STOP","PF_SOURCE_ONE_STUDY_REGION_HOLDOUT_COMPLETE") else 1

if __name__=="__main__":
    raise SystemExit(main())
