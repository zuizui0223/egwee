#!/usr/bin/env python3
"""Post-outcome source-roster ascertainment challenge to genetic-sire contact excess.

Original 741 offspring / 16 experimental groups; source SHA checked.
This analysis explicitly retains reported prior co10 positive contact statistics,
and asks whether alternative handling of missing directed pair rows changes
the ecological meaning. Two separately seeded, marginal-preserving chains.

No source rows/IDs, observed assigned parents, genotypes or visitation events
published. Everything is a postprimary/retrospective methodological diagnostic.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random

import test_qpf007_contact_parentage_conditional_null as prior

SEEDS=(20261125,20261126)
N_NULL=2000
WARMUP=1500
BETWEEN=100
CO=10
CATS=("P","Z","U","A")

def cat(s,m,f,lookup):
    r=lookup.get((s,m,f))
    if r is None:return "A"
    v=r.get(CO)
    if v is None:return "U"
    return "P" if v>0 else "Z"

def tally(kids,lookup):
    counts=Counter()
    per_sess={}
    for s,events in kids.items():
        c=Counter(cat(s,m,f,lookup) for m,f in events)
        for k in CATS:counts[k]+=c[k]
        per_sess[s]=c
    return counts,per_sess

def ratios(c):
    n=sum(c[k] for k in CATS)
    if n<=0:raise ValueError("Empty source-paternal margin set")
    measured=c["P"]+c["Z"]
    return {
       "documented_positive":c["P"]/n,
       "optimistic_missing_as_positive":(c["P"]+c["U"]+c["A"])/n,
       "roster_presence":(c["P"]+c["Z"]+c["U"])/n,
       "positive_given_measured_row":c["P"]/measured if measured else None,
    }

def quantile(arr,p):
    a=sorted(arr)
    x=(len(a)-1)*p
    lo=math.floor(x);hi=math.ceil(x)
    return a[lo]+(x-lo)*(a[hi]-a[lo])

def one_chain(kids,lookup,seed):
    rng=random.Random(seed)
    original={s:list(events) for s,events in kids.items()}
    sessions=sorted(original)
    orig_deg={s:(Counter(m for m,f in ev),Counter(f for m,f in ev))
              for s,ev in original.items()}
    legal_sessions=[]
    for s,events in original.items():
        legal=any(m1!=m2 and f1!=f2 and f1!=m2 and f2!=m1
                  for i,(m1,f1) in enumerate(events)
                  for (m2,f2) in events[i+1:])
        if legal:legal_sessions.append(s)
    if len(legal_sessions)!=15:
        raise ValueError("Original source 15 exchangeable sessions drift")
    state={s:list(events) for s,events in original.items()}
    attempted=0;accepted=0
    for s in legal_sessions:
        for _ in range(WARMUP):
            attempted+=1
            accepted+=int(prior.swap_once(rng,state[s]))
    draws={key:[] for key in ("documented_positive","optimistic_missing_as_positive",
                             "roster_presence","positive_given_measured_row")}
    group_optimistic={s:0 for s in sessions}
    # Observed session evidence MUST use the unpermuted author-assigned
    # parentage, not the chain state after the warm-up swaps.
    group_original_fraction={s:ratios(Counter(cat(s,m,f,lookup) for m,f in original[s]))
                             ["optimistic_missing_as_positive"] for s in sessions}
    # Avoid repeated original contact table lookups on impossible phenotype.
    for _ in range(N_NULL):
        for s in legal_sessions:
            for _ in range(BETWEEN):
                attempted+=1
                accepted+=int(prior.swap_once(rng,state[s]))
        c,groups=tally(state,lookup)
        metric=ratios(c)
        for k,v in metric.items():
            if v is None:raise ValueError("Original null has no numeric source-contact evidence")
            draws[k].append(v)
        for s,cs in groups.items():
            group_optimistic[s]+=ratios(cs)["optimistic_missing_as_positive"]
    for s,events in state.items():
        ma,pa=orig_deg[s]
        if Counter(m for m,f in events)!=ma:
            raise ValueError("Maternal source outcross offspring counts changed")
        if Counter(f for m,f in events)!=pa:
            raise ValueError("Sire source outcross offspring counts changed")
        if any(m==f for m,f in events):
            raise ValueError("MCMC generated artificial selfing")
    group_excess=[group_original_fraction[s]-group_optimistic[s]/N_NULL
                  for s in sessions]
    out={}
    for k,v in draws.items():
        out[k]={
           "null_expected":sum(v)/len(v),
           "null_2p5_97p5_quantiles_not_effect_CI":[quantile(v,.025),quantile(v,.975)],
        }
    return {
        "rng_seed":seed,
        "conditional_null_draws":N_NULL,
        "null_metrics":out,
        "null_optimistic_source_session_excess_mean":sum(group_excess)/len(group_excess),
        "null_optimistic_source_sessions_positive":sum(x>0 for x in group_excess),
        "null_optimistic_source_session_excess_range":[min(group_excess),max(group_excess)],
        "attempted_swaps":attempted,
        "accepted_swaps":accepted,
        "swap_acceptance_fraction":accepted/attempted,
    }

def audit():
    kids,selfs,lookup,source=prior.load_source()
    if len(kids)!=16 or sum(map(len,kids.values()))!=741:
        raise ValueError("Original 741/16 source biological frame drift")
    obs,by_session=tally(kids,lookup)
    if [obs[x] for x in CATS]!=[688,23,0,30]:
        raise ValueError("Source observed P/Z/U/A differs from frozen 688/23/0/30")
    if sum(selfs.values())!=358:
        raise ValueError("Original 358 selfed genotyped offspring drift")
    observed=ratios(obs)
    chains=[one_chain(kids,lookup,s) for s in SEEDS]
    comparison={}
    for k in observed:
        nulls=[chain["null_metrics"][k]["null_expected"] for chain in chains]
        comparison[k]={
           "observed":observed[k],
           "expected_by_independent_chain":nulls,
           "observed_minus_expected_by_independent_chain":[observed[k]-v for v in nulls],
           "between_chain_expected_absolute_difference":abs(nulls[0]-nulls[1]),
        }
    pos_test=all(v>0 for v in comparison["documented_positive"]["observed_minus_expected_by_independent_chain"])
    optimistic=all(v>0 for v in comparison["optimistic_missing_as_positive"]["observed_minus_expected_by_independent_chain"])
    sessiontest=all(x["null_optimistic_source_sessions_positive"]>=12 for x in chains)
    maximum=max(v["between_chain_expected_absolute_difference"] for k,v in comparison.items()
                if k!="positive_given_measured_row")
    return {
      "status":"QPF007_SOURCE_ROSTER_ASC_BOUNDS_POSTOUTCOME_COMPLETE",
      "original_source":"Barbot et al. 2026 10.5281/zenodo.21628183",
      "source_SHA256_author_verified":True,
      "source_original_positive_evidence_P":obs["P"],
      "source_explicit_zero_evidence_Z":obs["Z"],
      "source_present_but_contact_unknown_U":obs["U"],
      "source_directed_pair_row_absent_A":obs["A"],
      "original_outcrossed_offspring":741,
      "original_selfed_offspring_excluded":358,
      "n_original_experimental_sessions":len(kids),
      "source_pair_absence_is_unknown_not_negative_contact":True,
      "original_barbot_co10_primary_reported_not_changed":True,
      "analytical_comparisons":comparison,
      "independent_null_chains":chains,
      "null_between_chain_convergence_warning":maximum>0.01,
      "null_max_absolute_chain_mean_difference":maximum,
      "retrospective_robustness_rule":{
         "documented_positive_excess_positive_both_chains":pos_test,
         "optimistic_missing_as_positive_excess_positive_both_chains":optimistic,
         "optimistic_12plus_sessions_above_source_expected_each_chain":sessiontest,
         "contact_inference_robust_to_pair_roster":pos_test and optimistic and sessiontest,
      },
      "decision":("CONTACT_INFERENCE_SURVIVES_OPTIMISTIC_SOURCE_ROSTER_BOUND"
                  if pos_test and optimistic and sessiontest
                  else "CONTACT_ASSOCIATION_DEPENDS_ON_ROSTER_ASCERTAINMENT"),
      "one_original_published_research_programme":True,
      "not_an_independent_registrational_confirmation":True,
      "all_observed_results_postoutcome_sensitivity":True,
      "source_original_phenotypes_genotypes_mother_father_offspring_IDs_not_redistributed":True,
    }

def synthetic():
    d={("a","m","f"):{10:3},("a","m","g"):{10:0},
       ("a","m","h"):{10:None}}
    assert [cat("a","m",x,d) for x in ("f","g","h","z")]==list(CATS)
    r=ratios(Counter(P=2,Z=1,U=0,A=1))
    assert abs(r["documented_positive"]-.5)<1e-12
    assert abs(r["optimistic_missing_as_positive"]-.75)<1e-12
    assert abs(r["roster_presence"]-.75)<1e-12
    assert abs(r["positive_given_measured_row"]-2/3)<1e-12
    print("QPF007_SOURCE_ROSTER_MISSINGNESS_BOUNDS_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:synthetic();return 0
    if args.output is None:p.error("--output required")
    try:r=audit()
    except Exception as e:r={
       "status":"QPF007_POSTOUTCOME_SOURCE_OR_MCMC_STOP",
       "error_type":type(e).__name__,
       "reason":str(e)[:280],
       "source_original_phenotypes_genotypes_mother_father_offspring_IDs_not_redistributed":True}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    brief={
       "status":r["status"],"decision":r.get("decision"),
       "P":r.get("source_original_positive_evidence_P"),
       "Z":r.get("source_explicit_zero_evidence_Z"),
       "U":r.get("source_present_but_contact_unknown_U"),
       "A":r.get("source_directed_pair_row_absent_A"),
       "comparison":r.get("analytical_comparisons"),
       "retrospective_rule":r.get("retrospective_robustness_rule"),
       "convergence_warning":r.get("null_between_chain_convergence_warning"),
       "error":r.get("reason"),
    }
    print("QPF007_ORIGINAL_SOURCE_ROSTER_ASCERTAINMENT "+json.dumps(brief,sort_keys=True),flush=True)
    return 0 if r["status"]=="QPF007_SOURCE_ROSTER_ASC_BOUNDS_POSTOUTCOME_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
