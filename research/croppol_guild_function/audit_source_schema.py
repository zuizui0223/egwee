#!/usr/bin/env python3
"""CropPol original source-only schema and immutable Git-blob integrity gate.

No insect records, flower counts, yield values, cultivar, sample IDs or
coordinates written to results or logs. Outcome associations not opened.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ORIGINAL_REPO="ibartomeus/CropPol"
ORIGINAL_COMMIT="99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b"
FILES={
  "field": {
    "path":"Final_Data/CropPol_field_level_data.csv",
    "git_blob_sha1":"cd19a354741ac40428e6b94aa1ec2ee596ff0547",
    "max_bytes":4_000_000
  },
  "sample": {
    "path":"Final_Data/CropPol_sampling_data.csv",
    "git_blob_sha1":"b7ab3fd92da0be5e8ec41b6ada50c2da7d4756c2",
    "max_bytes":28_000_000
  },
}

def source_bytes(spec):
    path=spec["path"]
    url=f"https://raw.githubusercontent.com/{ORIGINAL_REPO}/{ORIGINAL_COMMIT}/{path}"
    req=urllib.request.Request(url,headers={
        "User-Agent":"EGWEE-CropPol-original-source-schema-gate/1.0",
        "Accept":"text/csv"
    })
    buffers=[]
    n=0
    with urllib.request.urlopen(req,timeout=90) as fh:
        while True:
            chunk=fh.read(1024*1024)
            if not chunk:break
            buffers.append(chunk)
            n+=len(chunk)
            if n>spec["max_bytes"]:
                raise ValueError("original source exceeds pre-registered byte cap")
    raw=b"".join(buffers)
    if not raw:
        raise ValueError("empty original source")
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if blob!=spec["git_blob_sha1"]:
        raise ValueError("immutable original Git blob mismatch "+blob)
    return raw

def schema(raw):
    encoding=None
    content=None
    for candidate in ("utf-8-sig","cp1252","latin-1"):
        try:
            content=raw.decode(candidate,errors="strict")
            encoding=candidate
            break
        except UnicodeDecodeError:
            continue
    if content is None:raise ValueError("source is not losslessly text decodable")
    reader=csv.reader(io.StringIO(content,newline=""))
    try:head=next(reader)
    except StopIteration:raise ValueError("missing header")
    if not 3<=len(head)<=300 or any(not x.strip() for x in head) or len(set(head))!=len(head):
        raise ValueError("missing or duplicated source header labels")
    n=0
    for row in reader:
        if len(row)!=len(head):
            raise ValueError("original source CSV row width does not match header")
        n+=1
    if n<100:
        raise ValueError("source contains less than 100 records; wrong original file")
    return {"source_header_names":head,"source_columns":len(head),
            "n_data_rows":n,"encoding_lossless":encoding,
            "biological_values_read_for_inference":False}

def run():
    records={}
    for key,spec in FILES.items():
        raw=source_bytes(spec)
        records[key]={"path":spec["path"],"git_blob_sha1":spec["git_blob_sha1"],
                      "original_sha256":hashlib.sha256(raw).hexdigest(),
                      "original_bytes":len(raw),**schema(raw)}
    return {
      "status":"ORIGINAL_CROPPOL_SOURCE_SCHEMA_PASS",
      "original_repository":ORIGINAL_REPO,
      "original_commit":ORIGINAL_COMMIT,
      "original_version_note":"source News.md most recent version 2.1.0",
      "source_files":records,
      "source_raw_rows_redistributed":False,
      "yield_values_inspected":False,
      "pollinator_group_counts_inspected":False,
      "outcome_associations_estimated":False,
      "same_field_join_verified":False,
      "cross_programme_prediction_done":False,
      "decision":"FREEZE_SOURCE_GRAIN_AND_GUILD_SEMANTICS_BEFORE_SIGNED_OUTCOMES",
    }

def self_test():
    a=schema(b"A,B,C\n1,2,3\n"*150)
    assert a["source_columns"]==3
    try:
        schema(b"a,a,c\n"+b"1,2,3\n"*101)
    except ValueError:pass
    else:raise AssertionError("duplicate source headers admitted")
    print("CROPPOL_SOURCE_GATE_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        self_test();return
    if a.output is None:p.error("--output is required")
    try:
        result=run()
    except Exception as exc:
        result={"status":"ORIGINAL_SOURCE_STOP","error_type":type(exc).__name__,
                "reason":str(exc)[:300],"yield_values_inspected":False,
                "outcome_associations_estimated":False,
                "source_raw_rows_redistributed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CROPPOL_ORIGINAL_SOURCE_GATE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="ORIGINAL_CROPPOL_SOURCE_SCHEMA_PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
