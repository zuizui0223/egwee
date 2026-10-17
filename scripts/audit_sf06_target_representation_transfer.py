#!/usr/bin/env python3
"""Source-held-out target-by-representation transfer for paired SF06 effects.

Crucial: SAME 54 constituent-consensus fragmentation pairs (or SAME 31
source-disjoint pairs) are used for ALL four predictors and BOTH female
targets. Never conflate 55 continuous-eligible rows with 54 sign-consensus
rows or reinterpret point-sign targets as 95% resolved effects.

Post hoc external literature diagnostic in empirical EGWEE, not a new
meta-analytic effect, ecological mechanism, or theory-side EGWE result.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from check_sf06_publication_delete_predictive_influence import OVERLAP

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
PINNED_BLOB="80edf240425c0e4439a276176bc1996c651fab92"
RIDGE=1.0
MODELS={
    "context_only": (),
    "pollination_direction_only": ("xsign",),
    "continuous_pollination_effect": ("I",),
    "direction_plus_magnitude": ("xsign","I"),
}

def load()->tuple[list[dict],dict]:
    raw=SOURCE.read_bytes()
    sha=hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
    assert sha==PINNED_BLOB, (sha,PINNED_BLOB)
    source=list(csv.DictReader(raw.decode("utf-8").splitlines()))
    assert len(source)==59
    rows=[]
    for r in source:
        if r["land_use_factor_normalized"]!="habitat fragmentation":
            continue
        xs,ys=r["I_component_consensus_sign"],r["F_component_consensus_sign"]
        if xs not in {"lower","nonlower"} or ys not in {"lower","nonlower"}:
            continue
        assert r["numeric_model_eligible"]=="yes"
        I,F=float(r["d_I"]),float(r["d_F"])
        varF=float(r["var_F"])
        assert all(math.isfinite(z) for z in (I,F,varF)) and varF>0
        xsign=int(xs=="lower")
        ysign=int(ys=="lower")
        assert xsign==int(I<0) and ysign==int(F<0)
        rows.append({
            "pub":r["source_publication_key"],
            "species":r["species"],
            "I":I,"F":F,"xsign":xsign,"ysign":ysign,
            "varF":varF,
        })
    assert len(rows)==54 and len({r["pub"] for r in rows})==32
    disjoint=[r for r in rows if r["pub"] not in OVERLAP]
    assert len(disjoint)==31 and len({r["pub"] for r in disjoint})==23
    return rows,{
        "source_Git_blob":sha,
        "total_physical_paired_rows":len(source),
        "all_consensus_fragmentation_pairs":len(rows),
        "consensus_publications":len({r["pub"] for r in rows}),
        "source_disjoint_pairs":len(disjoint),
        "source_disjoint_publications":len({r["pub"] for r in disjoint}),
        "target_frames_numerically_identical_across_models":True,
        "consensus_both_endpoints_95pct_resolved_is_separate_question":True,
    }

def solve(mat:list[list[float]],rhs:list[float])->list[float]:
    n=len(rhs)
    a=[r[:] + [v] for r,v in zip(mat,rhs)]
    for j in range(n):
        pivot=max(range(j,n),key=lambda k:abs(a[k][j]))
        a[j],a[pivot]=a[pivot],a[j]
        scale=a[j][j]
        assert abs(scale)>1e-10, (n,j,a)
        for k in range(j,n+1):
            a[j][k]/=scale
        for i in range(n):
            if i==j:
                continue
            fac=a[i][j]
            for k in range(j,n+1):
                a[i][k]-=fac*a[j][k]
    return [a[i][n] for i in range(n)]

def fitting_features(train:list[dict],keys:tuple[str,...]):
    assert train
    n=len(train)
    means={k:sum(r[k] for r in train)/n for k in keys}
    scales={k:max(1e-8,math.sqrt(sum((r[k]-means[k])**2 for r in train)/n))
            for k in keys}
    def vec(r):
        return [1.0]+[(r[k]-means[k])/scales[k] for k in keys]
    return [vec(r) for r in train],vec

def predict_continuous(train:list[dict],test:list[dict],
                       features:tuple[str,...],penalty:float)->list[float]:
    assert penalty>0
    X,vec=fitting_features(train,features)
    n=len(X[0])
    y=[r["F"] for r in train]
    gram=[[sum(row[i]*row[j] for row in X)+
           (penalty if i==j and i>0 else 0.0)
           for j in range(n)] for i in range(n)]
    cross=[sum(x[i]*z for x,z in zip(X,y)) for i in range(n)]
    beta=solve(gram,cross)
    return [sum(v*b for v,b in zip(vec(r),beta)) for r in test]

def predict_lower_prob(train:list[dict],test:list[dict],
                       features:tuple[str,...],penalty:float)->list[float]:
    """Penalized logistic likelihood, unpenalized intercept, within-fold standardization."""
    assert penalty>0
    X,vec=fitting_features(train,features)
    n=len(X[0])
    y=[r["ysign"] for r in train]
    positive=sum(y)
    assert 0<positive<len(y)
    beta=[math.log((positive+0.5)/(len(y)-positive+0.5))]+[0.]*(n-1)
    def sig(z):
        if z>=0:
            return 1/(1+math.exp(-z))
        e=math.exp(z)
        return e/(1+e)
    for iteration in range(55):
        prob=[sig(sum(v*b for v,b in zip(row,beta))) for row in X]
        w=[max(1e-8,p*(1-p)) for p in prob]
        grad=[sum(row[i]*(z-p) for row,z,p in zip(X,y,prob))
              -(penalty*beta[i] if i>0 else 0.0) for i in range(n)]
        mat=[[sum(w[k]*row[i]*row[j] for k,row in enumerate(X))+
              (penalty if i==j and i>0 else 0.0)
              for j in range(n)] for i in range(n)]
        delta=solve(mat,grad)
        for i in range(n):
            beta[i]+=delta[i]
        if sum(x*x for x in delta)<1e-12:
            break
    return [min(1-1e-9,max(1e-9,sig(sum(v*b for v,b in zip(vec(r),beta)))))
            for r in test]

def held_publications(rows:list[dict],features:tuple[str,...],
                      target:str,penalty:float)->dict:
    groups=sorted({r["pub"] for r in rows})
    predictions=[]
    for pub in groups:
        train=[r for r in rows if r["pub"]!=pub]
        test=[r for r in rows if r["pub"]==pub]
        assert train and test
        if target=="female_d":
            preds=predict_continuous(train,test,features,penalty)
        else:
            assert target=="female_lower_consensus_point_sign"
            preds=predict_lower_prob(train,test,features,penalty)
        for r,pred in zip(test,preds):
            predictions.append({
                "pub":pub,"species":r["species"],
                "target":r["F"] if target=="female_d" else r["ysign"],
                "prediction":pred,
            })
    assert len(predictions)==len(rows)
    by_pub={}
    for pub in groups:
        pred=[r for r in predictions if r["pub"]==pub]
        sq=sum((r["target"]-r["prediction"])**2 for r in pred)/len(pred)
        err=sum(abs(r["target"]-r["prediction"]) for r in pred)/len(pred)
        by_pub[pub]={"n":len(pred),"MSE":sq,"MAE":err}
        if target!="female_d":
            by_pub[pub]["logloss"]=sum(
                - (r["target"]*math.log(r["prediction"]) +
                   (1-r["target"])*math.log1p(-r["prediction"]))
                for r in pred)/len(pred)
    n=len(predictions)
    ans={
        "n_pairs":n,
        "n_publications":len(groups),
        "MSE_equal_pairs":sum(v["MSE"]*v["n"] for v in by_pub.values())/n,
        "MAE_equal_pairs":sum(v["MAE"]*v["n"] for v in by_pub.values())/n,
        "MSE_equal_publications":sum(v["MSE"] for v in by_pub.values())/len(groups),
        "by_publication":by_pub,
    }
    if target!="female_d":
        ans["logloss_equal_pairs"]=sum(v["logloss"]*v["n"] for v in by_pub.values())/n
        ans["logloss_equal_publications"]=sum(v["logloss"] for v in by_pub.values())/len(groups)
    return ans

def compare(rows:list[dict],penalty:float)->dict:
    assert len(rows)>=20 and len({r["pub"] for r in rows})>=15
    outcome={}
    for target in ("female_d","female_lower_consensus_point_sign"):
        fits={k:held_publications(rows,v,target,penalty) for k,v in MODELS.items()}
        basis=fits["context_only"]
        magnitude=fits["continuous_pollination_effect"]
        direction=fits["pollination_direction_only"]
        both=fits["direction_plus_magnitude"]
        outcome[target]={
            "models":fits,
            "changes_equal_pair_MSE":{
                "direction_minus_baseline":direction["MSE_equal_pairs"]-basis["MSE_equal_pairs"],
                "magnitude_minus_baseline":magnitude["MSE_equal_pairs"]-basis["MSE_equal_pairs"],
                "magnitude_minus_direction":magnitude["MSE_equal_pairs"]-direction["MSE_equal_pairs"],
                "both_minus_magnitude":both["MSE_equal_pairs"]-magnitude["MSE_equal_pairs"],
            },
            "changes_equal_publication_MSE":{
                "direction_minus_baseline":direction["MSE_equal_publications"]-basis["MSE_equal_publications"],
                "magnitude_minus_baseline":magnitude["MSE_equal_publications"]-basis["MSE_equal_publications"],
                "magnitude_minus_direction":magnitude["MSE_equal_publications"]-direction["MSE_equal_publications"],
                "both_minus_magnitude":both["MSE_equal_publications"]-magnitude["MSE_equal_publications"],
            },
        }
    return outcome

def deleted_publication_frame(rows:list[dict],penalty:float)->dict:
    """Repeated re-fit on delete-one-source frames; these are NOT independent votes."""
    out={}
    for source in sorted({r["pub"] for r in rows}):
        reduced=[r for r in rows if r["pub"]!=source]
        # Repeated complete publication CV, none of deleted source enters fit/test.
        results=compare(reduced,penalty)
        out[source]={
            target:result["changes_equal_pair_MSE"]
            for target,result in results.items()
        }
    report={}
    for target in ("female_d","female_lower_consensus_point_sign"):
        vals=[v[target] for v in out.values()]
        report[target]={
            label:{
                "positive_delitions":sum(v[label]>0 for v in vals),
                "negative_delitions":sum(v[label]<0 for v in vals),
                "range":[min(v[label] for v in vals),max(v[label] for v in vals)],
            } for label in vals[0]
        }
    return {"n_source_deletions":len(out),
            "summary":report,
            "source_deleted_cases":out}

def main():
    source,meta=load()
    frames={
        "identical_consensus_54":source,
        "publication_disjoint_consensus_31":[r for r in source if r["pub"] not in OVERLAP],
    }
    results={}
    for frame,rows in frames.items():
        main=compare(rows,RIDGE)
        deletions=deleted_publication_frame(rows,RIDGE)
        results[frame]={
            "pairs":len(rows),"publications":len({r["pub"] for r in rows}),
            "female_point_sign_lower":sum(r["ysign"] for r in rows),
            "pollination_point_sign_lower":sum(r["xsign"] for r in rows),
            "ridge_penalty":RIDGE,
            "target_comparison":main,
            "source_deletion_diagnostics":deletions,
            "penalty_sensitivity":{
                str(p):{
                    target:result["changes_equal_pair_MSE"]
                    for target,result in compare(rows,p).items()
                } for p in (0.25,4.0)
            },
        }
    full=results["identical_consensus_54"]["target_comparison"]
    dis=results["publication_disjoint_consensus_31"]["target_comparison"]
    def near(value,expected):
        assert math.isclose(value,expected,rel_tol=1e-8,abs_tol=1e-8),(value,expected)
    # Frozen source and early results protect against accidental target swaps.
    near(full["female_d"]["models"]["context_only"]["MSE_equal_pairs"],
         0.46289504217909677)
    near(full["female_d"]["models"]["pollination_direction_only"]["MSE_equal_pairs"],
         0.4467340277018514)
    near(full["female_d"]["models"]["continuous_pollination_effect"]["MSE_equal_pairs"],
         0.4524951394608734)
    near(dis["female_d"]["models"]["pollination_direction_only"]["MSE_equal_pairs"],
         0.6576124830473895)
    near(dis["female_d"]["models"]["continuous_pollination_effect"]["MSE_equal_pairs"],
         0.6141034800468772)
    near(full["female_lower_consensus_point_sign"]["models"]["context_only"]["MSE_equal_pairs"],
         0.17673914129141965)
    near(dis["female_lower_consensus_point_sign"]["models"]["pollination_direction_only"]["MSE_equal_pairs"],
         0.1939486447975955)
    report={
        "status":"EXPLORATORY_MATCHED_TARGET_REPRESENTATION_TRANSFER_NOT_CAUSAL",
        "provenance":meta,"results":results,
        "inference_ceiling":[
            "All model targets and cases held exactly constant within each frame and target.",
            "The 54 sign-consensus pairs are distinct from the 55 continuous-numeric eligible pairs in other audits; do not compare their CV as if same case sets.",
            "The x binary class is sign of d_I in this frame; direction+magnitude is formally nested but adds flexible fitting variance.",
            "Female point sign is not 95%-resolved physiological lower reproductive success. The original source includes only three jointly 95%-resolved pairs.",
            "Continuous female standardized endpoints aggregate different reproductive functions and within-pair d_I/d_F covariance is unavailable.",
            "Whole-publication holdouts prevent same-source fitting leakage, but 32/23 publications are selected literature, not randomized independent habitat treatments.",
            "Publication deletion folds are overlapping diagnostics, not 32 independent replication tests.",
            "Penalties 0.25, 1, 4 and the two targets were inspected after seeing existing outcomes. Model selection is not preregistered.",
            "A shift in loss ranking across source inclusion and target choice is not proof of an ecological regime switch or universal nonlinear biology.",
            "MSE of continuous effects and Brier of sign are different losses; never directly compare their numeric magnitudes.",
            "This remains an external published-S1 reanalysis in empirical egwee, separate from theoretical egwe. No frozen EGWEE study or effect denominator is changed.",
        ]
    }
    folder=ROOT/"build"
    folder.mkdir(exist_ok=True,parents=True)
    (folder/"sf06_target_representation_transfer_v1.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("SF06_MATCHED_TARGET_REPRESENTATION_TRANSFER: PASS")
    print(json.dumps({
        "source":meta,
        "comparison":{
            frame:{
                target:{
                    name:{
                        "MSE_equal_pairs":v["MSE_equal_pairs"],
                        "MSE_equal_publications":v["MSE_equal_publications"],
                        **({"logloss_equal_pairs":v["logloss_equal_pairs"]}
                           if target!="female_d" else {})
                    } for name,v in data["target_comparison"][target]["models"].items()
                } for target in ("female_d","female_lower_consensus_point_sign")
            } for frame,data in results.items()
        },
        "source_delete":{
            frame:{target:del_data["summary"][target]
                   for target in ("female_d","female_lower_consensus_point_sign")}
            for frame,del_data in (
                (f,data["source_deletion_diagnostics"]) for f,data in results.items()
            )
        },
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
