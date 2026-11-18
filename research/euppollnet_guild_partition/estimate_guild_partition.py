#!/usr/bin/env python3
"""Study-clustered, finite-sample-corrected wild-bee vs syrphid floral-use partition.

Predefined estimand: PROTOCOL_20261118.md was committed before opening
original author interaction values. Original author CSV never redistributed.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
import urllib.request

import numpy as np

SOURCE_SHA="31716d21d5aad8c27c1d91dd0620149ef42e8836"
SOURCE_PATH="Data/3_Final_data/Interaction_data.csv.gz"
EXPECTED_FILE_SHA256="6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a"
EXPECTED_ROWS=623476
SEED_NULL=20261118
SEED_BOOT=20261119
N_NULL=199
N_BOOT=2000
GUILD_BEE_FAMILIES={
    "apidae","megachilidae","andrenidae","halictidae",
    "colletidae","melittidae","stenotritidae",
}
GUILD_FLY_FAMILY="syrphidae"


def source_rows():
    url=f"https://raw.githubusercontent.com/joseblanuza/EuPPollNet/{SOURCE_SHA}/{SOURCE_PATH}"
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-original-source-guild-partition/1.0"})
    with urllib.request.urlopen(req,timeout=120) as response:
        blocks=[]
        total=0
        while True:
            b=response.read(1024*1024)
            if not b:
                break
            blocks.append(b)
            total+=len(b)
            if total>8*1024*1024:
                raise ValueError("SOURCE_STOP: gzip download larger than expected 8 MiB cap")
    compressed=b"".join(blocks)
    if hashlib.sha256(compressed).hexdigest()!=EXPECTED_FILE_SHA256:
        raise ValueError("SOURCE_STOP: original author source SHA256 mismatch")
    uncompressed=gzip.decompress(compressed)
    if len(uncompressed)>256*1024*1024:
        raise ValueError("SOURCE_STOP: uncompressed CSV exceeds cap")
    # Source has non-UTF8 bytes. Source-schema gate established strict lossless latin-1.
    rdr=csv.DictReader(io.StringIO(uncompressed.decode("latin-1"),newline=""))
    required={"Study_id","Network_id","Date","Sampling_method","Interaction",
              "Plant_accepted_name","Pollinator_accepted_name",
              "Pollinator_family","Pollinator_order"}
    if not rdr.fieldnames or not required.issubset(rdr.fieldnames):
        raise ValueError("SCHEMA_STOP: required source columns absent")
    for row in rdr:
        yield row


def year_of(raw):
    t=raw.strip()
    if not t or t.upper() in {"NA","NULL","NAN"}:
        return None
    for pattern in ("%Y-%m-%d","%Y/%m/%d","%d/%m/%Y","%d-%m-%Y",
                    "%Y-%m-%d %H:%M:%S","%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(t,pattern).year
        except ValueError:
            continue
    # Cannot impute year from site or study chronology.
    return None


def programme_of(study_id):
    m=re.match(r"^([0-9]+)_",study_id)
    if m and int(m.group(1)) in (23,24,25):
        return "source-split-23-24-25"
    return study_id


def category(row):
    family=(row["Pollinator_family"] or "").strip().lower()
    order=(row["Pollinator_order"] or "").strip().lower()
    species=(row["Pollinator_accepted_name"] or "").strip().lower()
    if (family in GUILD_BEE_FAMILIES and order=="hymenoptera"
            and not species.startswith("apis mellifera")):
        return "bee"
    if family==GUILD_FLY_FAMILY and order=="diptera":
        return "syrphid"
    return None


def harvest():
    nets=defaultdict(lambda: {"guild_plant_counts":defaultdict(lambda: [0,0]),
                              "methods":set()})
    coverage=Counter()
    seen_studies=set()
    for row in source_rows():
        coverage["source_interaction_rows"]+=1
        study=(row["Study_id"] or "").strip()
        network=(row["Network_id"] or "").strip()
        year=year_of(row["Date"] or "")
        if not study or not network or year is None:
            coverage["invalid_study_network_year"]+=1
            continue
        seen_studies.add(study)
        mode=(row["Sampling_method"] or "").strip()
        k=(study,network,year)
        nets[k]["methods"].add(mode)
        group=category(row)
        if group is None:
            coverage["nonfocal_or_unclassified_guild"]+=1
            continue
        plant=(row["Plant_accepted_name"] or "").strip()
        if plant.lower() in ("","na","unknown","null","nan"):
            coverage["missing_accepted_plant_taxon"]+=1
            continue
        # Original corrected EuPPollNet data are one interaction record per row,
        # per published author code using n(); reject nonunit incidence encoding.
        interaction=(row["Interaction"] or "").strip()
        if interaction not in ("1","1.0"):
            coverage["non_unit_Interaction_field"]+=1
            # Continue solely for coverage; mandatory global STOP before effects.
            continue
        a=nets[k]["guild_plant_counts"][plant]
        a[0 if group=="bee" else 1]+=1
        coverage["focal_wild_bee" if group=="bee" else "focal_hoverfly"]+=1
    if coverage["source_interaction_rows"]!=EXPECTED_ROWS:
        raise ValueError("SOURCE_STOP: source cardinality changed")
    # The source may code an interaction indicator differently; stop rather than silently
    # interpreting a count/weight as a single visit.
    if coverage["non_unit_Interaction_field"]:
        raise ValueError("UNIT_STOP: source 'Interaction' field not uniformly unit-coded; "
                         f"{coverage['non_unit_Interaction_field']} focal rows ambiguous")
    return nets,coverage,seen_studies


def jsd(b,h):
    b=np.asarray(b,dtype=float)
    h=np.asarray(h,dtype=float)
    if b.sum()<=0 or h.sum()<=0:
        raise ValueError("no information for within-network guild JSD")
    p=b/b.sum()
    q=h/h.sum()
    mix=(p+q)/2
    bp=p>0
    hq=q>0
    return float(0.5*((p[bp]*np.log(p[bp]/mix[bp])).sum()
                      +(q[hq]*np.log(q[hq]/mix[hq])).sum()))


def sample_excess(b,h,rng,n_null=N_NULL):
    b=np.asarray(b,dtype=np.int64)
    h=np.asarray(h,dtype=np.int64)
    n=b+h
    obs=jsd(b,h)
    sims=np.asarray(rng.multivariate_hypergeometric(n,int(b.sum()),size=n_null))
    nulls=[jsd(sim,n-sim) for sim in sims]
    return obs, float(np.mean(nulls)), obs-float(np.mean(nulls))


def analyze(nets,coverage,seen_studies):
    rng=np.random.default_rng(SEED_NULL)
    selected=[]
    exclusions=Counter()
    for key in sorted(nets):
        row=nets[key]
        if len(row["methods"])!=1 or "" in row["methods"]:
            exclusions["ambiguous_source_method_network"]+=1
            continue
        groups=row["guild_plant_counts"]
        counts=[groups[p] for p in sorted(groups)]
        b=np.array([c[0] for c in counts],dtype=np.int64)
        h=np.array([c[1] for c in counts],dtype=np.int64)
        if len(counts)<3 or b.sum()<20 or h.sum()<20:
            exclusions["below_fixed_counts_or_plant_threshold"]+=1
            continue
        obs,null,excess=sample_excess(b,h,rng)
        selected.append({
            "programme":programme_of(key[0]),
            "sampling_method":next(iter(row["methods"])),
            "excess":excess,"observed":obs,"null":null,
        })
    study=defaultdict(list)
    for r in selected:
        study[r["programme"]].append(r["excess"])
    programme_means=np.array([float(np.mean(study[k])) for k in sorted(study)])
    if len(study)<5 or len(selected)<20:
        return {"status":"COVERAGE_STOP",
                "coverage":{"total_source_rows":coverage["source_interaction_rows"],
                            "n_original_study_ids":len(seen_studies),
                            "n_networks_keys":len(nets),
                            "n_eligible_networks":len(selected),
                            "n_eligible_programmes":len(study),
                            "exclusions":dict(exclusions),
                            "row_classification":dict(coverage)},
                "effects_reported":False}
    rng_boot=np.random.default_rng(SEED_BOOT)
    index=rng_boot.integers(0,len(programme_means),
                            size=(N_BOOT,len(programme_means)))
    boot_means=programme_means[index].mean(axis=1)
    global_mean=float(programme_means.mean())
    ci=[float(x) for x in np.percentile(boot_means,[2.5,97.5])]
    pos=int((programme_means>0).sum())
    loo=[float((programme_means.sum()-v)/(len(programme_means)-1))
         for v in programme_means]
    by_method=defaultdict(list)
    for r in selected:
        by_method[r["sampling_method"]].append(r["excess"])
    return {
        "status":"PRIMARY_ESTIMATED",
        "coverage":{"total_source_rows":coverage["source_interaction_rows"],
                    "n_original_study_ids":len(seen_studies),
                    "n_original_programmes_with_eligible_networks":len(study),
                    "n_networks_keys":len(nets),
                    "n_eligible_networks":len(selected),
                    "n_eligible_programmes":len(study),
                    "exclusions":dict(exclusions),
                    "row_classification":dict(coverage),
                    "n_eligible_networks_per_programme_distribution": {
                        "min":min(map(len,study.values())),
                        "median":float(np.median(list(map(len,study.values())))),
                        "max":max(map(len,study.values())),
                    }},
        "primary":{
            "estimand":"equally weighted programme mean of network JSD_observed-minus-hypergeometric-expected",
            "unit":"nats of Jensen-Shannon divergence",
            "equal_study_mean_excess":global_mean,
            "equal_study_95pct_bootstrap_CI":ci,
            "programme_bootstrap_replicates":N_BOOT,
            "null_draws_per_network":N_NULL,
            "programmes_with_positive_excess":pos,
            "fraction_programmes_positive":pos/len(study),
            "programme_LOO_range":[min(loo),max(loo)],
            "directional_support_frozen_rule":ci[0]>0 and pos/len(study)>=0.70,
        },
        "secondary":{
            "equal_network_mean_excess":float(np.mean([r["excess"] for r in selected])),
            "observed_JSD_equal_network_mean":float(np.mean([r["observed"] for r in selected])),
            "expected_null_JSD_equal_network_mean":float(np.mean([r["null"] for r in selected])),
            "method_N_and_mean_excess": {
                k:{"n_networks":len(v),"mean_excess":float(np.mean(v))}
                for k,v in sorted(by_method.items())
            },
        },
        "original_source_rows_distributed":False,
        "biological_limit":"Observed visit-guild flower partition only; not flower availability, fertility, compatible pollen or causal fragmentation",
    }


def self_test():
    p=np.array([30,0,10])
    h=np.array([0,30,10])
    r=np.random.default_rng(24)
    obs,expected,excess=sample_excess(p,h,r)
    if obs<=0 or excess<=0 or expected<0:
        raise AssertionError("Synthetic split-guild high-JSD scenario failed")
    e=np.random.default_rng(2)
    z=e.multivariate_hypergeometric(np.array([10,15,9]),12,size=10)
    if not (z.shape==(10,3) and np.all(z.sum(axis=1)==12)):
        raise AssertionError("Finite-population hypergeometric source null failed")
    print("EUPPOLLNET_GUILD_SYNTHETIC_PASS "+json.dumps({"example_observed":obs,"null_mean":expected}))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        self_test()
        return 0
    if a.output is None:
        p.error("--output required unless --self-test")
    receipt={
        "protocol":"research/euppollnet_guild_partition/PROTOCOL_20261118.md",
        "source_commit_sha":SOURCE_SHA,
        "source_csv_gzip_sha256":EXPECTED_FILE_SHA256,
        "correction_doi":"10.1111/geb.70054",
        "source_observation_grain":"one original corrected interaction row per recorded visitor-plant interaction",
        "null_seed":SEED_NULL,"programme_bootstrap_seed":SEED_BOOT,
    }
    try:
        nets,counts,studies=harvest()
        receipt.update(analyze(nets,counts,studies))
    except Exception as exc:
        receipt["status"]="SOURCE_OR_MODEL_STOP"
        receipt["reason"]=type(exc).__name__+": "+str(exc)[:350]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("EUPPOLLNET_GUILD_DERIVED "+json.dumps(receipt,sort_keys=True),flush=True)
    return 0 if receipt["status"] in ("PRIMARY_ESTIMATED","COVERAGE_STOP") else 1


if __name__=="__main__":
    sys.exit(main())
