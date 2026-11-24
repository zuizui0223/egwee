#!/usr/bin/env python3
"""LUPF1 post-stop data-quality diagnosis: no coefficients, treatment effects, or raw rows.

After SOURCE_ENDPOINT_INVALID_STOP (run 45328288235), classify all original
seed/onset values into MISSING, NONNUMERIC, NEGATIVE, FRACTIONAL,
VALID_NONNEGATIVE_INTEGER. This is NOT a revision of the frozen analysis.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import math
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from run_lupf1_genotype_holdout import (
    ARTICLE, NAME, FREEZE, download, decode_source_sheet,
    numeric, clean, freeze_gate, SourceStop
)

def classify_seed(v):
    s=clean(v)
    if not s or s.casefold() in {"na","n/a","nan","null","#n/a","none"}:
        return "MISSING_OR_NA"
    x=numeric(s)
    if x is None:
        return "NONNUMERIC_OR_NONFINITE"
    if x<0: return "NEGATIVE"
    if abs(x-round(x))>1e-7: return "NONINTEGER"
    return "VALID_INTEGER"

def classify_onset(v):
    s=clean(v)
    if not s or s.casefold() in {"na","n/a","nan","null","#n/a","none"}:
        return "MISSING_OR_NA"
    x=numeric(s)
    if x is None: return "NONNUMERIC_OR_NONFINITE"
    if x<0: return "NEGATIVE"
    return "VALID_NONNEGATIVE"

def diagnose(rows):
    status_seed=Counter()
    status_onset=Counter()
    pair=Counter()
    valid_core=0
    for row in rows:
        core=(clean(row.get("population")) in {"FRO","PIC"}
              and clean(row.get("line")) in {"C","J","L","R","T","X"}
              and bool(clean(row.get("genotype"))))
        if core:valid_core+=1
        s=classify_seed(row.get("number_of_seeds"))
        p=classify_onset(row.get("flowering_onset"))
        status_seed[s]+=1
        status_onset[p]+=1
        pair[s+"__"+p]+=1
    n=len(rows)
    assert sum(status_seed.values())==sum(status_onset.values())==n
    both=sum(k.startswith("VALID_INTEGER__VALID_NONNEGATIVE")*v for k,v in pair.items())
    return {
        "status":"POST_STOP_OUTCOME_VALIDITY_ONLY",
        "original_rows":n,
        "valid_core_source_labels":valid_core,
        "seed_value_categories":dict(sorted(status_seed.items())),
        "onset_value_categories":dict(sorted(status_onset.items())),
        "seed_and_onset_both_valid_rows":both,
        "new_predictive_model_ran":False,
        "frozen_model_redefined":False,
        "source_values_or_individual_ids_exported":False,
        "genotype_SNP_values_read":False,
        "genetic_intervention_effect_estimated":False,
        "ecological_interaction_function_validated":False,
        "decision":"SOURCE_ENDPOINT_INVALID_STOP_MAINTAINED"
    }

def run():
    freeze_gate()
    metadata=json.loads(download(f"https://api.figshare.com/v2/articles/{ARTICLE}").decode())
    ds=str(metadata.get("doi","")).lower().removeprefix("https://doi.org/")
    if ds!="10.6084/m9.figshare.29606180" and not ds.startswith("10.6084/m9.figshare.29606180.v"):
        raise SourceStop("SOURCE_DOI_MISMATCH")
    files=[f for f in metadata.get("files",[]) if f.get("name")==NAME]
    if len(files)!=1:raise SourceStop("SOURCE_FILE_NOT_UNIQUE")
    url=files[0].get("download_url","")
    if urlparse(url).scheme!="https" or urlparse(url).hostname not in {
            "figshare.com","ndownloader.figshare.com","api.figshare.com"}:
        raise SourceStop("UNREGISTERED_DOWNLOAD_HOST")
    blob=download(url)
    rows=decode_source_sheet(blob)
    x=diagnose(rows)
    x.update(source_article_id=ARTICLE,original_sha256=hashlib.sha256(blob).hexdigest(),
             pre_outcome_protocol_commit=FREEZE)
    return x

if __name__=="__main__":
    try: r=run()
    except (SourceStop,HTTPError,URLError,ValueError,KeyError,TypeError,IndexError) as exc:
        r={"status":"SOURCE_DIAGNOSTIC_ACCESS_OR_SCHEMA_STOP",
           "reason_type":type(exc).__name__,"new_predictive_model_ran":False,
           "source_values_or_individual_ids_exported":False,
           "decision":"SOURCE_ENDPOINT_INVALID_STOP_MAINTAINED"}
    print(json.dumps(r,indent=2,ensure_ascii=False))
