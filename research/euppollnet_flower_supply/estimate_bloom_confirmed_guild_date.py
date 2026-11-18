#!/usr/bin/env python3
"""Post-primary, source-exact same-day BLOOM-CONFIRMED guild use test.

Dates are reconstituted only from originally linked study-network-year-merger
records, never by botanical/geographic fuzzy joins. Flower_count is used solely
to certify positive bloom availability, NOT to calibrate supply density.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import io
import json
import math
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_source_flower_availability import (
    count_rows, e, int_code, norm, is_real, ymd, interaction_date,
)

PROTOCOL="research/euppollnet_flower_supply/DATE_ASSEMBLY_FREEZE_20261118.md"
RNG_NULL=20261124
RNG_BOOT=20261125
N_NULL=199
N_BOOT=2000

def gather():
    nets=defaultdict(lambda:{"methods":set(),
                             "all_counts":defaultdict(lambda:[0,0]),
                             "orig_to_acc":defaultdict(set),"accepted":set()})
    episodes=defaultdict(lambda:defaultdict(lambda:[0,0]))
    all_day=defaultdict(lambda:[0,0])
    cov=Counter()
    for r in e.source_rows():
        cov["source_interactions"]+=1
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        date_val=interaction_date(r["Date"] or "")
        year=e.year_of(r["Date"] or "")
        if not study or not network or year is None:
            cov["bad_native_network"]+=1
            continue
        netkey=(study,network,year)
        net=nets[netkey]
        net["methods"].add((r["Sampling_method"] or "").strip())
        acc=norm(r["Plant_accepted_name"])
        raw=norm(r["Plant_original_name"])
        if is_real(acc):
            net["accepted"].add(acc)
            if is_real(raw):
                net["orig_to_acc"][raw].add(acc)
        guild=e.category(r)
        if guild is None or not is_real(acc):
            continue
        if (r["Interaction"] or "").strip() not in ("1","1.0"):
            raise ValueError("SOURCE_STOP: interaction records no longer single visit events")
        i=0 if guild=="bee" else 1
        net["all_counts"][acc][i]+=1
        if date_val is None:
            cov["focal_no_date"]+=1
            continue
        daykey=(study,network,year,date_val)
        all_day[daykey][i]+=1
        merge=norm(r["Flower_data_merger"])
        if not is_real(merge):
            cov["focal_no_merger"]+=1
            continue
        episodes[(study,network,year,merge,date_val)][acc][i]+=1
    if cov["source_interactions"]!=623476 or len(nets)!=1864:
        raise ValueError("SOURCE_STOP: published corrected original source changed")
    original_eligible=set()
    for k,net in nets.items():
        if len(net["methods"])!=1 or "" in net["methods"]:
            continue
        c=list(net["all_counts"].values())
        if len(c)>=3 and sum(v[0] for v in c)>=20 and sum(v[1] for v in c)>=20:
            original_eligible.add(k)
    if len(original_eligible)!=311:
        raise ValueError("SOURCE_STOP: primary 311-network risk set changed")
    flowers=defaultdict(lambda:{"units":set(),"records":[]})
    for r in count_rows():
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        year=int_code(r["Year"])
        dt=ymd(r["Year"],r["Month"],r["Day"])
        merge=norm(r["Flower_data_merger"])
        if not study or not network or year is None or dt is None or not is_real(merge):
            cov["flower_unverifiable_exact_date_merger"]+=1
            continue
        k=(study,network,year,merge,dt)
        entry=flowers[k]
        entry["units"].add(norm(r["Units"]))
        taxon=norm(r["Plant_species"])
        if not is_real(taxon):
            cov["flower_missing_taxon"]+=1
            continue
        try:
            v=float((r["Flower_count"] or "").strip())
        except ValueError:
            cov["flower_invalid_count"]+=1
            continue
        if not math.isfinite(v) or v<0:
            cov["flower_invalid_count"]+=1
            continue
        if v>0:
            entry["records"].append(taxon)
    cov["original_networks"]=len(nets)
    cov["original_primary_networks"]=len(original_eligible)
    cov["original_flower_rows"]=199692
    cov["exact_record_episode_keys_intersect"]=0

    # Each distinct raw source-merger episode contributes its source visit events
    # to exactly one native study/network/year/day. Counted plants are a union,
    # not summed across merger episodes (prevents counting repeated floral census).
    assembled=defaultdict(lambda:{"guild_plants":defaultdict(lambda:[0,0]),
                                  "units":set(),"bloom_raw":set(),"raw_count":0})
    for k,plants in episodes.items():
        if k[:3] not in original_eligible or k not in flowers:
            continue
        cov["exact_record_episode_keys_intersect"]+=1
        datekey=(k[0],k[1],k[2],k[4])
        dest=assembled[datekey]
        dest["units"].update(flowers[k]["units"])
        dest["bloom_raw"].update(flowers[k]["records"])
        dest["raw_count"]+=1
        for p,v in plants.items():
            dest["guild_plants"][p][0]+=v[0]
            dest["guild_plants"][p][1]+=v[1]
    cov["assembled_native_dates_with_exact_merger_matches"]=len(assembled)
    cov["assembled_programmes"]=len({e.programme_of(k[0]) for k in assembled})
    excluded=Counter()
    kept=[]
    for k,row in sorted(assembled.items()):
        if not row["units"] or "" in row["units"] or len(row["units"])!=1:
            excluded["nonuniform_or_missing_flower_units"]+=1
            continue
        net=nets[k[:3]]
        available=set()
        for raw in row["bloom_raw"]:
            if raw in net["accepted"]:
                available.add(raw)
            elif raw in net["orig_to_acc"] and len(net["orig_to_acc"][raw])==1:
                available.add(next(iter(net["orig_to_acc"][raw])))
            elif raw in net["orig_to_acc"] and len(net["orig_to_acc"][raw])>1:
                excluded["ambiguous_source_taxon_map"]+=1
        if len(available)<3:
            excluded["fewer_than_three_blooming_identifiable_taxa"]+=1
            continue
        visit=row["guild_plants"]
        visited=[p for p in sorted(available) if p in visit and sum(visit[p])>0]
        if len(visited)<3:
            excluded["fewer_than_three_bloom_confirmed_visited_taxa"]+=1
            continue
        bee=np.array([visit[p][0] for p in visited],dtype=np.int64)
        fly=np.array([visit[p][1] for p in visited],dtype=np.int64)
        if bee.sum()<10 or fly.sum()<10:
            excluded["fewer_than_ten_visits_each_on_blooming_plants"]+=1
            continue
        denom=all_day[k]
        if denom[0]<=0 or denom[1]<=0:
            excluded["invalid_source_day_totals"]+=1
            continue
        if bee.sum()/denom[0]<.70 or fly.sum()/denom[1]<.70:
            excluded["below_70pct_original_day_guild_coverage"]+=1
            continue
        kept.append((e.programme_of(k[0]),bee,fly))
    progs={x[0] for x in kept}
    gate=len(kept)>=20 and len(progs)>=5
    out={
      "status":"BLOOM_CONFIRMED_DATE_COVERAGE_COMPLETE",
      "programme_comparison_postprimary_exploratory":True,
      "source_interaction_sha256":e.EXPECTED_FILE_SHA256,
      "source_flower_sha256":"aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a",
      "source_commit":e.SOURCE_SHA,
      "date_aggregation_freeze":PROTOCOL,
      "counts":dict(cov),
      "nonexclusive_source_gate_exclusion_counts":dict(excluded),
      "qualifying_native_network_dates":len(kept),
      "qualifying_independent_original_programmes":len(progs),
      "coverage_threshold_met":gate,
      "original_author_source_rows_redistributed":False,
      "true_flower_number_supply_correction_performed":False,
      "seed_or_pollen_quality_measured":False,
    }
    if not gate:
        out.update({"status":"BLOOM_CONFIRMED_DATE_COVERAGE_STOP",
                    "effect_estimated":False,"decision":"coverage_insufficient_no_guild_JSD"})
        return out
    rng=np.random.default_rng(RNG_NULL)
    byprog=defaultdict(list)
    raw=[]
    null=[]
    for prog,bee,fly in kept:
        obs,exp,excess=e.sample_excess(bee,fly,rng,N_NULL)
        byprog[prog].append(excess)
        raw.append(obs)
        null.append(exp)
    means=np.array([np.mean(byprog[p]) for p in sorted(byprog)],dtype=float)
    rng_boot=np.random.default_rng(RNG_BOOT)
    boot=means[rng_boot.integers(0,len(means),size=(N_BOOT,len(means)))].mean(axis=1)
    loo=(means.sum()-means)/(len(means)-1)
    out.update({
        "status":"POSTPRIMARY_BLOOM_CONFIRMED_DATE_ESTIMATED",
        "effect_estimated":True,
        "null":"hypergeometric_shuffle_within_exact_network_date_conditioning_on_pooled_visited_plants",
        "not_a_quantitative_flower_supply_correction":True,
        "mean_excess_JSD_nats_equal_programme":float(means.mean()),
        "whole_programme_bootstrap_95pct":[float(x) for x in np.percentile(boot,[2.5,97.5])],
        "n_positive_programme_means":int((means>0).sum()),
        "programme_LOO_mean_range":[float(np.min(loo)),float(np.max(loo))],
        "observed_JSD_equal_date_mean":float(np.mean(raw)),
        "expected_shuffled_JSD_equal_date_mean":float(np.mean(null)),
        "n_null_per_date":N_NULL,"n_bootstrap":N_BOOT,
        "rng_seed_null":RNG_NULL,"rng_seed_bootstrap":RNG_BOOT,
        "decision":"exploratory_observed_use_partition_among_bloom_confirmed_host_taxa_only",
    })
    return out

def self_test():
    assert ymd("2020","6","1")=="2020-06-01"
    assert norm("  Rosa  rugosa ")=="rosa rugosa"
    b=np.array([10,0,3])
    f=np.array([0,12,3])
    obs,expect,excess=e.sample_excess(b,f,np.random.default_rng(3),199)
    assert excess>0 and obs>expect>=0
    print("BLOOM_CONFIRMED_SOURCE_DATE_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test();return 0
    if a.output is None:
        p.error("--output required")
    try:
        result=gather()
    except Exception as exc:
        result={"status":"SOURCE_OR_UNIT_STOP","reason":type(exc).__name__+": "+str(exc)[:500],
                "effect_estimated":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("BLOOM_CONFIRMED_GUILD_DATE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"] in (
        "POSTPRIMARY_BLOOM_CONFIRMED_DATE_ESTIMATED",
        "BLOOM_CONFIRMED_DATE_COVERAGE_STOP") else 1

if __name__=="__main__":
    sys.exit(main())
