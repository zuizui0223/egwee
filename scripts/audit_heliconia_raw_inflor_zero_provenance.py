#!/usr/bin/env python3
"""Recover explicitly entered zero flowering counts from pre-cleaning raw data.

Do NOT equate the archive's NA infl with no flowering. Historical 2016 wide
raw survey has some explicit INFL_YYYY=0 entries. Link only unique
plot+tag+subplot keys, and report unlinked/corrected/conflicted entries rather
than imputing them. This is provenance sensitivity, NOT a new ecological study.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request

from analyze_heliconia_census_panel import load_csv

REPO = "https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/"
PIN = "0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0"
RAWP = "data/survey_raw/Hacuminata_98-09_12oct2016.csv"
RAW_BLOB = "b42963be30b993b93755f7f40ad09d1361def056"
YEARS = tuple(range(1998, 2006))
PLOTS = ("CF-1", "CF-2", "CF-3", "FF-1", "FF-2", "FF-3", "FF-4",
         "FF-5", "FF-6", "FF-7")
MAP = {
    "Florestal":"CF-1", "Florestal-CF":"CF-1", "5750":"CF-2", "5756":"CF-3",
    "2107":"FF-1", "2108":"FF-2", "5751":"FF-3", "5753":"FF-4",
    "2206":"FF-5", "5752":"FF-6", "5754":"FF-7",
}

def normalize_tag(x: str | None) -> str | None:
    if x is None:
        return None
    x=x.strip()
    if not x or x.upper() in ("NA","N/A","NONE"):
        return None
    try:
        y=float(x)
        if y >= 0 and y.is_integer():
            return str(int(y))
    except ValueError:
        pass
    return x.upper()

def subplot(row: str | None, col: str | None) -> str | None:
    if not row or not col:
        return None
    row=row.strip().upper()
    col=col.strip().upper()
    if not row or not col or row=="NA" or col=="NA":
        return None
    if col.endswith(".0"):
        col=col[:-2]
    return row+col

def raw_category(v: str | None) -> str:
    if v is None or not v.strip() or v.strip().upper()=="NA":
        return "not_entered"
    try:
        x=float(v)
    except ValueError:
        return "non_numeric"
    if x<0:
        return "negative_code"
    return "zero" if x==0 else "positive"

def get_raw(local_file: Path | None) -> bytes:
    if local_file:
        data=local_file.read_bytes()
    else:
        req=urllib.request.Request(REPO+PIN+"/"+RAWP,
                                   headers={"User-Agent":"egwee-raw-source-audit/1"})
        with urllib.request.urlopen(req,timeout=60) as response:
            data=response.read()
    sha=hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
    assert sha==RAW_BLOB,(sha,RAW_BLOB)
    return data

def audit(raw_bytes:bytes,archive:list[dict])->dict:
    # A few Portuguese-accented free-text note bytes are not UTF-8. Keep
    # them with lossless Latin-1; only ASCII structural fields are used.
    reader=csv.DictReader(io.StringIO(raw_bytes.decode("latin-1")))
    assert reader.fieldnames and {"PLOT","Tag_Number","Row","Column",
                                   "INFL_2001","INFL_2002"} <= set(reader.fieldnames)
    raw_lines=list(reader)
    by_key=defaultdict(list)
    raw_unknown_plot=Counter()
    for row in raw_lines:
        place=row["PLOT"].strip()
        p=MAP.get(place)
        if p is None:
            raw_unknown_plot[place]+=1
            continue
        tag=normalize_tag(row["Tag_Number"])
        sub=subplot(row["Row"],row["Column"])
        if tag is not None and sub is not None:
            by_key[(p,tag,sub)].append(row)
    unique={key:values[0] for key,values in by_key.items() if len(values)==1}
    ambiguous={key for key,values in by_key.items() if len(values)!=1}

    matched={}
    source_counts=defaultdict(Counter)
    by_year=defaultdict(Counter)
    by_plot=defaultdict(Counter)
    archive_keys=defaultdict(set)
    for r in archive:
        p,year=r["plot_id"],int(r["year"])
        if p not in PLOTS or year not in YEARS or r["census_status"]!="measured":
            continue
        tag=normalize_tag(r["tag_number"])
        sub=r["subplot"].strip().upper()
        key=(p,tag,sub)
        category=("archive_positive" if r["infl"].strip() not in ("NA","",None)
                  else "archive_no_positive")
        # In source archive recorded infl is conditional on a positive count.
        if category=="archive_positive":
            assert float(r["infl"])>0
        row=unique.get(key) if tag is not None else None
        if row is None:
            raw_cat="ambiguous_source_key" if key in ambiguous else "unlinked"
        else:
            raw_cat=raw_category(row.get(f"INFL_{year}"))
        name=category+"__"+raw_cat
        source_counts[p][name]+=1
        by_year[str(year)][name]+=1
        by_plot[p][name]+=1
        archive_keys[(p,r["plant_id"])].add((year,raw_cat,category))
        if raw_cat in {"zero","positive"} and key in unique:
            matched[(p,r["plant_id"],year)]=(raw_cat,category)
    pairwise={}
    for year in range(1998,2005):
        c=Counter()
        for (p,ident,yr),(ca,archive_ca) in matched.items():
            if yr!=year:
                continue
            next_state=matched.get((p,ident,year+1))
            if next_state is None:
                continue
            cb,archive_cb=next_state
            c[ca+"_to_"+cb]+=1
            c["fully_raw_confirmed_plant_transitions"]+=1
            if (ca=="zero" and archive_ca!="archive_no_positive") or (
                    ca=="positive" and archive_ca!="archive_positive"):
                c["old_raw_archive_class_conflict"]+=1
            if (cb=="zero" and archive_cb!="archive_no_positive") or (
                    cb=="positive" and archive_cb!="archive_positive"):
                c["next_raw_archive_class_conflict"]+=1
        pairwise[f"{year}_{year+1}"]=dict(c)
    return {
        "status":"EXPLORATORY_PINNED_RAW_ZERO_VS_ARCHIVE_NA_PROVENANCE",
        "raw_filename":RAWP,"raw_blob":RAW_BLOB,
        "raw_total_rows":len(raw_lines),
        "source_plant_years":len(archive),
        "raw_unique_identifiers":len(unique),
        "raw_ambiguous_plot_tag_subplot_identifiers":len(ambiguous),
        "raw_unrecognized_plot_codes":dict(raw_unknown_plot),
        "per_year_matches":{k:dict(v) for k,v in sorted(by_year.items())},
        "per_plot_matches":{k:dict(v) for k,v in sorted(by_plot.items())},
        "strict_unique_matched_raw_zero_positive_pairs":pairwise,
        "limitations":[
            "Raw 2016 wide input precedes plot/tag corrections; some same-tag links can be spurious despite unique key and subplot.",
            "Raw numeric zero is a documented data-entry zero, not proof a flowering survey exhaustively detected all inflorescences.",
            "Raw zero and archive NA need not mean any semantic corruption: archived variable may intentionally record inflorescences conditional on flowering.",
            "Unlinked and ambiguous raw entries must remain unresolved; do not impute them as raw zero or as biological nonflowering.",
            "Raw positive/archive NA and raw zero/archive positive may represent authorized data-cleaning corrections; do not silently choose old raw as truth.",
            "This archival provenance can check a record-state measurement boundary but not causal fecundity, pollen transfer or recruitment.",
            "Existing empirical EGWEE evidence denominators and draft status remain unchanged."
        ]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--local-raw",type=Path)
    ap.add_argument("--local-archive",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    archive=load_csv("HDP_survey.csv",args.local_archive)
    assert len(archive)==66396
    report=audit(get_raw(args.local_raw),archive)
    assert report["raw_total_rows"]>1000
    assert report["raw_unique_identifiers"]>100
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("HELICONIA_RAW_INFLORESCENCE_PROVENANCE: PASS")
    print(json.dumps({
        k:v for k,v in report.items()
        if k in ("raw_total_rows","raw_unique_identifiers",
                 "raw_ambiguous_plot_tag_subplot_identifiers",
                 "raw_unrecognized_plot_codes","per_year_matches",
                 "strict_unique_matched_raw_zero_positive_pairs")
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
