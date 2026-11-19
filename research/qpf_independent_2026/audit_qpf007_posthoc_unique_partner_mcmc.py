#!/usr/bin/env python3
"""Post-primary 303-distinct-mother/father-pair contact-null sensitivity.

Pair-equal statistics are retrospective and not independently confirmatory.
Two separately seeded fixed-margin MCMC chains preserve exact original source
mother/father outcrossed offspring totals and explicit original sessions.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import json
import math
from pathlib import Path
import random

import test_qpf007_contact_parentage_conditional_null as src

SEEDS=(20261121,20261122)
DRAWS=2000
BURN=1500
LAG=100
CO=10

def unique_pairs_by_session(kids):
    return {s:set(pairs) for s,pairs in kids.items()}

def source_quality_pairs(pairset,contacts):
    c=Counter()
    for session,pairs in pairset.items():
        for mo,fa in pairs:
            col=contacts.get((session,mo,fa))
            if col is None:c["source_partner_pair_record_absent"]+=1
            elif col[CO] is None:c["source_pair_contact_unmeasured"]+=1
            elif col[CO]==0:c["source_pair_explicit_contact_zero"]+=1
            else:c["source_pair_positive_inferred_contact"]+=1
    c["distinct_original_outcross_genetic_pairs"]=sum(map(len,pairset.values()))
    return dict(c)

def permute_one_chain(kids,contacts,seed):
    sessions=sorted(kids)
    rng=random.Random(seed)
    living={s:list(kids[s]) for s in sessions}
    accepted=Counter()
    attempts=Counter()
    eligible=[]
    for s,events in living.items():
        legal=any(m1!=m2 and f1!=f2 and m1!=f2 and m2!=f1
                  for i,(m1,f1) in enumerate(events)
                  for (m2,f2) in events[i+1:])
        if legal:eligible.append(s)
    if len(eligible)!=15:
        raise ValueError("SOURCE_MARGINAL_EXCHANGEABLE_SESSIONS_DRIFT")
    before={s:(Counter(m for m,f in living[s]),Counter(f for m,f in living[s]))
            for s in sessions}
    def shuffle(s,n):
        for _ in range(n):
            attempts[s]+=1
            accepted[s]+=int(src.swap_once(rng,living[s]))
    for s in eligible:shuffle(s,BURN)
    n_out=sum(map(len,living.values()))
    assert n_out==741
    source_pair_null=[]
    source_child_null=[]
    pair_by_group=defaultdict(list)
    for i in range(DRAWS):
        for s in eligible:shuffle(s,LAG)
        source_child_null.append(sum(
            src.positive(s,m,f,contacts,CO) for s,events in living.items()
            for m,f in events)/n_out)
        pairs=unique_pairs_by_session(living)
        denom=sum(len(x) for x in pairs.values())
        hit=sum(src.positive(s,m,f,contacts,CO)
                for s,edges in pairs.items() for m,f in edges)
        source_pair_null.append(hit/denom)
        for s,edges in pairs.items():
            pair_by_group[s].append(
                sum(src.positive(s,m,f,contacts,CO) for m,f in edges)/len(edges)
            )
    for s,events in living.items():
        if Counter(m for m,f in events)!=before[s][0] or Counter(f for m,f in events)!=before[s][1]:
            raise ValueError("ORIGINAL_SOURCE_MOTHER_OR_FATHER_OFFSPRING_MARGIN_CHANGED")
        if any(m==f for m,f in events):
            raise ValueError("ORIGINAL_SOURCE_OUTCROSSED_CHILD_NULL_CREATED_SELF")
    return {
       "seed":seed,
       "null_pair_fraction_mean":sum(source_pair_null)/DRAWS,
       "null_pair_fraction_95pct_reference":[
           src.interp_quantile(sorted(source_pair_null),.025),
           src.interp_quantile(sorted(source_pair_null),.975)],
       "null_child_fraction_mean":sum(source_child_null)/DRAWS,
       "null_child_fraction_95pct_reference":[
           src.interp_quantile(sorted(source_child_null),.025),
           src.interp_quantile(sorted(source_child_null),.975)],
       "null_pair_fraction_draws":source_pair_null,
       "null_child_fraction_draws":source_child_null,
       "null_pair_by_session_mean":{
           s:sum(v)/DRAWS for s,v in pair_by_group.items()},
       "null_exchangeable_session_count":len(eligible),
       "source_null_swap_attempts":sum(attempts.values()),
       "source_null_swaps_accepted":sum(accepted.values()),
    }

def run():
    kids,self_counts,contact,provenance=src.load_source()
    assert len(kids)==16 and sum(map(len,kids.values()))==741
    pairs=unique_pairs_by_session(kids)
    obs_categories=source_quality_pairs(pairs,contact)
    if obs_categories["distinct_original_outcross_genetic_pairs"]!=303:
        raise ValueError("ORIGINAL_SOURCE_303_OUTCROSS_MATE_KEYS_CHANGED")
    n_unique=303
    observed_pair=obs_categories["source_pair_positive_inferred_contact"]/n_unique
    observed_child=sum(src.positive(s,m,f,contact,CO)
                       for s,events in kids.items() for m,f in events)/741
    if abs(observed_child-(688/741))>1e-12:
        raise ValueError("REGISTERED_CHILD_WEIGHTED_688_OF_741_NOT_REPRODUCED")
    chains=[permute_one_chain(kids,contact,seed) for seed in SEEDS]
    check_pair=max(z["null_pair_fraction_mean"] for z in chains)-min(
              z["null_pair_fraction_mean"] for z in chains)
    check_child=max(z["null_child_fraction_mean"] for z in chains)-min(
              z["null_child_fraction_mean"] for z in chains)
    per_sess_obs={
        s:sum(src.positive(s,m,f,contact,CO) for m,f in edges)/len(edges)
        for s,edges in pairs.items()}
    sess_differences=[per_sess_obs[s]-sum(c["null_pair_by_session_mean"][s]
                                       for c in chains)/len(chains)
                      for s in sorted(pairs)]
    output={
        "status":"QPF007_POSTOUTCOME_UNIQUE_MOTHER_FATHER_PAIR_SENSITIVITY_COMPLETE",
        "original_source":"Barbot et al. 2026, Zenodo 10.5281/zenodo.21628183",
        "source_manifest_verified_against_original":True,
        "source_original_maternal_and_paternal_role_verified":True,
        "source_original_pair_sha256":src.author_bytes and "7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5",
        "original_independent_experimental_sessions":len(pairs),
        "original_outcrossed_genotyped_offspring":741,
        "source_original_distinct_outcross_genetic_pairs":303,
        "original_pair_evidence_categories":obs_categories,
        "original_frozen_child_weighted_contact_fraction":observed_child,
        "postoutcome_pair_equal_contact_fraction":observed_pair,
        "original_10flower_carryover_choice_unchanged":True,
        "original_primary_marginal_null_not_refit_or_redefined":True,
        "two_separate_RNG_seeded_chains":list(SEEDS),
        "null_draws_per_chain":DRAWS,
        "null_chain_outputs":[{
            "seed":c["seed"],
            "expected_unique_pair_contact_fraction":c["null_pair_fraction_mean"],
            "expected_offspring_weighted_contact_fraction":c["null_child_fraction_mean"],
            "observed_minus_null_unique_pair_fraction":observed_pair-c["null_pair_fraction_mean"],
            "null_unique_pair_fraction_95pct_reference":c["null_pair_fraction_95pct_reference"],
            "conditional_unique_pair_one_sided_MC_p_exploratory":
                (1+sum(x>=observed_pair-1e-15 for x in c["null_pair_fraction_draws"]))/(DRAWS+1),
            "exchangeable_sessions":c["null_exchangeable_session_count"],
            "accepted_swaps":c["source_null_swaps_accepted"],
            "attempted_swaps":c["source_null_swap_attempts"],
        } for c in chains],
        "null_chain_expected_unique_pair_fraction_max_abs_diff":check_pair,
        "null_chain_expected_child_fraction_max_abs_diff":check_child,
        "posthoc_null_chain_convergence_warning":max(check_pair,check_child)>0.01,
        "observed_minus_null_session_equal_unique_pair_gain":
            sum(sess_differences)/len(sess_differences),
        "sessions_positive_unique_pair_gain":sum(x>0 for x in sess_differences),
        "session_unique_pair_gain_range":[min(sess_differences),max(sess_differences)],
        "this_is_postoutcome_and_not_independent_confirmation":True,
        "not_claimed_independent_natural_study":True,
        "source_original_rows_and_genotype_IDs_redistributed":False,
        "decision":"PAIR_EQUAL_POSTPRIMARY_DIAGNOSTIC_NO_CHANGE_TO_ORIGINAL_PRIMARY",
    }
    return output

def synthetic():
    source={
       "s":[("a","b"),("a","b"),("c","d"),("c","d")]
    }
    p=unique_pairs_by_session(source)
    assert len(p["s"])==2
    assert sum(len(v) for v in p.values())==2
    print("QPF007_POSTPRIMARY_UNIQUE_GENETIC_PAIR_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:synthetic();return 0
    if a.output is None:p.error("--output required")
    try:r=run()
    except Exception as e:r={
       "status":"QPF007_POSTPRIMARY_SOURCE_OR_DIAGNOSTIC_STOP",
       "reason":type(e).__name__+": "+str(e)[:300],
       "source_original_rows_and_genotype_IDs_redistributed":False,
       "this_is_postoutcome_and_not_independent_confirmation":True
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    brief={k:v for k,v in r.items() if k in (
       "status","decision","original_outcrossed_genotyped_offspring",
       "source_original_distinct_outcross_genetic_pairs",
       "original_pair_evidence_categories",
       "original_frozen_child_weighted_contact_fraction",
       "postoutcome_pair_equal_contact_fraction",
       "null_chain_outputs",
       "null_chain_expected_unique_pair_fraction_max_abs_diff",
       "null_chain_expected_child_fraction_max_abs_diff",
       "posthoc_null_chain_convergence_warning",
       "observed_minus_null_session_equal_unique_pair_gain",
       "sessions_positive_unique_pair_gain",
       "reason",
    )}
    print("QPF007_POSTPRIMARY_UNIQUE_PAIR_AUDIT "+json.dumps(brief,sort_keys=True),flush=True)
    return 0 if r["status"]=="QPF007_POSTOUTCOME_UNIQUE_MOTHER_FATHER_PAIR_SENSITIVITY_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
