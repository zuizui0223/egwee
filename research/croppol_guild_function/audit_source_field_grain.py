#!/usr/bin/env python3
"""CropPol field-level ecological grain/coverage audit BEFORE yield effects.

Only categorical source semantics, numeric availability and original key
cardinality are read. No signed yield values, yield/visit associations,
regression, rankings by outcome or original rows are emitted.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import csv
import io
import json
import math
from pathlib import Path

from audit_source_schema import FILES, source_bytes

NA={"","na","nan","none","null","not available","missing","unknown"}

def norm(x):
    return " ".join(str(x or "").strip().casefold().split())

def valid(x):
    return norm(x) not in NA

def num(x):
    if not valid(x):return None
    try:
        a=float(x)
        return a if math.isfinite(a) and a>=0 else None
    except (TypeError,ValueError):
        return None

def read_rows(key):
    raw=source_bytes(FILES[key])
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline="")))
    if len(rows)!={"field":3448,"sample":54191}[key]:
        raise ValueError(f"SOURCE_STOP: original CropPol {key} row grain changed")
    return rows

def source_gate():
    fields=read_rows("field")
    samples=read_rows("sample")
    required={
        "study_id","study_id2","site_id","crop","sampling_year","yield",
        "yield_units","yield2","yield2_units","use_visits_or_abundance",
        "taxa_recorded","sampling_visitation","visitation_rate",
        "visitation_rate_units","visit_honeybee","visit_bombus",
        "visit_wildbees","visit_syrphids",
    }
    if not required.issubset(fields[0].keys()):
        raise ValueError("SOURCE_STOP: missing documented field headers")
    if not {"study_id","site_id","guild","sampling_method","abundance"}.issubset(samples[0].keys()):
        raise ValueError("SOURCE_STOP: missing original sample headers")

    grain=Counter()
    labels=Counter()
    sample_labels=Counter()
    programmes=defaultdict(list)
    rowkeys=Counter()
    fieldkeys=Counter()
    study_ids=set()
    studyid2=set()
    samplekeys=Counter()
    yield_unit=Counter()
    visit_unit=Counter()
    valid_yield=0
    valid_visit=0
    both=0
    guild_visits=0
    zeros=Counter()
    missing=Counter()
    eligible_rowcount=0
    dup_field_key=0
    excluded_uncertified=Counter()
    explicit_panels=defaultdict(list)
    for row in fields:
        study=norm(row["study_id"])
        group=norm(row["study_id2"]) if valid(row["study_id2"]) else study
        site=norm(row["site_id"])
        crop=norm(row["crop"])
        yr=norm(row["sampling_year"])
        key=(study,site,yr)
        fieldkeys[key]+=1
        rowkeys[(study,site,yr,crop)]+=1
        if valid(study):study_ids.add(study)
        if valid(group):studyid2.add(group)
        y=num(row["yield"])
        v=num(row["visitation_rate"])
        valid_yield+=int(y is not None)
        valid_visit+=int(v is not None)
        both+=int(y is not None and v is not None)
        labels[("use_visits_or_abundance", norm(row["use_visits_or_abundance"]))]+=1
        labels[("taxa_recorded",norm(row["taxa_recorded"]))]+=1
        labels[("sampling_visitation",norm(row["sampling_visitation"]))]+=1
        if y is not None:yield_unit[norm(row["yield_units"])]+=1
        if v is not None:visit_unit[norm(row["visitation_rate_units"])]+=1
        nums={g:num(row[g]) for g in
              ("visit_honeybee","visit_bombus","visit_wildbees","visit_syrphids")}
        for g,n in nums.items():
            if n is None:missing[g]+=1
            elif n==0:zeros[g]+=1
            else:grain["positive_"+g]+=1
        if nums["visit_syrphids"] is not None and nums["visit_wildbees"] is not None:
            guild_visits+=1
        if not (valid(study) and valid(site) and valid(crop) and valid(yr)):
            excluded_uncertified["missing_source_field_key"]+=1
            continue
        if y is None or v is None:
            excluded_uncertified["missing_numeric_yield_or_total_visits"]+=1
            continue
        if not valid(row["yield_units"]) or not valid(row["visitation_rate_units"]):
            excluded_uncertified["missing_source_effect_unit"]+=1
            continue
        if any(x is None for x in nums.values()):
            excluded_uncertified["missing_one_of_four_recorded_guild_visit_columns"]+=1
            continue
        eligible_rowcount+=1
        # Only inspect presence & units, never retain/sign source outcome or
        # relationships to visitor counts. A panel is a source publication
        # study × crop × year × source-defined yield and visit units.
        panel=(group,crop,yr,norm(row["yield_units"]),norm(row["visitation_rate_units"]))
        explicit_panels[panel].append((study,site))
    for row in samples:
        st=norm(row["study_id"])
        si=norm(row["site_id"])
        if valid(st) and valid(si):samplekeys[(st,si)]+=1
        sample_labels[("sampling_method",norm(row["sampling_method"]))]+=1
        sample_labels[("guild",norm(row["guild"]))]+=1
    min8=[p for p,arr in explicit_panels.items() if len(arr)>=8 and len(set(arr))>=8]
    crop_programmes={p[0] for p in min8}
    true_sites=set((s,site) for key in explicit_panels for s,site in explicit_panels[key])
    source_surveys=set(samplekeys)
    result={
       "status":"ORIGINAL_CROPPOL_SOURCE_GRAIN_PASS",
       "source_commit":"99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b",
       "original_rows":{"field":len(fields),"pollinator_sampling":len(samples)},
       "n_unique_source_study_id":len(study_ids),
       "n_unique_source_study_id2_effective":len(studyid2),
       "n_field_study_site_year_keys":len(fieldkeys),
       "n_duplicate_field_study_site_year_keys":sum(v>1 for v in fieldkeys.values()),
       "n_duplicate_field_study_site_year_crop_keys":sum(v>1 for v in rowkeys.values()),
       "n_distinct_sampling_study_site_keys":len(samplekeys),
       "field_study_site_keys_present_in_sampling_files":len(true_sites & source_surveys),
       "n_finite_nonnegative_primary_yield_not_values":valid_yield,
       "n_finite_nonnegative_total_visits_not_values":valid_visit,
       "n_rows_both_yield_and_total_visits_available_not_values":both,
       "n_rows_with_both_wildbee_and_syrphid_columns_numeric_not_values":guild_visits,
       "n_rows_all_four_guild_visits_numeric_with_yield_visit_units":eligible_rowcount,
       "n_independent_study_crop_year_unit_panels_min_8_fields":len(min8),
       "n_source_programmes_with_panel_min_8_fields":len(crop_programmes),
       "n_fields_in_min8_panels":sum(len(explicit_panels[x]) for x in min8),
       "source_zero_counts":dict(zeros),
       "source_missing_guild_visit_counts":dict(missing),
       "source_positive_guild_visit_counts":dict(grain),
       "source_required_effect_unit_coverage_exclusions":dict(excluded_uncertified),
       "field_source_metadata_labels":{
           k:{v:n for (kk,v),n in labels.items() if kk==k}
           for k in ("use_visits_or_abundance","taxa_recorded","sampling_visitation")},
       "source_sampling_guild_and_method_labels":{
           k:{v:n for (kk,v),n in sample_labels.items() if kk==k}
           for k in ("guild","sampling_method")},
       "source_yield_unit_counts_not_values":dict(yield_unit),
       "source_visitation_unit_counts_not_values":dict(visit_unit),
       "yield_values_output_or_modelled":False,
       "same_unit_syphid_zero_certified_by_source_effort":False,
       "source_raw_rows_redistributed":False,
       "source_effect_estimated":False,
       "decision":"REQUIRE_GUILD_SURVEY_ZERO_VERIFICATION_BEFORE_ANY_QF_MODEL",
    }
    return result

def self_test():
    assert num("") is None
    assert num("NA") is None
    assert num("-1") is None
    assert num("0")==0
    assert num("2.5")==2.5
    assert norm(" bees and   syrphids ")=="bees and syrphids"
    print("CROPPOL_GRAIN_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        self_test();return 0
    if a.output is None:p.error("--output required")
    try:r=source_gate()
    except Exception as ex:
        r={"status":"SOURCE_OR_GRAIN_STOP",
           "reason":type(ex).__name__+": "+str(ex)[:400],
           "yield_values_output_or_modelled":False,"source_effect_estimated":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CROPPOL_PREOUTCOME_GRAIN "+json.dumps(r,sort_keys=True),flush=True)
    return 0 if r["status"]=="ORIGINAL_CROPPOL_SOURCE_GRAIN_PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
