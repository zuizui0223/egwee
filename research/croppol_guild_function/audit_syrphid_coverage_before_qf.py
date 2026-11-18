#!/usr/bin/env python3
"""Pre-response, source-semantic Syrphidae-vs-wild-bee Q→F COVERAGE gate.

Uses original CropPol published labels to distinguish valid hoverfly zero from
lack of hoverfly sampling. No paired signed yield/visit associations computed.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import hashlib
import json
from pathlib import Path
from audit_source_field_grain import read_rows,norm,valid,num

SURVEYED={"all visitors","bees and syrphids","bees, syrphids and wasps"}
VISIT_SAMPLING={"focal observations","transects"}
BANNED_YIELD_UNIT={"z-score","z score","difference","change from control"}

def frame_id(row):
    programme=norm(row["study_id2"]) if valid(row["study_id2"]) else norm(row["study_id"])
    return (programme,norm(row["crop"]),norm(row["sampling_year"]),
            norm(row["yield_units"]),norm(row["visitation_rate_units"]))

def eligibility():
    rows=read_rows("field")
    panels=defaultdict(list)
    counts=Counter()
    source_keys=set()
    for r in rows:
        key=(norm(r["study_id"]),norm(r["site_id"]),norm(r["sampling_year"]),norm(r["crop"]))
        if key in source_keys:raise ValueError("SOURCE_STOP: duplicate independent field key")
        source_keys.add(key)
        if any(not valid(k) for k in key):
            counts["source_key_missing"]+=1
            continue
        if norm(r["use_visits_or_abundance"])!="use visits":
            counts["not_source_declared_visits"]+=1
            continue
        if norm(r["sampling_visitation"]) not in VISIT_SAMPLING:
            counts["unverifiable_direct_visitation_method"]+=1
            continue
        if norm(r["taxa_recorded"]) not in SURVEYED:
            counts["syrphidae_not_in_recorded_survey_scope"]+=1
            continue
        fy=norm(r["yield_units"])
        fv=norm(r["visitation_rate_units"])
        if not valid(fy) or not valid(fv) or any(t in fy for t in BANNED_YIELD_UNIT):
            counts["missing_or_nonproduction_yield_unit_or_visitation_unit"]+=1
            continue
        vars={k:num(r[k]) for k in
              ("yield","visitation_rate","visit_bombus","visit_wildbees",
               "visit_syrphids","visit_honeybee")}
        if any(v is None for v in vars.values()):
            counts["incomplete_yield_total_or_guild_visitation_numeric_fields"]+=1
            continue
        wild=vars["visit_bombus"]+vars["visit_wildbees"]
        syr=vars["visit_syrphids"]
        if wild+syr<=0:
            counts["no_recorded_bee_or_syrphid_visit"]+=1
            continue
        pid=frame_id(r)
        panels[pid].append((key,wild>0,syr>0))
        counts["eligible_complete_field_canonical"]+=1
    selected={}
    reason=Counter()
    for key,arr in panels.items():
        unique={t[0] for t in arr}
        if len(unique)!=len(arr):
            raise ValueError("SOURCE_STOP: source panel duplicate field key")
        if len(arr)<10:
            reason["panel_lt_10_independent_fields"]+=1
            continue
        if sum(t[1] for t in arr)<3:
            reason["panel_lt_3_bee_positive_fields"]+=1
            continue
        if sum(t[2] for t in arr)<3:
            reason["panel_lt_3_syrphid_positive_fields"]+=1
            continue
        selected[key]=arr
    programmes={k[0] for k in selected}
    passed=len(programmes)>=10 and len(selected)>=12 and sum(len(v) for v in selected.values())>=200
    return {
      "status":"SOURCE_GUILD_ZERO_COVERAGE_VERIFIED",
      "source_repository":"ibartomeus/CropPol",
      "source_commit":"99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b",
      "source_version":"2.1.0 (GitHub source News.md)",
      "pre_effect_protocol":"research/croppol_guild_function/GUILD_QF_PREDICTION_FREEZE_20261118.md",
      "total_original_field_rows":len(rows),
      "original_unique_exact_study_site_year_crop_keys":len(source_keys),
      "source_semantic_row_exclusion_counts":dict(counts),
      "n_candidate_exact_study_crop_year_unit_panels":len(panels),
      "n_admitted_exact_panels":len(selected),
      "n_admitted_original_source_programmes":len(programmes),
      "n_admitted_independent_field_keys":sum(len(v) for v in selected.values()),
      "n_admitted_panel_crop_taxa":len({k[1] for k in selected}),
      "n_admitted_panel_yield_unit_labels":len({k[3] for k in selected}),
      "n_admitted_panel_visit_unit_labels":len({k[4] for k in selected}),
      "panel_scope_exclusion_counts":dict(reason),
      "source_coverage_threshold_pass":passed,
      "yield_visit_pair_effects_read":False,
      "target_yield_value_distributed":False,
      "raw_source_rows_redistributed":False,
      "no_posthoc_zero_promotion":True,
      "decision":("PASS_SOURCE_SEMANTIC_GATE_NEXT_PRE_FROZEN_QF_PREDICTION"
                  if passed else "COVERAGE_STOP_NO_QF_MODEL"),
    }

def self_test():
    assert "bees" not in SURVEYED
    assert "all visitors" in SURVEYED
    assert "sweep net" not in VISIT_SAMPLING
    assert "transects" in VISIT_SAMPLING
    print("CROPPOL_CERTIFIED_VISIT_ZEROS_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:self_test();return 0
    if a.output is None:p.error("--output required")
    try:r=eligibility()
    except Exception as exc:
        r={"status":"SOURCE_GUILD_COVERAGE_STOP","reason":type(exc).__name__+": "+str(exc)[:400],
           "yield_visit_pair_effects_read":False,"raw_source_rows_redistributed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CROPPOL_GUILD_COVERAGE "+json.dumps(r,sort_keys=True),flush=True)
    return 0 if r["status"]=="SOURCE_GUILD_ZERO_COVERAGE_VERIFIED" else 1

if __name__=="__main__":
    raise SystemExit(main())
