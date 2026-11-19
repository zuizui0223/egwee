#!/usr/bin/env python3
"""QPF007 postprimary pollen carryover-10 contact evidence vs assigned sires.

All original source tables and the R source script are SHA/MD5 verified.
The fixed-margin null shuffles fathers of outcrossed genotyped offspring
WITHIN ORIGINAL SESSIONS, never creating selfing; mother/father offspring
totals remain exactly fixed. No original individual data are exported.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import random

from audit_brassica_rapa_zenodo_source_keys import load_manifest,trusted_get
from audit_qpf007_partner_parentage_ids import (
    author_bytes,tabular,FILE_MAIN,FILE_PAIR,FILE_PATERNITY
)
from audit_qpf007_published_author_code_roles import code_source

PAPER="10.1371/journal.pbio.3003579"
SOURCE="10.5281/zenodo.21628183"
SCRIPT_SHA="a8e47abb7b2b4e7d6f85574fa6444eddd35a2bf0537592eccb4354fabb2402e9"
N_EXPECTED_PLANT=160
N_EXPECTED_PAIR=1363
N_EXPECTED_CHILD=1099
N_EXPECTED_PAIR_ROWS_16=1209
CARRYOVER=(1,5,10,20,50,300)
TARGET_COLS=tuple("import_nb_visit_co"+str(k) for k in CARRYOVER)
N_NULL=2000
WARMUP=1500
BETWEEN=100
SEED=20261119
BOOT_SEED=20261120

def source_published_readme():
    meta=load_manifest()
    selected=[f for f in meta["files"] if (f.get("key") or f.get("filename"))=="README.txt"]
    if len(selected)!=1:
        raise ValueError("SOURCE_STOP: original Zenodo README is missing/ambiguous")
    f=selected[0]
    href=(f.get("links") or {}).get("self") or (f.get("links") or {}).get("content")
    if not href:
        raise ValueError("SOURCE_STOP: README has no published source link")
    raw=trusted_get(href,30_000)
    declared=f.get("checksum","")
    if not declared.startswith("md5:") or hashlib.md5(raw).hexdigest()!=declared[4:]:
        raise ValueError("SOURCE_STOP: published original README checksum drift")
    try:src=raw.decode("utf-8-sig",errors="strict")
    except UnicodeDecodeError:src=raw.decode("latin-1",errors="strict")
    if not all(term in src for term in ("import_nb_visit_coXX","seed_couple_on_foc","focal individual")):
        raise ValueError("SOURCE_STOP: README lacks original visit carryover/recipient semantics")
    return hashlib.sha256(raw).hexdigest()

def contact_number(raw):
    t=str(raw).strip().strip('"')
    if t.lower() in ("","na","nan","none","null","missing"):return None
    try:
        n=float(t)
    except (ValueError,TypeError):
        raise ValueError("SOURCE_STOP: unrecognized original contact numeric token")
    if not math.isfinite(n) or n<0:
        raise ValueError("SOURCE_STOP: original negative/nonfinite contact field")
    return n

def load_source():
    blobs=author_bytes()
    hmain,main=tabular(blobs[FILE_MAIN],("session","ID_full"))
    hpair,pair=tabular(blobs[FILE_PAIR],
        ("session","ID_full_foc","ID_full_part",*TARGET_COLS))
    hpat,pat=tabular(blobs[FILE_PATERNITY],
        ("offspring_id","known_id","candidate_id"))
    if tuple(map(len,(main,pair,pat)))!=(160,1363,1099):
        raise ValueError("SOURCE_STOP: three original source row counts changed")
    if any(hpair["headers"].count(col)!=1 for col in TARGET_COLS):
        raise ValueError("SOURCE_STOP: expected original carryover columns drift")
    main_set=set(main)
    if len(main_set)!=160 or len({s for s,p in main})!=16:
        raise ValueError("SOURCE_STOP: main mother/session identity mismatch")
    id_to_session={p:s for s,p in main}
    if len(id_to_session)!=160:
        raise ValueError("SOURCE_STOP: source plant IDs reused across sessions")
    orig_code,sha,size=code_source()
    if sha!=SCRIPT_SHA or size!=297463:
        raise ValueError("SOURCE_STOP: original author assignment code changed")
    lines=orig_code.splitlines()
    author_tests={
        "session_from_known_id":"mutate(session = substr(known_id,1,5))" in lines[87],
        "paternal_grouping":"group_by(candidate_id)" in lines[101],
        "maternal_grouping":"group_by(known_id)" in lines[107],
    }
    if not all(author_tests.values()):
        raise ValueError("SOURCE_STOP: original author maternal/paternal roles changed")
    readme_sha=source_published_readme()

    contacts={}
    outsessions=set()
    for row in pair:
        ses,recipient,donor,*raws=row
        if (ses,recipient) not in main_set or (ses,donor) not in main_set:
            outsessions.add((ses,recipient,donor))
            continue
        key=(ses,recipient,donor)
        if key in contacts:raise ValueError("SOURCE_STOP: duplicate directed pair key")
        contacts[key]={k:contact_number(raw) for k,raw in zip(CARRYOVER,raws)}
    if len(contacts)!=N_EXPECTED_PAIR_ROWS_16 or len(outsessions)!=154:
        raise ValueError("SOURCE_STOP: source original 1209/154 pair roster drift")
    kids=defaultdict(list)
    child_ids=set()
    self_children=Counter()
    for child,mother,father in pat:
        if child in child_ids:
            raise ValueError("SOURCE_STOP: duplicate original genotyped offspring ID")
        child_ids.add(child)
        if mother not in id_to_session or father not in id_to_session:
            raise ValueError("SOURCE_STOP: parent ID missing in original source")
        ses=id_to_session[mother]
        if mother[:5]!=ses or id_to_session[father]!=ses:
            raise ValueError("SOURCE_STOP: original author-code session mismatch")
        if mother==father:self_children[ses]+=1
        else:kids[ses].append((mother,father))
    if len(child_ids)!=1099 or len(kids)!=16:
        raise ValueError("SOURCE_STOP: original offspring/session coverage changed")
    return kids,self_children,contacts,{
      "original_readme_sha256":readme_sha,
      "source_author_R_role_contract":author_tests,
      "original_roster_plant":len(main),
      "original_roster_source_partner_rows":len(pair),
      "original_roster_genotyped_offspring":len(child_ids),
      "source_main_original_sessions":16,
      "original_pair_contact_rows_in_main_16":len(contacts),
      "original_pair_contact_rows_excluded_extra_sessions":len(outsessions),
    }

def positive(s,m,f,contact,carryover):
    # The absence of a source candidate pair row does not assert ecological 0.
    col=contact.get((s,m,f))
    return bool(col is not None and col[carryover] is not None and col[carryover]>0)

def score_sessions(kids,contact,co):
    out={}
    for session,pairs in kids.items():
        n=len(pairs)
        if not n:raise ValueError("SOURCE_STOP: session has no outcross paternity")
        npos=sum(positive(session,m,f,contact,co) for m,f in pairs)
        out[session]=(npos,n)
    return out

def source_observed_quality(kids,contact,co):
    counts=Counter()
    unique_edge=set()
    for session,pairs in kids.items():
        for mother,father in pairs:
            key=(session,mother,father)
            unique_edge.add(key)
            tab=contact.get(key)
            if tab is None:counts["not_in_original_partner_pair_table"]+=1
            elif tab[co] is None:counts["recorded_pair_contact_missing_or_unmeasured"]+=1
            elif tab[co]==0:counts["recorded_pair_explicit_zero_contact"]+=1
            else:counts["recorded_pair_positive_contact"]+=1
    counts["total_outcross_genotyped_offspring"]=sum(map(len,kids.values()))
    counts["distinct_outcross_mother_father_genetic_pairs"]=len(unique_edge)
    return dict(counts)

def swap_once(rng,events):
    n=len(events)
    i,j=rng.randrange(n),rng.randrange(n)
    if i==j:return False
    m1,f1=events[i]
    m2,f2=events[j]
    if m1==m2 or f1==f2 or f1==m2 or f2==m1:
        return False
    events[i]=(m1,f2)
    events[j]=(m2,f1)
    return True

def fixed_margin_null(kids,contact):
    rng=random.Random(SEED)
    sessions=sorted(kids)
    state={s:list(kids[s]) for s in sessions}
    ready=[]
    nonexchange=[]
    accepted=Counter()
    attempted=Counter()
    for s in sessions:
        # Registered source eligibility: at least two eligible distinct mothers
        # and sires and an attainable nonself same-session swap.
        if len({m for m,f in state[s]})<2 or len({f for m,f in state[s]})<2:
            nonexchange.append(s);continue
        legal=any(m1!=m2 and f1!=f2 and m1!=f2 and m2!=f1
                  for i,(m1,f1) in enumerate(state[s])
                  for j,(m2,f2) in enumerate(state[s]) if j>i)
        if not legal:
            nonexchange.append(s);continue
        ready.append(s)
    if len(ready)<12:
        return None,{"n_exchangeable_sessions":len(ready),
                     "n_nonexchangeable_sessions":len(nonexchange)}
    for s in ready:
        for _ in range(WARMUP):
            attempted[s]+=1
            accepted[s]+=int(swap_once(rng,state[s]))
    null_all={co:[] for co in CARRYOVER}
    null_by_session={co:defaultdict(list) for co in CARRYOVER}
    nall=sum(len(events) for events in kids.values())
    for repetition in range(N_NULL):
        for s in ready:
            for _ in range(BETWEEN):
                attempted[s]+=1
                accepted[s]+=int(swap_once(rng,state[s]))
        for co in CARRYOVER:
            total=0
            for s in sessions:
                pos=sum(positive(s,m,f,contact,co) for m,f in state[s])
                total+=pos
                null_by_session[co][s].append(pos/len(state[s]))
            null_all[co].append(total/nall)
    return (null_all,null_by_session),{
      "n_exchangeable_sessions":len(ready),
      "n_nonexchangeable_sessions":len(nonexchange),
      "total_swap_attempts":sum(attempted.values()),
      "accepted_swaps":sum(accepted.values()),
      "accepted_swaps_fraction":sum(accepted.values())/sum(attempted.values()),
    }

def interp_quantile(sorted_vals,p):
    if not sorted_vals:return None
    i=(len(sorted_vals)-1)*p
    lo=math.floor(i);hi=math.ceil(i)
    return sorted_vals[lo]+(i-lo)*(sorted_vals[hi]-sorted_vals[lo])

def bootstrap_sessions(differences):
    rng=random.Random(BOOT_SEED)
    original=list(differences)
    n=len(original)
    return sorted(sum(original[rng.randrange(n)] for _ in range(n))/n
                  for _ in range(N_NULL))

def audit():
    kids,self_counts,contact,source=load_source()
    total_out=sum(map(len,kids.values()))
    total_self=sum(self_counts.values())
    if total_self+total_out!=1099:
        raise ValueError("SOURCE_STOP: outcross+self offspring denominator drift")
    observed={co:score_sessions(kids,contact,co) for co in CARRYOVER}
    quality={co:source_observed_quality(kids,contact,co) for co in CARRYOVER}
    primary_total=quality[10]["total_outcross_genotyped_offspring"]
    if primary_total!=total_out:
        raise ValueError("SOURCE_STOP: primary contact quality denominator drift")
    null,diagnostics=fixed_margin_null(kids,contact)
    base={
      "source":"original Barbot et al. 2026 Zenodo 21628183",
      "published_article_doi":PAPER,
      "frozen_exploratory_protocol":"research/qpf_independent_2026/QPF007_CONTACT_NULL_FROZEN_20261119.md",
      "registered_primary_carryover_flowers":10,
      "original_source_provenance":source,
      "original_cervus_80pct_assignment_accepted_as_reported":True,
      "original_paternity_rows":1099,
      "original_outcrossed_assigned_offspring":total_out,
      "original_selfed_assigned_offspring_excluded_from_primary":total_self,
      "n_original_experimental_sessions":len(kids),
      "original_contact_evidence_categories":quality,
      "original_raw_data_rows_or_parent_identifiers_redistributed":False,
      "original_preexisting_positive_recovery_not_claimed_novel":True,
      "source_pair_row_absence_not_biological_zero":True,
      "source_outcross_genotype_not_directly_observed_stigma_pollen":True,
      "n_independent_natural_habitats":0,
      "inference_scope":"One manipulated original Brassica experiment with 16 repeated sessions",
      "null_permutation_diagnostics":diagnostics,
      "primary_is_postprimary_exploratory":True,
    }
    if null is None:
        return {**base,"status":"ORIGINAL_SOURCE_FIXED_MARGINAL_NULL_COVERAGE_STOP",
                "new_effect_estimated":False,"decision":"STOP_NO_EXCHANGEABLE_STUDY_SOURCE"}
    null_global,null_by_session=null
    metrics={}
    for co in CARRYOVER:
        obs=sum(pos for pos,n in observed[co].values())/total_out
        null_draws=null_global[co]
        mean_null=sum(null_draws)/len(null_draws)
        session_gain=[]
        for s,(positive_n,n) in sorted(observed[co].items()):
            null_m=sum(null_by_session[co][s])/len(null_by_session[co][s])
            session_gain.append(positive_n/n-null_m)
        sorted_null=sorted(null_draws)
        metric={
           "original_positive_contact_evidence_outcross_offspring_fraction":obs,
           "conditional_fixed_margin_null_fraction_mean":mean_null,
           "observed_minus_fixed_margin_null_evidence_excess":obs-mean_null,
           "null_95pct_quantiles_not_effect_CI":[interp_quantile(sorted_null,.025),
                                                  interp_quantile(sorted_null,.975)],
           "monte_carlo_one_sided_p_conditional_null":
               (1+sum(z>=obs-1e-15 for z in null_draws))/(N_NULL+1),
           "source_session_equal_observed_minus_null_mean":
               sum(session_gain)/len(session_gain),
           "source_sessions_with_positive_minus_null":sum(x>0 for x in session_gain),
           "source_session_gain_range":[min(session_gain),max(session_gain)],
        }
        if co==10:
            bs=bootstrap_sessions(session_gain)
            metric["whole_original_session_bootstrap_95pct"]=[
               interp_quantile(bs,.025),interp_quantile(bs,.975)]
            metric["predeclared_bounded_positive_rule_pass"] = (
                metric["monte_carlo_one_sided_p_conditional_null"] < .05
                and metric["whole_original_session_bootstrap_95pct"][0]>0
                and metric["source_sessions_with_positive_minus_null"]>=12)
        metrics[str(co)]=metric
    yes=metrics["10"]["predeclared_bounded_positive_rule_pass"]
    return {**base,
       "status":"ORIGINAL_PARENTAGE_CONTACT_FIXED_MARGINAL_NULL_COMPLETE",
       "new_effect_estimated":True,
       "original_2000_fixed_margin_null_realizations":N_NULL,
       "outcome_statistic":"Positive import_nb_visit_co10 among OUTCROSSED genotyped offspring, not all rows",
       "prespecified_contact_evidence_metrics":metrics,
       "conditional_inference_no_causal_genetic_compatibility_claim":True,
       "predeclared_bounded_positive_rule":yes,
       "decision":("ONE_STUDY_EXPLORATORY_EXCESS_CONTACT_EVIDENCE_ABOVE_MARGINAL_NULL"
                   if yes else "NO_PRESPECIFIED_STUDY_GENERAL_CONTACT_ENRICHMENT"),
    }

def synthetic():
    # A legal swap must conserve paternal and maternal child margins and
    # exclude self events, with a source-constructed phenotype-free toy roster.
    x=[("A","B"),("A","D"),("C","B"),("C","D"),("E","B"),("E","D")]
    oldm=Counter(m for m,f in x)
    oldf=Counter(f for m,f in x)
    rng=random.Random(42)
    accepted=0
    for _ in range(1000):
        accepted+=int(swap_once(rng,x))
    assert accepted>0 and Counter(m for m,f in x)==oldm
    assert Counter(f for m,f in x)==oldf
    assert all(m!=f for m,f in x)
    assert contact_number("NA") is None and contact_number("0")==0
    assert contact_number("2.5")==2.5
    contact={("s","a","b"):{10:2.0},("s","a","c"):{10:0.0}}
    assert positive("s","a","b",contact,10)
    assert not positive("s","a","c",contact,10)
    assert not positive("s","a","d",contact,10)
    print("QPF007_FATHER_CONTACT_FIXED_MARGINS_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:synthetic();return 0
    if a.output is None:p.error("--output required")
    try:r=audit()
    except Exception as exc:
        r={"status":"ORIGINAL_SOURCE_OR_CONTACT_NULL_STOP",
           "reason":type(exc).__name__+": "+str(exc)[:300],
           "new_effect_estimated":False,
           "original_raw_data_rows_or_parent_identifiers_redistributed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    brief={
       "status":r["status"],"decision":r.get("decision"),
       "n_outcross":r.get("original_outcrossed_assigned_offspring"),
       "n_selfed":r.get("original_selfed_assigned_offspring_excluded_from_primary"),
       "source_counts":r.get("original_contact_evidence_categories",{}).get(10),
       "primary_metric":r.get("prespecified_contact_evidence_metrics",{}).get("10"),
       "null_diagnostics":r.get("null_permutation_diagnostics"),
       "error":r.get("reason"),"postprimary":True
    }
    print("QPF007_SOURCE_FATHER_CONTACT_NULL "+json.dumps(brief,sort_keys=True),flush=True)
    return 0 if r["status"] in (
       "ORIGINAL_PARENTAGE_CONTACT_FIXED_MARGINAL_NULL_COMPLETE",
       "ORIGINAL_SOURCE_FIXED_MARGINAL_NULL_COVERAGE_STOP") else 1

if __name__=="__main__":
    raise SystemExit(main())
