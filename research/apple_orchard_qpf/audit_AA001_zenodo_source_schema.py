#!/usr/bin/env python3
"""AA001 original Zenodo four-file schema only; NO original biological values.

This assay is NOT a novel apple Q->P->F mechanism test. It verifies that
published source files can be fetched and checksums/headers are legitimate.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

RECORD_ID=19403906
DOI="10.5281/zenodo.19403906"
API=f"https://zenodo.org/api/records/{RECORD_ID}"
EXPECTED=("TransectIN.txt","GerminatedPollen.txt",
          "initial_final_fruitset.txt","apple_weight.txt")
MAX_META=2_000_000
MAX_FILE=512_000
HEADER_SAFE=re.compile(r"^[A-Za-z][A-Za-z0-9_.() /+-]{0,70}$")

def get_bytes(url, maxsize=MAX_META):
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.netloc not in ("zenodo.org","www.zenodo.org"):
        raise ValueError("Only author-advertised Zenodo HTTPS URL accepted")
    request=Request(url,headers={
        "User-Agent":"egwee-AA001-original-reproducibility-gate/1.0",
        "Accept":"application/json,text/plain,*/*"})
    with urlopen(request, timeout=40) as response:
        raw=response.read(maxsize+1)
        if len(raw)>maxsize:
            raise ValueError("Source file exceeds bounded original schema gate")
    return raw

def entries_of(meta):
    files=meta.get("files") or {}
    if isinstance(files,dict):
        entries=files.get("entries")
        if isinstance(entries,dict):return entries
        if isinstance(entries,list):
            return {str(e["key"]):e for e in entries}
    if isinstance(files,list):
        return {str(e["key"]):e for e in files}
    raise ValueError("No approved file entries in Zenodo metadata")

def parse_source_header(raw):
    text=None
    encoding=None
    for name in ("utf-8-sig","cp1252","latin-1"):
        try:
            text=raw.decode(name,"strict")
            encoding=name
            break
        except UnicodeDecodeError:pass
    if text is None:raise ValueError("No lossless encoding")
    first=next((line for line in text.splitlines() if line.strip()),None)
    if first is None:raise ValueError("Original source text empty")
    counts={k:first.count(k) for k in ("\t",";",",")}
    sep=max(counts,key=counts.get)
    if counts[sep]<2:raise ValueError("Cannot establish at least 3 original source columns")
    rows=list(csv.reader(io.StringIO(text,newline=""),delimiter=sep))
    rows=[r for r in rows if any(c.strip() for c in r)]
    if len(rows)<2:raise ValueError("Missing original source rows")
    header=rows[0]
    if not 3<=len(header)<=80 or any(not h.strip() for h in header):
        raise ValueError("Invalid original source header cardinality")
    if len(set(header))!=len(header):raise ValueError("Repeated source field names")
    if any(len(row)!=len(header) for row in rows):
        raise ValueError("Ragged original table; do not parse numeric values")
    looks_header=all(HEADER_SAFE.fullmatch(h.strip()) for h in header)
    return {
      "n_rows_after_first_physical_row":len(rows)-1,
      "n_fields":len(header),
      "delimiter_kind":{"\t":"tab",";":"semicolon",",":"comma"}[sep],
      "lossless_encoding":encoding,
      "header_likely_structural":looks_header,
      "header_labels_only": [h.strip() for h in header] if looks_header else [],
      "original_numeric_rows_interpreted":False,
    }

def source_metadata():
    raw=get_bytes(API)
    meta=json.loads(raw)
    if int(meta.get("id",-1))!=RECORD_ID:
        raise ValueError("Wrong Zenodo id")
    doi=str(meta.get("doi","")).lower()
    if doi!=DOI.lower():
        raise ValueError("Zenodo DOI mismatch: "+doi[:90])
    if str(meta.get("status","")).lower() not in ("published",""):
        raise ValueError("Original Zenodo record is not published")
    names=entries_of(meta)
    if any(name not in names for name in EXPECTED):
        raise ValueError("Missing one of four pre-frozen source files: "+
                         ",".join(n for n in EXPECTED if n not in names))
    return meta,names

def audit():
    result={
       "status":"SOURCE_SCHEMA_NOT_CHECKED",
       "source_record_id":RECORD_ID,
       "doi":DOI,
       "original_published_article":"10.1016/j.scitotenv.2026.181767",
       "expected_original_files":list(EXPECTED),
       "original_numeric_rows_examined_for_inference":False,
       "site_treatment_join_verified":False,
       "biological_mediation_or_yield_effect_tested":False,
       "third_same_flower_qpf_programme_admitted":False,
       "source_rows_redistributed":False,
       "per_source":[],
    }
    try:
        metadata,entries=source_metadata()
    except (HTTPError,URLError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        result["status"]="SOURCE_METADATA_OR_ACCESS_STOP"
        result["error_type"]=type(exc).__name__
        if isinstance(exc,HTTPError):result["http_status"]=exc.code
        result["decision"]="STOP_NO_QPF_OR_COEFFICIENT_INFERENCE"
        return result
    result["source_metadata_verified"]=True
    result["source_files_in_record"]=len(entries)
    for name in EXPECTED:
        info=entries[name]
        r={"original_filename":name,"status":"FILE_NOT_ACCESSED"}
        try:
            size=info.get("size")
            if not isinstance(size,int) or size<10 or size>MAX_FILE:
                raise ValueError("Source size missing or outside safe bound")
            href=(info.get("links") or {}).get("content")
            if not href:raise ValueError("No Zenodo-advertised original file content link")
            blob=get_bytes(href,MAX_FILE)
            if len(blob)!=size:
                raise ValueError("Original size checksum mismatch")
            declared=str(info.get("checksum","")).lower()
            if declared:
                algo,sep,expected=declared.partition(":")
                if sep!=":" or algo not in ("md5","sha256"):
                    raise ValueError("Unsupported original checksum type")
                got=(hashlib.md5(blob).hexdigest() if algo=="md5"
                     else hashlib.sha256(blob).hexdigest())
                if got.lower()!=expected.lower():
                    raise ValueError("Source original checksum mismatch")
            r.update(parse_source_header(blob))
            r["size_bytes"]=len(blob)
            r["source_sha256"]=hashlib.sha256(blob).hexdigest()
            r["checksum_verified"]=bool(declared)
            r["status"]="ORIGINAL_FILE_SCHEMA_PASS"
        except (HTTPError,URLError,ValueError,TypeError,KeyError,UnicodeError) as exc:
            r["status"]="ORIGINAL_FILE_ACCESS_OR_FORMAT_STOP"
            r["error_type"]=type(exc).__name__
            if isinstance(exc,HTTPError):r["http_status"]=exc.code
        result["per_source"].append(r)
    ok=sum(p["status"]=="ORIGINAL_FILE_SCHEMA_PASS" for p in result["per_source"])
    result["files_schema_verified"]=ok
    result["status"]="ALL_FOUR_SOURCE_HEADERS_VERIFIED" if ok==4 else "PARTIAL_OR_BLOCKED_SOURCE_SCHEMA"
    result["decision"]="SEPARATE_BIOLOGICAL_GRAIN_FREEZE_REQUIRED" if ok==4 else "STOP_NO_QPF_OR_COEFFICIENT_INFERENCE"
    return result

def self_test():
    a=parse_source_header(b"Region\tSite\tTreatment\tNumber\nA\t1\tO\t14\nB\t2\tE\t0\n")
    assert a["n_fields"]==4 and a["n_rows_after_first_physical_row"]==2
    assert a["header_likely_structural"]
    try:
        parse_source_header(b"Region\tSite\tSite\nA\t1\t2\n")
    except ValueError:pass
    else:raise AssertionError("Duplicate column allowed")
    print("AA001_ZENODO_SCHEMA_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        self_test();return 0
    if a.output is None:p.error("--output required")
    result=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("AA001_ZENODO_ORIGINAL_SCHEMA "+json.dumps(result,sort_keys=True),flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
