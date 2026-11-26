#!/usr/bin/env python3
"""Posthoc observational support audit for executed LUPF2: NO new model fit.

Only per anonymized population×line completeness counts and source label-group
denominators. No biological code meanings inferred and no individual values emitted.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlparse
from urllib.error import HTTPError,URLError

sys.path.insert(0,str(Path(__file__).resolve().parent))
import run_lupf1_genotype_holdout as src
import run_lupf2_exploratory_continuous_seed as exp

SOURCE_SHA="7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734"

def aggregate(rows, check_denominator=True):
    out={}
    raw_groups=defaultdict(set)
    for row in rows:
        pop,code,g=[src.clean(row.get(x)) for x in ("population","line","genotype")]
        if pop not in {"FRO","PIC"} or code not in exp.SOURCE_COUNTS or not g:
            raise src.SourceStop("CORE_SOURCE_LABELS_INVALID")
        label=pop+"|"+code
        raw_groups[label].add(pop+"|"+g)
        item=out.setdefault(label,Counter())
        item["total"]+=1
        seed=exp.continuous_numeric(row.get("number_of_seeds"),"SEED")
        onset=exp.continuous_numeric(row.get("flowering_onset"),"ONSET")
        if seed is None and onset is None:item["both_missing"]+=1
        elif seed is None:item["seed_missing_only"]+=1
        elif onset is None:item["onset_missing_only"]+=1
        else:item["both_present"]+=1
        if seed is not None:
            if seed==0:item["observed_zero_source_index"]+=1
            if abs(seed-round(seed))>1e-7:item["fractional_source_index"]+=1
    result={
        "status":"POSTHOC_OBSERVATION_SUPPORT_ONLY",
        "no_new_model_fitted":True,
        "no_new_effect_estimated":True,
        "anonymous_line_codebook_verified":False,
        "individual_values_redistributed":False,
        "source_genotype_calls_read":False,
        "study_scope":"same 2026 two-founder-population programme",
        "source_original_sha256":SOURCE_SHA,
        "strata":[{"population_code":label.split("|",1)[0],
                   "anonymous_line_code":label.split("|",1)[1],
                   "n_source_rows":ct["total"],
                   "n_both_present":ct["both_present"],
                   "n_both_missing":ct["both_missing"],
                   "n_seed_missing_only":ct["seed_missing_only"],
                   "n_onset_missing_only":ct["onset_missing_only"],
                   "n_explicit_zero_numeric_seed":ct["observed_zero_source_index"],
                   "n_fractional_numeric_seed":ct["fractional_source_index"],
                   "n_source_genotype_label_groups":len(raw_groups[label]),
                  } for label,ct in sorted(out.items())],
    }
    if check_denominator:
        if sum(x["n_source_rows"] for x in result["strata"])!=3024:
            raise src.SourceStop("SOURCE_DENOMINATOR_CHANGED")
        if sum(x["n_both_present"] for x in result["strata"])!=2008:
            raise src.SourceStop("SOURCE_ELIGIBLE_COUNT_CHANGED")
    return result

def run():
    m=json.loads(src.download(f"https://api.figshare.com/v2/articles/{src.ARTICLE}").decode())
    doi=str(m.get("doi","")).lower().removeprefix("https://doi.org/")
    if not(doi=="10.6084/m9.figshare.29606180" or
           doi.startswith("10.6084/m9.figshare.29606180.v")):
        raise src.SourceStop("SOURCE_DOI_MISMATCH")
    files=[f for f in m.get("files",[]) if f.get("name")==src.NAME]
    if len(files)!=1:raise src.SourceStop("SOURCE_FILE_NOT_UNIQUE")
    url=files[0].get("download_url","")
    if urlparse(url).scheme!="https" or urlparse(url).hostname not in {
        "api.figshare.com","ndownloader.figshare.com","figshare.com"}:
        raise src.SourceStop("UNAPPROVED_SOURCE_HOST")
    buf=src.download(url)
    if hashlib.sha256(buf).hexdigest()!=SOURCE_SHA:
        raise src.SourceStop("ORIGINAL_SOURCE_SHA_MISMATCH")
    rows=src.decode_source_sheet(buf)
    return aggregate(rows)

if __name__=="__main__":
    try:r=run()
    except (src.SourceStop,HTTPError,URLError,ValueError,KeyError,TypeError,IndexError) as e:
        r={"status":"POSTHOC_SUPPORT_SOURCE_STOP","reason_type":type(e).__name__,
           "no_new_model_fitted":True,"no_new_effect_estimated":True,
           "individual_values_redistributed":False,
           "anonymous_line_codebook_verified":False}
    print(json.dumps(r,ensure_ascii=False,indent=2))
