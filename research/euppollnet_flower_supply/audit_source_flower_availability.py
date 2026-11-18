#!/usr/bin/env python3
"""EuPPollNet floral-availability crosswalk audit, source hashes and grain only.

This gate tests *coverage* of independently measured flower-count context after
the original positive guild-JSD result. It never calculates pollen choice,
guild–plant affinity, divergence, regression or seed/fitness effects.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import hashlib
import io
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EUPP = HERE.parent / "euppollnet_guild_partition"
sys.path.insert(0, str(EUPP))
import estimate_guild_partition as e
from audit_source_schema import download_original

ORIGINAL_COUNT_PATH="Data/3_Final_data/Flower_counts.csv"
ORIGINAL_COUNT_SHA="aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a"
ORIGINAL_COUNT_ROWS=199692
FIRST_SOURCE_DATE="2026-11-18"
PROTOCOL="research/euppollnet_flower_supply/SOURCE_COVERAGE_PROTOCOL_20261118.md"

def norm(x):
    return " ".join((x or "").strip().casefold().split())

def is_real(x):
    return norm(x) not in ("", "na", "nan", "none", "null", "unknown")

def int_code(x):
    t=(x or "").strip()
    try:
        v=float(t)
        return int(v) if math.isfinite(v) and int(v)==v else None
    except ValueError:
        return None

def ymd(y,m,d):
    year,month,day=int_code(y),int_code(m),int_code(d)
    if year is None or month is None or day is None:
        return None
    try:
        return date(year,month,day).isoformat()
    except (ValueError,OverflowError):
        return None

def interaction_date(s):
    # Reuse the source-hardened date parser already tested in PR #72.
    from robustness_same_day_shared_hosts import date_literal
    return date_literal(s)

def count_rows():
    data=download_original(ORIGINAL_COUNT_PATH)
    if hashlib.sha256(data).hexdigest()!=ORIGINAL_COUNT_SHA:
        raise ValueError("SOURCE_STOP: original independent flower-count source digest")
    try:
        text=data.decode("cp1252",errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("SOURCE_STOP: nonlossless flower encoding") from exc
    reader=csv.DictReader(io.StringIO(text,newline=""))
    required={"Study_id","Network_id","Day","Month","Year","Plant_species",
              "Flower_count","Units","Flower_data_merger"}
    if reader.fieldnames is None or not required.issubset(reader.fieldnames):
        raise ValueError("SOURCE_STOP: flower count schema changed")
    rows=list(reader)
    if len(rows)!=ORIGINAL_COUNT_ROWS:
        raise ValueError("SOURCE_STOP: corrected flower row cardinality changed")
    return rows

def source_gate():
    nets=defaultdict(lambda:{"methods":set(),
                              "plants":defaultdict(lambda:[0,0]),
                              "names":defaultdict(set),"accepted":set()})
    # Source units always keep biological source study/network/year/merger/date.
    visits=defaultdict(lambda:defaultdict(lambda:[0,0]))
    coverage=Counter()
    for r in e.source_rows():
        coverage["interaction_rows"]+=1
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        dt=interaction_date(r["Date"] or "")
        year=e.year_of(r["Date"] or "")
        if not study or not network or year is None:
            coverage["interaction_missing_native_network_year"]+=1
            continue
        k=(study,network,year)
        net=nets[k]
        net["methods"].add((r["Sampling_method"] or "").strip())
        plant=norm(r["Plant_accepted_name"])
        orig=norm(r["Plant_original_name"])
        if is_real(plant):
            net["accepted"].add(plant)
            if is_real(orig):
                net["names"][orig].add(plant)
        group=e.category(r)
        if group is None:
            continue
        if not is_real(plant):
            coverage["focal_missing_accepted_plant"]+=1
            continue
        if (r["Interaction"] or "").strip() not in ("1","1.0"):
            raise ValueError("SOURCE_STOP: interaction unit no longer 1")
        idx=0 if group=="bee" else 1
        net["plants"][plant][idx]+=1
        merge=norm(r["Flower_data_merger"])
        if not is_real(merge):
            coverage["focal_no_merger"]+=1
            continue
        if dt is None:
            coverage["focal_no_exact_date"]+=1
            continue
        if dt[:4] != str(year):
            raise ValueError("SOURCE_STOP: interaction date/year conflicts")
        visits[(study,network,year,merge,dt)][plant][idx]+=1
        coverage["focal_records_with_native_merge_and_date"]+=1
    if coverage["interaction_rows"]!=e.EXPECTED_ROWS:
        raise ValueError("SOURCE_STOP: interaction row count changed")

    eligible=set()
    for k,v in nets.items():
        if len(v["methods"])!=1 or "" in v["methods"]:
            continue
        if len(v["plants"])<3:
            continue
        counts=list(v["plants"].values())
        if sum(x[0] for x in counts)>=20 and sum(x[1] for x in counts)>=20:
            eligible.add(k)
    if len(eligible)!=311 or len(nets)!=1864:
        raise ValueError(f"SOURCE_STOP: PR72 network identity changed {len(eligible)}/{len(nets)}")
    
    flower_rows=count_rows()
    flower_units=defaultdict(lambda:{"units":set(),"records":[],"invalid_numeric":0,
                                     "missing_plant":0,"total":0})
    flower_netkeys=set()
    flower_key_without_date=set()
    all_distinct_units=Counter()
    for r in flower_rows:
        study=(r["Study_id"] or "").strip()
        network=(r["Network_id"] or "").strip()
        yr=int_code(r["Year"])
        if not study or not network or yr is None:
            coverage["flower_invalid_network_year"]+=1
            continue
        netkey=(study,network,yr)
        flower_netkeys.add(netkey)
        merge=norm(r["Flower_data_merger"])
        if not is_real(merge):
            coverage["flower_no_merger"]+=1
            continue
        flower_key_without_date.add((study,network,yr,merge))
        dt=ymd(r["Year"],r["Month"],r["Day"])
        if dt is None:
            coverage["flower_missing_exact_date"]+=1
            continue
        key=(study,network,yr,merge,dt)
        group=flower_units[key]
        group["total"]+=1
        unit=norm(r["Units"])
        group["units"].add(unit)
        all_distinct_units[unit or "<missing>"]+=1
        nm=norm(r["Plant_species"])
        if not is_real(nm):
            group["missing_plant"]+=1
            continue
        v=(r["Flower_count"] or "").strip()
        try:
            count=float(v)
        except ValueError:
            group["invalid_numeric"]+=1
            continue
        if not math.isfinite(count) or count<0:
            group["invalid_numeric"]+=1
            continue
        group["records"].append((nm,count))

    coverage["flower_rows"]=len(flower_rows)
    coverage["study_network_year_eligible_original"]=len(eligible)
    eligible_prog={e.programme_of(k[0]) for k in eligible}
    coverage["source_programmes_with_original_eligible_networks"]=len(eligible_prog)
    coverage["study_network_year_with_any_flower_records"]=len(flower_netkeys)
    coverage["study_network_year_shared_before_merger_or_date"]=len(eligible & flower_netkeys)
    episodes={k:v for k,v in visits.items() if k[:3] in eligible}
    coverage["eligible_networks_with_focal_date_and_merger"]=len({k[:3] for k in episodes})
    coverage["focal_network_episodes_on_original_eligible_networks"]=len(episodes)
    flower_has_year_merger={(k[:4]) for k in flower_units}
    i_merged={(k[:4]) for k in episodes}
    coverage["study_network_year_merger_overlap_without_date"]=len(i_merged & flower_key_without_date)
    matched_keys=set(episodes).intersection(flower_units)
    coverage["same_day_study_network_year_merger_episodes"]=len(matched_keys)
    coverage["same_day_programmes"]=len({e.programme_of(k[0]) for k in matched_keys})
    coverage["source_distinct_flower_unit_labels"]=len(all_distinct_units)
    coverage["nonempty_flower_unit_labels"]=sum(bool(v) for v in all_distinct_units)
    coverage["ambiguous_original_to_accepted_mappings"]=sum(
        len(vals)>1 for k in eligible for vals in nets[k]["names"].values()
    )

    explain=Counter()
    robust_units=[]
    candidate_units=0
    matched_taxa_visits=[0,0]
    visit_totals=[0,0]
    for k in sorted(matched_keys):
        meta=flower_units[k]
        net=nets[k[:3]]
        original_to_accepted=net["names"]
        matched_supply=set()
        if meta["invalid_numeric"]:
            explain["flower_non_numeric_or_negative_rows"]+=1
        if not meta["units"] or "" in meta["units"] or len(meta["units"])!=1:
            explain["inconsistent_or_missing_units"]+=1
            continue
        if meta["missing_plant"]:
            explain["flower_missing_plant_rows"]+=1
        for raw,number in meta["records"]:
            if not number>0:
                continue
            if raw in net["accepted"]:
                matched_supply.add(raw)
            elif raw in original_to_accepted and len(original_to_accepted[raw])==1:
                matched_supply.add(next(iter(original_to_accepted[raw])))
            elif raw in original_to_accepted and len(original_to_accepted[raw])>1:
                explain["ambiguous_taxon_mapping_source_episode"]+=1
        visit=episodes[k]
        total=[sum(b[0] for b in visit.values()),sum(b[1] for b in visit.values())]
        covered=[sum(v[0] for p,v in visit.items() if p in matched_supply),
                 sum(v[1] for p,v in visit.items() if p in matched_supply)]
        for j in (0,1):
            matched_taxa_visits[j]+=covered[j]
            visit_totals[j]+=total[j]
        candidate_units+=1
        if (len(matched_supply)<3 or total[0]<20 or total[1]<20):
            explain["below_3_matched_flowering_taxa_or_20_visits_each"]+=1
            continue
        if min(covered)<20:
            explain["below_20_visits_each_on_measured_positive_flowering_taxa"]+=1
            continue
        if covered[0]/total[0]<.70 or covered[1]/total[1]<.70:
            explain["below_70pct_of_plant_visits_measured_in_both_guilds"]+=1
            continue
        robust_units.append(k)
    coverage["same_day_episodes_with_single_nonmissing_unit_label"]=candidate_units
    coverage["matched_guild_visitor_records_wild_bee"]=matched_taxa_visits[0]
    coverage["same_day_total_guild_visitor_records_wild_bee"]=visit_totals[0]
    coverage["matched_guild_visitor_records_syrphid"]=matched_taxa_visits[1]
    coverage["same_day_total_guild_visitor_records_syrphid"]=visit_totals[1]
    passing_prog={e.programme_of(k[0]) for k in robust_units}
    threshold_pass=len(robust_units)>=20 and len(passing_prog)>=5
    return {
        "status":"SOURCE_COVERAGE_VERIFIED",
        "source_commit_sha":e.SOURCE_SHA,
        "source_interaction_sha256":e.EXPECTED_FILE_SHA256,
        "source_flower_counts_sha256":ORIGINAL_COUNT_SHA,
        "source_article_correction_doi":"10.1111/geb.70054",
        "source_eligibility_gate":"exact study, network, year, merger, calendar day, one recorded flower-unit label",
        "analysis_origin":"post_primary_exploratory_not_clean_preregistration",
        "protocol":PROTOCOL,
        "coverage":dict(coverage),
        "exclusion_reason_nonexclusive_episode_counts":dict(explain),
        "strict_qualifying_flower_source_episodes":len(robust_units),
        "strict_independent_original_programmes":len(passing_prog),
        "strict_n_network_years":len({k[:3] for k in robust_units}),
        "strict_gate_threshold_pass":threshold_pass,
        "distinct_flower_unit_string_count":len(all_distinct_units),
        "flower_count_units_semantic_homogeneity_certified":False,
        "observed_guild_use_jsd_recomputed":False,
        "flower_supply_relative_preference_calculated":False,
        "pollen_deposition_or_reproductive_outcome_read":False,
        "source_raw_rows_redistributed":False,
        "decision":("ELIGIBLE_ONLY_FOR_NEW_EXPLICITLY_EXPLORATORY_SUPPLY_ANALYSIS_WITH_SECOND_FREEZE"
                    if threshold_pass else "SAME_DAY_COMPARABLE_FLOWER_SUPPLY_COVERAGE_STOP"),
    }

def test():
    assert norm("  Allium  subvillosum  ")=="allium subvillosum"
    assert ymd("2020","2","29")=="2020-02-29"
    assert ymd("2021","2","29") is None
    assert ymd("NA","1","1") is None
    assert int_code("2.0")==2 and int_code("2.1") is None
    print("SUPPLY_JOIN_SYNTHETIC_SOURCE_GATE_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:
        test()
        return 0
    if args.output is None:
        p.error("--output required")
    try:
        result=source_gate()
    except Exception as exc:
        result={"status":"SOURCE_GATE_STOP","reason":type(exc).__name__+": "+str(exc)[:500],
                "observed_guild_use_jsd_recomputed":False,
                "flower_supply_relative_preference_calculated":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("EUPPOLLNET_FLOWER_SUPPLY_COVERAGE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="SOURCE_COVERAGE_VERIFIED" else 1

if __name__=="__main__":
    sys.exit(main())
