#!/usr/bin/env python3
"""LUPF2: explicitly exploratory source-stored continuous seed-proxy audit.

Original LUPF1 remains stopped; same model/folds, but source-supported
nonnegative fractional seeds are retained. Lock the new protocol's ancestry.
Never call this a confirmatory outcome, genetic rescue, or G×I×F test.
"""
from __future__ import annotations
from collections import Counter
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse
from urllib.error import HTTPError,URLError

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import run_lupf1_genotype_holdout as base

FREEZE="053eca26bc1b527e828cb82cbac9318d20be7621"
MISSING={"na","n/a","nan","null","#n/a","none",""}
SOURCE_COUNTS={"C":720,"J":648,"L":720,"R":144,"T":720,"X":72}

def freeze_gate():
    base.freeze_gate()
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE,"HEAD"],
                   cwd=ROOT,check=True,stdout=subprocess.DEVNULL)

def continuous_numeric(value, name):
    raw=base.clean(value)
    if raw.casefold() in MISSING:
        return None
    out=base.numeric(raw)
    if out is None or out<0:
        raise base.SourceStop("SOURCE_"+name+"_INVALID_STOP")
    return out

def source_prepare(rows, check_denominator=True):
    if check_denominator and len(rows)!=3024:
        raise base.SourceStop("SOURCE_ROW_COUNT_MISMATCH")
    pop_counts,line_counts=Counter(),Counter()
    missing, flags=Counter(),Counter()
    records,groups=[],set()
    for row in rows:
        pop,code,g=[base.clean(row.get(k)) for k in ("population","line","genotype")]
        pop_counts[pop]+=1
        line_counts[code]+=1
        if pop not in {"FRO","PIC"} or code not in SOURCE_COUNTS or not g:
            raise base.SourceStop("SOURCE_CORE_LABELS_INVALID")
        group=pop+"|"+g
        groups.add(group)
        y=continuous_numeric(row.get("number_of_seeds"),"SEED")
        onset=continuous_numeric(row.get("flowering_onset"),"ONSET")
        if y is None:missing["missing_seed_index"]+=1
        else:
            if abs(y-round(y))>1e-7:flags["fractional_nonnegative_seed_index"]+=1
            else:flags["integer_nonnegative_seed_index"]+=1
            if y==0:flags["explicit_source_zero_seed_index"]+=1
        if onset is None:missing["missing_onset"]+=1
        if y is not None and onset is None:
            flags["seed_numeric_onset_missing"]+=1
        if y is None or onset is None:continue
        records.append((pop,code,group,onset,y))
    if check_denominator:
        if pop_counts!=Counter({"FRO":1584,"PIC":1440}):
            raise base.SourceStop("SOURCE_POPULATION_DENOMINATOR_MISMATCH")
        if line_counts!=Counter(SOURCE_COUNTS):
            raise base.SourceStop("SOURCE_LINE_DENOMINATOR_MISMATCH")
        if len(groups)!=84:raise base.SourceStop("SOURCE_GENOTYPE_GROUP_COUNT_MISMATCH")
        if (missing["missing_seed_index"]!=990 or missing["missing_onset"]!=982 or
            flags["fractional_nonnegative_seed_index"]!=153 or
            flags["integer_nonnegative_seed_index"]!=1881):
            raise base.SourceStop("SOURCE_PRIOR_ENDPOINT_AUDIT_COUNT_MISMATCH")
    return records,missing,flags,len(groups)

def run():
    freeze_gate()
    m=json.loads(base.download(f"https://api.figshare.com/v2/articles/{base.ARTICLE}").decode())
    doi=str(m.get("doi","")).lower().removeprefix("https://doi.org/")
    if not (doi=="10.6084/m9.figshare.29606180" or
            doi.startswith("10.6084/m9.figshare.29606180.v")):
        raise base.SourceStop("SOURCE_DOI_MISMATCH")
    files=[f for f in m.get("files",[]) if f.get("name")==base.NAME]
    if len(files)!=1:raise base.SourceStop("SOURCE_FILE_NOT_UNIQUE")
    url=files[0].get("download_url","")
    if urlparse(url).scheme!="https" or urlparse(url).hostname not in {
       "api.figshare.com","figshare.com","ndownloader.figshare.com"}:
        raise base.SourceStop("UNREGISTERED_DOWNLOAD_HOST")
    blob=base.download(url)
    rows=base.decode_source_sheet(blob)
    recs,missing,flags,groups=source_prepare(rows)
    metric=base.evaluate(recs)
    val=metric.pop("decision")
    result={
      "status":"EXPLORATORY_SOURCE_CONTINUOUS_SEED_AUDIT_COMPLETE",
      "new_exploratory_protocol_commit":FREEZE,
      "original_lupf1_preregistered_status":"SOURCE_ENDPOINT_INVALID_STOP",
      "original_source_article_id":base.ARTICLE,
      "source_workbook_sha256":hashlib.sha256(blob).hexdigest(),
      "all_original_rows":len(rows),
      "observed_source_genotype_groups":groups,
      "source_missingness":dict(sorted(missing.items())),
      "source_category_flags":dict(sorted(flags.items())),
      "seed_measurement_interpretation":"numeric seed-production proxy, precise 2026 derivation unverified",
      "scientific_scope":"exploratory same-season phenology vs reproductive proxy only",
      "intervention_codebook_verified":False,
      "genotype_is_sequenced_SNP":False,
      "new_genetic_rescue_effect":False,
      "measured_pollination_or_effective_pollen":False,
      "new_natural_GxIxF_validation":False,
      "original_individual_rows_redistributed":False,
    }
    result.update(metric)
    result["decision"]=("EXPLORATORY_PREDICTIVE_INCREMENT"
                         if val=="WITHIN_PROGRAMME_PREDICTIVE_INCREMENT"
                         else "EXPLORATORY_NO_ROBUST_INCREMENT")
    result["result_is_confirmatory"]=False
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=run()
    except (base.SourceStop,HTTPError,URLError,ValueError,KeyError,TypeError,
            IndexError,subprocess.CalledProcessError) as exc:
        result={"status":"EXPLORATORY_SOURCE_OR_ANALYSIS_STOP",
                "new_exploratory_protocol_commit":FREEZE,
                "original_lupf1_preregistered_status":"SOURCE_ENDPOINT_INVALID_STOP",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:120] if isinstance(exc,base.SourceStop) else type(exc).__name__,
                "original_individual_rows_redistributed":False,
                "new_genetic_rescue_effect":False,
                "new_natural_GxIxF_validation":False,
                "result_is_confirmatory":False}
        if isinstance(exc,HTTPError):result["http_status"]=exc.code
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
