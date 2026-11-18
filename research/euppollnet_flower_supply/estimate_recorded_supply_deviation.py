#!/usr/bin/env python3
"""Post-primary ORIGINAL counted-bloom-relative guild visitation deviation.

Source-locked, no external source rows redistributed. This is not biological
preference, pollination quality, seed set, or independent validation of PR #72.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
import math
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_source_flower_availability import (
    count_rows, e, int_code, norm, is_real, ymd, interaction_date,
)

SPEC="research/euppollnet_flower_supply/SUPPLY_RELATIVE_ESTIMAND_FREEZE_20261118.md"
N_NULL=199
N_BOOT=2000
RNG_NULL=20261126
RNG_BOOT=20261127

def source_data():
    net=defaultdict(lambda:{"method":set(),"all":defaultdict(lambda:[0,0]),
                            "acc":set(),"orig":defaultdict(set)})
    ev=defaultdict(lambda:defaultdict(lambda:[0,0]))
    all_day=defaultdict(lambda:[0,0])
    for r in e.source_rows():
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        dt=interaction_date(r["Date"] or "")
        yr=e.year_of(r["Date"] or "")
        if not study or not network or yr is None:
            continue
        nk=(study,network,yr)
        n=net[nk]
        n["method"].add((r["Sampling_method"] or "").strip())
        accepted=norm(r["Plant_accepted_name"])
        original=norm(r["Plant_original_name"])
        if is_real(accepted):
            n["acc"].add(accepted)
            if is_real(original):
                n["orig"][original].add(accepted)
        guild=e.category(r)
        if guild is None or not is_real(accepted):
            continue
        if (r["Interaction"] or "").strip() not in ("1","1.0"):
            raise ValueError("SOURCE_STOP: visit weight/record identity changed")
        gi=0 if guild=="bee" else 1
        n["all"][accepted][gi]+=1
        if dt is None:
            continue
        all_day[(study,network,yr,dt)][gi]+=1
        merge=norm(r["Flower_data_merger"])
        if is_real(merge):
            ev[(study,network,yr,merge,dt)][accepted][gi]+=1
    if len(net)!=1864:
        raise ValueError("SOURCE_STOP: original network cardinality changed")
    eligible=set()
    for k,g in net.items():
        if len(g["method"])!=1 or "" in g["method"]:
            continue
        c=list(g["all"].values())
        if len(c)>=3 and sum(v[0] for v in c)>=20 and sum(v[1] for v in c)>=20:
            eligible.add(k)
    if len(eligible)!=311:
        raise ValueError("SOURCE_STOP: original registered network risk set changed")
    return net,ev,all_day,eligible

def assemble(net,ev,all_day,eligible):
    flowers=defaultdict(lambda:{"units":set(),"rows":[]})
    invalid=0
    for r in count_rows():
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        yr=int_code(r["Year"])
        dt=ymd(r["Year"],r["Month"],r["Day"])
        merge=norm(r["Flower_data_merger"])
        if not study or not network or yr is None or dt is None or not is_real(merge):
            continue
        k=(study,network,yr,merge,dt)
        z=flowers[k]
        z["units"].add(norm(r["Units"]))
        plant=norm(r["Plant_species"])
        if not is_real(plant):
            continue
        try:
            val=float((r["Flower_count"] or "").strip())
        except ValueError:
            invalid+=1;continue
        if not math.isfinite(val) or val<0:
            invalid+=1;continue
        if val>0:
            z["rows"].append((plant,val))
    date_groups=defaultdict(lambda:{"units":set(),
                                   "visit":defaultdict(lambda:[0,0]),
                                   "flowers":defaultdict(float),
                                   "merger_count":0})
    for k,vs in ev.items():
        if k[:3] not in eligible or k not in flowers:
            continue
        dk=(k[0],k[1],k[2],k[4])
        o=date_groups[dk]
        o["merger_count"]+=1
        o["units"].update(flowers[k]["units"])
        ng=net[k[:3]]
        for p,v in vs.items():
            o["visit"][p][0]+=v[0]
            o["visit"][p][1]+=v[1]
        for source_plant,num in flowers[k]["rows"]:
            if source_plant in ng["acc"]:
                mapped=source_plant
            elif source_plant in ng["orig"] and len(ng["orig"][source_plant])==1:
                mapped=next(iter(ng["orig"][source_plant]))
            else:
                continue
            o["flowers"][mapped]+=num
    if len(date_groups)!=583:
        raise ValueError("SOURCE_STOP: original source co-date crosswalk drift")
    kept=[]
    excl=Counter()
    for dk,z in sorted(date_groups.items()):
        if len(z["units"])!=1 or "" in z["units"]:
            excl["heterogeneous_or_unknown_units"]+=1
            continue
        flowering=sorted(p for p,n in z["flowers"].items() if n>0)
        if len(flowering)<3:
            excl["less_than_3_identified_positive_bloom_taxa"]+=1
            continue
        visited=[p for p in flowering if p in z["visit"] and sum(z["visit"][p])>0]
        if len(visited)<3:
            excl["less_than_3_bloom_confirmed_visited_taxa"]+=1
            continue
        b=np.array([z["visit"][p][0] for p in flowering],dtype=np.int64)
        s=np.array([z["visit"][p][1] for p in flowering],dtype=np.int64)
        if b.sum()<10 or s.sum()<10:
            excl["below_10_positive_bloom_visits_per_guild"]+=1
            continue
        denom=all_day[dk]
        if min(denom)<=0 or b.sum()/denom[0]<.70 or s.sum()/denom[1]<.70:
            excl["below_source_date_guild_coverage"]+=1
            continue
        fl=np.array([z["flowers"][p] for p in flowering],dtype=float)
        if not np.all(np.isfinite(fl)) or np.any(fl<=0):
            raise ValueError("SOURCE_STOP: nonfinite positive flower opportunity")
        kept.append((e.programme_of(dk[0]),b,s,fl))
    programmes={r[0] for r in kept}
    if (len(kept),len(programmes))!=(213,18):
        raise ValueError(f"SOURCE_STOP: frozen 213/18 date cohort drift {len(kept)}/{len(programmes)}")
    return kept,invalid,excl

def expected_sampling_jsd(visits,flowers,rng):
    obs=e.jsd(visits,flowers)
    flower_prop=flowers/np.sum(flowers)
    draws=rng.multinomial(int(visits.sum()),flower_prop,size=N_NULL)
    expected=float(np.mean([e.jsd(z,flowers) for z in draws]))
    return obs,expected,obs-expected

def analyze():
    net,ev,all_day,eligible=source_data()
    units,invalid,excluded=assemble(net,ev,all_day,eligible)
    rng=np.random.default_rng(RNG_NULL)
    byprog=defaultdict(lambda:{"bee":[],"fly":[],"delta":[]})
    dist={"bee_raw":[],"fly_raw":[],"bee_expected":[],"fly_expected":[]}
    count_flowertaxa=[]
    for prog,b,f,flower in units:
        rb,eb,cb=expected_sampling_jsd(b,flower,rng)
        rf,ef,cf=expected_sampling_jsd(f,flower,rng)
        byprog[prog]["bee"].append(cb)
        byprog[prog]["fly"].append(cf)
        byprog[prog]["delta"].append(cb-cf)
        dist["bee_raw"].append(rb)
        dist["fly_raw"].append(rf)
        dist["bee_expected"].append(eb)
        dist["fly_expected"].append(ef)
        count_flowertaxa.append(len(flower))
    pr=sorted(byprog)
    bee_means=np.array([np.mean(byprog[p]["bee"]) for p in pr],dtype=float)
    fly_means=np.array([np.mean(byprog[p]["fly"]) for p in pr],dtype=float)
    differences=bee_means-fly_means
    rngb=np.random.default_rng(RNG_BOOT)
    draw=rngb.integers(0,len(pr),size=(N_BOOT,len(pr)))
    boot=differences[draw].mean(axis=1)
    boot_bee=bee_means[draw].mean(axis=1)
    boot_fly=fly_means[draw].mean(axis=1)
    loo=(sum(differences)-differences)/(len(pr)-1)
    return {
        "status":"EXPLORATORY_RECORDED_FLOWER_SUPPLY_COMPARISON_COMPLETED",
        "source_commit":e.SOURCE_SHA,
        "source_interaction_sha256":e.EXPECTED_FILE_SHA256,
        "source_flower_sha256":"aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a",
        "estimand_freeze":SPEC,
        "source_original_networks":1864,
        "source_original_primary_eligible_networks":311,
        "n_exact_source_study_network_dates":len(units),
        "n_independent_original_programmes":len(pr),
        "n_positive_programme_delta":int(np.sum(differences>0)),
        "n_positive_programme_bee_excess":int(np.sum(bee_means>0)),
        "n_positive_programme_syrphid_excess":int(np.sum(fly_means>0)),
        "mean_excess_jsd_bee_to_source_recorded_flowers":float(np.mean(bee_means)),
        "mean_excess_jsd_syrphid_to_source_recorded_flowers":float(np.mean(fly_means)),
        "primary_delta_bee_minus_syrphid_excess_jsd":float(np.mean(differences)),
        "post_outcome_secondary_bee_bootstrap_95pct":[float(v) for v in np.percentile(boot_bee,[2.5,97.5])],
        "post_outcome_secondary_syrphid_bootstrap_95pct":[float(v) for v in np.percentile(boot_fly,[2.5,97.5])],
        "whole_programme_bootstrap_95pct":[float(v) for v in np.percentile(boot,[2.5,97.5])],
        "programme_leave_one_out_delta_range":[float(np.min(loo)),float(np.max(loo))],
        "source_units_3plus_bloom_taxa":True,
        "median_positive_source_bloom_taxa_per_date":float(np.median(count_flowertaxa)),
        "mean_raw_visit_to_bloom_jsd_by_date":{k:float(np.mean(dist[k])) for k in ("bee_raw","fly_raw")},
        "mean_finite_sampling_expected_jsd_by_date":{k:float(np.mean(dist[k])) for k in ("bee_expected","fly_expected")},
        "original_flower_count_invalid_rows":invalid,
        "source_source_date_excluded_nonexclusive_counts":dict(excluded),
        "source_recorded_counts_are_not_calibrated_true_flower_supply":True,
        "this_is_not_independent_from_previous_euppollnet_main":True,
        "measured_actual_compatible_pollen_or_seed_function":False,
        "raw_original_source_rows_redistributed":False,
        "Monte_Carlo": {"n_draws_per_guild_date":N_NULL,"bootstrap_draws":N_BOOT,
                        "seed_null":RNG_NULL,"seed_bootstrap":RNG_BOOT},
        "claim_ceiling":"source-recorded within-date flower abundance mismatch, NOT innate preference, resource competition, pollination effectiveness or fragmentation causality"
    }

def self_test():
    supply=np.array([11.,11.,11.])
    b=np.array([15,0,0])
    h=np.array([5,5,5])
    rng=np.random.default_rng(19)
    _,_,x=expected_sampling_jsd(b,supply,rng)
    _,_,y=expected_sampling_jsd(h,supply,rng)
    assert x>y and x>0
    print("EUPPOLLNET_RECORDED_SUPPLY_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.output is None:
        p.error("--output required")
    try:
        result=analyze()
    except Exception as exc:
        result={"status":"SOURCE_OR_MODEL_STOP","reason":type(exc).__name__+": "+str(exc)[:500],
                "effect_estimated":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("EUPPOLLNET_RECORDED_SUPPLY "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="EXPLORATORY_RECORDED_FLOWER_SUPPLY_COMPARISON_COMPLETED" else 1

if __name__=="__main__":
    sys.exit(main())
