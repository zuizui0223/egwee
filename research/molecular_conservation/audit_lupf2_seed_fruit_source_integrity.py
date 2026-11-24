#!/usr/bin/env python3
"""Source-only original Lupinus 2026 fruit/seed compatibility check; NO model fits.

Inspects only source record identifiers for provenance counts and fruit, seed,
flowering missingness categories. Prints no individual measurements or IDs.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

sys.path.insert(0,str(Path(__file__).resolve().parent))
import run_lupf1_genotype_holdout as source
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rescue_coupling"))
from audit_lupinus_id_linkage import data_to_sparse_rows

DOI="10.6084/m9.figshare.29606180"
SOURCE_SHA="7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734"
RAW_FIELDS={"id","population","line","genotype","flowering_onset","number of fruits","number of seeds"}
POP_DENOMS={"FRO":1584,"PIC":1440}
SEED_EXPECTED={"MISSING":990,"NONNEGATIVE_INTEGER":1881,"NONNEGATIVE_FRACTION":153}
LINES={"C","J","L","R","T","X"}

def classify(raw):
    s=source.clean(raw)
    if s.casefold() in {"","na","n/a","nan","null","#n/a","none"}:
        return "MISSING",None
    v=source.numeric(s)
    if v is None:
        return "NONNUMERIC_NONFINITE",None
    if v<0:
        return "NEGATIVE",None
    if abs(v-round(v))>1e-7:
        return "NONNEGATIVE_FRACTION",v
    return "NONNEGATIVE_INTEGER",v

def profile(rows, strict=True):
    if strict and len(rows)!=3024:
        raise source.SourceStop("SOURCE_ROW_COUNT_MISMATCH")
    status=Counter()
    pop_counts=Counter()
    groups=set()
    checks=defaultdict(Counter)
    for row in rows:
        pop=source.clean(row.get("population"))
        code=source.clean(row.get("line"))
        genotype=source.clean(row.get("genotype"))
        if pop not in POP_DENOMS or code not in LINES or not genotype:
            raise source.SourceStop("INVALID_SOURCE_DESIGN_CATEGORY")
        pop_counts[pop]+=1
        groups.add(pop+"|"+genotype)
        c_f,f=classify(row.get("number of fruits"))
        c_s,s=classify(row.get("number of seeds"))
        c_o,_=classify(row.get("flowering_onset"))
        status[("fruit",c_f)]+=1
        status[("seed",c_s)]+=1
        status[("onset",c_o)]+=1
        for label in ("TOTAL",pop):
            ctr=checks[label]
            ctr["original_rows"]+=1
            ctr["seed_"+c_s]+=1
            ctr["fruit_"+c_f]+=1
            ctr["onset_"+c_o]+=1
            if c_f=="NONNEGATIVE_INTEGER" and f==0:ctr["observed_zero_fruit"]+=1
            if c_s=="NONNEGATIVE_INTEGER" and s==0:ctr["observed_zero_seed_index"]+=1
            if c_s=="NONNEGATIVE_FRACTION":
                ctr["fractional_seed_with_fruit_"+("positive" if f is not None and f>0
                                                  else "zero" if f==0 else "missing_or_invalid")]+=1
            if s is not None and s>0 and f==0:
                ctr["positive_seed_index_with_zero_fruit"]+=1
            if s is None and f is not None and f>0:
                ctr["missing_seed_index_with_positive_fruit"]+=1
            if s is not None and f is None:
                ctr["fruit_missing_with_numeric_seed"]+=1
            if c_s=="MISSING" and c_o=="MISSING":
                ctr["both_seed_and_onset_missing"]+=1
            if c_s!="MISSING" and c_s not in {"NEGATIVE","NONNUMERIC_NONFINITE"} and c_o not in {"MISSING","NEGATIVE","NONNUMERIC_NONFINITE"}:
                ctr["both_seed_and_onset_numeric_nonnegative"]+=1
    if strict:
        if dict(pop_counts)!=POP_DENOMS or len(groups)!=84:
            raise source.SourceStop("SOURCE_GRAIN_DENOMINATOR_CHANGED")
        if any(status[("seed",key)]!=v for key,v in SEED_EXPECTED.items()):
            raise source.SourceStop("ORIGINAL_SEED_CATEGORY_COUNTS_CHANGED")
        if status[("seed","NEGATIVE")]+status[("seed","NONNUMERIC_NONFINITE")]:
            raise source.SourceStop("UNEXPECTED_INVALID_SEED_VALUES")
        if checks["TOTAL"]["both_seed_and_onset_numeric_nonnegative"]!=2008:
            raise source.SourceStop("ORIGINAL_COMPLETE_CASE_COUNT_CHANGED")
    out={
        "status":"POSTHOC_FRUIT_SEED_SOURCE_INTEGRITY_COUNTS_ONLY",
        "all_original_rows":len(rows),
        "source_genotype_label_groups":len(groups),
        "global_fruit_categories":dict(sorted((k[1],v) for k,v in status.items() if k[0]=="fruit")),
        "global_seed_categories":dict(sorted((k[1],v) for k,v in status.items() if k[0]=="seed")),
        "by_source_population":{k:dict(sorted(v.items())) for k,v in checks.items()},
        "no_new_regression_or_effect_estimated":True,
        "no_original_rows_or_source_identifiers_redistributed":True,
        "new_genetic_intervention_claim":False,
        "new_pollination_or_recruitment_function_claim":False,
        "2026_seed_derived_as_fruit_times_mean_seed":"NOT_ESTABLISHED",
        "physical_block_id_field_present":False,
        "no_missing_as_zero_imputation":True,
        "no_line_code_to_intervention_mapping":True,
        "decision":"SEED_FRUIT_DESCRIPTIVE_ALIGNMENT_ONLY_RETAIN_MEASUREMENT_AMBIGUITY",
    }
    return out

def run():
    m=json.loads(source.download(f"https://api.figshare.com/v2/articles/{source.ARTICLE}").decode("utf8"))
    doi=str(m.get("doi","")).lower().removeprefix("https://doi.org/")
    if doi!=DOI and not (doi.startswith(DOI+".v") and doi[len(DOI)+2:].isdigit()):
        raise source.SourceStop("SOURCE_DOI_CHANGED")
    matches=[f for f in m.get("files",[]) if f.get("name")==source.NAME]
    if len(matches)!=1:
        raise source.SourceStop("SOURCE_FILE_NAME_CHANGED")
    url=matches[0].get("download_url","")
    loc=urlparse(url)
    if loc.scheme!="https" or loc.hostname not in {"figshare.com","api.figshare.com","ndownloader.figshare.com"}:
        raise source.SourceStop("SOURCE_HOST_NOT_OFFICIAL")
    raw=source.download(url)
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
        raise source.SourceStop("SOURCE_ARCHIVE_DIGEST_CHANGED")
    headers,rows=data_to_sparse_rows(raw,"xl/worksheets/sheet2.xml",RAW_FIELDS)
    if not RAW_FIELDS.issubset(set(headers)):
        raise source.SourceStop("SOURCE_COLUMN_HEADER_CHANGED")
    receipt=profile(rows)
    receipt["archive_sha256"]=SOURCE_SHA
    receipt["original_article_id"]=source.ARTICLE
    receipt["verification_protocol"]=( "research/molecular_conservation/"
        "LUPF2_SEED_FRUIT_SOURCE_INTEGRITY_PROTOCOL_20261124.md")
    return receipt

if __name__=="__main__":
    try:
        r=run()
    except (source.SourceStop,HTTPError,URLError,ValueError,KeyError,TypeError,IndexError) as e:
        r={
            "status":"POSTHOC_FRUIT_SEED_SOURCE_INTEGRITY_STOP",
            "reason_type":type(e).__name__,
            "reason":str(e)[:120] if isinstance(e,source.SourceStop) else type(e).__name__,
            "no_new_regression_or_effect_estimated":True,
            "no_original_rows_or_source_identifiers_redistributed":True,
            "new_genetic_intervention_claim":False,
            "new_pollination_or_recruitment_function_claim":False,
        }
        if isinstance(e,HTTPError):
            r["http_status"]=e.code
    print(json.dumps(r,ensure_ascii=False,indent=2))
