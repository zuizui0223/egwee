#!/usr/bin/env python3
"""QPF007 genetic mating success SOURCE-MISSINGNESS gate only.

Read exact SHA-pinned original author mother file, original 160 stigma keys,
and merely mark necessary source values as finite/nonnegative. Never compute
mate-count distribution, correlations, visitor effects, or fitted coefficients.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import shlex

from audit_brassica_rapa_zenodo_source_keys import load_manifest, trusted_binary
from run_qpf007_brassica_2026_session_holdout import (
    PLANT_SOURCE_FILE,PLANT_SOURCE_SHA, original_stigma_keys, float_or_none,
)

COLUMNS=("session","ID_full","poll_treat","nb_visit","nb_flo_all",
         "height_max","pl_mean","gMS_fem_all")
EXPECTED_MAIN=160
EXPECTED_SESSIONS=16

def parse_source_required(binary):
    try:txt=binary.decode("utf-8-sig","strict")
    except UnicodeDecodeError:txt=binary.decode("latin-1","strict")
    lines=[x for x in txt.splitlines() if x.strip()]
    if len(lines)!=EXPECTED_MAIN+1:
        raise ValueError("Source 160 row count drift")
    header=shlex.split(lines[0],posix=True)
    if len(header)<len(COLUMNS):
        raise ValueError("Invalid original mother source header")
    positions={}
    for col in COLUMNS:
        matches=[i for i,x in enumerate(header) if x==col]
        if len(matches)!=1:
            raise ValueError("Missing/duplicated required ORIGINAL column: "+col)
        positions[col]=matches[0]
    rows=[]
    indexed=None
    for row in lines[1:]:
        cells=shlex.split(row,posix=True)
        shift=len(cells)-len(header)
        if shift not in (0,1) or (shift==1 and not cells[0].isdigit()):
            raise ValueError("Unknown original R text export leading row number")
        if indexed is None:indexed=shift
        if indexed!=shift:
            raise ValueError("Inconsistent source row index format")
        rows.append({name:cells[i+shift] for name,i in positions.items()})
    if len(rows)!=160:
        raise ValueError("Original 160 plants not retained")
    keys={(r["session"],r["ID_full"]) for r in rows}
    if len(keys)!=160 or len({r["session"] for r in rows})!=16:
        raise ValueError("Original plant/source key cardinality changed")
    return rows,keys

def coverage():
    meta=load_manifest()
    files={x.get("key") or x.get("filename"):x for x in meta["files"]}
    if PLANT_SOURCE_FILE not in files:
        raise ValueError("Original source has no main plant file")
    raw=trusted_binary(files[PLANT_SOURCE_FILE])
    if hashlib.sha256(raw).hexdigest()!=PLANT_SOURCE_SHA:
        raise ValueError("Pinned original author source SHA drift")
    rows,keys=parse_source_required(raw)
    stigma=original_stigma_keys(meta)
    if keys!=stigma:
        raise ValueError("Original plant/stigma key identity mismatch")
    missing=Counter()
    eligible_per_session=Counter()
    eligible_n=0
    treatments=set()
    for row in rows:
        treatment=row["poll_treat"].strip()
        if not treatment or treatment.casefold() in ("na","nan","none"):
            missing["poll_treat"]+=1
        else:treatments.add(treatment)
        valid=bool(treatment and treatment.casefold() not in ("na","nan","none"))
        for k in COLUMNS[3:]:
            value=float_or_none(row[k])
            if value is None or value<0:
                missing[k]+=1
                valid=False
        if valid:
            eligible_n+=1
            eligible_per_session[row["session"]]+=1
    if len(treatments)<2 or len(treatments)>5:
        raise ValueError("Unexpected original treatment category count")
    sessions=sorted({r["session"] for r in rows})
    n_per=[eligible_per_session.get(s,0) for s in sessions]
    passed=(eligible_n>=120 and len(n_per)==16 and min(n_per)>=2)
    return {
       "analysis_id":"QPF007_postprimary_genetic_mating_success_source_grain_v1",
       "status":"SOURCE_ONLY_GENETIC_TARGET_COVERAGE_VERIFIED",
       "source_record":21628183,
       "source_original_main_sha256":PLANT_SOURCE_SHA,
       "source_original_stigma_sha256":"ec7217acb683a0d0475622f3510228f3062a72a8bfd17162888f160db369a495",
       "target_literal_source_column":"gMS_fem_all",
       "source_matched_maternal_keys":len(keys),
       "source_stigma_matched_keys":len(stigma),
       "source_all_sessions":len(sessions),
       "source_treatment_category_count":len(treatments),
       "missing_or_invalid_flags_by_field":dict(missing),
       "complete_source_mothers_for_genetic_target":eligible_n,
       "complete_mother_sessions":sum(n>=1 for n in n_per),
       "min_complete_mothers_per_source_session":min(n_per),
       "max_complete_mothers_per_source_session":max(n_per),
       "median_complete_mothers_per_source_session":float(sorted(n_per)[len(n_per)//2-1]+sorted(n_per)[len(n_per)//2])/2,
       "source_numerical_mating_values_inspected_for_direction":False,
       "registered_original_seed_coverage_stop_changed":False,
       "independent_natural_study_n":1,
       "source_original_data_rows_redistributed":False,
       "model_fitted":False,
       "postprimary_genetic_source_gate_pass":passed,
       "decision":"MAY_RUN_FROZEN_GENETIC_TARGET_EXPLORATORY_TEST" if passed else "GENETIC_TARGET_COVERAGE_STOP",
    }

def self_test():
    assert len(COLUMNS)==8
    assert COLUMNS[-1]=="gMS_fem_all"
    assert float_or_none("NA") is None
    assert float_or_none("0")==0
    assert float_or_none("-1")==-1
    print("QPF007_GENETIC_SOURCE_ONLY_SYNTHETIC_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.self_test:
        self_test();return 0
    if args.output is None:ap.error("--output is required")
    try:result=coverage()
    except Exception as ex:
        result={"status":"SOURCE_OR_GRANULARITY_STOP",
                "reason":type(ex).__name__+": "+str(ex)[:250],
                "model_fitted":False,"source_original_data_rows_redistributed":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("QPF007_GENETIC_SOURCE_COVERAGE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="SOURCE_ONLY_GENETIC_TARGET_COVERAGE_VERIFIED" else 1

if __name__=="__main__":
    raise SystemExit(main())
