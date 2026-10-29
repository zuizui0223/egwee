#!/usr/bin/env python3
"""Audit ecological moderator transfer on exactly matched SF06 source units.

Can classical breeding-system/pollinator-guild labels improve held-publication
female-fitness effect prediction beyond continuous pollination effect size?

Post hoc source-sensitive predictive check, not an independent cohort, causal
analysis, significance test, or change to frozen EGWEE corpus.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from check_sf06_publication_delete_predictive_influence import OVERLAP

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
GIT_BLOB = "80edf240425c0e4439a276176bc1996c651fab92"
MODELS = {
    "context_only": (),
    "breeding_SC": ("SC",),
    "pollination_dI": ("I",),
    "dI_plus_SC": ("I", "SC"),
    "dI_SC_interaction": ("I", "SC", "IxSC"),
    "dI_plus_vertebrate": ("I", "vertebrate"),
    "dI_plus_specialist": ("I", "specialist"),
    "dI_SC_vertebrate": ("I", "SC", "vertebrate"),
    "dI_SC_specialist": ("I", "SC", "specialist"),
}
RIDGE = 1.0


def load() -> tuple[list[dict], dict]:
    raw=CSV.read_bytes()
    blob=hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
    assert blob == GIT_BLOB, (blob, GIT_BLOB)
    with CSV.open(encoding="utf-8",newline="") as fh:
        data=list(csv.DictReader(fh))
    assert len(data)==59
    frag=[r for r in data if r["land_use_factor_normalized"]=="habitat fragmentation"
          and r["I_component_consensus_sign"] in {"lower","nonlower"}
          and r["F_component_consensus_sign"] in {"lower","nonlower"}]
    assert len(frag)==54
    assert len({r["source_publication_key"] for r in frag})==32
    # Fair comparison denominator: every model uses the identical known
    # breeding-system records, including context-only and dI-only baselines.
    # The continuous-effect analysis includes ONE extra positive-numeric
    # row with mixed constituent sign, which is excluded from the 54-pair
    # qualitative sign-consensus analysis. These denominators MUST NOT be
    # conflated. Retain it only for d_I -> d_F quantitative prediction.
    numeric=[r for r in data if r["land_use_factor_normalized"]=="habitat fragmentation"
             and r["numeric_model_eligible"]=="yes"]
    assert len(numeric)==55
    assert len([r for r in numeric if r not in frag])==1
    known=[r for r in numeric if r["compatibility"] in {"SI","SC"}]
    assert len(known)==49
    rows=[]
    for r in known:
        i,f=float(r["d_I"]),float(r["d_F"])
        assert math.isfinite(i) and math.isfinite(f)
        v=int(r["compatibility"]=="SC")
        typ=r["pollination_context"].lower()
        assert "invertebrate" in typ or "vertebrate" in typ
        assert "generalist" in typ or "specialist" in typ
        rows.append({
            "pub":r["source_publication_key"], "species":r["species"],
            "I":i,"F":f,"SC":v, "IxSC":i*v,
            "vertebrate":int("vertebrate" in typ and "invertebrate" not in typ),
            "specialist":int("specialist" in typ),
            "varF":float(r["var_F"]),
        })
    assert len({r["pub"] for r in rows})==27
    dis=[r for r in rows if r["pub"] not in OVERLAP]
    assert len(dis)==26 and len({r["pub"] for r in dis})==18
    return rows, {
        "sha_git_blob":blob,
        "physical_paired_rows":len(data),
        "fragmentation_consensus_pairs":len(frag),
        "fragmentation_numeric_d_effect_pairs":len(numeric),
        "numeric_pairs_excluded_from_sign_consensus":len(numeric)-len(frag),
        "fragmentation_numeric_known_breeding_system_pairs":len(rows),
        "fragmentation_known_breeding_system_publications":27,
        "disjoint_known_breeding_system_pairs":len(dis),
        "disjoint_known_breeding_system_publications":18,
        "n_SI":sum(r["SC"]==0 for r in rows),
        "n_SC":sum(r["SC"]==1 for r in rows),
        "model_comparison_uses_the_exact_same_rows":True,
    }


def solve(mat: list[list[float]], rhs: list[float]) -> list[float]:
    n=len(rhs)
    a=[row[:] + [rhs[i]] for i,row in enumerate(mat)]
    for j in range(n):
        piv=max(range(j,n), key=lambda i:abs(a[i][j]))
        a[piv],a[j]=a[j],a[piv]
        assert abs(a[j][j])>1e-11, (n,j,a)
        scale=a[j][j]
        for k in range(j,n+1):
            a[j][k]/=scale
        for i in range(n):
            if i==j:
                continue
            z=a[i][j]
            for k in range(j,n+1):
                a[i][k]-=z*a[j][k]
    return [a[i][-1] for i in range(n)]


def predict(train: list[dict],test: list[dict], features: tuple[str,...],
            weight_publications: bool,penalty: float,
            variance_floor: float | None = None) -> list[float]:
    assert train and test and penalty>0
    counts=Counter(r["pub"] for r in train)
    weights=[1.0/counts[r["pub"]] if weight_publications else 1.0 for r in train]
    if variance_floor is not None:
        assert variance_floor >= 0
        assert all(r["varF"]>0 for r in train)
        weights=[w/(r["varF"]+variance_floor) for w,r in zip(weights,train)]
    nw=sum(weights)
    means={}
    sds={}
    for key in features:
        means[key]=sum(w*r[key] for w,r in zip(weights,train))/nw
        sds[key]=max(1e-8,math.sqrt(
            sum(w*(r[key]-means[key])**2 for w,r in zip(weights,train))/nw))
    def vec(row:dict)->list[float]:
        return [1.0]+[(row[key]-means[key])/sds[key] for key in features]
    x=[vec(row) for row in train]
    n=len(features)+1
    mat=[[sum(w*z[i]*z[j] for w,z in zip(weights,x))
          + (penalty*nw/len(train) if i==j and i>0 else 0.0)
          for j in range(n)] for i in range(n)]
    rhs=[sum(w*xx[i]*r["F"] for w,xx,r in zip(weights,x,train))
         for i in range(n)]
    beta=solve(mat,rhs)
    return [sum(a*b for a,b in zip(vec(r),beta)) for r in test]


def held_group(rows:list[dict],features:tuple[str,...],by:str,
               balance_training_pub:bool,penalty:float,
               variance_floor:float|None=None)->dict:
    groups=sorted({r[by] for r in rows})
    out=[]
    for group in groups:
        train=[r for r in rows if r[by]!=group]
        test=[r for r in rows if r[by]==group]
        assert train and test
        preds=predict(train,test,features,balance_training_pub,penalty,variance_floor)
        losses=[(r["F"]-yh)**2 for r,yh in zip(test,preds)]
        out.append({"key":group,"n":len(test),
                    "sum_squared_error":sum(losses),
                    "mse":sum(losses)/len(test)})
    return {
        "n":len(rows),"held_groups":len(groups),
        "mse_row_weighted":sum(x["sum_squared_error"] for x in out)/len(rows),
        "mse_equal_held_group":sum(x["mse"] for x in out)/len(groups),
        "by_group":{x["key"]:x["mse"] for x in out},
    }


def compare(rows:list[dict],training_weight:str, penalty:float,
            evaluate_species:bool=False)->dict:
    balance=training_weight=="equal_publication"
    data={name:held_group(rows,features,"pub",balance,penalty)
          for name,features in MODELS.items()}
    metrics={}
    for name,x in data.items():
        metrics[name]={
            "mse_held_publication_row_weighted":x["mse_row_weighted"],
            "mse_held_publication_equal_publication":x["mse_equal_held_group"],
        }
    baseline=data["context_only"]
    sc=data["breeding_SC"]
    I=data["pollination_dI"]
    both=data["dI_plus_SC"]
    sources=sorted(baseline["by_group"])
    metrics["pairwise_checks"]={
        "dI_gain_vs_context_row_MSE":baseline["mse_row_weighted"]-I["mse_row_weighted"],
        "dI_gain_vs_context_equalpub_MSE":baseline["mse_equal_held_group"]-I["mse_equal_held_group"],
        "SC_gain_vs_context_row_MSE":baseline["mse_row_weighted"]-sc["mse_row_weighted"],
        "SC_gain_vs_context_equalpub_MSE":baseline["mse_equal_held_group"]-sc["mse_equal_held_group"],
        "SC_increment_over_dI_row_MSE":I["mse_row_weighted"]-both["mse_row_weighted"],
        "SC_increment_over_dI_equalpub_MSE":I["mse_equal_held_group"]-both["mse_equal_held_group"],
        "n_pubs_SC_improves_over_dI":sum(both["by_group"][p]<I["by_group"][p]
                                        for p in sources),
        "n_pubs_dI_improves_over_context":sum(I["by_group"][p]<baseline["by_group"][p]
                                             for p in sources),
    }
    if evaluate_species:
        metrics["held_species"]={
            name:{k:held_group(rows,MODELS[name],"species",balance,penalty)[k]
                  for k in ("mse_row_weighted","mse_equal_held_group")}
            for name in ("context_only","breeding_SC","pollination_dI","dI_plus_SC")
        }
    return metrics


def nested_influence(rows:list[dict],balance:bool,penalty:float)->dict:
    changes={}
    for pub in sorted({r["pub"] for r in rows}):
        source=[r for r in rows if r["pub"]!=pub]
        if len({r["pub"] for r in source})<5:
            raise ValueError("Too few held-publication groups")
        sc=held_group(source,MODELS["breeding_SC"],"pub",balance,penalty)
        dI=held_group(source,MODELS["pollination_dI"],"pub",balance,penalty)
        add=held_group(source,MODELS["dI_plus_SC"],"pub",balance,penalty)
        bas=held_group(source,MODELS["context_only"],"pub",balance,penalty)
        changes[pub]={
            "dI_gain_vs_context":bas["mse_row_weighted"]-dI["mse_row_weighted"],
            "SC_increment_over_dI":dI["mse_row_weighted"]-add["mse_row_weighted"],
            "SC_gain_vs_context":bas["mse_row_weighted"]-sc["mse_row_weighted"],
        }
    return {
        "n_publications_deleted_one_at_a_time":len(changes),
        "dI_improvement_after_n_deletions":sum(
            v["dI_gain_vs_context"]>0 for v in changes.values()),
        "SC_increment_improvement_after_n_deletions":sum(
            v["SC_increment_over_dI"]>0 for v in changes.values()),
        "SC_over_context_improvement_after_n_deletions":sum(
            v["SC_gain_vs_context"]>0 for v in changes.values()),
        "dI_gain_range":[min(v["dI_gain_vs_context"] for v in changes.values()),
                         max(v["dI_gain_vs_context"] for v in changes.values())],
        "SC_increment_range":[
            min(v["SC_increment_over_dI"] for v in changes.values()),
            max(v["SC_increment_over_dI"] for v in changes.values())],
        "by_deleted_publication":changes,
    }


def main()->None:
    source,profile=load()
    reports={}
    for sub,rows in (
        ("all_49_known_breeding",source),
        ("EGWEE_source_disjoint_26",[r for r in source if r["pub"] not in OVERLAP])):
        reports[sub]={
            "n_pairs":len(rows),
            "n_publications":len({r["pub"] for r in rows}),
            "known_SC":sum(r["SC"] for r in rows),
            "known_SI":sum(1-r["SC"] for r in rows),
            "predictions":{
                weight:compare(rows,weight,RIDGE,evaluate_species=True)
                for weight in ("equal_pair","equal_publication")
            },
            "ridge_penalty_sensitivity":{
                str(k):{
                    weight:compare(rows,weight,k)["pairwise_checks"]
                    for weight in ("equal_pair","equal_publication")
                }
                for k in (0.1,4.0)
            },
            "source_delete_influence":{
                weight:nested_influence(rows,weight=="equal_publication",RIDGE)
                for weight in ("equal_pair","equal_publication")
            },
            "female_endpoint_variance_training_sensitivity":{
                str(floor):{
                    name:held_group(rows,MODELS[name],"pub",False,RIDGE,floor)[
                        "mse_row_weighted"]
                    for name in ("context_only","breeding_SC","pollination_dI",
                                 "dI_plus_SC","dI_plus_vertebrate","dI_plus_specialist")
                } for floor in (0.0,0.1,0.5)
            },
        }
    full=reports["all_49_known_breeding"]["predictions"]["equal_pair"]
    dis=reports["EGWEE_source_disjoint_26"]["predictions"]["equal_pair"]
    assert abs(full["context_only"]["mse_held_publication_row_weighted"]-
               0.3951705624265321)<1e-9
    assert abs(full["pollination_dI"]["mse_held_publication_row_weighted"]-
               0.3834109223889319)<1e-9
    assert abs(dis["dI_plus_SC"]["mse_held_publication_row_weighted"]-
               0.5292723605936349)<1e-9
    out={
        "status":"POST_HOC_MODERATOR_INCREMENTAL_VALUE_NOT_CAUSAL",
        "source":profile,
        "models":list(MODELS),
        "primary_penalty":RIDGE,
        "results":reports,
        "interpretation_ceiling":[
            "All models compare on identical SI/SC-known rows, never silently changing the denominator by covariate missingness.",
            "The 49 known breeding-system rows are continuous numeric d_I/d_F eligible, including one row excluded from the separate 54-pair constituent-sign consensus, so sign and numeric denominators must never be conflated.",
            "Twenty-six of the 49 known breeding-system pairs are source-publication disjoint from EGWEE matched map; this is one external literature extraction, not independent preregistered replication.",
            "Observed d_I and d_F are heterogeneous standardized endpoints; observed uncertainty and unknown paired covariance limit interpretation.",
            "The published original meta-analysis includes broader data and analyses; this secondary restricted reproduction is not a new biological meta-analysis.",
            "Raw publication-species effect points are not synchronized seed-to-flower transitions or true physiological response states.",
            "Self-compatibility metadata are trait categories, not measured realized self-fertilization, incompatibility strength, or pollinator effectiveness.",
            "Specialist/generalist and vertebrate/invertebrate labels are exploratory, sparse and publication-confounded.",
            "A modest held-publication MSE improvement is predictive association, not a causal pollen supply effect or proof of transport to new ecosystems.",
            "Publication-balanced training is a sensitivity to papers contributing different numbers of taxa, not a design-based estimator.",
            "Female-endpoint inverse-variance training uses archived marginal var_F only; it ignores uncertainty in d_I and unknown within-study dI/dF covariance, and is not a full meta-regression.",
            "Outcome-driven multiple moderator models and smoothing choices were inspected post hoc; do not claim nominal significance or ecological universality.",
            "No impact on frozen five-cluster, eight-matched, sixteen-programme or SF06 pair denominators, no manuscript primary claim promotion.",
        ]
    }
    p=ROOT/"build"/"sf06_moderator_transfer_v1.json"
    p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("SF06_MODERATOR_HELD_PUBLICATION_TRANSFER: PASS")
    print(json.dumps({
        "source":profile,
        "primary":{n:{
            "n":d["n_pairs"],"publications":d["n_publications"],
            "known_SC":d["known_SC"],"known_SI":d["known_SI"],
            "held_publication":{w:{
                k:{mk:val for mk,val in a.items() if mk!="held_species"}
                for k,a in d["predictions"][w].items() if k in (
                    "context_only","pollination_dI","breeding_SC","dI_plus_SC",
                    "dI_plus_vertebrate","dI_plus_specialist","pairwise_checks")}
                for w in d["predictions"]},
            "source_delete_summary":{w:{
                k:v for k,v in d["source_delete_influence"][w].items()
                if k!="by_deleted_publication"} for w in d["source_delete_influence"]},
            "precision_sensitivity":d["female_endpoint_variance_training_sensitivity"],
            "held_species":{w:d["predictions"][w]["held_species"]
                            for w in d["predictions"]},
            "ridge_sensitivity":d["ridge_penalty_sensitivity"]
        } for n,d in reports.items()},
    },indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
