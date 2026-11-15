#!/usr/bin/env python3
"""Public Figshare metadata and optional FIRST-ROW schema audit; no outcome values.

Official API article lookup returns public file download URLs. Downloads remain on
the CI runner and raw files are neither printed nor uploaded.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from io import BytesIO, StringIO
import json
from pathlib import Path
import urllib.request
import urllib.error
import zipfile
from audit_pyrus_dryad_schema import workbook_sheet_headers

SOURCE_ARTICLES=[
    {"article_id":30290722,"expected_doi":"10.6084/m9.figshare.30290722","system":"Pseudoziziphus_celata_parentage_2025"},
    {"article_id":28304024,"expected_doi":"10.6084/m9.figshare.28304024","system":"Lupinus_angustifolius_AGF_2025"}
]
MAX_BYTES=15*1024*1024

def pull(url: str, limit:int=MAX_BYTES) -> bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-research-schema/0.1 (public-data-audit)","Accept":"application/json,*/*"})
    with urllib.request.urlopen(req,timeout=35) as r:
        content=r.read(limit+1)
        if len(content)>limit:
            raise ValueError("Download exceeds CI schema limit")
        return content

def file_head(name: str, buf:bytes):
    lower=name.lower()
    if lower.endswith(".xlsx"):
        if not zipfile.is_zipfile(BytesIO(buf)):
            return {"kind":"xlsx","error":"Invalid XLSX structure"}
        return {"kind":"xlsx","worksheets":workbook_sheet_headers(buf)}
    if lower.endswith((".csv",".tsv",".txt")):
        # Do not parse population/genomic outcome values. Only the header line.
        first=buf.splitlines()[0] if buf.splitlines() else b""
        if len(first)>10000:
            return {"kind":"delimited_text","error":"Oversize first row"}
        sep="\t" if lower.endswith((".tsv",".txt")) else ","
        try:
            header=next(csv.reader([first.decode("utf-8-sig")],delimiter=sep))
        except (UnicodeError,StopIteration,csv.Error):
            return {"kind":"delimited_text","error":"Header encoding/format not readable"}
        return {"kind":"delimited_text","first_row_fields":header[:90],"column_count":len(header),"physical_line_count":buf.count(b"\n")+1}
    return {"kind":"metadata_only_unsupported_extension"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    rows=[]
    for entry in SOURCE_ARTICLES:
        article_id=entry["article_id"]
        rec={"article_id":article_id,"source_system":entry["system"],"expected_doi":entry["expected_doi"],
             "raw_data_redistributed":False,"outcome_values_examined":False,"statistical_effects_estimated":False}
        url=f"https://api.figshare.com/v2/articles/{article_id}"
        try:
            meta=json.loads(pull(url,limit=2*1024*1024).decode("utf-8"))
            doi=meta.get("doi","").lower().removeprefix("https://doi.org/")
            if doi!=entry["expected_doi"].lower():
                # Some Figshare DOI aliases include a version suffix: fail closed.
                raise ValueError("DOI mismatch or unexpected version: "+doi)
            rec["article_title"]=meta.get("title")
            rec["article_doi"]=doi
            rec["metadata_status"]="verified"
            files=meta.get("files",[])
            rec["files"]=[]
            for f in files:
                info={"name":f.get("name"),"size":f.get("size"),"supplied_md5":f.get("supplied_md5"),
                      "is_link_only":f.get("is_link_only",False),"source_file_id":f.get("id")}
                file_url=f.get("download_url")
                if info["name"] and isinstance(info["size"],int) and info["size"]<=MAX_BYTES and file_url and info["name"].lower().endswith((".xlsx",".csv",".tsv",".txt")):
                    try:
                        data=pull(file_url)
                        info["observed_sha256"]=hashlib.sha256(data).hexdigest()
                        info["content_schema_status"]="first_row_only_verified"
                        info["content_schema"]=file_head(info["name"],data)
                    except Exception as e:
                        info["content_schema_status"]="file_access_stop"
                        info["content_schema_error"]=str(e)[:200]
                else:
                    info["content_schema_status"]="file_not_supported_or_size_limited"
                rec["files"].append(info)
            rec["decision"]="FIGSHARE_FILES_REVIEWED_NO_EFFECT_VALUES"
        except Exception as e:
            rec["metadata_status"]="access_stop"
            rec["metadata_error"]=str(e)[:200]
            rec["decision"]="FIGSHARE_ACCESS_STOP"
        rows.append(rec)
    result={"status":"METADATA_AND_FIRST_ROW_SCHEMA_ONLY_NO_OUTCOME_VALUES",
            "date":"2026-11-15","sources":rows,"raw_data_redistributed":False,
            "candidate_effect_size_claims":0}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"sources":[{
        "id":e["article_id"],"status":e["metadata_status"],"files":len(e.get("files",[])),
        "first_row_schema_verified":sum(f.get("content_schema_status")=="first_row_only_verified" for f in e.get("files",[]))
    } for e in rows]},indent=2))

if __name__=="__main__":
    main()
